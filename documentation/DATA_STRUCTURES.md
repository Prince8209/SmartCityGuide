# Data Structures Implementation Guide

## Overview
This document provides comprehensive information about the 5 fundamental data structures implemented in the Smart City Guide backend.

---

## Implemented Data Structures

### 1. Queue (FIFO - First In, First Out)
**File**: `backend/app/data_structures/queue.py`

#### Operations
- `enqueue(item)` - Add item to rear - **O(1)**
- `dequeue()` - Remove item from front - **O(n)**
- `peek()` - View front item - **O(1)**
- `is_empty()` - Check if empty - **O(1)**
- `size()` - Get number of items - **O(1)**
- `clear()` - Remove all items - **O(1)**

#### Use Cases
- Task scheduling
- Request processing
- Breadth-first search
- Print job management

#### Example
```python
from app.data_structures import Queue

task_queue = Queue()
task_queue.enqueue("Process payment")
task_queue.enqueue("Send email")
task = task_queue.dequeue()  # Returns "Process payment"
```

---

### 2. Stack (LIFO - Last In, First Out)
**File**: `backend/app/data_structures/stack.py`

#### Operations
- `push(item)` - Add item to top - **O(1)**
- `pop()` - Remove item from top - **O(1)**
- `peek()` - View top item - **O(1)**
- `is_empty()` - Check if empty - **O(1)**
- `size()` - Get number of items - **O(1)**
- `clear()` - Remove all items - **O(1)**

#### Use Cases
- Undo/Redo operations
- Navigation history (back button)
- Expression evaluation
- Function call stack

#### Example
```python
from app.data_structures import Stack

nav_stack = Stack()
nav_stack.push("Home")
nav_stack.push("Cities")
nav_stack.push("Mumbai")
current = nav_stack.pop()  # Returns "Mumbai"
```

---

### 3. Linked List
**File**: `backend/app/data_structures/linked_list.py`

#### Operations
- `insert_at_beginning(data)` - Insert at start - **O(1)**
- `insert_at_end(data)` - Insert at end - **O(n)**
- `insert_at_position(data, pos)` - Insert at position - **O(n)**
- `delete_at_beginning()` - Delete first node - **O(1)**
- `delete_at_end()` - Delete last node - **O(n)**
- `delete_by_value(value)` - Delete by value - **O(n)**
- `search(value)` - Find position of value - **O(n)**
- `get(position)` - Get value at position - **O(n)**
- `to_list()` - Convert to Python list - **O(n)**

#### Use Cases
- Dynamic memory allocation
- Implementing other data structures
- Recently viewed items
- Playlist management

#### Example
```python
from app.data_structures import LinkedList

cities = LinkedList()
cities.insert_at_end("Mumbai")
cities.insert_at_end("Delhi")
cities.insert_at_position("Bangalore", 1)
position = cities.search("Delhi")  # Returns 2
```

---

### 4. HashMap (Hash Table)
**File**: `backend/app/data_structures/hashmap.py`

#### Operations
- `put(key, value)` - Insert/update - **O(1) average**
- `get(key, default)` - Retrieve value - **O(1) average**
- `delete(key)` - Remove key-value - **O(1) average**
- `contains(key)` - Check if key exists - **O(1) average**
- `keys()` - Get all keys - **O(n)**
- `values()` - Get all values - **O(n)**
- `items()` - Get all key-value pairs - **O(n)**

#### Features
- Automatic resizing when load factor > 0.75
- Separate chaining for collision resolution
- Supports bracket notation (`map[key]`)

#### Use Cases
- Caching
- Fast lookups
- Indexing
- Session management

#### Example
```python
from app.data_structures import HashMap

cache = HashMap()
cache.put("mumbai", {"population": "20M", "state": "Maharashtra"})
cache.put("delhi", {"population": "30M", "state": "Delhi"})
city = cache.get("mumbai")  # Returns city data
cache["bangalore"] = {"population": "12M"}  # Bracket notation
```

---

### 5. Binary Search Tree (BST)
**File**: `backend/app/data_structures/bst.py`

#### Operations
- `insert(data)` - Insert value - **O(log n) average**
- `search(data)` - Search for value - **O(log n) average**
- `delete(data)` - Delete value - **O(log n) average**
- `find_min()` - Find minimum - **O(log n)**
- `find_max()` - Find maximum - **O(log n)**
- `inorder_traversal()` - Get sorted order - **O(n)**
- `preorder_traversal()` - Root-first traversal - **O(n)**
- `postorder_traversal()` - Root-last traversal - **O(n)**
- `height()` - Get tree height - **O(n)**

#### Properties
- Left child < Parent < Right child
- Inorder traversal gives sorted order
- Efficient for sorted data operations

#### Use Cases
- Maintaining sorted data
- Range queries
- Priority systems
- Hierarchical data

#### Example
```python
from app.data_structures import BinarySearchTree

ratings = BinarySearchTree()
ratings.insert(85)
ratings.insert(92)
ratings.insert(78)
sorted_ratings = ratings.inorder_traversal()  # [78, 85, 92]
max_rating = ratings.find_max()  # 92
```

---

## Practical Integration Examples

### City Recommendation Service
**File**: `backend/app/services/data_structures_service.py`

```python
from app.services.data_structures_service import CityRecommendationService

service = CityRecommendationService()

# Cache city data
service.cache_city("mumbai", {"name": "Mumbai", "state": "Maharashtra"})

# Get from cache
city = service.get_cached_city("mumbai")

# Add ratings
service.add_city_rating(92)
top_cities = service.get_top_rated_cities()  # Sorted ratings

# Track recent cities
service.add_recent_city("Mumbai")
recent = service.get_recent_cities()
```

### Task Scheduler
```python
from app.services.data_structures_service import TaskScheduler

scheduler = TaskScheduler()
scheduler.schedule_task("Send welcome email")
scheduler.schedule_task("Process payment")

# Execute tasks in FIFO order
task = scheduler.execute_next_task()
```

### Session Manager
```python
from app.services.data_structures_service import SessionManager

session_mgr = SessionManager()
session_mgr.create_session("sess_123", {"user_id": 1, "name": "John"})
session = session_mgr.get_session("sess_123")
```

---

## Testing

### Run All Tests
```bash
python test_data_structures.py
```

### Test Results
All 5 data structures have been tested and verified:
- ✅ Queue - All operations working correctly
- ✅ Stack - All operations working correctly
- ✅ Linked List - All operations working correctly
- ✅ HashMap - All operations working correctly
- ✅ Binary Search Tree - All operations working correctly

---

## File Structure

```
backend/app/
├── data_structures/
│   ├── __init__.py          # Package initialization
│   ├── queue.py             # Queue implementation
│   ├── stack.py             # Stack implementation
│   ├── linked_list.py       # Linked List implementation
│   ├── hashmap.py           # HashMap implementation
│   └── bst.py               # Binary Search Tree implementation
└── services/
    └── data_structures_service.py  # Practical integration examples

test_data_structures.py      # Comprehensive test suite
```

---

## Time Complexity Summary

| Data Structure | Insert | Delete | Search | Access |
|---------------|--------|--------|--------|--------|
| Queue | O(1) | O(n) | O(n) | O(1) peek |
| Stack | O(1) | O(1) | O(n) | O(1) peek |
| Linked List | O(1)* | O(n) | O(n) | O(n) |
| HashMap | O(1)† | O(1)† | O(1)† | O(1)† |
| BST | O(log n)‡ | O(log n)‡ | O(log n)‡ | - |

*O(1) at beginning, O(n) at end or position  
†Average case, O(n) worst case  
‡Average case, O(n) worst case for unbalanced tree

---

## Best Practices

### When to Use Each Data Structure

**Queue**
- When you need FIFO processing
- Task scheduling systems
- Breadth-first search algorithms

**Stack**
- When you need LIFO processing
- Undo/Redo functionality
- Depth-first search algorithms

**Linked List**
- When you need frequent insertions/deletions
- When size is unknown or changes frequently
- When you don't need random access

**HashMap**
- When you need fast lookups by key
- Caching frequently accessed data
- Counting occurrences

**Binary Search Tree**
- When you need sorted data
- When you need range queries
- When you need to find min/max efficiently

---

## Future Enhancements

### Potential Additions
1. **Priority Queue** - For weighted task scheduling
2. **Doubly Linked List** - For bidirectional traversal
3. **AVL Tree** - Self-balancing BST for guaranteed O(log n)
4. **Trie** - For autocomplete and prefix search
5. **Graph** - For route optimization between cities

### Performance Improvements
1. Implement Queue using circular buffer for O(1) dequeue
2. Add caching to frequently accessed operations
3. Implement lazy deletion for better performance
4. Add thread-safety for concurrent access

---

## References

- **Queue**: Used in `CityRecommendationService` for request processing
- **Stack**: Used in `CityRecommendationService` for navigation history
- **Linked List**: Used in `CityRecommendationService` for recent cities
- **HashMap**: Used in `SessionManager` and `CityRecommendationService` for caching
- **BST**: Used in `CityRecommendationService` for sorted ratings

---

## Support

For questions or issues with the data structures:
1. Check the inline documentation in each file
2. Run the test suite to verify functionality
3. Review the practical examples in `data_structures_service.py`
4. Refer to this documentation for usage guidelines
