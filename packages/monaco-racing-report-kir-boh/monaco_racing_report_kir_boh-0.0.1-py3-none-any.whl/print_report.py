from build_report import build_report
from build_report import constants
import prepare_data_to_be_print


def print_report():
    '''Checks if driver was specifided, then calls proper func'''
    dict_to_be_printed, args = build_report()
    if args.driver:
        print_report_if_args_driver(dict_to_be_printed, args)
    else:
        print_report_if_no_args_provided(dict_to_be_printed)


def print_report_if_args_driver(dict_to_be_printed, args):
    '''Finds proper driver in the dict, prits his info.
    Dict keys are places(1-20) and values are list [driver's name, comand, time]'''
    prepare_data_to_be_print.check_if_driver_exists(dict_to_be_printed, args)
    for list_with_items_to_be_printed in dict_to_be_printed.values():
        if list_with_items_to_be_printed[0] == args.driver:
            list_with_info_to_print = []
            string_to_be_printed = prepare_data_to_be_print.string_to_print_preparer(list_with_items_to_be_printed)
            print(string_to_be_printed)


def print_report_if_no_args_provided(dict_to_be_printed):
    '''Prints first 16 drivers, then '______________' and other drivers
    Dict keys are places(1-20) and values are list [driver's name, comand, time]'''
    for place, list_with_items_to_be_printed in dict_to_be_printed.items():
        string_to_print = prepare_data_to_be_print.string_to_print_preparer(list_with_items_to_be_printed)
        if int(place) == constants.const_predivided_racers:
            print(constants.const_divider * constants.const_divider_length)
        print(string_to_print)


if __name__ == '__main__':
    print_report()
