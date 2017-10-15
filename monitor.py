from location import *


"""
The Monitor module contains the Monitor class, the Activity class,
and a collection of constants. Together the elements of the module
help keep a record of activities that have occurred.

Activities fall into two categories: Rider activities and Driver
activities. Each activity also has a description, which is one of
request, cancel, pickup, or drop-off.

=== Constants ===
@type RIDER: str
    A constant used for the Rider activity category.
@type DRIVER: str
    A constant used for the Driver activity category.
@type REQUEST: str
    A constant used for the request activity description.
@type CANCEL: str
    A constant used for the cancel activity description.
@type PICKUP: str
    A constant used for the pickup activity description.
@type DROPOFF: str
    A constant used for the dropoff activity description.
"""

RIDER = "rider"
DRIVER = "driver"

REQUEST = "request"
CANCEL = "cancel"
PICKUP = "pickup"
DROPOFF = "dropoff"


class Activity:
    """An activity that occurs in the simulation.

    === Attributes ===
    @type timestamp: int
        The time at which the activity occurred.
    @type description: str
        A description of the activity.
    @type identifier: str
        An identifier for the person doing the activity.
    @type location: Location
        The location at which the activity occurred.
    """

    def __init__(self, timestamp, description, identifier, location):
        """Initialize an Activity.

        @param self: Activity
        @param timestamp: int
        @param description: str
        @param identifier: str
        @param location: Location
        @rtype: None

        >>> activity = Activity(0, 'request', 'rider1', Location(1, 1))
        >>> print(activity.time)
        0
        """
        self.description = description
        self.time = timestamp
        self.id = identifier
        self.location = location
        
    def __str__(self):
        """ Return a string representation.

        @param self: Activity
        @return: str

        >>> activity = Activity(0, 'request', 'rider1', Location(1, 1))
        >>> print(activity)
        0---rider1---request---(1,1)
        """
        return "{}---{}---{}---{}".format(self.time, self.id, self.description, self.location)


class Monitor:
    """A monitor keeps a record of activities that it is notified about.
    When required, it generates a report of the activities it has recorded.
    """

    # === Private Attributes ===
    # @type _activities: dict[str, dict[str, list[Activity]]]
    #       A dictionary whose key is a category, and value is another
    #       dictionary. The key of the second dictionary is an identifier
    #       and its value is a list of Activities.

    def __init__(self):
        """Initialize a Monitor.

        @param self: Monitor
        @rtype self: None

        >>> monitor = Monitor()
        """
        self._activities = {
            RIDER: {},
            DRIVER: {}
        }
        """@type _activities: dict[str, dict[str, list[Activity]]]"""

    def __str__(self):
        """Return a string representation.

        @param self: Monitor
        @rtype: str

        >>> monitor = Monitor()
        >>> print(monitor)
        Monitor (0 drivers, 0 riders)
        """
        return "Monitor ({} drivers, {} riders)".format(
                len(self._activities[DRIVER]), len(self._activities[RIDER]))

    def notify(self, timestamp, category, description, identifier, location):
        """Notify the monitor of the activity.

        @param self: Monitor
        @param timestamp: int
            The time of the activity.
        @param category: DRIVER | RIDER
            The category for the activity.
        @param description: REQUEST | CANCEL | PICKUP | DROP_OFF
            A description of the activity.
        @param identifier: str
            The identifier for the actor.
        @param location: Location
            The location of the activity.
        @rtype: None

        >>> monitor = Monitor()
        >>> monitor.notify(0, RIDER, REQUEST, 'rider1', Location(1,1))
        >>> print(monitor._activities[RIDER].keys())
        dict_keys(['rider1'])
        """
        if identifier not in self._activities[category]:
            self._activities[category][identifier] = []

        activity = Activity(timestamp, description, identifier, location)
        self._activities[category][identifier].append(activity)

    def report(self):
        """Return a report of the activities that have occurred.

        @param self: Monitor
        @rtype: dict[str, object]

        >>> monitor = Monitor()
        >>> print(sum(monitor.report().values()))
        0
        """
        return {"rider_wait_time": self._average_wait_time(),
                "driver_total_distance": self._average_total_distance(),
                "driver_ride_distance": self._average_ride_distance()}

    def _average_wait_time(self):
        """Return the average wait time of riders that have either been picked
        up or have cancelled their ride.

        @param self: Monitor
        @rtype: float

        >>> monitor = Monitor()
        >>> monitor._average_wait_time()
        0
        """
        wait_time = 0
        count = 0
        for activities in self._activities[RIDER].values():
            # A rider that has less than two activities hasn't finished
            # waiting (they haven't cancelled or been picked up).
            if len(activities) >= 2:
                # The first activity is REQUEST, and the second is PICKUP
                # or CANCEL. The wait time is the difference between the two.
                wait_time += activities[1].time - activities[0].time
                count += 1
        try:        
            return wait_time / count
        except ZeroDivisionError:
            return 0        

    def _average_total_distance(self):
        """Return the average distance drivers have driven.

        Total distance = distance that the driver drives to the rider's origin
                        + distance that the driver drives to the the rider's
                          destination if applicable.

        @param self: Monitor
        @rtype: float

        >>> monitor = Monitor()
        >>> monitor._average_total_distance()
        0
        """
        total_shifts = dict()
        for activities in self._activities[DRIVER].items():
            if len(activities[1]) >= 2:
                total_shifts[activities[0]] = \
                    [s for s in activities[1]]
                        
        count = len(total_shifts)
        distance = 0
        for event in total_shifts.values():            
            for i in range(1, len(event)):
                distance += manhattan_distance(event[i].location, event[i-1].location)            
        try:
            return distance / count
        except ZeroDivisionError:
            return 0        

    def _average_ride_distance(self):
        """Return the average distance drivers have driven on rides.

        @param self: Monitor
        @rtype: float

        >>> monitor = Monitor()
        >>> monitor._average_ride_distance()
        0
        """
        total_rides = dict()
        for activities in self._activities[DRIVER].items():
            if len(activities[1]) >= 4:
                total_rides[activities[0]] = \
                    [a for a in activities[1]
                     if a.description == PICKUP or a.description == DROPOFF]
                                
        count = len(total_rides)
        distance = 0        
        for request in total_rides.values():            
            for i in range(1, len(request), 2):
                distance += manhattan_distance(request[i].location, request[i-1].location)            
        try:
            return distance / count
        except ZeroDivisionError:
            return 0

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    monitor = Monitor()
    print(sum(monitor.report().values()))
    print(monitor.report())
