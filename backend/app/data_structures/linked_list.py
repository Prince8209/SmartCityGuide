"""
Linked List Data Structure Implementation
Dynamic data structure - useful for dynamic memory allocation, efficient insertions/deletions
"""


class Node:
    """
    Node class for Linked List
    Each node contains data and a reference to the next node
    """
    
    def __init__(self, data):
        """
        Initialize a node with data
        
        Args:
            data: The data to store in the node
        """
        self.data = data
        self.next = None
    
    def __str__(self):
        """String representation of the node"""
        return str(self.data)


class LinkedList:
    """
    Singly Linked List implementation
    Operations: insert (O(1) at head, O(n) at position), delete (O(n)), search (O(n))
    """
    
    def __init__(self):
        """Initialize an empty linked list"""
        self.head = None
        self._size = 0
    
    def insert_at_beginning(self, data):
        """
        Insert a new node at the beginning of the list
        Time Complexity: O(1)
        
        Args:
            data: The data to insert
        """
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1
    
    def insert_at_end(self, data):
        """
        Insert a new node at the end of the list
        Time Complexity: O(n)
        
        Args:
            data: The data to insert
        """
        new_node = Node(data)
        
        if self.head is None:
            self.head = new_node
            self._size += 1
            return
        
        current = self.head
        while current.next:
            current = current.next
        
        current.next = new_node
        self._size += 1
    
    def insert_at_position(self, data, position):
        """
        Insert a new node at a specific position
        Time Complexity: O(n)
        
        Args:
            data: The data to insert
            position: The position to insert at (0-indexed)
            
        Raises:
            IndexError: If position is invalid
        """
        if position < 0 or position > self._size:
            raise IndexError(f"Invalid position: {position}")
        
        if position == 0:
            self.insert_at_beginning(data)
            return
        
        new_node = Node(data)
        current = self.head
        
        for _ in range(position - 1):
            current = current.next
        
        new_node.next = current.next
        current.next = new_node
        self._size += 1
    
    def delete_at_beginning(self):
        """
        Delete the first node
        Time Complexity: O(1)
        
        Returns:
            The data from the deleted node
            
        Raises:
            IndexError: If the list is empty
        """
        if self.is_empty():
            raise IndexError("Cannot delete from an empty list")
        
        data = self.head.data
        self.head = self.head.next
        self._size -= 1
        return data
    
    def delete_at_end(self):
        """
        Delete the last node
        Time Complexity: O(n)
        
        Returns:
            The data from the deleted node
            
        Raises:
            IndexError: If the list is empty
        """
        if self.is_empty():
            raise IndexError("Cannot delete from an empty list")
        
        if self.head.next is None:
            data = self.head.data
            self.head = None
            self._size -= 1
            return data
        
        current = self.head
        while current.next.next:
            current = current.next
        
        data = current.next.data
        current.next = None
        self._size -= 1
        return data
    
    def delete_by_value(self, value):
        """
        Delete the first node with the specified value
        Time Complexity: O(n)
        
        Args:
            value: The value to delete
            
        Returns:
            bool: True if deleted, False if not found
        """
        if self.is_empty():
            return False
        
        # If head node contains the value
        if self.head.data == value:
            self.head = self.head.next
            self._size -= 1
            return True
        
        current = self.head
        while current.next:
            if current.next.data == value:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        
        return False
    
    def search(self, value):
        """
        Search for a value in the list
        Time Complexity: O(n)
        
        Args:
            value: The value to search for
            
        Returns:
            int: The position of the value (0-indexed), or -1 if not found
        """
        current = self.head
        position = 0
        
        while current:
            if current.data == value:
                return position
            current = current.next
            position += 1
        
        return -1
    
    def get(self, position):
        """
        Get the data at a specific position
        Time Complexity: O(n)
        
        Args:
            position: The position to get (0-indexed)
            
        Returns:
            The data at the position
            
        Raises:
            IndexError: If position is invalid
        """
        if position < 0 or position >= self._size:
            raise IndexError(f"Invalid position: {position}")
        
        current = self.head
        for _ in range(position):
            current = current.next
        
        return current.data
    
    def is_empty(self):
        """
        Check if the list is empty
        Time Complexity: O(1)
        
        Returns:
            bool: True if list is empty, False otherwise
        """
        return self.head is None
    
    def size(self):
        """
        Get the number of nodes in the list
        Time Complexity: O(1)
        
        Returns:
            int: Number of nodes in the list
        """
        return self._size
    
    def clear(self):
        """
        Remove all nodes from the list
        Time Complexity: O(1)
        """
        self.head = None
        self._size = 0
    
    def to_list(self):
        """
        Convert linked list to Python list
        Time Complexity: O(n)
        
        Returns:
            list: Python list containing all elements
        """
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
    
    def __len__(self):
        """Return the size of the list"""
        return self.size()
    
    def __str__(self):
        """String representation of the linked list"""
        if self.is_empty():
            return "LinkedList([])"
        
        elements = []
        current = self.head
        while current:
            elements.append(str(current.data))
            current = current.next
        
        return f"LinkedList([{' -> '.join(elements)}])"
    
    def __repr__(self):
        """Official string representation"""
        return self.__str__()


# Example usage and practical application
if __name__ == "__main__":
    # Example: Managing a list of visited cities
    print("=" * 60)
    print("LINKED LIST DATA STRUCTURE - Visited Cities Example")
    print("=" * 60)
    
    visited_cities = LinkedList()
    
    # Add cities to the list
    print("\n🏙️ Adding visited cities:")
    cities = ["Mumbai", "Delhi", "Bangalore", "Kolkata"]
    
    for city in cities:
        visited_cities.insert_at_end(city)
        print(f"  ✓ Added: {city}")
    
    print(f"\n📊 Total cities visited: {visited_cities.size()}")
    print(f"🗺️ Cities list: {visited_cities}")
    
    # Search for a city
    print("\n🔍 Searching for 'Bangalore':")
    position = visited_cities.search("Bangalore")
    if position != -1:
        print(f"  ✓ Found at position: {position}")
    else:
        print(f"  ✗ Not found")
    
    # Insert a city at specific position
    print("\n➕ Inserting 'Chennai' at position 2:")
    visited_cities.insert_at_position("Chennai", 2)
    print(f"  ✓ Updated list: {visited_cities}")
    
    # Delete a city
    print("\n🗑️ Removing 'Delhi':")
    if visited_cities.delete_by_value("Delhi"):
        print(f"  ✓ Deleted successfully")
        print(f"  📋 Updated list: {visited_cities}")
    
    # Get city at position
    print("\n📍 Getting city at position 1:")
    city = visited_cities.get(1)
    print(f"  ✓ City: {city}")
    
    # Convert to Python list
    print(f"\n📝 As Python list: {visited_cities.to_list()}")
