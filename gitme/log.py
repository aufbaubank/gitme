import logging

level_number = [
    'critical',
    'error',
    'warn',
    'warning',
    'info',
    'debug'
]

levels = [
    logging.CRITICAL,
    logging.ERROR,
    logging.WARNING,
    logging.WARNING,
    logging.INFO,
    logging.DEBUG
]


def configure_logger(parsed_args):

    level_ix_from_str = level_number.index(parsed_args.loglevel)

    if level_ix_from_str > parsed_args.verbose:
        highest_level = level_ix_from_str
    else:
        highest_level = parsed_args.verbose

    level = levels[highest_level]
    logging.basicConfig(
        format='%(levelname)s: %(message)s',
        level=level
    )
