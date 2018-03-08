from argparse import Action as ArgParseAction
import logging


class DenominationsAction(ArgParseAction):
    def __init__(self, option_strings, dest, *a, **kw):
        super(DenominationsAction, self).__init__(option_strings, dest, **kw)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, self.extract_denominations(values))

    @staticmethod
    def parse_denomination(raw_denom):
        real_name, real_value = raw_denom.split(':')
        if real_name and real_value:
            return real_name.strip(), float(real_value)

        raise Exception(
            "Invalid denomination format. Should be name:realValue and not {0}".format(raw_denom))

    @staticmethod
    def extract_denominations(raw_denoms):
        return dict(map(lambda d: DenominationsAction.parse_denomination(d), raw_denoms))
