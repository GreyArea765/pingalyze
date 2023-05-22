from pandas import DataFrame
import pandas as pd

def print_stats(df: DataFrame) -> None:
    """
    Print detailed analysis info to the console.
    """
    print()
    print(f"{len(df):,} pings processed.")
    print(f"The first ping was on {df.iloc[0]['timestamp']}")
    print(f"The last ping was on {df.iloc[len(df) - 1]['timestamp']}")
    print(f"RTT max: {df['rtt'].max(): .3f} ms")
    print(f"RTT min: {df['rtt'].min(): .3f} ms")
    print(f"RTT mean: {df['rtt'].mean(): .3f} ms")
    print(f"RTT std dev: {df['rtt'].std(): .3f} ms")
    print(f"RTT 95th percentile: {df['rtt'].quantile(.95): .3f} ms")
    print()


def get_stats(dflist: list) -> DataFrame:
    """
    Pass a list of DataFrames to analyze
    """
    series = []
    for df in dflist:
        datum = _get_stat_datum(df)
        series.append(datum)

    dfstats = pd.DataFrame.from_records(series)

    return dfstats


def _get_stat_datum(df: DataFrame) -> dict:
    """
    When passed a DataFrame containing ping RTT series data, analyze and return
    the information as a new DataFrame.
    """

    num_pings = len(df)
    first_ping = df.iloc[0]['timestamp']
    last_ping = df.iloc[num_pings - 1]['timestamp']
    rtt_max = df['rtt'].max()
    rtt_min = df['rtt'].min()
    rtt_mean = df['rtt'].mean()
    rtt_stddev = df['rtt'].std()
    rtt_95th_percentile = df['rtt'].quantile(.95)

    datum = {'num_pings': num_pings,
             'first_ping': first_ping,
             'last_ping': last_ping,
             'rtt_max': rtt_max,
             'rtt_min': rtt_min,
             'rtt_mean': rtt_mean,
             'rtt_stddev': rtt_stddev,
             'rtt_95th_percentile': rtt_95th_percentile
    }

    return datum