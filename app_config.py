import sys
from denominations_action import DenominationsAction

flow = {
    "SANITY_WARNING_FORMAT": "Warning - Unable to match coins for remaining amount of {1}{0}. Suggesting to use {1}{2}. If you do so, you'll lose additional {1}{3}",
    "SEGMENT_EXTRACT_FORMAT": "- Remaining amount is {target_amount} after using {num_denom_units} * {current_denom}s which is {denom_symbol}{used_amount} {denom_name}",
    "invalid_denomination": "Invalid denomination format. Should be name:realValue and not %s"
}

boot = {
    "default_help": 'No help at the moment. You could try to ask nicely.',
    "description": "Computes the minimum amount of denominations needed in order to reach the total amount given (as change, as in money).",
    "cmd_args": {
        "denominations": {
            "display": ["--denominations", "-d"],
            "args": {
                "nargs": "+",
                "action": DenominationsAction
            },
            "help": "Dict of denominations with corrosponding real value",
            "usage": "Enter in the form of -d=k1:v1 k2:v2 => -d=cent:0.01, quarter:0.25...)"
        },
        "denom_name": {
            "display": [
                "--denom-name",
                "-n"
            ],
            "help": "Display name of currency. As in Dollar.')",
            "args": {}
        },
        "denom_symbol": {
            "display": [
                "--denom-symbol",
                "-s"
            ],
            "args": {},
            "help": "Currency symbol. As in $.')"
        },
        "amount": {
            "display": [
                "--amount",
                "-a"
            ],
            "args": {
                "dest": "inital_target_amount",
                "type": float
            },
            "help": "The amount of changed that will be divided into chnage.')"
        }
    }
}
