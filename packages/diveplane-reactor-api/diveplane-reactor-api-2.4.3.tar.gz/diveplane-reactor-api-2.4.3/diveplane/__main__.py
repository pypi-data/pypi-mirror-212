import argparse
from argparse import RawTextHelpFormatter
from datetime import date
import sys

from diveplane.client import __version__ as version_string, diveplane_banner

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=diveplane_banner,
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--version', dest='version', action='store_const', const=True,
        required=False, default=False,
        help='Display the version and quit.'
    )

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
    else:
        args = parser.parse_args()
        if args.version:
            print(diveplane_banner)
            print(f"""
Diveplane (R) client version: {version_string}
Copyright (c) 2018-{date.today().year}, Diveplane Corporation. All rights reserved.
""")
