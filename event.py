"""Simulation Events

This file should contain all of the classes necessary to model the different
kinds of events in the simulation.
"""
from rider import Rider, WAITING, CANCELLED, SATISFIED
from dispatcher import Dispatcher
from driver import Driver
from location import deserialize_location, Location
from monitor import Monitor, RIDER, DRIVER, REQUEST, CANCEL, PICKUP, DROPOFF


class Event:
    """An event.

    Events have an ordering that is based on the event timestamp: Events with
    older timestamps are less than those with newer timestamps.

    This class is abstract; subclasses must implement do().

    You may, if you wish, change the API of this class to add
    extra public methods or attributes. Make sure that anything
    you add makes sense for ALL events, and not just a particular
    event type.

    Document any such changes carefully!

    === Attributes ===
    @type timestamp: int
        A timestamp for this event.
    """

    def __init__(self, timestamp):
        """Initialize an Event with a given timestamp.

        @type self: Event
        @type timestamp: int
            A timestamp for this event.
            Precondition: must be a non-negative integer.
        @rtype: None

        >>> Event(7).timestamp
        7
        """
        self.timestamp = timestamp

    # The following six 'magic methods' are overridden to allow for easy
    # comparison of Event instances. All comparisons simply perform the
    # same comparison on the 'timestamp' attribute of the two events.
    def __eq__(self, other):
        """Return True iff this Event is equal to <other>.

        Two events are equal iff they have the same timestamp.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first == second
        False
        >>> second.timestamp = first.timestamp
        >>> first == second
        True
        """
        return self.timestamp == other.timestamp

    def __ne__(self, other):
        """Return True iff this Event is not equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first != second
        True
        >>> second.timestamp = first.timestamp
        >>> first != second
        False
        """
        return not self == other

    def __lt__(self, other):
        """Return True iff this Event is less than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first < second
        True
        >>> second < first
        False
        """
        return self.timestamp < other.timestamp

    def __le__(self, other):
        """Return True iff this Event is less than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first <= first
        True
        >>> first <= second
        True
        >>> second <= first
        False
        """
        return self.timestamp <= other.timestamp

    def __gt__(self, other):
        """Return True iff this Event is greater than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first > second
        False
        >>> second > first
        True
        """
        return not self <= other

    def __ge__(self, other):
        """Return True iff this Event is greater than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first >= first
        True
        >>> first >= second
        False
        >>> second >= first
        True
        """
        return not self < other

    def __str__(self):
        """Return a string representation of this event.

        @type self: Event
        @rtype: str
        """
        raise NotImplementedError("Implemented in a subclass")

    def do(self, dispatcher, monitor):
        """Do this Event.

        Update the state of the simulation, using the dispatcher, and any
        attributes according to the meaning of the event.

        Notify the monitor of any activities that have occurred during the
        event.

        Return a list of new events spawned by this event (making sure the
        timestamps are correct).

        Note: the "business logic" of what actually happens should not be
        handled in any Event classes.

        @type self: Event
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        raise NotImplementedError("Implemented in a subclass")


class RiderRequest(Event):
    """A rider requests a driver.

    === Attributes ===
    @type rider: Rider
        The rider.
    """

    def __init__(self, timestamp, rider):
        """Initialize a RiderRequest event.

        @param self: RiderRequest
        @param rider: Rider
        @rtype: None
        
        >>> dispatcher = Dispatcher()
        >>> monitor = Monitor()
        >>> rider_Bathe = Rider('Bathe', WAITING, 5, Location(1, 2), Location(5, 8))
        >>> rider_rq = RiderRequest(0, rider_Bathe)
        """
        super().__init__(timestamp)
        self.rider = rider

    def do(self, dispatcher, monitor):
        """Assign the rider to a driver or add the rider to a waiting list.
        
        If the rider is assigned to a driver, the driver starts driving to
        the rider' origin and hence a pickup event is scheduled and returned.

        Return a Cancellation event as well even no driver is assigned to the rider.

        @param self: RiderRequest
        @param dispatcher: Dispatcher
        @param monitor: Monitor
        @rtype: list[Event]
        
        >>> dispatcher = Dispatcher()
        >>> monitor = Monitor()
        >>> rider_Bathe = Rider('Bathe',WAITING, 5, Location(1,2), Location(5,8))
        >>> rider_rq = RiderRequest(0, rider_Bathe)
        >>> events = rider_rq.do(dispatcher, monitor)
        >>> print(len(events))
        1
        >>>
        """
        monitor.notify(self.timestamp, RIDER, REQUEST, self.rider.id, self.rider.origin)

        events = []
        driver = dispatcher.request_driver(self.rider)
        if driver is not None:
            travel_time = driver.start_drive(self.rider.origin)
            events.append(Pickup(self.timestamp + travel_time, self.rider, driver))
        events.append(Cancellation(self.timestamp + self.rider.patience, self.rider))
        return events

    def __str__(self):
        """Return a string representation of this event.

        @param self: RiderRequest
        @rtype: str
        
        >>> dispatcher = Dispatcher()
        >>> monitor = Monitor()
        >>> rider_Bathe = Rider('Bathe',WAITING, 5, Location(1,2), Location(5,8))
        >>> rider_rq = RiderRequest(0, rider_Bathe)
        >>> print(rider_rq)
        0 -- Bathe: Request a driver
        >>>
        """
        return "{} -- {}: Request a driver".format(self.timestamp, self.rider.id)


class DriverRequest(Event):
    """A driver requests a rider.

    === Attributes ===
    @type driver: Driver
        The driver.
    """

    def __init__(self, timestamp, driver):
        """Initialize a DriverRequest event.

        @param self: DriverRequest
        @param driver: Driver
        @rtype: None
        
        >>> dispatcher = Dispatcher()
        >>> monitor = Monitor()
        >>> driver_Atom = Driver('Atom', Location(0,0), 1)
        >>> driver_rq = DriverRequest(1, driver_Atom)
        >>>  
        """
        super().__init__(timestamp)
        self.driver = driver

    def do(self,dispatcher,monitor):
        """Register the driver, if this is the first request, and
        assign a rider to the driver, if one is available.

        If a rider is available, return a Pickup event initialized.

        The monitor is notified of the request event even no rider is assigned
        to the driver.

        @param self: DriverRequest
        @param dispatcher: Dispatcher
        @param monitor: Monitor
        @rtype: list[Event]
        
        >>> dispatcher = Dispatcher()
        >>> monitor = Monitor()
        >>> driver_Atom = Driver('Atom', Location(0,0), 1)
        >>> driver_rq = DriverRequest(1, driver_Atom)
        >>> events = driver_rq.do(dispatcher, monitor)
        >>> print(len(events))
        0
        >>>
        """
        # Notify the monitor about the request.

        # Request a rider from the dispatcher.
        # If there is one available, the driver starts driving towards the
        # rider, and the method returns a Pickup event for when the driver
        # arrives at the riders location.

        monitor.notify(self.timestamp, DRIVER, REQUEST, self.driver.id, 
                       self.driver.location)       
        
        events = []
        rider = dispatcher.request_rider(self.driver)
        if rider is not None:
            travel_time = self.driver.start_drive(rider.origin)
            events.append(Pickup(self.timestamp + travel_time, rider, self.driver))
        return events 

    def __str__(self):
        """Return a string representation of this event.

        @param self: DriverRequest
        @rtype: str
        
        >>> dispatcher = Dispatcher()
        >>> monitor = Monitor()
        >>> driver_Atom = Driver('Atom', Location(0,0), 1)
        >>> driver_rq = DriverRequest(1, driver_Atom)
        >>> print(driver_rq)
        1 -- Atom: Request a rider
        """
        return "{} -- {}: Request a rider".format(self.timestamp, self.driver.id)


class Cancellation(Event):
    """A rider cancels his driver request.
    
    === Attributes ===   
    @type rider: Rider
        The rider.
    """   
    def __init__(self, timestamp, rider):
        """Initialize a Cancellation event.

        A cancellation event is initialized when the rider requested
        a driver without regard to if the rider was assigned a driver or not.
        
        @param self: Cancellation
        @param rider: Rider
        @rtype: None
        
        >>> dispatcher = Dispatcher()
        >>> monitor = Monitor()
        >>> rider_Bathe = Rider('Bathe',WAITING, 5, Location(1,2), Location(5,8))
        >>> rider_rq = RiderRequest(0, rider_Bathe)
        >>> cancellation = rider_rq.do(dispatcher, monitor)[0]
        >>> print(cancellation.timestamp)
        5
        >>>
        """     
        super().__init__(timestamp)
        self.rider = rider
        
    def do(self, dispatcher, monitor):
        """ Execute the scheduled cancellation event.
        
        The cancellation event is scheduled when the rider requested a driver.
        So the event is executed at the time when the rider's patience runs out . 
        
        However, if the rider was picked up and his status became
        'satisfied', the cancellation event is not allowed.
        
        The cancellation event also removes the rider from the dispatcher's
        waiting list if applicable.
        
        The monitor is notified of the cancellation even if executed.
        
        No future even is scheduled when the cancellation is finished.
        
        @param self: Cancellation
        @param dispatcher: Dispatcher
        @param monitor: Monitor
        @rtype: list[event] 
        
        >>> dispatcher = Dispatcher()
        >>> monitor = Monitor()
        >>> rider_Bathe = Rider('Bathe',WAITING, 5, Location(1,2), Location(5,8))
        >>> rider_rq = RiderRequest(0, rider_Bathe)
        >>> cancellation = rider_rq.do(dispatcher, monitor)[0]
        >>> event = cancellation.do(dispatcher, monitor)
        >>> print(len(event))
        0
        >>>
        """        
        events = []
        if self.rider.status == SATISFIED:
            return events         
        if self.rider in dispatcher.waiting_riders:
            dispatcher.cancel_ride(self.rider)
        self.rider.status = CANCELLED
        monitor.notify(self.timestamp, RIDER, CANCEL, self.rider.id, 
                       self.rider.origin)
        return events
    
    def __str__(self):
        """ Return a string representation.
        
        @param self: Cancellation
        @rtype: str
        
        >>> dispatcher = Dispatcher()
        >>> monitor = Monitor()
        >>> rider_Bathe = Rider('Bathe',WAITING, 5, Location(1,2), Location(5,8))
        >>> rider_rq = RiderRequest(0, rider_Bathe)
        >>> cancellation = rider_rq.do(dispatcher, monitor)[0]
        >>> print(cancellation)
        5 -- Bathe: Cancel the ride
        >>>
        """             
        return '{} -- {}: Cancel the ride'.format(self.timestamp, self.rider.id)
        

class Pickup(Event):
    """A driver picks up the assigned rider.
        
        === Attributes ===   
        @param driver: Driver
            The driver.
        @type rider: Rider
            The rider
    """  
    def __init__(self, timestamp, rider, driver):
        """Initialize a Pickup event.
       
        A pickup event is initialized when the request of a rider and a driver 
        are matched and then the assignment is finished by the dispatcher.
               
        @param self: Pickup
        @param rider: Rider
        @param driver Driver
        @rtype: None
               
        >>> dispatcher = Dispatcher()
        >>> monitor = Monitor()
        >>> rider_Bathe = Rider('Bathe',WAITING, 5, Location(1,2), Location(5,8))
        >>> driver_Atom = Driver('Atom', Location(0,0), 1)
        >>> rider_rq = RiderRequest(0, rider_Bathe)
        >>> cancellation = rider_rq.do(dispatcher,monitor)[0]
        >>> driver_rq = DriverRequest(1, driver_Atom)
        >>> pickup = driver_rq.do(dispatcher, monitor)[0]
        >>> print(pickup.timestamp)
        4
        >>>
        """  
        super().__init__(timestamp)
        self.rider = rider
        self.driver = driver
    
    def do(self, dispatcher, monitor):
        """ Execute the scheduled pickup event.
                
        A pickup event is scheduled when the requests of a rider and a driver
        are matched and hence the assignment is finished by the dispatcher.
        
        So the event is executed when the driver arrives the assigned rider's origin 
        even the rider may cancel the request before the pickup event.
                
        If the pickup is successfully done, a drop-off event is scheduled and the rider's
        status becomes 'satisfied'. If the pickup is failed because it's happened after
        the rider's cancellation, a new request for a rider is send out immediately.
        
        The monitor is notified of the pickup or driver_request event.

        @param self: Pickup
        @param dispatcher: Dispatcher
        @param monitor: Monitor
        @rtype: list[event] 
                
        >>> dispatcher = Dispatcher()
        >>> monitor = Monitor()
        >>> rider_Bathe = Rider('Bathe',WAITING, 5, Location(1,2), Location(5,8))
        >>> driver_Atom = Driver('Atom', Location(0,0), 1)
        >>> rider_rq = RiderRequest(0, rider_Bathe)
        >>> cancellation = rider_rq.do(dispatcher,monitor)[0]
        >>> driver_rq = DriverRequest(1, driver_Atom)
        >>> pickup = driver_rq.do(dispatcher, monitor)[0]
        >>> print(len(pickup.do(dispatcher, monitor)))
        1
        >>>
        """         
        events = []
        self.driver.end_drive()
        if self.rider.status == "waiting":
            travel_time = self.driver.start_ride(self.rider)
            events.append(Dropoff(self.timestamp + travel_time, self.driver, 
                                  self.rider))
            self.rider.status = "satisfied"
            monitor.notify(self.timestamp, DRIVER, PICKUP, self.driver.id, 
                           self.driver.location)
            monitor.notify(self.timestamp, RIDER, PICKUP, self.rider.id, 
                           self.rider.origin)
            return events
        elif self.rider.status == "cancelled":
            events.append(DriverRequest(self.timestamp, self.driver))
            monitor.notify(self.timestamp, DRIVER, REQUEST, self.driver.id, 
                           self.driver.location)
            return events 
        
    def __str__(self):
        """Return a string representation of this event.
        
        @param self: Pickup
        @rtype: str
        
        >>> dispatcher = Dispatcher()
        >>> monitor = Monitor()
        >>> rider_Bathe = Rider('Bathe',WAITING, 5, Location(1,2), Location(5,8))
        >>> driver_Atom = Driver('Atom', Location(0,0), 1)
        >>> rider_rq = RiderRequest(0, rider_Bathe)
        >>> cancellation = rider_rq.do(dispatcher,monitor)[0]
        >>> driver_rq = DriverRequest(1, driver_Atom)
        >>> pickup = driver_rq.do(dispatcher, monitor)[0]
        >>> print(pickup)
        4 -- Atom -- Bathe: the driver Pick up the rider
        >>>
        """       
        return '{} -- {} -- {}: the driver Pick up the rider'.format(self.timestamp, 
                                                                     self.driver.id, 
                                                                     self.rider.id)           


class Dropoff(Event):
    """A driver drops off the assigned rider.
           
    === Attributes ===   
    @type driver: Driver
        The driver.
    @type rider: Rider
        The rider
       """      
    def __init__(self, timestamp, driver, rider):
        """Initialize a Dropoff event.
              
        A dropoff event is initialized when the pickup event is successfully 
        finished. 
                      
        @param self: Dropoff        
        @param rider: Rider
        @param driver Driver
        @rtype: None

        >>> dispatcher = Dispatcher()
        >>> monitor = Monitor()
        >>> rider_Bathe = Rider('Bathe',WAITING, 5, Location(1,2), Location(5,8))
        >>> driver_Atom = Driver('Atom', Location(0,0), 1)
        >>> rider_rq = RiderRequest(0, rider_Bathe)
        >>> cancellation = rider_rq.do(dispatcher,monitor)[0]
        >>> driver_rq = DriverRequest(1, driver_Atom)
        >>> pickup = driver_rq.do(dispatcher, monitor)[0]
        >>> dropoff = pickup.do(dispatcher, monitor)[0]
        >>> print(dropoff.timestamp)
        14
        >>>
        """       
        super().__init__(timestamp)
        self.driver = driver
        self.rider = rider

    def do(self, dispatcher, monitor):
        """ Execute the scheduled dropoff event.
                        
        A dropoff event is scheduled when the pickup event is successfully finished.            
        So the event is executed when the driver arrives the assigned rider's destination. 
               
        The monitor is notified of the dropoff event.
        
        When the dropoff is finished, a new request for a rider is send out immediately.
        
        @param self: Dropoff
        @param dispatcher: Dispatcher
        @param monitor: Monitor
        @rtype: list[event] 
                        
        >>> dispatcher = Dispatcher()
        >>> monitor = Monitor()
        >>> rider_Bathe = Rider('Bathe',WAITING, 5, Location(1,2), Location(5,8))
        >>> driver_Atom = Driver('Atom', Location(0,0), 1)
        >>> rider_rq = RiderRequest(0, rider_Bathe)
        >>> cancellation = rider_rq.do(dispatcher,monitor)[0]
        >>> driver_rq = DriverRequest(1, driver_Atom)
        >>> pickup = driver_rq.do(dispatcher, monitor)[0]
        >>> dropoff = pickup.do(dispatcher, monitor)[0]
        >>> driver_rq1 = dropoff.do(dispatcher, monitor)[0]
        >>> print(driver_rq1.timestamp)
        14
        >>>
        """     
        events = []
        self.driver.end_ride()
        monitor.notify(self.timestamp, DRIVER, DROPOFF, self.driver.id, 
                       self.driver.location)
        monitor.notify(self.timestamp, RIDER, DROPOFF, self.rider.id, 
                       self.rider.destination)
        
        events.append(DriverRequest(self.timestamp, self.driver))
        monitor.notify(self.timestamp, DRIVER, REQUEST, self.driver.id, 
                       self.driver.location)        
        return events 
    
    def __str__(self):
        """Return a string representation of this event.
               
        @type self: Dropoff
        @rtype: str
               
        >>> dispatcher = Dispatcher()
        >>> monitor = Monitor()
        >>> rider_Bathe = Rider('Bathe',WAITING, 5, Location(1,2), Location(5,8))
        >>> driver_Atom = Driver('Atom', Location(0,0), 1)
        >>> rider_rq = RiderRequest(0, rider_Bathe)
        >>> cancellation = rider_rq.do(dispatcher,monitor)[0]
        >>> driver_rq = DriverRequest(1, driver_Atom)
        >>> pickup = driver_rq.do(dispatcher, monitor)[0]
        >>> dropoff = pickup.do(dispatcher, monitor)[0]
        >>> print(dropoff)
        14 -- Atom -- Bathe: the driver Drop off the rider
        >>>
        """                
        return '{} -- {} -- {}: the driver Drop off the rider'.\
            format(self.timestamp, self.driver.id, self.rider.id)
        

def create_event_list(filename):
    """Return a list of Events based on raw list of events in <filename>.

    Precondition: the file stored at <filename> is in the format specified
    by the assignment handout.

    @param filename: str
        The name of a file that contains the list of events.
    @rtype: list[Event]
    """
    events = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()            

            if not line or line.startswith("#"):
                # Skip lines that are blank or start with #.
                continue

            # Create a list of words in the line, e.g.
            # ['10', 'RiderRequest', 'Cerise', '4,2', '1,5', '15'].
            # Note that these are strings, and you'll need to convert some
            # of them to a different type.
            tokens = line.split()            
            timestamp = int(tokens[0])
            event_type = tokens[1]            

            # HINT: Use Location.deserialize to convert the location string to
            # a location.

            if event_type == "DriverRequest":               
                # Create a DriverRequest event.
                _id = tokens[2]
                location = deserialize_location(tokens[3])
                speed = int(tokens[4])
                driver = Driver(_id, location, speed)
                event = DriverRequest(timestamp, driver)
                
            elif event_type == "RiderRequest":               
                # Create a RiderRequest event.
                _id = tokens[2]
                origin = deserialize_location(tokens[3])
                destination = deserialize_location(tokens[4])
                patience = int(tokens[5])
                status = 'waiting'
                rider = Rider(_id, status, patience, origin, destination)
                event = RiderRequest(timestamp, rider)

            events.append(event)
    return events

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    dispatcher = Dispatcher()
    monitor = Monitor()
    rider_Bathe = Rider('Bathe', WAITING, 5, Location(1, 2), Location(5, 8))
    driver_Atom = Driver('Atom', Location(0, 0), 1)    
    rider_rq = RiderRequest(0, rider_Bathe)
    print(rider_rq)
    cancellation = rider_rq.do(dispatcher, monitor)[0]    
    driver_rq = DriverRequest(1, driver_Atom)
    print(driver_rq)
    pickup = driver_rq.do(dispatcher, monitor)[0]
    print(pickup)
    print(cancellation)
    dropoff = pickup.do(dispatcher, monitor)[0]
    print(dropoff)
    driver_rq1 = dropoff.do(dispatcher, monitor)[0]
    print(driver_rq1)
