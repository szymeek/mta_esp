import csv
import os
from datetime import datetime

def append_timing_to_csv(event, cycle, position, value):
    """
    Log a timing event to timing_data.csv

    event: str, description (e.g. 'cycle', 'keypress', 'position_delay', etc)
    cycle: int, cycle number
    position: int or None, which position (1/2/3) or None for full cycle
    value: float, time taken (seconds)
    """
    filename = 'timing_data.csv'
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['timestamp', 'event', 'cycle', 'position', 'time_seconds']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            'timestamp': datetime.now().isoformat(timespec='seconds'),
            'event': event,
            'cycle': cycle,
            'position': position if position is not None else "",
            'time_seconds': "{:.4f}".format(value)
        })
