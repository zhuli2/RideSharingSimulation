class Container:
    """A container that holds objects.

    This is an abstract super class.  Only child classes should be instantiated.
    """
    def __init__(self):
        """ Initialize an empty Container.

        @param self: Container
        @return: None
        """
        raise NotImplementedError("Implemented in a subclass")

    def add(self, item):
        """Add <item> to this Container.

        @param self: Container
        @param item: Object
        @rtype: None
        """
        raise NotImplementedError("Implemented in a subclass")

    def remove(self):
        """Remove and return a single item from this Container.

        @param self: Container
        @rtype: Object
        """
        raise NotImplementedError("Implemented in a subclass")

    def is_empty(self):
        """Return True iff this Container is empty.

        @param self: Container
        @rtype: bool
        """
        raise NotImplementedError("Implemented in a subclass")


class PriorityQueue(Container):
    """A queue of items that operates in priority order.

    Items are removed from the queue according to priority; the item with the
    highest priority is removed first. Ties are resolved in FIFO order,
    meaning the item which was inserted *earlier* is the first one to be
    removed.

    Priority is defined by the rich comparison methods for the objects in the
    container (__lt__, __le__, __gt__, __ge__).

    If x < y, then x has a *HIGHER* priority than y.

    All objects in the container must be of the same type.
    """

    # === Private Attributes ===
    # @type _items: list
    #     The items stored in the priority queue.
    #
    # === Representation Invariants ===
    # _items is a sorted list, where the first item in the queue is the
    # item with the highest priority.

    def __init__(self):
        """Initialize an empty PriorityQueue.

        @type self: PriorityQueue
        @rtype: None

        >>> pq = PriorityQueue()
        >>>
        """       
        self.items = []

    def remove(self):
        """Return the item removed from this PriorityQueue.

        Precondition: <self> should not be empty.

        @type self: PriorityQueue
        @rtype: object

        >>> pq = PriorityQueue()
        >>> pq.add("red")
        >>> pq.add("blue")
        >>> pq.add("yellow")
        >>> pq.add("green")
        >>> pq.remove()
        'blue'
        >>> pq.remove()
        'green'
        >>> pq.remove()
        'red'
        >>> pq.remove()
        'yellow'
        """
        try:
            return self.items.pop(0)
        except IndexError:
            return None

    def is_empty(self):
        """
        Return true iff this PriorityQueue is empty.

        @param self: PriorityQueue
        @rtype: bool

        >>> pq = PriorityQueue()
        >>> pq.is_empty()
        True
        >>> pq.add("thing")
        >>> pq.is_empty()
        False
        """
        return len(self.items) == 0

    def add(self, item):
        """Add <item> to this PriorityQueue.

        The new item has the Highest priority if it is LOWER than
        every item in self.items. Otherwise, it has the Lowest
        priority.

        @param self: PriorityQueue
        @param item: object
        @rtype: None

        >>> pq = PriorityQueue()
        >>> pq.add("yellow")
        >>> pq.add("blue")
        >>> pq.add("red")
        >>> pq.add("green")
        >>> pq.items
        ['blue', 'green', 'red', 'yellow']
        """
        if self.is_empty():
            self.items.append(item)
        else:
            low_priority = []
            high_priority = []
            while not self.is_empty():
                current_item = self.remove()
                if current_item > item:
                    low_priority.append(current_item)
                else:
                    high_priority.append(current_item)
            self.items = high_priority + [item] + low_priority
                
    def __str__(self):
        """ Return a string representation.

        @param self: PriorityQueue
        @return: str

        >>> pq = PriorityQueue()
        >>> pq.add("yellow")
        >>> pq.add("blue")
        >>> pq.add("red")
        >>> pq.add("green")
        >>> print(pq)
        ['blue', 'green', 'red', 'yellow']
        """
        return '{}'.format(self.items)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    pq = PriorityQueue()
    pq.add(7)
    pq.add(6)
    pq.add(8)
    pq.add(2)
    print(pq)
    while not pq.is_empty():
        print(pq.remove())
    print(pq.is_empty())
