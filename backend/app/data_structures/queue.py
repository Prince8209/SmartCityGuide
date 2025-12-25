"""
Queue Data Structure Implementation
FIFO (First In, First Out) - useful for request processing, task scheduling
"""


class Queue:
    """
    Queue implementation using Python list
    Operations: enqueue (O(1)), dequeue (O(n)), peek (O(1))
    """
    
    def __init__(self):
        """Initialize an empty queue"""
        self._items = []
    
    def enqueue(self, item):
        """
        Add an item to the rear of the queue
        Time Complexity: O(1)
        
        Args:
            item: The item to add to the queue
        """
        self._items.append(item)
    
    def dequeue(self):
        """
        Remove and return the front item from the queue
        Time Complexity: O(n) due to list shifting
        
        Returns:
            The front item from the queue
            
        Raises:
            IndexError: If the queue is empty
        """
        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty queue")
        return self._items.pop(0)
    
    def peek(self):
        """
        Return the front item without removing it
        Time Complexity: O(1)
        
        Returns:
            The front item from the queue
            
        Raises:
            IndexError: If the queue is empty
        """
        if self.is_empty():
            raise IndexError("Cannot peek at an empty queue")
        return self._items[0]
    
    def is_empty(self):
        """
        Check if the queue is empty
        Time Complexity: O(1)
        
        Returns:
            bool: True if queue is empty, False otherwise
        """
        return len(self._items) == 0
    
    def size(self):
        """
        Get the number of items in the queue
        Time Complexity: O(1)
        
        Returns:
            int: Number of items in the queue
        """
        return len(self._items)
    
    def clear(self):
        """
        Remove all items from the queue
        Time Complexity: O(1)
        """
        self._items = []
    
    def __len__(self):
        """Return the size of the queue"""
        return self.size()
    
    def __str__(self):
        """String representation of the queue"""
        return f"Queue({self._items})"
    
    def __repr__(self):
        """Official string representation"""
        return self.__str__()


# Example usage and practical application
if __name__ == "__main__":
    # Example: Task scheduling system
    print("=" * 60)
    print("QUEUE DATA STRUCTURE - Task Scheduling Example")
    print("=" * 60)
    
    task_queue = Queue()
    
    # Add tasks to the queue
    print("\n📝 Adding tasks to queue:")
    tasks = [
        "Process user registration",
        "Send welcome email",
        "Update database",
        "Generate report"
    ]
    
    for task in tasks:
        task_queue.enqueue(task)
        print(f"  ✓ Enqueued: {task}")
    
    print(f"\n📊 Queue size: {task_queue.size()}")
    print(f"👀 Front task (peek): {task_queue.peek()}")
    
    # Process tasks
    print("\n⚙️ Processing tasks:")
    while not task_queue.is_empty():
        task = task_queue.dequeue()
        print(f"  ✓ Processing: {task}")
    
    print(f"\n📊 Queue size after processing: {task_queue.size()}")
    print(f"❓ Is queue empty? {task_queue.is_empty()}")
