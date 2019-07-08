from dronekit import Command
command_list = [] # List of commands from original WP file
diffs = [] # List of (lat diff, long diff): differences between waypoints
new_command_list = [] # Recentered list of commands
wp_list = [] # List of all waypoints

def readMission(aFileName):
    """
    Load a mission from a file into a list. The mission definition is in the Waypoint file
    format (http://qgroundcontrol.org/mavlink/waypoint_protocol#waypoint_file_format).

    Returns a list of latitude, longitude pairs.
    """
    global command_list
    global wp_list
    command_list = []
    wp_list = []

    print("Reading mission...")
    # Opens the filename
    with open(aFileName) as f:
        for i, line in enumerate(f):
            # Raises exception if not correct file
            if i==0:
                if not line.startswith('QGC WPL 110'):
                    raise Exception('File is not supported WP version')
            else:
                # Grabs the latitude and longitude, appending to coordinate list
                linearray=line.strip().split('\t')
                print(linearray)
                command_type = float(linearray[3])
                # If the command is a new waypoint, add it to the list to calculate
                if command_type == 16.0:
                    wp_list.append(linearray)
                command_list.append((linearray))

def calcDiff():
    """
    Calculates the difference between waypoints. Right now only supports
    takeoff and waypoint commands.
    """
    global wp_list
    global diffs

    # Goes through each coordinate in list of coordinates
    # Calculates the difference between each pair
    # Appends to an array
    for i in range(len(wp_list) - 1):
        # Grab the latitudes and longitudes from the waypoint list
        next_lat = float(wp_list[i + 1][8])
        lat = float(wp_list[i][8])
        next_long = float(wp_list[i + 1][9])
        long = float(wp_list[i][9])

        lat_diff = next_lat - lat
        long_diff = next_long - long
        diffs.append((lat_diff, long_diff))

def createNewCoords(vehicle):
    """
    Makes a list of new commands centered around the new home point.
    """
    global diffs
    global command_list
    global new_command_list

    # Gets the current latitude, longitude, and altitude of the drone
    lat = vehicle.location.global_relative_frame.lat
    long = vehicle.location.global_relative_frame.lon
    alt = vehicle.location.global_frame.alt

    # Deep copies the old command list to modify
    new_command_list = command_list.copy()

    prev_lat = lat
    prev_long = long
    new_command_list[0][8] = prev_lat
    new_command_list[0][9] = prev_long
    new_command_list[0][10] = alt

    # Adds the difference between coordinates to the previous latitude
    # and longitude by indexing into difference array
    for i in range(1, len(new_command_list)):
        if float(new_command_list[i][3]) == 16:
            lat_diff, long_diff = diffs.pop(0)
            new_command_list[i][8] = lat_diff + prev_lat
            new_command_list[i][9] = long_diff + prev_long
            prev_lat = float(new_command_list[i][8])
            prev_long = float(new_command_list[i][9])

    print('New Command List:')
    for command in new_command_list:
        print(command)


def makeCommands():
    # Makes commands out of the new command list with modified coordinates
    # From the 3DR example code
    global new_command_list
    print('Making new commands...')
    missionList = []
    for command in new_command_list:
        ln_index=int(command[0])
        ln_currentwp=int(command[1])
        ln_frame=int(command[2])
        ln_command=int(command[3])
        ln_param1=float(command[4])
        ln_param2=float(command[5])
        ln_param3=float(command[6])
        ln_param4=float(command[7])
        ln_param5=float(command[8])
        ln_param6=float(command[9])
        ln_param7=float(command[10])
        ln_autocontinue=int(command[11])
        cmd = Command(0, 0, 0, ln_frame, ln_command, ln_currentwp, ln_autocontinue, ln_param1, ln_param2, ln_param3, ln_param4, ln_param5, ln_param6, ln_param7)
        missionList.append(cmd)
    return missionList

def processMission(fileName, vehicle):
    """
    Ties everything together.
    First, reads the current mission, calculating difference between lats and longs
    With these differences, generates a list of new commands.
    Formats these commands appropriately.
    Parameters:
        filename (str) of WP Formats
        vehicle (dronekit-vehicle)
    Returns: dronekit-python formatted commands
    """
    readMission(fileName)
    calcDiff()
    createNewCoords(vehicle)
    changedMissionList = makeCommands()
    return changedMissionList

#print(processMission('mission_basic.txt'))
