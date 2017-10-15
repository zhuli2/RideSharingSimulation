from container import *
from dispatcher import Dispatcher
from event import Event, create_event_list
from monitor import *


class Simulation:
    """A simulation.

    This is the class which is responsible for setting up and running a
    simulation.

    The API is given to you: your main task is to implement the two methods
    according to their docstrings.

    Of course, you may add whatever private attributes and methods you want.
    But because you should not change the interface, you may not add any public
    attributes or methods.

    This is the entry point into your program, and in particular is used for
    auto-testing purposes. This makes it ESSENTIAL that you do not change the
    interface in any way!
    """

    # === Private Attributes ===
    # @type _events: PriorityQueue[Event]
    #     A sequence of events arranged in priority determined by the event
    #     sorting order.
    # @type _dispatcher: Dispatcher
    #     The dispatcher associated with the simulation.

    def __init__(self):
        """Initialize a Simulation.

        @param self: Simulation
        @rtype: None
        
        >>> sim = Simulation()
        """
        self._events = PriorityQueue()
        self._dispatcher = Dispatcher()
        self._monitor = Monitor()

    def run(self, initial_events):
        """Run the simulation on the list of events in <initial_events>.

        Return a dictionary containing statistics of the simulation,
        according to the specifications in the assignment handout.

        @param self: Simulation
        @param initial_events: list[Event]
            An initial list of events.
        @rtype: dict[str, object]

        >>> sim = Simulation()
        >>> filename1 = 'events_small.txt'
        >>> events = create_event_list(filename1)
        >>> report = sim.run(events)
        >>> print(report)
        {'driver_total_distance': 14.0, 'rider_wait_time': 11.0, 'driver_ride_distance': 10.0} 
        """
        # Add all initial events to the event queue.
        # Until there are no more events, remove an event
        # from the event queue and do it. Add any returned
        # events to the event queue.        
        
        for event in initial_events:           
            self._events.add(event)        
        while not self._events.is_empty():
            new_events = self._events.remove()
            next_events = new_events.do(self._dispatcher, self._monitor)
            if len(next_events) >= 1:
                for event in next_events:                   
                        self._events.add(event)
        return self._monitor.report()

    def __str__(self):
        """ Return a string representation.
        
        @param self: Simulation
        @rtype: str

        >>> sim = Simulation()
        >>> filename1 = 'events_small.txt'
        >>> events = create_event_list(filename)
        >>> report = sim.run(events)
        >>> print(sim)
        ----------------------------------------
        Riders:
		1---Dan---request---(1,1)
		12---Dan---pickup---(1,1)
		17---Dan---dropoff---(6,6)
        ----------------------------------------
        Drivers:
		10---Arnold---request---(3,3)
		12---Arnold---pickup---(1,1)
		17---Arnold---dropoff---(6,6)
		17---Arnold---request---(6,6)
		17---Arnold---request---(6,6)
        ----------------------------------------
        """
        rider_str = 'Riders:\n'
        riders = sim._monitor._activities[RIDER]
        for events in riders.values():
            for event in events:
                rider_str += '\t{}\n'.format(event)
                
        driver_str = 'Drivers:\n'
        drivers = sim._monitor._activities[DRIVER]
        for events in drivers.values():
            for event in events:
                driver_str += '\t{}\n'.format(event)
                
        return (20*'--') + '\n' + rider_str + \
               (20*"--") + '\n' + driver_str + \
               (20*"--")


if __name__ == "__main__":
    filename = 'events.txt'
    events = create_event_list(filename)
    filename1 = 'events_small.txt'    
    #events = create_event_list(filename1)
    sim = Simulation()    
    final_stats = sim.run(events)
    print(final_stats)    
    print(sim)
