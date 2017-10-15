class Location:
    """A class for a location point that contains number of row and column.

    === Attributes ===
    @type row: int
        A row number for the same location point.
    @type column:
        The column number for the same location point .
    """

    def __init__(self, row, column):
        """Initialize a location.

        @param self: Location
        @param row: int
        @param column: int
        @rtype: None

        >>> location = Location(3, 2)
        >>>
        """
        self.row = int(row)
        self.column = int(column)

    def __str__(self):
        """Return a string representation.
        
        @param self:location
        @rtype: str

        >>> location = Location(3,2)
        >>> print(location)
        (3,2)
        """
        return "({},{})".format(self.row, self.column)

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.
        
        @param self:Location
        @param other:Location
        @rtype: bool

        >>> location1 = Location(3,2)
        >>> location2 = Location(1,5)
        >>> location1 == location1
        True
        >>> location1 == location2
        False
        """
        return type(self) == type(other) and (self.row, self.column) == (other.row, other.column)


def manhattan_distance(origin, destination):
    """Return the Manhattan distance between the origin and the destination.

    @param origin: Location
    @param destination: Location
    @rtype: int
    
    >>> distance = manhattan_distance(Location(0,0), Location(5,6))
    >>> print(distance)
    11
    """
    return int(abs(destination.row - origin.row) + abs(destination.column - origin.column))


def deserialize_location(location_str):
    """Deserialize a location.

    @param location_str: str
        A location in the format 'row,col'
    @rtype: Location
        object of Location
        
    >>> location_str = "5,6"
    >>> location = deserialize_location(location_str)
    >>> print(location)
    (5,6)
    """
    location = location_str.split(sep=',')
    return Location(int(location[0]), int(location[1]))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    origin = Location(0, 0)
    destination = Location(5, 6)
    distance = manhattan_distance(origin, destination)
    print(distance)
    location1 = deserialize_location("5,6")
    print(location1)
