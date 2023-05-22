#!/usr/bin/python3
import re
import pandas as pd
import argparse
from pathlib import Path
from analysis.textual import print_stats, get_stats
from analysis.graphs import save_linear_graph, save_log_graph, save_latency_compare
from analysis.graphs import  save_linear_graph_compare, save_log_graph_compare

class DataValidationError(Exception):
    """
    Exception raised when unable to validate input data.
    
    Attributes:
        message -- explanation of the error
    """

    def __init__(self,
                 message="Could not read data line, check input file!"):
        self.message = message
        super().__init__(self.message)


def process_line(line: str) -> dict:
    """
    Process a line of text from an input file.
    
    params: Line of text as string.

    returns: Time series data point as dict.
    """
    # Given the example data below, match various components as regex groups.
    # [1684491050.574247] 64 bytes from 10.1.10.114: icmp_seq=1 ttl=254 time=0.453 ms
    #
    # \[(\d*.\d*)\]         Match the epoch date as a group.
    # .*                    Skip forward, match anything, don't care.
    # icmp_seq=(\d*)        Match the icmp_seq number as a group.
    # .*                    Skip forward, match anything, don't care.
    # time=(\d*+.?\d*)      Match the ping time in ms as a group, may be integer.
    # \sm
    pattern='^\[(\d*\.\d*)\].*icmp_seq=(\d*).*time=(\d*\.?\d*) ms'

    m = re.search(pattern, line)

    # A match fail anywhere is a hard failure as the input file may be corrupt.
    if m is not None:
        # Enforce type casting on results to prevent weirdness later.
        timestamp = float(m.group(1))
        seq = int(m.group(2)) # seq isn't that useful as it's 4 bytes but in
                                # practice seems to only use 2 bytes and loops
                                # quite regularly, including it anyway <shrug>.
        rtt = float(m.group(3))
    
        return {'timestamp': timestamp, 'seq': seq, 'rtt': rtt}
    else:
        # print("ERROR: Could not read data.")
        # raise DataValidationError
        return None


def get_df_from_file(file: str):
    pingdata = []
    pingdf = None

    print(f"Reading file {file}")

    with open(file, 'r') as f:
        for line in f:
            datapoint = process_line(line)
            if datapoint is not None:
                pingdata.append(datapoint)

    print(f"Read {len(pingdata):,} pings.")

    # Construct a Pandas dataframe from the series data.
    pingdf = pd.DataFrame.from_records(pingdata)

    # Override the unit, even though the data is ns precision.
    pingdf['timestamp'] = pd.to_datetime(pingdf['timestamp'], unit='s')

    return pingdf


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog = 'processping.py',
        description='Process and analyze output from ping.',
        epilog='NOTE: ping must be run with the -D flag to produce compatible output.')
    parser.add_argument('filename')
    parser.add_argument('-c', '--compare', help="Compare log data with file")      # option that takes a value

    args = parser.parse_args()

    return args


def main():
    args = get_args()

    # TODO: Many functions accept a str value for filename, pathlib is compatible
    # with this but should be updated to accept a pathlib spec instead.
    filea = Path(args.filename)
    if args.compare is not None:
        fileb = Path(args.compare)

    # List will contain more than one DataFrame if --compare is used.
    dflist = []
    if args.compare is None:
        df = get_df_from_file(filea)
        print_stats(df)
        dflist.append(df)
    else:
        for filename in [args.filename, args.compare]:
            df = get_df_from_file(filename)
            print_stats(df)
            dflist.append(df)

    # A single stats summarising all input files.
    dfstats = get_stats(dflist)
    dfstats.to_csv('stats.csv')

    # TODO: Need to rewrite this to show as table (or just use the CSV output)
    # print_stats(dfstats)


    # TODO: Passing by list reference is a lazy hack that needs fixing.
    save_linear_graph(dflist[0], filea.stem)
    save_log_graph(dflist[0], filea.stem)

    # TODO: Passing by list reference is a lazy hack that needs fixing.
    if args.compare is not None:
        save_linear_graph_compare(dflist[0], dflist[1], fileb.stem)
        save_log_graph_compare(dflist[0], dflist[1], fileb.stem)
        save_latency_compare(dfstats)


# execute only if run as a script
if __name__ == "__main__":
    main()

