from __future__ import annotations

import datetime
import types
from dataclasses import dataclass
from typing import List, Dict, Union, Mapping, Optional, Set

import pandas as pd

from seeq import spy
from seeq.sdk import *
from seeq.spy import _common, _login, _metadata, _push, _swap
from seeq.spy._errors import *
from seeq.spy._redaction import safely, request_safely
from seeq.spy._session import Session
from seeq.spy._status import Status

RESERVED_SEARCH_COLUMN_NAMES = ['Path', 'Asset', 'Type', 'Depth', 'Estimated Sample Period', 'Formula Parameters',
                                'Datasource Name']


@dataclass
class SearchContext:
    session: Session
    status: Status

    all_properties: bool
    workbook: str
    recursive: bool
    ignore_unindexed_properties: bool
    include_archived: bool
    estimate_sample_period: dict
    include_swap_info: bool
    old_asset_format: bool
    order_by: Optional[Union[str, list]]

    status_index: int
    columns: List[str]
    metadata: List
    ids: Set
    comparison: str
    dupe_count: int
    sample_periods: Dict
    workbook_id: str
    pd_start: Optional[pd.Timestamp]
    pd_end: Optional[pd.Timestamp]
    use_search_items_api: bool
    timer: datetime.datetime

    items_api: ItemsApi
    trees_api: TreesApi
    formulas_api: FormulasApi
    displays_api: DisplaysApi
    display_templates_api: DisplayTemplatesApi

    def __init__(self, session: Session, status: Status):
        self.session = session
        self.status = status

        self.columns = list()
        self.metadata = list()
        self.ids = set()
        self.datasource_ids = dict()
        self.dupe_count = 0
        self.sample_periods = dict()

        self.items_api = ItemsApi(session.client)
        self.trees_api = TreesApi(session.client)
        self.formulas_api = FormulasApi(session.client)
        self.displays_api = DisplaysApi(session.client)
        self.display_templates_api = DisplayTemplatesApi(session.client)


@Status.handle_keyboard_interrupt()
def search(query, *, all_properties=False, workbook=_common.DEFAULT_WORKBOOK_PATH, recursive=True,
           ignore_unindexed_properties=True, include_archived=False, include_swappable_assets=False,
           estimate_sample_period=None, old_asset_format=None, order_by=None, errors=None, quiet=None, status=None,
           session: Optional[Session] = None):
    """
    Issues a query to the Seeq Server to retrieve metadata for signals,
    conditions, scalars and assets. This metadata can then be used to retrieve
    samples, capsules for a particular time range via spy.pull().

    Parameters
    ----------
    query : {str, dict, list, pd.DataFrame, pd.Series}
        A mapping of property / match-criteria pairs or a Seeq Workbench URL

        If you supply a dict or list of dicts, then the matching
        operations are "contains" (instead of "equal to").

        If you supply a DataFrame or a Series, then the matching
        operations are "equal to" (instead of "contains").

        If you supply a str, it must be the URL of a Seeq Workbench worksheet.
        The retrieved metadata will be the signals, conditions and scalars
        currently present on the Details Panel.

        'Name' and 'Description' fields support wildcard and regular expression
        (regex) matching with the same syntax as within the Data tab in Seeq
        Workbench.

        The 'Path' field allows you to query within an asset tree, where >>
        separates each level from the next. E.g.: 'Path': 'Example >> Cooling*'
        You can use wildcard and regular expression matching at any level but,
        unlike the Name/Description fields, the match must be a "full match",
        meaning that 'Path': 'Example' will match on a root asset tree node of
        'Example' but not 'Example (AF)'.

        Available options are:

        =================== ===================================================
        Property            Description
        =================== ===================================================
        Name                Name of the item (wildcards/regex supported)
        Path                Asset tree path of the item (should not include the
                            "leaf" asset), using ' >> ' hierarchy delimiters
        Asset               Asset name (i.e., the name of the leaf asset) or ID
        Type                The item type. One of 'Signal', 'Condition',
                            'Scalar', 'Asset', 'Chart', 'Metric', 'Workbook',
                            and 'Worksheet'
        Description         Description of the item (wildcards/regex supported)
        Datasource Name     Name of the datasource
        Datasource ID       The datasource ID, which corresponds to the Id
                            field in the connector configuration
        Datasource Class    The datasource class (e.g. 'OSIsoft PI')
        Data ID             The data ID, whose format is managed by the
                            datasource connector
        Cache Enabled       True to find items where data caching is enabled
        Scoped To           The Seeq ID of a workbook such that results are
                            limited to ONLY items scoped to that workbook.
        =================== ===================================================

    all_properties : bool, default False
        True if all item properties should be retrieved. This currently makes
        the search operation much slower as retrieval of properties for an item
        requires a separate call.

    workbook : {str, None}, default 'Data Lab >> Data Lab Analysis'
        A path string (with ' >> ' delimiters) or an ID to indicate a workbook
        such that, in addition to globally-scoped items, the workbook's scoped
        items will also be returned in the results.

        If you want all items regardless of scope, use
        workbook=spy.GLOBALS_AND_ALL_WORKBOOKS

        If you want only globally-scoped items, use
        workbook=spy.GLOBALS_ONLY

        If you don't want globally-scoped items in your results, use the
        'Scoped To' field in the 'query' argument instead. (See 'query'
        argument documentation above.)

        The ID for a workbook is visible in the URL of Seeq Workbench, directly
        after the "workbook/" part.

    recursive : bool, default True
        If True, searches that include a Path entry will include items at and
        below the specified location in an asset tree. If False, then only
        items at the specified level will be returned. To get only the root
        assets, supply a Path value of ''.

    ignore_unindexed_properties : bool, default True
        If False, a ValueError will be raised if any properties are supplied
        that cannot be used in the search.

    include_archived : bool, default False
        If True, includes trashed/archived items in the output.

    include_swappable_assets : bool, default False
        Adds a "Swappable Assets" column to the output where each cell is an
        embedded DataFrame that includes the assets that the item refers to and
        can theoretically be swapped for other assets using spy.swap().

    estimate_sample_period : dict, default None
        A dict with the keys 'Start' and 'End'. If provided, an estimated
        sample period for all signals will be included in the output. The
        values for the 'Start' and 'End' keys must be a string that
        pandas.to_datetime() can parse, or a pandas.Timestamp. The start
        and end times are used to bound the calculation of the sample period.
        If the start and end times encompass a time range that is insufficient
        to determine the sample period, a pd.NaT will be returned.
        If the value of 'Start' is set to None, it will default to the value of
        'End' minus 1 hour. Conversely, if the value of 'End' is set to None,
        it will default to now.

    old_asset_format : bool, default True
        Historically, spy.search() returned rows with a "Type" of "Asset" whereby
        the "Asset" column was the name of the parent asset. This is inconsistent
        with all other aspects of SPy, including spy.push(metadata). If you would
        like Asset rows to instead be consistent with the rest of SPy (whereby
        the "Asset" column is the name of the current asset, not the parent),
        pass in False for this argument.

    order_by : {str, list}, default None
        An optional field or list of fields used to sort the search results.
        Fields on which results can be sorted are 'ID', 'Name', and 'Description'.

    quiet : bool, default False
        If True, suppresses progress output. Note that when status is
        provided, the quiet setting of the Status object that is passed
        in takes precedence.

    errors : {'raise', 'catalog'}, default 'raise'
        If 'raise', any errors encountered will cause an exception. If 'catalog',
        errors will be added to a 'Result' column in the status.df DataFrame.

    status : spy.Status, optional
        If specified, the supplied Status object will be updated as the command
        progresses. It gets filled in with the same information you would see
        in Jupyter in the blue/green/red table below your code while the
        command is executed. The table itself is accessible as a DataFrame via
        the status.df property.

    session : spy.Session, optional
        If supplied, the Session object (and its Options) will be used to
        store the login session state. This is useful to log in to different
        Seeq servers at the same time or with different credentials.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with rows for each item found and columns for each
        property.

        Additionally, the following properties are stored on the "spy"
        attribute of the output DataFrame:

        =================== ===================================================
        Property            Description
        =================== ===================================================
        func                A str value of 'spy.search'
        kwargs              A dict with the values of the input parameters
                            passed to spy.search to get the output DataFrame
        old_asset_format    True if the old Asset format was used (see doc for
                            old_asset_format argument)
        status              A spy.Status object with the status of the
                            spy.search call
        =================== ===================================================

    Examples
    --------
    Search for signals with the name 'Humid' on the asset tree under
    'Example >> Cooling Tower 1', retrieving all properties on the results:

    >>> search_results = spy.search({'Name': 'Humid', 'Path': 'Example >> Cooling Tower 1'}, all_properties=True)

    To access the stored properties:
    >>> search_results.spy.kwargs
    >>> search_results.spy.status

    Search for signals that have a name that starts with 'Area' in the datasource 'Example Data' and
    determine the sample period of each signal during the month of January 2018

    >>> search_results = spy.search({
    >>>    'Name': 'Area ?_*',
    >>>    'Datasource Name': 'Example Data'
    >>> }, estimate_sample_period=dict(Start='2018-01-01', End='2018-02-01'))

    Using a pandas.DataFrame as the input:

    >>> my_items = pd.DataFrame(
    >>>     {'Name': ['Area A_Temperature', 'Area B_Compressor Power', 'Optimize' ],
    >>>      'Datasource Name': 'Example Data'})
    >>> spy.search(my_items)

    Using a URL from a Seeq Workbench worksheet:

    >>> my_worksheet_items = spy.search(
    >>> 'https://seeq.com/workbook/17F31703-F0B6-4C8E-B7FD-E20897BD4819/worksheet/CE6A0B92-EE00-45FC-9EB3-D162632DBB48')

    """
    input_args = _common.validate_argument_types([
        (query, 'query', (str, dict, list, pd.DataFrame, pd.Series)),
        (all_properties, 'all_properties', bool),
        (workbook, 'workbook', str),
        (recursive, 'recursive', bool),
        (ignore_unindexed_properties, 'ignore_unindexed_properties', bool),
        (include_archived, 'include_archived', bool),
        (estimate_sample_period, 'estimate_sample_period', dict),
        (include_swappable_assets, 'include_swappable_assets', bool),
        (old_asset_format, 'old_asset_format', bool),
        (order_by, 'order_by', (str, list)),
        (quiet, 'quiet', bool),
        (errors, 'errors', str),
        (status, 'status', Status),
        (session, 'session', Session)
    ])

    status = Status.validate(status, quiet, errors)
    session = Session.validate(session)
    _login.validate_login(session, status)

    context = SearchContext(session, status)
    context.all_properties = all_properties
    context.workbook = workbook
    context.recursive = recursive
    context.ignore_unindexed_properties = ignore_unindexed_properties
    context.include_archived = include_archived
    context.estimate_sample_period = estimate_sample_period
    context.include_swap_info = include_swappable_assets
    context.old_asset_format = old_asset_format
    context.order_by = order_by

    if context.order_by:
        context.order_by = _validate_order_by(context.order_by)

    if context.estimate_sample_period is not None:
        if context.estimate_sample_period.keys() != {'Start', 'End'}:  # strict comparison, allowing only these two keys
            raise SPyValueError(f"estimate_sample_period must have 'Start' and 'End' keys but got "
                                f"{context.estimate_sample_period.keys()}")
        context.pd_start, context.pd_end = _login.validate_start_and_end(context.session,
                                                                         context.estimate_sample_period['Start'],
                                                                         context.estimate_sample_period['End'])

    if not context.recursive and 'Path' not in query:
        raise SPyValueError("'Path' must be included in query when recursive=False")

    context.old_asset_format = old_asset_format
    if context.old_asset_format is None:
        # In the future, we may wish to change this default to False, in which case we should use
        # spy.options.compatibility and keep it True for users expecting older behavior.
        context.old_asset_format = True

    queries: List[Union[Dict, Mapping]]
    if isinstance(query, pd.DataFrame):
        queries = query.to_dict(orient='records')
        context.comparison = '=='
    elif isinstance(query, pd.Series):
        queries = [query.to_dict()]
        context.comparison = '=='
    elif isinstance(query, list):
        queries = query
        context.comparison = '~='
    elif isinstance(query, str):
        worksheet = spy.utils.get_analysis_worksheet_from_url(query, context.include_archived,
                                                              quiet=context.status.quiet)
        queries = worksheet.display_items.to_dict(orient='records')
        context.comparison = '=='
    else:
        queries = [query]
        context.comparison = '~='

    context.status.df = pd.DataFrame(queries)
    context.status.df['Time'] = 0
    context.status.df['Count'] = 0
    context.status.df['Pages'] = 0
    context.status.df['Result'] = 'Queued'
    context.status.update('Initializing', Status.RUNNING)

    context.workbook_id = None
    if context.workbook:
        if _common.is_guid(context.workbook):
            context.workbook_id = _common.sanitize_guid(context.workbook)
        else:
            search_query, _ = _push.create_analysis_search_query(context.workbook)
            search_df = spy.workbooks.search(search_query,
                                             status=context.status.create_inner('Find Workbook', quiet=True),
                                             session=context.session)
            context.workbook_id = search_df.iloc[0]['ID'] if len(search_df) > 0 else None
            if context.workbook == _common.DEFAULT_WORKBOOK_PATH and context.workbook_id is None:
                context.workbook_id = _common.GLOBALS_ONLY

    context.use_search_items_api = False

    for status_index in range(len(queries)):
        context.status_index = status_index
        _process_query(context, queries[status_index])

    if context.dupe_count > 0:
        if context.use_search_items_api:
            arg_to_use = context.order_by if context.order_by else []
            if 'ID' in arg_to_use:
                context.status.warn(
                    f'{context.dupe_count} duplicates removed from returned DataFrame. If you used a list of '
                    f'searches, those searches may have had overlap.')
            else:
                arg_to_use.append('ID')
                context.status.warn(
                    f'{context.dupe_count} duplicates removed from returned DataFrame. Use order_by={arg_to_use} in '
                    f'your spy.search to ensure results are not missing any items.')
        else:
            context.status.warn(f'{context.dupe_count} duplicates removed from returned DataFrame.')

    context.status.update('Query successful', Status.SUCCESS)

    if len(context.columns) == 0:
        context.columns = ['ID', 'Type']
    output_df = pd.DataFrame(data=context.metadata, columns=context.columns)
    if context.order_by and not output_df.empty:
        output_df.sort_values(context.order_by, ignore_index=True, inplace=True)

    if old_asset_format is None:
        type_column = output_df['Type']
        if len(type_column.loc[type_column == 'Asset']) > 0:
            context.status.warn(
                'This search result includes Assets. Consider passing in "old_asset_format=False" so that the '
                '"Path" and "Asset" columns are populated in a way that is consistent with all other aspects '
                'of SPy. The default behavior without this argument emulates the (incorrect) way SPy would '
                'return such results historically.')
            context.status.display()

    output_df_properties = types.SimpleNamespace(
        func='spy.search',
        kwargs=input_args,
        old_asset_format=context.old_asset_format,
        status=context.status)

    _common.put_properties_on_df(output_df, output_df_properties)

    return output_df


def _process_query(context: SearchContext, current_query):
    context.timer = _common.timer_start()

    if _common.present(current_query, 'ID'):
        # If ID is specified, short-circuit everything and just get the item directly.
        prop_dict = dict()
        current_id = current_query['ID']
        _add_all_properties(context, current_id, prop_dict)

        # Since this method bypasses the search_items() route that would normally supply the asset ancestors, we
        # specifically call _add_tree() to make the trees_api call that will fetch the ancestors.
        _add_tree(context, current_id, prop_dict)

        # Still need to determine sample period for signals and have NaT for non-signal items
        if context.estimate_sample_period is not None:
            if 'Signal' in current_query['Type']:
                _estimate_sample_period(context, current_id, prop_dict['Name'])
            else:
                context.sample_periods[current_query['ID']] = pd.NaT

            _add_to_dict(
                context, prop_dict, 'Estimated Sample Period', context.sample_periods[current_query['ID']])

        _add_to_metadata(context, prop_dict)

        context.status.df.at[context.status_index, 'Time'] = _common.timer_elapsed(context.timer)
        context.status.df.at[context.status_index, 'Count'] = 1
        context.status.df.at[context.status_index, 'Result'] = 'Success'
        return

    # If the user wants a recursive search or there's no 'Path' in the query, then use the ItemsApi.search_items API
    context.use_search_items_api = context.recursive or not _common.present(current_query, 'Path')

    if not context.use_search_items_api and context.include_archived:
        # As you can see in the code below, the TreesApi.get_tree() API doesn't have the ability to request
        # archived items
        raise SPyValueError('include_archived=True can only be used with recursive searches or searches that do '
                            'not involve a Path parameter')

    allowed_properties = ['Type', 'Name', 'Description', 'Path', 'Asset', 'Datasource Class', 'Datasource ID',
                          'Datasource Name', 'Data ID', 'Cache Enabled', 'Scoped To']

    disallowed_properties = list()
    for key, value in current_query.items():
        if key not in allowed_properties:
            disallowed_properties.append(key)

    for key in disallowed_properties:
        del current_query[key]

    allowed_properties_str = '", "'.join(allowed_properties)
    if len(disallowed_properties) > 0:
        disallowed_properties_str = '", "'.join(disallowed_properties)
        message = f'The following properties are not indexed' \
                  f'{" and will be ignored" if context.ignore_unindexed_properties else ""}:\n' \
                  f'"{disallowed_properties_str}"\n' \
                  f'Use any of the following searchable properties and then filter further using DataFrame ' \
                  f'operations:\n"{allowed_properties_str}"'

        if not context.ignore_unindexed_properties:
            raise SPyValueError(message)
        else:
            context.status.warn(message)

    if len(current_query) == 0:
        raise SPyValueError('No recognized properties present in "query" argument. You must provide a dict or a '
                            'DataFrame with keys or columns with at least one of the following properties: \n' +
                            allowed_properties_str)

    item_types = list()
    clauses: Dict = dict()

    if _common.present(current_query, 'Type'):
        item_type_specs = list()
        if isinstance(current_query['Type'], list):
            item_type_specs.extend(current_query['Type'])
        else:
            item_type_specs.append(current_query['Type'])

        valid_types = ['StoredSignal', 'CalculatedSignal',
                       'StoredCondition', 'CalculatedCondition',
                       'LiteralScalar', 'CalculatedScalar',
                       'Datasource',
                       'ThresholdMetric', 'Chart', 'Asset',
                       'Workbook', 'Worksheet',
                       'Display', 'DisplayTemplate']

        for item_type_spec in item_type_specs:
            if item_type_spec == 'Signal':
                item_types.extend(['StoredSignal', 'CalculatedSignal'])
            elif item_type_spec == 'Condition':
                item_types.extend(['StoredCondition', 'CalculatedCondition'])
            elif item_type_spec == 'Scalar':
                item_types.extend(['LiteralScalar', 'CalculatedScalar'])
            elif item_type_spec == 'Datasource':
                item_types.extend(['Datasource'])
            elif item_type_spec == 'Metric':
                item_types.extend(['ThresholdMetric'])
            elif item_type_spec not in valid_types:
                raise SPyValueError(f'Type field value not recognized: {item_type_spec}\n'
                                    f'Valid types: {", ".join(valid_types)}')
            else:
                item_types.append(item_type_spec)

        del current_query['Type']

    for prop_name in ['Name', 'Description', 'Datasource Class', 'Datasource ID', 'Data ID']:
        if prop_name in current_query and not pd.isna(current_query[prop_name]):
            clauses[prop_name] = (context.comparison, current_query[prop_name])

    if _common.present(current_query, 'Datasource Name'):
        datasource_name = _common.get(current_query, 'Datasource Name')
        if datasource_name in context.datasource_ids:
            clauses['Datasource ID'], clauses['Datasource Class'] = context.datasource_ids[datasource_name]
        else:
            filters = ['Name == %s' % datasource_name]
            if _common.present(current_query, 'Datasource ID'):
                filters.append('Datasource ID == %s' % _common.get(current_query, 'Datasource ID'))
            if _common.present(current_query, 'Datasource Class'):
                filters.append('Datasource Class == %s' % _common.get(current_query, 'Datasource Class'))

            filter_list = [' && '.join(filters)]
            if context.include_archived:
                filter_list.append('@includeUnsearchable')

            datasource_results = context.items_api.search_items(
                filters=filter_list, types=['Datasource'], limit=100000)  # type: ItemSearchPreviewPaginatedListV1

            if len(datasource_results.items) > 1:
                raise SPyRuntimeError('Multiple datasources found that match "%s"' % datasource_name)
            elif len(datasource_results.items) == 0:
                raise SPyRuntimeError('No datasource found that matches "%s"' % datasource_name)

            datasource = datasource_results.items[0]  # type: ItemSearchPreviewV1

            @request_safely(action_description=f'get datasource details for "{datasource_name}" {datasource.id}',
                            status=context.status)
            def request_datasource_and_set_clause():
                property_output = context.items_api.get_property(id=datasource.id, property_name='Datasource Class')
                clauses['Datasource Class'] = ('==', property_output.value)
                property_output = context.items_api.get_property(id=datasource.id, property_name='Datasource ID')
                clauses['Datasource ID'] = ('==', property_output.value)
                context.datasource_ids[datasource_name] = (clauses['Datasource ID'], clauses['Datasource Class'])

            request_datasource_and_set_clause()

        del current_query['Datasource Name']

    filters = list()
    if len(clauses.items()) > 0:
        filters.append(' && '.join([p + c + v for p, (c, v) in clauses.items()]))

    if context.include_archived:
        filters.append('@includeUnsearchable')

    kwargs = {
        'filters': filters,
        'types': item_types,
        'limit': context.session.options.search_page_size
    }

    if context.workbook:
        if context.workbook_id:
            kwargs['scope'] = context.workbook_id
        elif context.workbook != _common.DEFAULT_WORKBOOK_PATH:
            raise SPyRuntimeError(f'Workbook "{context.workbook}" not found, or is not accessible by you')

    if _common.present(current_query, 'Scoped To'):
        kwargs['scope'] = current_query['Scoped To']
        kwargs['filters'].append('@excludeGloballyScoped')

    if _common.present(current_query, 'Asset'):
        if _common.is_guid(_common.get(current_query, 'Asset')):
            kwargs['asset'] = _common.get(current_query, 'Asset')
        elif not _common.present(current_query, 'Path'):
            raise SPyValueError('"Path" query parameter must be present when "Asset" name parameter present')

    path_to_query = None
    if _common.present(current_query, 'Path'):
        path_to_query = current_query['Path']
        if _common.present(current_query, 'Asset'):
            path_to_query = path_to_query + ' >> ' + current_query['Asset']

    if not _common.present(current_query, 'Path'):
        # If there's no 'Path' property in the query, we can immediately proceed to the results gathering stage.
        _gather_results(context, current_query, kwargs)
    else:
        # If there is a 'Path' property in the query, then first we have to drill down through the tree to the
        # appropriate depth so we can find the asset ID to use for the results gathering stage.

        if len(path_to_query) == 0:
            _gather_results(context, current_query, kwargs, list())
        else:
            _process_query_path_string(context, current_query, kwargs, path_to_query, list(), clauses)

    context.status.df.at[context.status_index, 'Result'] = 'Success'


def _validate_order_by(order_by):
    """
    Validate and process order_by arg of spy.search
    :param order_by: {str, list}
    :return: list
    """
    # convert string order_by to a list
    if isinstance(order_by, str):
        order_by = [order_by]

    # validate order_by
    order_fields = ['ID', 'Name', 'Description']
    invalid_fields = [x for x in order_by if x not in order_fields]
    if len(invalid_fields) > 0:
        raise SPyValueError(
            f"Invalid order_by fields: {invalid_fields}. Search results can only be ordered on "
            f"{order_fields} fields.")

    return order_by


def _add_to_dict(context: SearchContext, _dict, key, val):
    if key in ['Archived', 'Cache Enabled', 'Enabled', 'Unsearchable'] and isinstance(val, str):
        val = val.lower() == 'true'
    _dict[key] = _common.none_to_nan(val)

    # We want the columns to appear in a certain order (the order we added them in) for readability
    if key not in context.columns:
        context.columns.append(key)


def _add_ancestors_to_prop_dict_from_item_output(context: SearchContext, item_output, prop_dict):
    _ancestors = [a.name for a in item_output.ancestors]
    _add_ancestors_to_prop_dict(context, item_output.type, item_output.name, _ancestors, prop_dict)


def _add_ancestors_to_prop_dict(context: SearchContext, _type, name, ancestors, prop_dict):
    _common.add_ancestors_to_definition(_type, name, ancestors, prop_dict, context.old_asset_format)
    for key in ['Path', 'Asset']:
        if key in prop_dict and key not in context.columns:
            context.columns.append(key)


def _add_to_metadata(context: SearchContext, prop_dict):
    if prop_dict['ID'] not in context.ids:
        context.metadata.append(prop_dict)
        context.ids.add(prop_dict['ID'])
    else:
        context.dupe_count += 1


def _estimate_sample_period(context: SearchContext, signal_id, signal_name):
    sampling_formula = "$signal.estimateSamplePeriod(" \
                       f"capsule('{context.pd_start.isoformat()}','{context.pd_end.isoformat()}'))"

    formula_run_output = safely(
        lambda: context.formulas_api.run_formula(formula=sampling_formula, parameters=[f"signal={signal_id}"]),
        action_description='estimate sample period',
        status=context.status,
        additional_errors=[400])

    if formula_run_output is not None and formula_run_output.scalar.value is not None:
        context.sample_periods[signal_id] = pd.to_timedelta(
            formula_run_output.scalar.value, unit=formula_run_output.scalar.uom)
    else:
        context.status.warn(
            f'Could not determine the sample period for signal "{signal_name}" {signal_id} within the '
            f'time period {context.pd_start.isoformat()} to {context.pd_end.isoformat()}. '
            f'There might not be enough data in the specified time range. Modify the time period with the '
            f'`estimate_start` and `estimate_end` arguments.'
        )
        context.sample_periods[signal_id] = pd.NaT


def _add_all_properties(context: SearchContext, _id, prop_dict):
    def _add_error_message_and_warn(msg):
        _add_to_dict(context, prop_dict, 'Pull Result', msg)
        context.status.warn(msg)

    @request_safely(action_description=f'get all item properties for {_id}',
                    status=context.status,
                    on_error=_add_error_message_and_warn)
    def _request_item_properties():
        item = context.items_api.get_item_and_all_properties(id=_id)  # type: ItemOutputV1
        # Name and Type don't appear in additional properties
        _add_to_dict(context, prop_dict, 'Name', item.name)
        _add_to_dict(context, prop_dict, 'Type', item.type)
        _add_to_dict(context, prop_dict, 'Scoped To', _common.none_to_nan(item.scoped_to))
        for prop in item.properties:  # type: PropertyOutputV1
            if prop.name not in RESERVED_SEARCH_COLUMN_NAMES:
                _add_to_dict(context, prop_dict, prop.name, prop.value)

        if item.type in ['CalculatedSignal', 'CalculatedCondition', 'CalculatedScalar', 'LiteralScalar']:
            formula_output = context.formulas_api.get_item(id=_id)  # type: FormulaItemOutputV1
            _add_to_dict(context, prop_dict, 'Formula Parameters', [
                '%s=%s' % (_p.name, _p.item.id if _p.item else _p.formula) for _p in formula_output.parameters
            ])

        elif item.type == 'ThresholdMetric':
            formula_parameters = _metadata.formula_parameters_dict_from_threshold_metric(context.session, _id)
            for key, value in formula_parameters.items():
                _add_to_dict(context, prop_dict, key, value)

        elif item.type == 'Display':
            display_output = context.displays_api.get_display(id=_id)
            _add_to_dict(context, prop_dict, 'Template ID', display_output.template.id)
            if display_output.swap is not None:
                _add_to_dict(context, prop_dict, 'Swap Out Asset ID', display_output.swap.swap_out)
                _add_to_dict(context, prop_dict, 'Swap In Asset ID', display_output.swap.swap_in)
            else:
                _add_to_dict(context, prop_dict, 'Swap Out Asset ID', display_output.template.swap_source_asset_id)

        elif item.type == 'DisplayTemplate':
            display_template_output = context.display_templates_api.get_display_template(id=_id)
            _add_to_dict(context, prop_dict, 'Source Workstep ID', display_template_output.source_workstep_id)

    _request_item_properties()
    return prop_dict


def _add_tree(context: SearchContext, _id, prop_dict):
    item_output = None
    if context.include_swap_info:
        item_dependency_output = safely(lambda: context.items_api.get_formula_dependencies(id=_id),
                                        action_description=f'get dependencies for {_id}',
                                        status=context.status)  # type: ItemDependencyOutputV1
        if item_dependency_output is not None:
            item_output = item_dependency_output

        dependencies_with_relevant_assets = _swap.get_swappable_assets(item_dependency_output)

        def _swappable_asset_dict(d):
            leaf_asset = d.ancestors[-1]
            return {
                'ID': leaf_asset.id,
                'Type': leaf_asset.type,
                'Path': _common.path_list_to_string([a.name for a in d.ancestors[0:-1]]),
                'Asset': leaf_asset.name
            }

        swappable_assets = pd.DataFrame([_swappable_asset_dict(d) for d in dependencies_with_relevant_assets],
                                        columns=['ID', 'Type', 'Path', 'Asset'])

        _add_to_dict(context, prop_dict, 'Swappable Assets', swappable_assets)
    else:
        asset_tree_output = safely(lambda: context.trees_api.get_tree(id=_id),
                                   action_description=f'get asset tree ancestors for {_id}',
                                   status=context.status)  # type: AssetTreeOutputV1
        if asset_tree_output is not None:
            item_output = asset_tree_output.item
    if item_output is not None:
        _add_ancestors_to_prop_dict_from_item_output(context, item_output, prop_dict)

    return prop_dict


def _process_query_path_string(context: SearchContext, current_query, kwargs, remaining_query_path_string,
                               actual_path_list, clauses: dict, asset_id=None):
    query_path_list = _common.path_string_to_list(remaining_query_path_string)

    query_path_part = query_path_list[0]

    tree_kwargs = dict()
    tree_kwargs['limit'] = kwargs['limit']
    tree_kwargs['offset'] = 0

    if 'scope' in kwargs and isinstance(kwargs['scope'], str):
        tree_kwargs['scope'] = [kwargs['scope']]

    while True:
        if not asset_id:
            tree_output = context.trees_api.get_tree_root_nodes(**tree_kwargs)  # type: AssetTreeOutputV1
        else:
            tree_kwargs['id'] = asset_id
            tree_output = context.trees_api.get_tree(**tree_kwargs)  # type: AssetTreeOutputV1

        for child in tree_output.children:  # type: TreeItemOutputV1
            if not asset_id:
                @request_safely(action_description=f'check if "{child.name}" {child.id} has '
                                                   f'datasource matching request',
                                status=context.status,
                                default_value=True)
                def _is_item_in_filter_datasources():
                    child_item_output = context.items_api.get_item_and_all_properties(
                        id=child.id)  # type: ItemOutputV1
                    for prop in ['Datasource Class', 'Datasource ID']:
                        if prop in clauses:
                            _, val = clauses[prop]
                            p_list = [_p.value for _p in child_item_output.properties if
                                      _p.name == prop]
                            if len(p_list) == 0 or p_list[0] != val:
                                return False
                    return True

                # We only filter out datasource at the top level, in case the tree is mixed
                if not _is_item_in_filter_datasources():
                    continue

            if _common.does_query_fragment_match(query_path_part, child.name, contains=False):
                actual_path_list_for_child = actual_path_list.copy()
                actual_path_list_for_child.append(child.name)
                if len(query_path_list) == 1:
                    kwargs['asset'] = child.id
                    _gather_results(context, current_query, kwargs, actual_path_list=actual_path_list_for_child)
                else:
                    _process_query_path_string(context,
                                               current_query,
                                               kwargs,
                                               _common.path_list_to_string(query_path_list[1:]),
                                               actual_path_list_for_child,
                                               clauses,
                                               child.id)

        if len(tree_output.children) < tree_kwargs['limit']:
            break

        tree_kwargs['offset'] += tree_kwargs['limit']


# noinspection PyUnusedLocal
def _gather_results_via_item_search(context: SearchContext, current_query, _actual_path_list, _result):
    item_search_preview = _result  # type: ItemSearchPreviewV1
    prop_dict = dict()

    _add_ancestors_to_prop_dict_from_item_output(context, item_search_preview, prop_dict)

    uom = item_search_preview.value_unit_of_measure if item_search_preview.value_unit_of_measure \
        else item_search_preview.source_value_unit_of_measure
    _add_to_dict(context, prop_dict, 'Value Unit Of Measure', uom)
    datasource_item_preview = item_search_preview.datasource  # type: ItemPreviewV1
    _add_to_dict(context, prop_dict, 'Datasource Name',
                 datasource_item_preview.name if datasource_item_preview else None)
    _add_common_properties(context, prop_dict, item_search_preview)


def _gather_results_via_get_tree(context: SearchContext, current_query, _actual_path_list, _result):
    tree_item_output = _result  # type: TreeItemOutputV1
    prop_dict = dict()

    for prop, _attr in [('Name', 'name'), ('Description', 'description')]:
        if prop not in current_query:
            continue

        if not _common.does_query_fragment_match(current_query[prop],
                                                 getattr(tree_item_output, _attr),
                                                 contains=(context.comparison == '~=')):
            return

    _add_ancestors_to_prop_dict(
        context, tree_item_output.type, tree_item_output.name, _actual_path_list, prop_dict)

    _add_to_dict(context, prop_dict, 'Value Unit Of Measure', tree_item_output.value_unit_of_measure)
    _add_common_properties(context, prop_dict, tree_item_output)


def _add_common_properties(context: SearchContext, prop_dict, output_object):
    _add_to_dict(context, prop_dict, 'ID', output_object.id)
    _add_to_dict(context, prop_dict, 'Name', output_object.name)
    _add_to_dict(context, prop_dict, 'Description', output_object.description)
    _add_to_dict(context, prop_dict, 'Type', output_object.type)
    _add_to_dict(context, prop_dict, 'Archived', output_object.is_archived)
    if context.all_properties:
        _add_all_properties(context, output_object.id, prop_dict)
    if context.include_swap_info:
        _add_tree(context, output_object.id, prop_dict)
    if context.estimate_sample_period is not None:
        _add_to_dict(context, prop_dict, 'Estimated Sample Period',
                     context.sample_periods[output_object.id])
    _add_to_metadata(context, prop_dict)


def _iterate_over_output(context: SearchContext, _output_func, _collection_name, _action_func, current_query,
                         kwargs, _actual_path_list):
    offset = 0
    while True:
        output = _output_func(context, kwargs, offset)

        collection = getattr(output, _collection_name)
        # Determine sample period for all signals and have NaT for non-signal items
        if context.estimate_sample_period is not None:
            for item in collection:
                if 'Signal' in item.type:
                    _estimate_sample_period(context, item.id, item.name)
                else:
                    context.sample_periods[item.id] = pd.NaT

        context.status.df.at[context.status_index, 'Time'] = _common.timer_elapsed(context.timer)
        context.status.df.at[context.status_index, 'Count'] = offset + len(collection)
        context.status.df.at[context.status_index, 'Pages'] += 1
        context.status.df.at[context.status_index, 'Result'] = 'Querying'
        context.status.update('Querying Seeq Server for items', Status.RUNNING)

        for item in collection:
            _action_func(context, current_query, _actual_path_list, item)

        if len(collection) != output.limit:
            break

        offset += output.limit


def _do_search(context: SearchContext, kwargs: dict, offset):
    kwargs['offset'] = offset
    if 'scope' in kwargs and isinstance(kwargs['scope'], str):
        kwargs['scope'] = [kwargs['scope']]
    if context.use_search_items_api:
        if context.order_by:
            kwargs['order_by'] = context.order_by
        return context.items_api.search_items(**kwargs)

    kwargs2 = {
        'offset': kwargs['offset'],
        'limit': kwargs['limit'],
        'scope': _common.get(kwargs, 'scope'),
        'exclude_globally_scoped': ('@excludeGloballyScoped' in kwargs['filters'])
    }
    if 'asset' in kwargs:
        kwargs2['id'] = kwargs['asset']
        tree_output = context.trees_api.get_tree(**kwargs2)
    else:
        tree_output = context.trees_api.get_tree_root_nodes(**kwargs2)
    if len(kwargs['types']) > 0:
        tree_output.children = [x for x in tree_output.children if x.type in kwargs['types']]
    return tree_output


def _gather_results(context: SearchContext, current_query, kwargs, actual_path_list=None):
    if context.use_search_items_api:
        _iterate_over_output(context, _do_search, 'items', _gather_results_via_item_search, current_query, kwargs,
                             actual_path_list)
    else:
        _iterate_over_output(context, _do_search, 'children', _gather_results_via_get_tree, current_query, kwargs,
                             actual_path_list)
