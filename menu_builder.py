import argparse
import sys
from app_config import boot
import logging

def parse_input_args():
    logging.debug("Parsing input data")
    # Load help menu
    parser = argparse.ArgumentParser(description=boot['description'])
    default_help = boot.get('default_help')
    for (arg_name, arg_meta) in boot.get('cmd_args').items():
        display = arg_meta.pop('display')
        arg_args = arg_meta.pop('args')
        arg_args.update(dest=arg_args.pop('dest', arg_name),
                        help=arg_meta.pop('help', default_help))

        parser.add_argument(*display, **arg_args)
        logging.debug("Added %s as menu arg" % arg_name)

    # Parse user input into cmd args
    user_args = parser.parse_args(sys.argv[1:])

    # Convert to plain dict
    logging.debug("Input data parsed.")
    return user_args.__dict__
