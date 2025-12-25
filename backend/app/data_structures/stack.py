"""
Stack Data Structure Implementation
LIFO (Last In, First Out) - useful for undo operations, navigation history, expression evaluation
"""


class Stack:
    """
    Stack implementation using Python list
    Operations: push (O(1)), pop (O(1)), peek (O(1))
    """
    
    def __init__(self):
        """Initialize an empty stack"""
        self._items = []
    
    def push(self, item):
        """
        Add an item to the top of the stack
        Time Complexity: O(1)
        
        Args:
            item: The item to add to the stack
        """
        self._items.append(item)
    
    def pop(self):
        """
        Remove and return the top item from the stack
        Time Complexity: O(1)
        
        Returns:
            The top item from the stack
            
        Raises:
            IndexError: If the stack is empty
        """
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack")
        return self._items.pop()
    
    def peek(self):
        """
        Return the top item without removing it
        Time Complexity: O(1)
        
        Returns:
            The top item from the stack
            
        Raises:
            IndexError: If the stack is empty
        """
        if self.is_empty():
            raise IndexError("Cannot peek at an empty stack")
        return self._items[-1]
    
    def is_empty(self):
        """
        Check if the stack is empty
        Time Complexity: O(1)
        
        Returns:
            bool: True if stack is empty, False otherwise
        """
        return len(self._items) == 0
    
    def size(self):
        """
        Get the number of items in the stack
        Time Complexity: O(1)
        
        Returns:
            int: Number of items in the stack
        """
        return len(self._items)
    
    def clear(self):
        """
        Remove all items from the stack
        Time Complexity: O(1)
        """
        self._items = []
    
    def __len__(self):
        """Return the size of the stack"""
        return self.size()
    
    def __str__(self):
        """String representation of the stack"""
        return f"Stack({self._items})"
    
    def __repr__(self):
        """Official string representation"""
        return self.__str__()


# Example usage and practical application
if __name__ == "__main__":
    # Example 1: Navigation history (like browser back button)
    print("=" * 60)
    print("STACK DATA STRUCTURE - Navigation History Example")
    print("=" * 60)
    
    navigation_stack = Stack()
    
    # User navigates through pages
    print("\n🌐 User navigation:")
    pages = [
        "Home Page",
        "Cities Page",
        "Mumbai Details",
        "Book Trip"
    ]
    
    for page in pages:
        navigation_stack.push(page)
        print(f"  ✓ Visited: {page}")
    
    print(f"\n📊 Navigation history size: {navigation_stack.size()}")
    print(f"👀 Current page (peek): {navigation_stack.peek()}")
    
    # User clicks back button
    print("\n⬅️ Going back:")
    for _ in range(2):
        if not navigation_stack.is_empty():
            page = navigation_stack.pop()
            print(f"  ✓ Left: {page}")
            if not navigation_stack.is_empty():
                print(f"  → Now on: {navigation_stack.peek()}")
    
    # Example 2: Undo operation
    print("\n" + "=" * 60)
    print("STACK DATA STRUCTURE - Undo Operation Example")
    print("=" * 60)
    
    undo_stack = Stack()
    
    print("\n✏️ User actions:")
    actions = [
        "Added city to favorites",
        "Updated profile",
        "Booked hotel",
        "Deleted review"
    ]
    
    for action in actions:
        undo_stack.push(action)
        print(f"  ✓ Action: {action}")
    
    print(f"\n↩️ Undo last 2 actions:")
    for _ in range(2):
        if not undo_stack.is_empty():
            action = undo_stack.pop()
            print(f"  ✓ Undoing: {action}")
    
    print(f"\n📊 Remaining actions: {undo_stack.size()}")
