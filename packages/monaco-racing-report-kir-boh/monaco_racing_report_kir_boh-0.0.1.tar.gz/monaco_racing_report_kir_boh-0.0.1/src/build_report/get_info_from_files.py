from . import constants


def abbreviations_decoder(dict_with_racers_info, path_to_file_with_racers_info):
    '''Add inner dict to each abrev consisting of keys 'name', 'comand' and values racer's name, racer's comand'''
    list_with_racers_names = []
    with open(path_to_file_with_racers_info, 'r', encoding='utf-8') as file:
        for line in file:
            if not line.isspace():
                line = line.split('_')
                abbreviation, name, comand = line
                dict_with_racers_info[abbreviation][constants.const_name] = name.strip()
                dict_with_racers_info[abbreviation][constants.const_comand] = comand.strip()
    return dict_with_racers_info


def return_dict_with_time_and_racer_abbreviations(dict_with_racers_info, path_to_file_with_star_time_and_abreviations,
                                                  path_to_file_with_end_time_and_abreviations):
    '''One_by-one read files with racers' time, return dict which keys are abreviations values are inner dicts with
    start/end time keys and values start/end time in str format'''
    path_to_files_with_time_and_abreviations = [path_to_file_with_star_time_and_abreviations,
                                                path_to_file_with_end_time_and_abreviations]
    for i, path_to_file_with_time_and_abreviations in enumerate(path_to_files_with_time_and_abreviations, start=1):
        with open(path_to_file_with_time_and_abreviations, 'r') as file:
            for line in file:
                if not line.isspace():
                    abbreviation, date, racer_time = get_time_date_and_racer_abbreviations_from_line(line)
                    if i == 1:
                        dict_with_racers_info[abbreviation] = {constants.const_start_time: racer_time.strip()}
                    elif i == 2:
                        dict_with_racers_info[abbreviation][constants.const_end_time] = racer_time.strip()
    return dict_with_racers_info


def get_time_date_and_racer_abbreviations_from_line(line_to_process):
    '''Reads file, returns abbreviation, date, racer_time in str format'''
    # 'i' is used to identify wether char belongs to abbreviation(chars 1-3), date(chars 4-16) or time(chars > 17)
    abbreviation, date, racer_time = '', '', ''
    for i, char in enumerate(line_to_process, start=1):
        if i <= 3:
            abbreviation += char
        elif i <= 16:
            date += char
        elif i > 17:
            racer_time += char
    return abbreviation, date, racer_time
