#!/usr/bin/env python3

# -------------------------------------------------------------------------------
# InternetSpeedLogger
#
# A Python script that continuously monitors and logs your internet speed. It
# tests both download and upload speeds at regular intervals and records the
# data in a CSV file for easy analysis and tracking. Ideal for auditing your
# network performance or ISP reliability over time.
#
# https://github.com/Andreas-Menzel/InternetSpeedLogger
# https://pypi.org/project/InternetSpeedLogger/
# -------------------------------------------------------------------------------
# @author: Andreas Menzel
# @license: MIT License
# -------------------------------------------------------------------------------

import argparse
import csv
from datetime import datetime
from pathlib import Path
from signal import signal, SIGINT
from speedtest import Speedtest
from time import sleep


script_version = '1.1.0'


def argparse_check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue

def setupArgumentParser():
    parser = argparse.ArgumentParser(
        prog='InternetSpeedLogger',
        description="""
A Python script that continuously monitors and logs your internet
speed. It tests both download and upload speeds at regular intervals
and records the data in a CSV file for easy analysis and tracking.
Ideal for auditing your network performance or ISP reliability over
time.
            """,
        epilog="""
Default location of the log-file:
    A .csv-file will be created, which will contain all logged information.
    Default Filename: "YYYY-MM-DD_HH:MM:SS_internet_speeds.csv"
    Default Location: typically "/home/<username>" on Linux
                      typically "C:\\Users\\<username>" on Windows
                      typically "/Users/<username>" on macOS
            """,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + script_version)
    parser.add_argument('-i', '--interval',
                        help='Testing interval in seconds. Make sure that the interval is not shorter than the time needed for testing. (default: %(default)s)',
                        type=argparse_check_positive,
                        default=60)
    parser.add_argument('-d', '--duration',
                        help='Duration of the entire test runs. The script will automatically end after this duration. Set to <= 0 for infinite. (default: %(default)s)',
                        type=int,
                        default=0)
    parser.add_argument('-l', '--log_file',
                        help='Filename for the log-file. NOTE: ".csv" will be automatically appended to the filename!',
                        default='')
    return parser.parse_args()


def main():
    args = setupArgumentParser()

    st = Speedtest()

    if args.log_file != '':
        csv_file = Path(f'{args.log_file}.csv')
    else:
        # Set to default/fallback location.
        csv_file = Path(
            f'{Path.home().joinpath(datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))}_internet_speeds.csv')

    print(f"""\
InternetSpeedLogger (version {script_version})

Testing interval: {args.interval} s
Testing duration: {args.duration} s
Log-file: "{csv_file.absolute()}"\
    """)

    csv_file.parent.mkdir(parents=True, exist_ok=True)
    with open(csv_file, mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Download (bps)', 'Upload (bps)',
                        'Datetime', 'Download (Mbps)', 'Upload (Mbps)'])
        file.flush()

    start_time = datetime.now().timestamp()
    while True:
        testing_time = datetime.now()
        testing_timestamp = testing_time.timestamp()

        print(f'\nTesting at {testing_time.strftime("%Y-%m-%d %H:%M:%S")}')
        print(f'\tDownload: ', end='')
        download = st.download()
        print(f'{round(download / 1000000)} Mbps')
        print(f'\tUpload: ', end='')
        upload = st.upload()
        print(f'{round(upload / 1000000)} Mbps')

        with open(csv_file, mode='w') as file:
            writer = csv.writer(file)
            writer.writerow([
                testing_timestamp,
                download,
                upload,

                testing_time.strftime("%Y-%m-%d %H:%M:%S"),
                round(download / 1000000),
                round(upload / 1000000)
            ])
            file.flush()

        if(args.duration > 0
                and testing_timestamp + args.interval > start_time + args.duration):
            break

        sleep(args.interval - (testing_timestamp - start_time)
              % args.interval)


def end(signal_received, frame):
    print('Goodbye!')
    exit(0)


if __name__ == "__main__":
    signal(SIGINT, end)
    main()
    end(None, None)
