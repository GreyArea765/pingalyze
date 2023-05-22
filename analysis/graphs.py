from pandas import DataFrame
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt

COLOUR1 = 'blue'
COLOUR2 = 'maroon'
COLOUR3 = 'green'


def _human_format(num, pos):
    """
    Formatter for matplotlib/Pandas plots.  Returns number with magnitude.
    Positive prefixes from 'K' to 'P' are supported.

    Params:
        num: Number to convert.
        pos: Position along axis (not used).

    Returns:
        (str) SI prefixed string.
    """
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0

    # If first digit after the decimal place is a zero, don't show it.
    if num % 1 == 0.0:
        val = '%.0f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])
    else:
        val = '%.1f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])
    return val


def save_linear_graph(df: DataFrame, filename: str) -> None:

    fig, ax = plt.subplots()

    formatter = FuncFormatter(_human_format)

    ax.yaxis.set_major_formatter(formatter)

    ax.set_xlabel('latency (ms)')
    ax.set_ylabel('# packets Linear')
    ax.set_title(f'Ping response distribution (linear)')

    ax = plt.hist(df['rtt'], log=False, color=COLOUR1)

    plt.savefig(f'{filename}-lin.png')


def save_log_graph(df: DataFrame, filename: str) -> None:
    """
    Save a histogram chart showing distribution of ping latency with a
    logarithmic Y axis.

    Params:
        df (DataFrame): Pandas DataFrame containing ping RTT series data.

        filename: (stt): Name of the filename to save.

    Returns:
        None
    """
    fig, ax = plt.subplots()

    ax.set_xlabel('latency (ms)')
    ax.set_ylabel('# packets Linear')
    ax.set_title(f'Ping response distribution (logarithmic)')

    ax.hist(df['rtt'], log=True, histtype='bar', color=COLOUR1)

    plt.savefig(f'{filename}-log.png')


def save_linear_graph_compare(df1: DataFrame, df2: DataFrame, filename: str) -> None:

    fig, ax = plt.subplots()

    formatter = FuncFormatter(_human_format)

    ax.yaxis.set_major_formatter(formatter)

    ax.set_xlabel('latency (ms)')
    ax.set_ylabel('# packets Linear')
    ax.set_title(f'Ping response distribution (linear)')

    # ax = plt.hist(df1['rtt'], log=False)

    colours = [COLOUR1, COLOUR2]
    ax.hist((df1['rtt'], df2['rtt']), log=False, histtype='bar', color=colours, label=['A', 'B'])

    ax.legend()

    plt.savefig(f'{filename}-lin-compare.png')


def save_log_graph_compare(df1: DataFrame, df2: DataFrame, filename: str) -> None:

    fig, ax = plt.subplots()

    formatter = FuncFormatter(_human_format)

    ax.yaxis.set_major_formatter(formatter)

    ax.set_xlabel('latency (ms)')
    ax.set_ylabel('# packets Linear')
    ax.set_title(f'Ping response distribution (log)')

    # ax = plt.hist(df1['rtt'], log=False)

    colours = [COLOUR1, COLOUR2]
    ax.hist((df1['rtt'], df2['rtt']), log=True, histtype='bar', color=colours, label=['A', 'B'])

    ax.legend()

    plt.savefig(f'{filename}-log-compare.png')


def save_latency_compare(df: DataFrame):
    dfplot = df['rtt_95th_percentile']

    COLOUR1 = 'blue'
    COLOUR2 = 'maroon'
    COLOUR3 = 'green'

    colours = [COLOUR1, COLOUR2, COLOUR3]

    # dfplot.plot(kind='bar',logy=True
    plot = dfplot.plot(kind='bar', logy=False, color=colours, rot=0).get_figure()

    # plt.savefig(f'{filename}-latency-compare.png')
    plot.savefig(f'latency-compare.png')
