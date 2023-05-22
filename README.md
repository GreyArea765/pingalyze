# Analyze Ping Logs (pingalyze)

Pingalyze takes logfile output fromt the linux commnd `ping` and generates
analytic data in CSV and graph form.

## Installation

Once you've downloaded and/or extracted the code to the system, install the
requirements with:

`pip install -r requirements.txt`

## Generating log files

The parser is very primitive and based on regex pattern patching on the output
of the `ping` command with the mandatory`-D` flag.

The log files must contain output like the example below for the code to work:
```
PING 192.168.0.254 (192.168.0.254) 56(84) bytes of data.
[1684491055.490728] 64 bytes from 192.168.0.254: icmp_seq=1 ttl=254 time=0.701 ms
[1684491055.691722] 64 bytes from 192.168.0.254: icmp_seq=2 ttl=254 time=0.635 ms
[1684491055.892580] 64 bytes from 192.168.0.254: icmp_seq=3 ttl=254 time=0.553 ms
...
...
...
```

`ping -D <hostname> > logfile.log`

However for improved precision the recommended command would be:

`ping -D -A <hostname> > logfile.log`

And to limit the run to one hour (in seconds), use:

`ping -w 3600 -D -A <hostname> > logfile.log`

## Using pingalyze

Help is available by running:

`python3 pingalyze.py -h`

Running the following command will generate analysis graphs and CSV files
containing statistics to the current directory.

`python3 pingalyze.py <logfile.log>`

To run a comparison against another log file:

`python3 pingalyze.py <logfile.log> --compare <logfile2.log>`
