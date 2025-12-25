"""
Managers
Consolidated services for data structures, caching, queuing, and tracking.
"""
from datetime import datetime
from app.data_structures.hashmap import HashMap
from app.data_structures.queue import Queue
from app.data_structures.bst import BinarySearchTree
from app.data_structures.stack import Stack
from app.data_structures.linked_list import LinkedList

# -----------------------------------------------------------------------------
# Cache Manager
# -----------------------------------------------------------------------------
class CacheManager:
    """Global cache manager using HashMap for fast lookups"""
    def __init__(self):
        self.cache = HashMap()
        self.stats = {'hits': 0, 'misses': 0, 'total_requests': 0}
    
    def get(self, key):
        self.stats['total_requests'] += 1
        value = self.cache.get(key)
        if value is not None:
            self.stats['hits'] += 1
        else:
            self.stats['misses'] += 1
        return value
    
    def set(self, key, value):
        self.cache.put(key, value)
    
    def delete(self, key):
        return self.cache.delete(key)
    
    def clear(self):
        self.cache.clear()
        self.stats = {'hits': 0, 'misses': 0, 'total_requests': 0}
    
    def get_stats(self):
        hit_rate = 0
        if self.stats['total_requests'] > 0:
            hit_rate = (self.stats['hits'] / self.stats['total_requests']) * 100
        return {
            'hits': self.stats['hits'],
            'misses': self.stats['misses'],
            'total_requests': self.stats['total_requests'],
            'hit_rate': round(hit_rate, 2),
            'cache_size': len(self.cache)
        }

# Global cache instance
city_cache = CacheManager()

# -----------------------------------------------------------------------------
# Queue Manager
# -----------------------------------------------------------------------------
class QueueManager:
    """Global queue manager for processing booking requests"""
    def __init__(self):
        self.booking_queue = Queue()
        self.processed_count = 0
    
    def enqueue_booking(self, booking_data):
        booking_request = {
            'data': booking_data,
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'pending'
        }
        self.booking_queue.enqueue(booking_request)
        return {
            'message': 'Booking request queued successfully',
            'queue_position': self.booking_queue.size(),
            'status': 'pending'
        }
    
    def process_next_booking(self):
        if self.booking_queue.is_empty():
            return None
        booking = self.booking_queue.dequeue()
        booking['status'] = 'processed'
        booking['processed_at'] = datetime.utcnow().isoformat()
        self.processed_count += 1
        return booking
    
    def get_queue_status(self):
        return {
            'pending_requests': self.booking_queue.size(),
            'processed_count': self.processed_count,
            'is_empty': self.booking_queue.is_empty()
        }
    
    def peek_next(self):
        if self.booking_queue.is_empty():
            return None
        return self.booking_queue.peek()

# Global queue instance
booking_queue_manager = QueueManager()

# -----------------------------------------------------------------------------
# Rating Manager
# -----------------------------------------------------------------------------
class RatingManager:
    """Manage city ratings using BST for sorted access"""
    def __init__(self):
        self.rating_tree = BinarySearchTree()
        # Map ratings to city IDs (since BST stores only ratings)
        self.rating_to_cities = {}
    
    def add_rating(self, city_id, rating):
        self.rating_tree.insert(rating)
        if rating not in self.rating_to_cities:
            self.rating_to_cities[rating] = []
        if city_id not in self.rating_to_cities[rating]:
            self.rating_to_cities[rating].append(city_id)
    
    def get_top_ratings(self, limit=10):
        sorted_ratings = self.rating_tree.inorder_traversal()
        top_ratings = sorted_ratings[-limit:][::-1]
        result = []
        for rating in top_ratings:
            cities = self.rating_to_cities.get(rating, [])
            for city_id in cities:
                result.append({'rating': rating, 'city_id': city_id})
        return result[:limit]
    
    def get_highest_rating(self):
        return self.rating_tree.find_max()
    
    def get_lowest_rating(self):
        return self.rating_tree.find_min()
    
    def get_rating_stats(self):
        if self.rating_tree.is_empty():
            return {'total_ratings': 0, 'highest': None, 'lowest': None, 'tree_height': 0}
        all_ratings = self.rating_tree.inorder_traversal()
        avg_rating = sum(all_ratings) / len(all_ratings) if all_ratings else 0
        return {
            'total_ratings': len(all_ratings),
            'highest': self.rating_tree.find_max(),
            'lowest': self.rating_tree.find_min(),
            'average': round(avg_rating, 2),
            'tree_height': self.rating_tree.height()
        }

# Global rating manager instance
rating_manager = RatingManager()

# -----------------------------------------------------------------------------
# User Tracking Manager
# -----------------------------------------------------------------------------
class UserTracker:
    """Track user navigation and recently viewed cities"""
    def __init__(self):
        self.navigation_stacks = {}
        self.recent_cities = {}
    
    def track_navigation(self, user_id, page):
        if user_id not in self.navigation_stacks:
            self.navigation_stacks[user_id] = Stack()
        self.navigation_stacks[user_id].push({
            'page': page,
            'timestamp': datetime.utcnow().isoformat()
        })
    
    def go_back(self, user_id):
        if user_id not in self.navigation_stacks: return None
        stack = self.navigation_stacks[user_id]
        if stack.is_empty(): return None
        stack.pop() # Pop current
        if not stack.is_empty(): return stack.peek() # Return prev
        return None
    
    def get_navigation_history(self, user_id, limit=10):
        if user_id not in self.navigation_stacks: return []
        stack = self.navigation_stacks[user_id]
        history = []
        temp_stack = Stack()
        count = 0
        while not stack.is_empty() and count < limit:
            item = stack.pop()
            history.append(item)
            temp_stack.push(item)
            count += 1
        while not temp_stack.is_empty():
            stack.push(temp_stack.pop())
        return history
    
    def add_recent_city(self, user_id, city_id, city_name):
        if user_id not in self.recent_cities:
            self.recent_cities[user_id] = LinkedList()
        recent_list = self.recent_cities[user_id]
        recent_list.delete_by_value(city_id)
        if recent_list.size() >= 10:
            recent_list.delete_at_beginning()
        recent_list.insert_at_end({
            'city_id': city_id,
            'city_name': city_name,
            'viewed_at': datetime.utcnow().isoformat()
        })
    
    def get_recent_cities(self, user_id):
        if user_id not in self.recent_cities: return []
        return self.recent_cities[user_id].to_list()

# Global user tracker instance
user_tracker = UserTracker()
