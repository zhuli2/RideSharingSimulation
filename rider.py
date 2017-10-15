from location import *

"""
The rider module contains the Rider class. It also contains
constants that represent the status of the rider.

=== Constants ===
@type WAITING: str
    A constant used for the waiting rider status.
@type CANCELLED: str
    A constant used for the cancelled rider status.
@type SATISFIED: str
    A constant used for the satisfied rider status
"""

WAITING = "waiting"
CANCELLED = "cancelled"
SATISFIED = "satisfied"


class Rider:
    """ A rider for a ride-sharing service.

    === Attributes ===
    @type id: str
        A unique identifier for the rider.
    @type status: str
        The status is one of WAITING, CANCELLED and SATISFIED
    @type patience: int
        The minutes that the rider will be waiting before his request is cancelled.
    @type origin: Location
        The rider's location where he send out request for a driver.
    @type destination: Location
        The rider's destination where he wants the driver driver to.
    """

    def __init__(self, identifier, status, patience, origin, destination):
        """ Initialize an object of Rider.

        @param self:Rider
        @param identifier: str
        @param status: str
        @param patience: int
        @param origin: Location
        @param destination: Location
        @return: None

        >>> rider_Bathe = Rider('Bathe',"waiting", 5, Location(1,2), Location(5,8))
        >>>
        """
        self.id = identifier
        self.status = status
        self.patience = patience
        self.origin = origin
        self.destination = destination

    def __str__(self):
        """ Return a string representation.

        @param self: Rider
        @return: str

        >>> rider_Bathe = Rider('Bathe',WAITING, 5, Location(1,2), Location(5,8))
        >>> print(rider_Bathe)
        Rider_ID: Bathe, status: waiting, patience: 5, origin: (1,2), destination: (5,8)
        """
        return 'Rider_ID: {}, status: {}, patience: {}, origin: {}, ' \
               'destination: {}'.format(self.id, self.status, self.patience, 
                                        self.origin, self.destination)
    
    def __eq__(self, other):
        """ Check if two objects are equal.

        @param self: Rider
        @param other: Rider
        @return: bool

        >>> rider_Bathe = Rider('Bathe',WAITING, 5, Location(1,2), Location(5,8))
        >>> rider_Cast = Rider('Cast',WAITING, 3, Location(5,2), Location(3,8))
        >>> rider_Bathe == rider_Bathe
        True
        >>> rider_Bathe == rider_Cast
        False
        """
        return type(self) == type(other) and self.id == other.id


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    rider1 = Rider('Rider1', WAITING, 3, Location(2, 2), Location(5, 5))
    print(rider1)   
    rider2 = Rider('Rider2', WAITING, 3, Location(2, 2), Location(5, 5))
    print(rider2)
    print(rider1 == rider2)
