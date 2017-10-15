from driver import Driver
from rider import Rider
from location import *


class Dispatcher:
    """A dispatcher fulfills requests from riders and drivers for a
    ride-sharing service.

    When a rider requests a driver, the dispatcher assigns a driver to the
    rider. If no driver is available, the rider is placed on a waiting
    list for the next available driver. A rider that has not yet been
    picked up by a driver may cancel their request.

    When a driver requests a rider, the dispatcher assigns a rider from
    the waiting list to the driver. If there is no rider on the waiting list
    the dispatcher does nothing. Once a driver requests a rider, the driver
    is registered with the dispatcher, and will be used to fulfill future
    rider requests.
    """
    # === Private Attribute ===
    # @type drivers: list
    #   The list of all drivers who are registered.
    #   When a driver requests a rider
    #   for the 1st time, he is registered even no rider is assigned to. 
    # @type waiting_riders: list
    #   The list of all riders who are waiting for an assigned driver within their patience.
    #   When a rider requests a driver, he will be placed to the waiting list
    #   if no driver is available then.
    
    def __init__(self):
        """Initialize a Dispatcher.

        @param self: Dispatcher
        @rtype: None

        >>> dispatcher = Dispatcher()
        >>>
        """
        self.drivers = []
        self.waiting_riders = []

    def __str__(self):
        """Return a string representation.

        @param self: Dispatcher
        @rtype: str

        >>> dispatcher = Dispatcher()
        >>> print(dispatcher)
        Drivers in idle:
        Drivers in driving:
        Riders in waiting:
        <BLANKLINE>
        """
        drivers_idle = 'Drivers in idle:\n'
        drivers_driving = 'Drivers in driving:\n'
        riders_waiting = 'Riders in waiting:\n'
        
        for driver in self.drivers:
            if driver.is_idle():
                drivers_idle += '\t{},{}\n'.format(driver.id, driver.location)                                                      
            else:
                drivers_driving += '\t{},{}\n'.format(driver.id, driver.location)
        
        for rider in self.waiting_riders:
            riders_waiting += '\t{}, {}, {}\n'.format(rider.id, rider.origin, 
                                                      rider.destination)
        
        return drivers_idle + drivers_driving + riders_waiting

    def request_driver(self, rider):
        """Return a driver for the rider, or None if no driver is available.
        
        If there are multiple drivers available, the dispatcher returns the 
        quickest driver based on the driving time.        

        Add the rider to the waiting list if no driver is available.

        @param self: Dispatcher
        @param rider: Rider
        @rtype: Driver | None

        >>> rider_Bathe = Rider('Bathe', 'waiting', 5, Location(1,2), Location(5,8))
        >>> dispatcher = Dispatcher()
        >>> print(dispatcher.request_driver(rider_Bathe))
        None
        >>> print(len(dispatcher.waiting_riders))
        1
        """
        available_drivers = []
        rider.status = "waiting"
        for driver in self.drivers:
            if driver.is_idle():
                time = driver.get_travel_time(rider.origin)               
                available_drivers.append((time, driver))
                
        if len(available_drivers) == 0:
            self.waiting_riders.append(rider)
            return None
        else:
            available_drivers.sort(key=lambda x: x[0])
            fastest_driver = available_drivers.pop(0)
            available_drivers.clear()
            return fastest_driver[1]
            
    def request_rider(self, driver):
        """Return a rider for the driver, or None if no rider is available.

        If this is a new driver, register the driver for future rider requests.

        @param self: Dispatcher
        @param driver: Driver
        @rtype: Rider | None
        
        >>> dispatcher = Dispatcher()        
        >>> rider_Bathe = Rider('Bathe','waiting', 5, Location(1,2), Location(5,8))
        >>> print(dispatcher.request_driver(rider_Bathe))
        None
        >>> driver_Atom = Driver('Atom', Location(10,9), 1)
        >>> print(dispatcher.request_rider(driver_Atom))
        Rider_ID: Bathe, status: waiting, patience: 5, origin: (1,2), destination: (5,8)
        """
        if driver not in self.drivers:
            self.drivers.append(driver)        
        if len(self.waiting_riders) > 0:
            return self.waiting_riders.pop(0)
        else:
            return None

    def cancel_ride(self, rider):
        """Cancel the ride request for the rider if he is on the 
            waiting list and the patience runs out.

        @param self: Dispatcher
        @param rider: Rider
        @rtype: None
                
        >>> rider_Bathe = Rider('Bathe','waiting', 5, Location(1,2), Location(5,8))
        >>> dispatcher = Dispatcher()
        >>> print(dispatcher.request_driver(rider_Bathe))
        None
        >>> print(dispatcher.cancel_ride(rider_Bathe))
        None

        """
        try:
            self.waiting_riders.remove(rider)
        except IndexError:
            print('No waiting riders!!!')
        except ValueError:
            print('The rider is not waiting!!!')
            
            
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    dispatcher = Dispatcher()    
    rider1 = Rider('rider1', 'waiting', 5, Location(1, 2), Location(5, 8))
    driver1 = Driver('driver1', Location(10, 9), 1)
    print(dispatcher.request_driver(rider1))
    print(dispatcher.request_rider(driver1))
    dispatcher.cancel_ride(rider1)
    print(dispatcher)
