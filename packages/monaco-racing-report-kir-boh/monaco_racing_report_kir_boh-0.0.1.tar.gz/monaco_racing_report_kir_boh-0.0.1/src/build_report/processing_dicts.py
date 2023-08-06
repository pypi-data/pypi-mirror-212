from datetime import datetime, timedelta
import logging
import warnings
from . import constants


def inserts_info_into_ordered_racers_dict(time_list, dict_with_racers_info):
    '''Return dict which keys are places(1-20) and values are list [driver's name, comand, time]. Since time_list is
    ordered, for each time func finds racer with same time, then adds info needed to be print in ordered_recers_dict '''
    ordered_recers_dict = {}
    place = 0
    list_with_used_keys = []
    for time in time_list:
        for abbrev in dict_with_racers_info:
            if str(dict_with_racers_info[abbrev][constants.const_absolute_time]) == str(
                    time) and abbrev not in list_with_used_keys:
                # Pice of code(shit) above is just enoying! Is there any stuf to skip current key after passing it to my dict?
                # Do not replace place += 1, becouse dict is looping till the end, so func will return only last racer
                # with datetime.timedelta(0)
                place += 1
                ordered_recers_dict[str(place)] = [dict_with_racers_info[abbrev][constants.const_name],
                                                   dict_with_racers_info[abbrev][constants.const_comand],
                                                   str(dict_with_racers_info[abbrev][constants.const_absolute_time])]
                list_with_used_keys.append(abbrev)  # This line is disgusting to, i hate it...
    return ordered_recers_dict


def time_counter(dict_with_racers_info):
    '''Add inner dict to each abrev consisting of key 'absolute_time' and value racer's absolute_time,
        which is timedelta obj, warning is raised when start_time is bigger than end_time, racer who has invalid time
        gets timedelta(0) which is zero'''
    for abbrev, inner_dict in dict_with_racers_info.items():
        start_time = datetime.strptime(inner_dict[constants.const_start_time], constants.const_time_format)
        end_time = datetime.strptime(inner_dict[constants.const_end_time], constants.const_time_format)
        if start_time > end_time:
            warnings.showwarning(
                f'Racer "{dict_with_racers_info[abbrev][constants.const_name]}", abrev - "{abbrev}", has invalid time!',
                UserWarning, filename='processing_dicts.py', lineno=35)
            invalid_time = timedelta(days=0, hours=0, minutes=0, milliseconds=0, microseconds=0)
            dict_with_racers_info[abbrev][constants.const_absolute_time] = invalid_time
        elif start_time < end_time:
            absolute_time = end_time - start_time
            dict_with_racers_info[abbrev][constants.const_absolute_time] = absolute_time
    return dict_with_racers_info


def time_snatcher(dict_with_racers_info, args):
    '''Returns list with ordered, depending on flags, time. Each time is timedelta obj!'''
    list_with_absolute_time = []
    for inner_dict in dict_with_racers_info.values():
        list_with_absolute_time.append(inner_dict[constants.const_absolute_time])
    if args.asc:
        list_with_absolute_time = sorted(list_with_absolute_time)
    elif args.desc:
        list_with_absolute_time = sorted(list_with_absolute_time, reverse=True)
    return list_with_absolute_time
