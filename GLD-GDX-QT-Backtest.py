import numpy as np

def initialize(context):
    schedule_function(check_pair_status, date_rules.every_day(), time_rules.market_close(minutes=1))

    context.stock1 = symbol('GLD')
    context.stock2 = symbol('GDX')

    # Our threshold for trading on the z-score
    context.entry_threshold = 0.4
    context.exit_threshold = 0

    # Flags to tell us if we're currently in a trade
    context.currently_long_the_spread = False
    context.currently_short_the_spread = False

    context.signals = []


def check_pair_status(context, data):

    # For notational convenience
    s1 = context.stock1
    s2 = context.stock2

    # Get pricing history
    prices = data.history([s1, s2], "price", 20, '1d')

    if True:
        signal = prices[s1].iloc[-1]*0.4577-prices[s2].iloc[-1] - 33.1
        context.signals.append(signal)
        record('std',np.std(context.signals))
        record('signal',signal)



        # Our two entry cases
        if signal > context.entry_threshold and \
            not context.currently_short_the_spread and not context.currently_long_the_spread:
            order(s1, -50) # short top
            order(s2, 100) # long bottom
            context.currently_short_the_spread = True
            print 'short entry'

        elif signal < -context.entry_threshold and \
            not context.currently_long_the_spread and not context.currently_short_the_spread:
            order(s1,50) # long top
            order(s2, -100) # short bottom
            context.currently_long_the_spread = True
            print 'long entry'

        # Our exit case
        elif signal > context.exit_threshold and context.currently_long_the_spread:
            order_target_percent(s1, 0)
            order_target_percent(s2, 0)
            context.currently_long_the_spread = False
            print 'long exit'

        elif signal < context.exit_threshold and context.currently_short_the_spread:
            order_target_percent(s1, 0)
            order_target_percent(s2, 0)
            context.currently_short_the_spread = False
            print 'short exit'
        #record('zscore', zscore)
