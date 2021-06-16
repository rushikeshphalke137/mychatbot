#!/usr/bin/env python3

import csv
import re
import os
from copy import deepcopy
from pathlib import Path
from pprint import pformat # format strings with pretty print for readability
from logging import (getLogger, getLevelName, basicConfig as logging_basicConfig,
        CRITICAL, ERROR, WARNING, INFO, DEBUG)
logger = getLogger(__name__)
logger.setLevel(WARNING)

# The following will set up the root logger handler with a default formatter
logging_basicConfig()
# Can INSTEAD use the following to customize for the local logger
#console_handler = logging.StreamHandler()
#console_format = logging.Formatter(logging.BASIC_FORMAT) # using the default format
#console_handler.setFormatter(console_format)
#logger.addHandler(console_handler)

# create a compact type to make it clearer what's being stored
class diseaseStates(object):
    __slots__ = ('confirmed', 'deaths', 'recovered')

    def __init__(self, confirmed = 0, deaths = 0, recovered = 0):

        self.confirmed = confirmed
        self.deaths = deaths
        self.recovered = recovered

    def __str__(self):
        return f"confirmed: {self.confirmed}, deaths: {self.deaths}, recovered: {self.recovered}"

class outputFile(object):
    """
    Created as an open
    """
    __slots__ = ('path', 'header', 'handle', 'valid')

    def __init__(self, path = None, header = None):

        self.path = path
        assert self.path is not None
        self.header = header
        assert self.header is not None
        self.handle = path.open(mode = 'w')
        assert self.handle.closed is not True
        self.valid = True
        self.handle.write(f"{header}\n")

    def close(self):
        self.handle.close()
        self.valid = False

area_level_choices = ("region", "name_region")


logger.info(f'Starting logging level: {getLevelName(logger.level)}')

def main(input):
    """
    A main entry point into this module or library of functionality.
    """

    if 'log_level' in input:
        logger.setLevel(input['log_level'].upper())

    logger.info(f'Logging level in main function: {getLevelName(logger.level)}')

    assert 'data_dir' in input
    data_dir_path = Path(input['data_dir'])
    assert data_dir_path.exists()
    logger.info(f'data_dir = {pformat(data_dir_path)}')

    assert 'area_level' in input
    area_level = input['area_level']
    area_level_dir_path = Path(data_dir_path / f"{area_level}s")
    Path.mkdir(area_level_dir_path, exist_ok = True)
    logger.info(f'area_level_dir_path = {pformat(area_level_dir_path)}')

    file_name_pattern = re.compile('^(.+)-([0-1][0-9]-[0-3][0-9]-[0-9]{4})$')

    header_string = "date,totalConfirmed,totalDeaths,totalRecovered,newConfirmed,newDeaths,newRecovered"
    logger.debug(f"header_string = {header_string}")

    output_files = dict()

    #region_total_states, region_total_states_prev = dict(), dict()

    # just here for outside debug logging. Probably can eventually delete
    pre_day_record, cur_day_record, date_diffs = dict(), dict(), dict()

    name, Region, date_string = None, None, None

    area_level_totals = dict()


    # Excluding these records (based on what is not included in the webif)
    exclude_set = (('Others (repatriated from Wuhan)', 'USA'),
            ('Unknown location US', 'USA'),
            ('USVI', 'USA'),
            ('Vermon', 'USA'))

    for file_path in sorted(data_dir_path.glob('nssac-ncov-sd-??-*.csv')):
        logger.info(f"processing {file_path}")

        file_name_prefix = file_name_pattern.match(file_path.stem)[1]
        date_string = file_name_pattern.match(file_path.stem)[2]

        logger.debug(f"file_name_prefix = {file_name_prefix}    date_string = {date_string}")

        with file_path.open() as csv_file:
            next(csv_file) # skip first line
            csv_reader = csv.reader(csv_file, delimiter = ',')

            for name, Region, Last_Update, Confirmed, Deaths, Recovered in csv_reader:

                if (name, Region) in exclude_set: continue

                assert area_level in area_level_choices
                if area_level == 'region': this_area_level = (Region,)  # Making these tuples will help later (needs comma)
                else: this_area_level = (name, Region)

                # Can collect any new output file we might need
                area_level_file_path = Path(area_level_dir_path / f"{file_name_prefix}-summary-{'_'.join(this_area_level).lower()}.csv")

                if this_area_level not in output_files:
                    logger.debug(f"trying to (create and) open  {area_level_file_path}")
                    output_file = output_files[this_area_level] = outputFile(area_level_file_path, header_string)
                    logger.info(f"opened {output_file.path} for output")

                current_states = diseaseStates(int(Confirmed), int(Deaths), int(Recovered))

                cur_name_region_record = cur_day_record[(name, Region)] = current_states

                pre_name_region_record = pre_day_record.setdefault((name, Region), diseaseStates())

                diff_confirmed = cur_name_region_record.confirmed - pre_name_region_record.confirmed
                diff_deaths = cur_name_region_record.deaths - pre_name_region_record.deaths
                diff_recovered = cur_name_region_record.recovered - pre_name_region_record.recovered
                if diff_confirmed < 0 or diff_deaths < 0 or diff_recovered < 0:
                    logger.warning(f"Cummulative total shouldn't go down! {pformat((name, Region))}")
                    logger.warning(f"diff_confirmed: {diff_confirmed}, diff_deaths: {diff_deaths}, diff_recovered: {diff_recovered}")
                    logger.warning(f"{date_string}")
                    logger.warning(f"{pre_name_region_record}")
                    logger.warning(f"{cur_name_region_record}")

                diff_states = diseaseStates(diff_confirmed, diff_deaths, diff_recovered)
                date_diffs.setdefault(date_string, dict())[(name, Region)] = diff_states

                pre_day_record[(name, Region)] = cur_day_record[(name, Region)]

                # Just initalizing these here, for later
                if this_area_level not in area_level_totals: area_level_totals[this_area_level] = diseaseStates()
                assert isinstance(this_area_level, tuple)

    for date, area_levels_diffs in date_diffs.items():
        logger.info(f"preparing {date} data for output")

        if area_level == 'region':
            # agregate regions
            region_diffs = dict()
            for (name, region), diff in area_levels_diffs.items():
                logger.debug(f"region: {region}    name: {name}   diff: {diff.confirmed} {diff.deaths} {diff.recovered}")
                # Make (region,) tuple just like (name, region)
                if (region,) not in region_diffs: region_diffs[(region,)] = diseaseStates()
                region_diffs[(region,)].confirmed += diff.confirmed
                region_diffs[(region,)].deaths += diff.deaths
                region_diffs[(region,)].recovered += diff.recovered
            
            area_levels_diffs = region_diffs

        # prepare and write output
        for area_lvl, diff in area_levels_diffs.items():
            assert isinstance(area_lvl, tuple)
            logger.debug(f"writing {date} data for {area_lvl}")
            area_level_totals[area_lvl].confirmed += diff.confirmed
            area_level_totals[area_lvl].deaths += diff.deaths
            area_level_totals[area_lvl].recovered += diff.recovered

            totals_string = f"{area_level_totals[area_lvl].confirmed},{area_level_totals[area_lvl].deaths},{area_level_totals[area_lvl].recovered}"
            diff_string = f"{diff.confirmed},{diff.deaths},{diff.recovered}"

            output_files[area_lvl].handle.write(f"{date},{totals_string},{diff_string}\n")

    # close all the output files
    for output_file in output_files.values():
        output_file.close()
        logger.info(f"closed {output_file.path}")
        logger.debug(f"output_file.handle can be reopened: {output_file.valid}")


if __name__ == '__main__':
    import argparse
    import json

    # Create the parser
    cli_parser = argparse.ArgumentParser(description='Generate region files')

    cli_parser.add_argument('data_dir',
                           type = str,
                           default = None,           # Value to use if it is empty
                           help ='the folder containing all the input csv data files')

    cli_parser.add_argument('-a',
                           '--area_level',   # Long version of flag argument,
                           choices = area_level_choices, # Limit the valid choices. --help will display these.
                           type = str,
                           default = "region",           # Value to use if it is empty
                           help ='Set the land aggregate counts on.')

    # Generate appropriate choices to limit command line input. Can be dynamically generated.
    loglevel_choices = tuple( getLevelName(level).lower() for level in ( CRITICAL, ERROR, WARNING, INFO, DEBUG ) )

    cli_parser.add_argument('-l',
                           '--log_level',   # Long version of flag argument,
                           choices = loglevel_choices, # Limit the valid choices. --help will display these.
                           type = str,
                           default = None,           # Value to use if it is empty
                           help ='Set the amount of information about the run you wish to see.')

    args = cli_parser.parse_args()

    config = {}

#    # The default config
#    default_config_file = Path('default_config.json').resolve(strict = True)
#    config = json.load(default_config_file.open())
#    default_config_report = f"config from default file: {pformat(config)}"

#    # Update with custom config
#    custom_config_report = None
#    if args.config_filename and args.config_filename.endswith('.json'):
#        custom_config_file = Path(args.config_filename).resolve(strict = True)
#        config.update(json.load(custom_config_file.open()))
#        custom_config_report = f"config update with custom file: {pformat(config)}"

    # Make sure the config is valid.
#    config_schema_file = Path('schema.json').resolve(strict = True)
#    config_schema = json.load(config_schema_file.open())
#    validate_json(instance = config, schema = config_schema)

    # Update with config options from the parser (only use ones with values set).
    commandline_config = {key: val for key, val in vars(args).items() if val}
    if commandline_config:
        config.update(commandline_config)
        commandline_config_report = f"config update from command line: {pformat(config)}"

    # Finally set the log level, so it's consistent, before logging output.
    if 'log_level' in config:
        logger.setLevel(config['log_level'].upper())

#logger.info(default_config_report)
#    if custom_config_report: logger.info(custom_config_report)
    if commandline_config: logger.info(commandline_config_report)

    main(config)
