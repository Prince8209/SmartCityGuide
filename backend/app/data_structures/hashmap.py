"""
HashMap (Hash Table) Data Structure Implementation
Key-value storage - useful for caching, fast lookups, indexing
"""


class HashMap:
    """
    HashMap implementation using separate chaining for collision resolution
    Operations: insert (O(1) average), get (O(1) average), delete (O(1) average)
    """
    
    def __init__(self, capacity=16):
        """
        Initialize a hash map with given capacity
        
        Args:
            capacity: Initial capacity of the hash map (default: 16)
        """
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]
    
    def _hash(self, key):
        """
        Hash function to compute bucket index
        
        Args:
            key: The key to hash
            
        Returns:
            int: Bucket index
        """
        return hash(key) % self.capacity
    
    def put(self, key, value):
        """
        Insert or update a key-value pair
        Time Complexity: O(1) average, O(n) worst case
        
        Args:
            key: The key to insert/update
            value: The value to associate with the key
        """
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]
        
        # Update if key exists
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        
        # Insert new key-value pair
        bucket.append((key, value))
        self.size += 1
        
        # Resize if load factor exceeds 0.75
        if self.size / self.capacity > 0.75:
            self._resize()
    
    def get(self, key, default=None):
        """
        Get the value associated with a key
        Time Complexity: O(1) average, O(n) worst case
        
        Args:
            key: The key to look up
            default: Default value if key not found
            
        Returns:
            The value associated with the key, or default if not found
        """
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]
        
        for k, v in bucket:
            if k == key:
                return v
        
        return default
    
    def delete(self, key):
        """
        Delete a key-value pair
        Time Complexity: O(1) average, O(n) worst case
        
        Args:
            key: The key to delete
            
        Returns:
            bool: True if deleted, False if key not found
        """
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return True
        
        return False
    
    def contains(self, key):
        """
        Check if a key exists in the map
        Time Complexity: O(1) average
        
        Args:
            key: The key to check
            
        Returns:
            bool: True if key exists, False otherwise
        """
        return self.get(key) is not None
    
    def keys(self):
        """
        Get all keys in the map
        Time Complexity: O(n)
        
        Returns:
            list: List of all keys
        """
        all_keys = []
        for bucket in self.buckets:
            for k, v in bucket:
                all_keys.append(k)
        return all_keys
    
    def values(self):
        """
        Get all values in the map
        Time Complexity: O(n)
        
        Returns:
            list: List of all values
        """
        all_values = []
        for bucket in self.buckets:
            for k, v in bucket:
                all_values.append(v)
        return all_values
    
    def items(self):
        """
        Get all key-value pairs
        Time Complexity: O(n)
        
        Returns:
            list: List of (key, value) tuples
        """
        all_items = []
        for bucket in self.buckets:
            for item in bucket:
                all_items.append(item)
        return all_items
    
    def clear(self):
        """
        Remove all key-value pairs
        Time Complexity: O(1)
        """
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
    
    def _resize(self):
        """
        Resize the hash map when load factor is too high
        Time Complexity: O(n)
        """
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        
        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)
    
    def __len__(self):
        """Return the number of key-value pairs"""
        return self.size
    
    def __getitem__(self, key):
        """Get item using bracket notation"""
        value = self.get(key)
        if value is None:
            raise KeyError(f"Key not found: {key}")
        return value
    
    def __setitem__(self, key, value):
        """Set item using bracket notation"""
        self.put(key, value)
    
    def __delitem__(self, key):
        """Delete item using bracket notation"""
        if not self.delete(key):
            raise KeyError(f"Key not found: {key}")
    
    def __contains__(self, key):
        """Check if key exists using 'in' operator"""
        return self.contains(key)
    
    def __str__(self):
        """String representation of the hash map"""
        items = ', '.join([f"'{k}': {v}" for k, v in self.items()])
        return f"HashMap({{{items}}})"
    
    def __repr__(self):
        """Official string representation"""
        return self.__str__()


# Example usage and practical application
if __name__ == "__main__":
    # Example: City information cache
    print("=" * 60)
    print("HASHMAP DATA STRUCTURE - City Cache Example")
    print("=" * 60)
    
    city_cache = HashMap()
    
    # Add city information
    print("\n🏙️ Caching city information:")
    cities = {
        "Mumbai": {"population": "20M", "state": "Maharashtra"},
        "Delhi": {"population": "30M", "state": "Delhi"},
        "Bangalore": {"population": "12M", "state": "Karnataka"},
        "Chennai": {"population": "10M", "state": "Tamil Nadu"}
    }
    
    for city, info in cities.items():
        city_cache.put(city, info)
        print(f"  ✓ Cached: {city} -> {info}")
    
    print(f"\n📊 Cache size: {len(city_cache)}")
    
    # Retrieve city information
    print("\n🔍 Looking up 'Bangalore':")
    info = city_cache.get("Bangalore")
    print(f"  ✓ Found: {info}")
    
    # Update city information
    print("\n✏️ Updating Mumbai population:")
    city_cache.put("Mumbai", {"population": "21M", "state": "Maharashtra"})
    print(f"  ✓ Updated: {city_cache.get('Mumbai')}")
    
    # Check if city exists
    print("\n❓ Does 'Kolkata' exist in cache?")
    print(f"  → {city_cache.contains('Kolkata')}")
    
    # Get all cities
    print(f"\n🗺️ All cached cities: {city_cache.keys()}")
    
    # Delete a city
    print("\n🗑️ Removing 'Chennai' from cache:")
    city_cache.delete("Chennai")
    print(f"  ✓ Deleted. Remaining cities: {city_cache.keys()}")
