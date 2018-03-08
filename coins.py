
from app_config import flow
import logging

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

def compute_change(denom_symbol, denom_name, denominations, inital_target_amount):
    logging.info("Minimal change will be computed according to %s%s" % (denom_symbol, inital_target_amount))
    sorted_denominations = sorted(denominations, key=denominations.__getitem__, reverse=True)
    segments = list()
    denom_symbol, denom_name = (denom_symbol.strip(), denom_name.strip())

    for current_denom in sorted_denominations:
        remaining_amount = segments[-1]['target_amount'] if segments else inital_target_amount
        segment = extract_segment(denominations, denom_symbol, denom_name, current_denom, remaining_amount)

        if segment:  # i.e. currency denom matched and extracted
            segments.append(segment)
            logging.info(flow['SEGMENT_EXTRACT_FORMAT'].format(**segment))

    return segments
