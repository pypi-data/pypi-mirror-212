import csv
from datetime import datetime
from signal import signal, SIGINT
from speedtest import Speedtest
from time import sleep


# Make sure that the interval is not shorter than the time needed for testing.
interval_in_secs = 30

# Duration of the entire test runs. The script will automatically end after this
# duration. Set to <= 0 for infinite.
testing_duration_secs = 60*60*24

# Filename for the results
csv_file = "internet_speeds.csv"


def main():
    st = Speedtest()

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

        if(testing_duration_secs > 0
                and testing_timestamp + interval_in_secs > start_time + testing_duration_secs):
            break

        sleep(interval_in_secs - (testing_timestamp - start_time)
              % interval_in_secs)


def end(signal_received, frame):
    print('Goodbye!')
    exit(0)


if __name__ == "__main__":
    signal(SIGINT, end)
    main()
    end(None, None)
