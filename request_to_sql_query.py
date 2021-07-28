import sqlite3

def select_statement_parsing(**kwargs):
    if('show' in kwargs):
        init_select_params = kwargs['show']
        show_list = []
        for item in init_select_params:
            # TODO: Insert CPI condition and processing
            aggregate_params = item.split(" ")
            if(aggregate_params[0] == 'CPI'):
                show_list.append(aggregate_params[1] + "(spend/installs) as " + aggregate_params[0])
            else:
                show_list.append(aggregate_params[1] + "(" + aggregate_params[0] + ") as " + aggregate_params[0])
        select_params = kwargs['break_down'] + show_list
        return "select " + ", ".join(select_params) + " from AdjustData "
    else:
        return ""

def condition_statement_parsing(**kwargs):
    if('filter' in kwargs):
        number_of_filters = len(kwargs['filter'].keys())
        filter_list = []
        if('country' in kwargs['filter']):
            filter_list.append("country = " + repr(kwargs['filter']['country']))
        if('os' in kwargs['filter']):
            filter_list.append("os = " + repr(kwargs['filter']['os']))
        if('channel' in kwargs['filter']):
            filter_list.append("channel = " + repr(kwargs['filter']['channel']))
        if('date' in kwargs['filter']):
            request_filter = kwargs['filter']['date'].split(" ")
            if(request_filter[0] in ['<', '>', '=']):
                filter_list.append("date " + request_filter[0] + " " + repr(request_filter[1]))
            else:
                filter_list.append("date >= " + repr(request_filter[0]) + " and date < " + repr(request_filter[1]))
        if(number_of_filters > 1):
            return "where (" + " AND ".join(filter_list) + ") "
        else:
            return "where " + "".join(filter_list) + " "
    else:
        return ""

def group_statement_parsing(**kwargs):
    if('break_down' in kwargs):
        return "group by " + ", ".join(kwargs['break_down']) + " "
    else:
        return ""

def order_statement_parsing(**kwargs):
    if('sort' in kwargs):
        return "order by " + kwargs['sort'] + " "
    else:
        return ""
