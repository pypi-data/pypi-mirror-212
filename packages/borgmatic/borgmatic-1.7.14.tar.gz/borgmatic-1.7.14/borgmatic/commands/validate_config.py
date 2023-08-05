import logging
import sys
from argparse import ArgumentParser

import borgmatic.config.generate
from borgmatic.config import collect, validate

logger = logging.getLogger(__name__)


def parse_arguments(*arguments):
    '''
    Given command-line arguments with which this script was invoked, parse the arguments and return
    them as an ArgumentParser instance.
    '''
    config_paths = collect.get_default_config_paths()

    parser = ArgumentParser(description='Validate borgmatic configuration file(s).')
    parser.add_argument(
        '-c',
        '--config',
        nargs='+',
        dest='config_paths',
        default=config_paths,
        help=f'Configuration filenames or directories, defaults to: {config_paths}',
    )
    parser.add_argument(
        '-s',
        '--show',
        action='store_true',
        help='Show the validated configuration after all include merging has occurred',
    )

    return parser.parse_args(arguments)


def main():  # pragma: no cover
    arguments = parse_arguments(*sys.argv[1:])

    logging.basicConfig(level=logging.INFO, format='%(message)s')

    config_filenames = tuple(collect.collect_config_filenames(arguments.config_paths))
    if len(config_filenames) == 0:
        logger.critical('No files to validate found')
        sys.exit(1)

    found_issues = False
    for config_filename in config_filenames:
        try:
            config, parse_logs = validate.parse_configuration(
                config_filename, validate.schema_filename()
            )
        except (ValueError, OSError, validate.Validation_error) as error:
            logging.critical(f'{config_filename}: Error parsing configuration file')
            logging.critical(error)
            found_issues = True
        else:
            for log in parse_logs:
                logger.handle(log)

            if arguments.show:
                print('---')
                print(borgmatic.config.generate.render_configuration(config))

    if found_issues:
        sys.exit(1)

    logger.info(f"All given configuration files are valid: {', '.join(config_filenames)}")
