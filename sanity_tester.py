import logging
from app_config import boot, flow
from functools import reduce

def sanity_test(denom_symbol, denom_name, segments, inital_target_amount, denominations):
    sanity_check = reduce(
        (lambda acc, seg: acc + seg['used_amount']), segments, 0.00)
    sanity_delta = inital_target_amount - sanity_check
    smallest_denom = min(denominations.values())

    is_delta_out_of_bound = sanity_delta > 0 and sanity_delta > smallest_denom
    if is_delta_out_of_bound:
        raise RuntimeError(flow['FAILURE'])

    # mod remainig is smaller than the smallest denom unit
    is_remaining_unpayable = sanity_delta > 0 and sanity_delta < smallest_denom
    if is_remaining_unpayable:
        logging.warn(flow['SANITY_WARNING_FORMAT'].format(round(sanity_delta, 4), denom_symbol,
                                                          smallest_denom, round(smallest_denom - sanity_delta, 3)))
    else:
        logging.info(flow['SUCCESS'])

    return {
        'sanity_check': sanity_check,
        'sanity_delta': sanity_delta,
        'smallest_denom': smallest_denom,
        'is_remaining_unpayable': is_remaining_unpayable
    }