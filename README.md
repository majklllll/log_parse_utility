Interview app - log parsing utility v1.01:
==============================================================================
Create a Python CLI application that will help you parse logs of various
kinds. The code should be easy to deploy and run and must be hosted in
a publicly available git repository. A test suite must be included as well.
Your solution can be as robust or as minimal as you want but please keep in
mind that this is your opportunity to show us what you can do. :)

You may leverage any open source Python library.
You may not leverage the 'head', 'tail' or 'grep' utilities.

Usage: `./util.py [OPTION]... [FILE]`

Supported options:
---------------------
```
  -h, --help         Print help
  -f, --first=NUM    Print first NUM lines
  -l, --last=NUM     Print last NUM lines
  -t, --timestamps   Print lines that contain a timestamp in HH:MM:SS format
  -i, --ipv4         Print lines that contain an IPv4 address, matching IPs
                     are highlighted
  -I, --ipv6         Print lines that contain an IPv6 address (standard
                     notation), matching IPs are highlighted
```
If FILE is omitted, standard input is used instead.

If multiple options are used at once, the result is the intersection of their
results.

The result (matching lines) is printed to standard output.

Example supported usage:
------------------------
```
./util.py -h
<prints help>

cat test_0.log | ./util.py --first 10
<prints the first 10 lines of test_0.log>

./util.py -l 5 test_1.log
<prints the last 5 lines of test_1.log>

./utils.py --timestamps test_2.log
<prints any lines from test_2.log that contain a timestamp>

./util.py --ipv4 test_3.log
<prints any lines from test_3.log that contain an IPv4 address>

./util.py --ipv6 test_4.log
<prints any lines from test_4.log that contain an IPv6 address>

./util.py --ipv4 --last 50 test_5.log
<prints any of the last 50 lines from test_5.log that contain an IPv4 address>
```

