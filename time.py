import datetime
import time

def start_election():
    """Starts the election at 8am."""
    start_time = datetime.time(hour=8, minute=0)
    while True:
        now = datetime.datetime.now().time()
        if now >= start_time:
            break
        time.sleep(60)  # Check again in 1 minute

    print("The election has started!")


def end_election():
    """Ends the election at 12 noon."""
    end_time = datetime.time(hour=12, minute=0)
    while True:
        now = datetime.datetime.now().time()
        if now >= end_time:
            break
        time.sleep(60)  # Check again in 1 minute

    print("The election has ended!")
