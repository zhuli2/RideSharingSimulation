from location import Location, manhattan_distance
from rider import *


class Driver:
    """A driver for a ride-sharing service.

    === Attributes ===
    @type id: str
        A unique identifier for the driver.
    @type location: Location
        The current location of the driver.
    @type speed: int
        The constant speed provided by the driver
    """
    
    # === Private Attribute ===
    # @type destination: Location
    #   The possible location where the driver is driving to.
    #   If it is None, the driver is idle. Otherwise, the driver is driving.

    def __init__(self, identifier, location, speed):
        """Initialize a Driver.

        @param self: Driver
        @param identifier: str
        @param location: Location
        @param speed: int
        @rtype: None

        >>> driver_Atom = Driver('Atom', Location(0,0), 1)
        >>>
        """
        self.id = identifier
        self.location = location
        self.speed = speed
        
        self.destination = None

    def __str__(self):
        """Return a string representation.

        @param self: Driver
        @rtype: str

        >>> driver_Atom = Driver('Atom', Location(0,0), 1)
        >>> print(driver_Atom)
        Driver_ID: Atom, current location: (0,0), speed: 1
        >>>
        """
        return "Driver_ID: {}, current location: {}, " \
               "speed: {}".format(self.id, self.location, self.speed)

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.

        @param self: Driver
        @rtype: bool

        >>> driver_Atom = Driver('Atom', Location(0,0), 1)
        >>> driver_Bathe = Driver('Bathe', Location(5,5), 1)
        >>> driver_Atom == driver_Atom
        True
        >>> driver_Atom == driver_Bathe
        False
        """
        return type(self) == type(other) and self.id == other.id

    def get_travel_time(self, destination):
        """Return the time it will take to arrive at the destination,
        rounded to the nearest integer.

        @param self: Driver
        @param destination: Location
        @rtype: int

        >>> driver_Atom = Driver('Atom', Location(0,0), 1)
        >>> driver_Atom.get_travel_time(Location(5,8))
        13
        >>>
        """
        return round(manhattan_distance(self.location, destination) / self.speed)

    def start_drive(self, location):
        """Start driving to the location and return the time the drive will take.

        The driver is given a location as the temporary destination
        when starting drive.

        @param self: Driver
        @param location: Location
        @rtype: int

        >>> driver_Atom = Driver('Atom', Location(0,0), 1)
        >>> driver_Atom.start_drive(Location(5,8))
        13
        >>>
        """
        self.destination = location
        return self.get_travel_time(location)  

    def end_drive(self):
        """End the drive and arrive at the rider's origin.

        Precondition: self.destination is not None when self starts drive.

        When the driver arrives the rider's origin, his location becomes the rider's
        origin regardless if he picks up the rider or not.

        @param self: Driver
        @rtype: None

        >>> driver_Atom = Driver('Atom', Location(0,0), 1)
        >>> driver_Atom.start_drive(Location(5,8))
        13
        >>> driver_Atom.end_drive()
        >>> print(driver_Atom.location)
        (5,8)
        >>>
        """
        self.location = self.destination
        self.destination = None    

    def start_ride(self, rider):
        """Start a ride and return the time the ride will take.

        @param self: Driver
        @param rider: Rider
        @rtype: int

        >>> driver_Atom = Driver('Atom', Location(1, 2), 1)
        >>> rider_Bathe = Rider('Bathe','waiting', 5, Location(1, 2), Location(5, 8))
        >>> driver_Atom.start_ride(rider_Bathe)
        10
        >>>
        """
        self.destination = rider.destination
        return self.get_travel_time(rider.destination)

    def end_ride(self):
        """End the current ride, and arrive at the rider's destination.

        Precondition: The driver has a rider.
        Precondition: self.destination is not None when the driver starts ride.

        When the driver drops off the rider, self.location becomes the rider's
        destination and hence temporary self.destination is None.

        @param self: Driver
        @rtype: None

        >>> driver_Atom = Driver('Atom', Location(1,2), 1)
        >>> rider_Bathe = Rider('Bathe','waiting', 5, Location(1,2), Location(5,8))
        >>> driver_Atom.start_ride(rider_Bathe)
        10
        >>> driver_Atom.end_ride()
        >>> print(driver_Atom.location)
        (5,8)
        >>>
        """
        self.location = self.destination
        self.destination = None
    
    def is_idle(self):
        """ Check if a driver is idle: True if the driver has a destination or False.

        @param self: Driver
        @return: bool
        
        >>> driver_Atom = Driver('Atom', Location(0,0), 1)
        >>> driver_Atom.start_drive(Location(5,8))
        13
        >>> driver_Atom.is_idle()
        False
        >>> driver_Atom.end_drive()
        >>> driver_Atom.is_idle()
        True
        >>>
        """              
        if self.destination is None:
            return True
        else:       
            return False    
        
if __name__ == '__main__':
    import doctest
    doctest.testmod()
    driver1 = Driver('Driver1', Location(1, 1), 1)
    print(driver1)
    print(driver1.is_idle())
    rider1 = Rider('Rider1', WAITING, 3, Location(2, 2), Location(5, 5))
    print(driver1.start_drive(rider1.origin))
    print(driver1.is_idle())
    driver1.end_drive()
    print(driver1.is_idle())
    print(driver1.location)
    print(driver1.start_ride(rider1))
    print(driver1.is_idle())
    driver1.end_ride()
    print(driver1.is_idle()) 
    print(driver1.location)
    print(driver1 == rider1)
