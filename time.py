import datetime

# set the start and end time for the election
start_time = datetime.time(hour=8, minute=0, second=0)
end_time = datetime.time(hour=12, minute=0, second=0)

def is_election_open():
    # get the current time
    current_time = datetime.datetime.now().time()

    # check if the current time is within the election window
    return current_time >= start_time and current_time < end_time
