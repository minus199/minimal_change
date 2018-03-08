# 
'''
Usage: 
    python3 coins.py \
        -d fifty_shekel:50 ten_shekel:10 five_shekel:5 shekel:1 half_shekel:0.5 quarter_shekel:0.25 agora:0.01 \
        -n ILS -a 1234.455 -s ₪
'''




from app_config import boot, flow
from functools import reduce
import logging
import json
import os
import argparse
import sys


SANITY_WARNING_FORMAT = "Warning - Unable to match coins for remaining amount of {1}{0}. Suggesting to use {1}{2}. If you do so, you'll lose additional {1}{3}"
SEGMENT_EXTRACT_FORMAT = "- Remaining {denom_symbol}{target_amount}, used {num_denom_units} * {current_denom}s which is {denom_symbol}{used_amount}{denom_name}"


def extract_segment(denominations, denom_symbol, denom_name, current_denom, target_amount=0):
    if target_amount == 0:
        return None

    current_denom_val = denominations.get(current_denom)
    remaining_amount = target_amount % current_denom_val
    used_amount = target_amount - remaining_amount
    num_denom_units = used_amount / current_denom_val if used_amount > 0 else 0

    if num_denom_units == 0:
        return None

    return {
        'current_denom': current_denom,
        'current_denom_val': current_denom_val,
        'remaining_amount': remaining_amount,
        'used_amount': used_amount,
        'num_denom_units': int(num_denom_units),
        'target_amount': round(target_amount - used_amount, 4),
        'denom_symbol': denom_symbol,
        'denom_name': denom_name
    }


def do_sanity(denom_symbol, denom_name, segments, inital_target_amount, denominations):
    sanity_check = reduce(
        (lambda acc, seg: acc + seg['used_amount']), segments, 0.00)
    sanity_delta = inital_target_amount - sanity_check
    smallest_denom = min(denominations.values())

    is_delta_out_of_bound = sanity_delta > 0 and sanity_delta > smallest_denom
    if is_delta_out_of_bound:
        raise RuntimeError("Computation failed, not sure why")

    # mod remainig is smaller than the smallest denom unit
    is_remaining_unpayable = sanity_delta > 0 and sanity_delta < smallest_denom

    if is_remaining_unpayable:
        format_args = round(sanity_delta, 4), denom_symbol, smallest_denom, round(
            smallest_denom - sanity_delta, 3)
        logging.warn(SANITY_WARNING_FORMAT.format(*format_args))
    else:
        logging.info("Computation successful!")

    return {
        'sanity_check': sanity_check,
        'sanity_delta': sanity_delta,
        'smallest_denom': smallest_denom,
        'is_remaining_unpayable': is_remaining_unpayable
    }


def compute(denom_symbol, denom_name, denominations, inital_target_amount=12271.314):
    sorted_denominations = sorted(
        denominations, key=denominations.__getitem__, reverse=True)
    segments = list()
    for current_denom in sorted_denominations:
        remaining_amount = segments[-1]['target_amount'] if segments else inital_target_amount
        segment = extract_segment(denominations, denom_symbol.strip(
        ), denom_name.strip(), current_denom, remaining_amount)

        if segment:  # i.e. currency denom matched and extracted
            segments.append(segment)
            logging.warn(SEGMENT_EXTRACT_FORMAT.format(**segment))

    return segments


'''
def prev_init_data():
    parser = argparse.ArgumentParser(
        description='Computes the minimum amount of denominations needed in order to reach the total amount given (as change, as in money).')

    parser.add_argument('--denominations', '-d', dest='denominations', nargs='+',
                        help='Enter in the form of -d=k1:v1 k2:v2 -- -d=cent:0.01, quarter: 0.25...')

    parser.add_argument('--denom-name', '-n', dest='denom_name',
                        help='Display name of currency. As in Dollar.')

    parser.add_argument('--denom-symbol', '-s',
                        dest='denom_symbol', help='Currency symbol. As in $.')

    parser.add_argument('--amount', '-a', dest='inital_target_amount', type=float,
                        help='The amount of changed that will be divided into chnage.')

    user_args = parser.parse_args(sys.argv[1:])

    denominations = {}
    for denom in user_args.denominations:
        real_name, real_value = denom.split(':')
        if not real_name or not real_value:
            raise Exception(
                "Invalid denomination format. Should be name:realValue and not {0}".format(denom))

        denominations[real_name.strip()] = float(real_value)

    user_args.denominations = denominations
    return dict((k.strip(), v) for k, v in user_args.__dict__.viewitems())
'''


def extract_initial_user_data():
    # Load help menu
    parser = argparse.ArgumentParser(description=boot['description'])
    default_help = boot.get('default_help')
    for (arg_name, arg_meta) in boot.get('cmd_args').items():
        display = arg_meta.pop('display')
        arg_args = arg_meta.pop('args')
        arg_args.update(dest=arg_args.pop('dest', arg_name),
                        help=arg_meta.pop('help', default_help))

        parser.add_argument(*display, **arg_args)

    # Parse user input into cmd args
    user_args = parser.parse_args(sys.argv[1:])

    # Convert to plain dict
    return user_args.__dict__

context = extract_initial_user_data()
segments = compute(**context)
do_sanity(segments=segments, **context)
