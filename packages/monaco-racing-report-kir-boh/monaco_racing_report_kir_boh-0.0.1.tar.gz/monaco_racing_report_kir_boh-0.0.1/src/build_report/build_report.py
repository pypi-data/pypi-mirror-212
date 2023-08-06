from . import get_info_from_files, processing_dicts, parser


def build_report():
    '''Return dict which keys are places(1-20) and values are list [driver's name, comand, time], and args from cmd '''
    args = parser.get_files_and_flags_from_cmd()
    racers_info_dict = {}
    racers_info_dict = get_info_from_files.return_dict_with_time_and_racer_abbreviations(racers_info_dict,
                                                                                         args.files[1],
                                                                                         args.files[2])
    racers_info_dict = get_info_from_files.abbreviations_decoder(racers_info_dict, args.files[0])
    racers_info_dict = processing_dicts.time_counter(racers_info_dict)
    ordered_time_list = processing_dicts.time_snatcher(racers_info_dict, args)
    ordered_recers_dict = processing_dicts.inserts_info_into_ordered_racers_dict(ordered_time_list, racers_info_dict)
    return ordered_recers_dict, args
