from build_report import const_for_join


def check_if_driver_exists(dict_to_be_printed, args):
    'Looks for driver in list of names taken from dict'
    list_with_names = []
    for inner_list in dict_to_be_printed.values():
        list_with_names.append(inner_list[0])
    if args.driver not in list_with_names:
        raise ValueError(f'There is no driver named "{args.driver}"!')


def string_to_print_preparer(list_with_items_to_be_printed):
    '''Returns str (joined list) with name, comand, time devided by '|'
    Brendon Hartley|SCUDERIA TORO ROSSO HONDA|0:01:13.179000'''
    list_with_info_to_print = []
    for item in list_with_items_to_be_printed:
        list_with_info_to_print.append(str(item))
    string_to_be_printed = const_for_join.join(list_with_info_to_print)
    return string_to_be_printed
