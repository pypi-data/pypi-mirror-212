import argparse
import os


def checks_if_file_is_readable(args):
    '''Cheks files's permission and existanse'''
    for file in args.files:
        if not os.path.exists(file):
            raise FileNotFoundError(f'file {file} does not exist')
        if not os.access(file, os.R_OK):
            raise PermissionError(f'file: "{file}", is not readable!')


def get_files_and_flags_from_cmd():
    '''Gets three files, order is described in help, two mutually exclusive flags (--asc is by defult True) and optional
     flag --driver, taking racer's full name. Returns all mentioned'''
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--asc', action='store_true')
    group.add_argument('--desc', action='store_true')
    parser.add_argument('-f', '--files', nargs=3,
                        help='files ordere: path_to_file_with_abbreviations, path_to_file_with_star_time, path_to_file_with_end_time)')
    parser.add_argument('-d', '--driver')
    args = parser.parse_args()
    # asc = True if neither --asc nor --desc
    if not args.asc and not args.desc:
        args.asc = True
    checks_if_file_is_readable(args)
    return args
