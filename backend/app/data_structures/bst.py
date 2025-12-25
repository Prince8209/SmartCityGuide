"""
Binary Search Tree (BST) Data Structure Implementation
Hierarchical data structure - useful for sorted data, range queries, hierarchical relationships
"""


class TreeNode:
    """
    Node class for Binary Search Tree
    Each node contains data, left child, and right child
    """
    
    def __init__(self, data):
        """
        Initialize a tree node with data
        
        Args:
            data: The data to store in the node
        """
        self.data = data
        self.left = None
        self.right = None
    
    def __str__(self):
        """String representation of the node"""
        return str(self.data)


class BinarySearchTree:
    """
    Binary Search Tree implementation
    Properties: Left child < Parent < Right child
    Operations: insert (O(log n) average), search (O(log n) average), delete (O(log n) average)
    """
    
    def __init__(self):
        """Initialize an empty binary search tree"""
        self.root = None
        self._size = 0
    
    def insert(self, data):
        """
        Insert a new value into the tree
        Time Complexity: O(log n) average, O(n) worst case
        
        Args:
            data: The data to insert
        """
        if self.root is None:
            self.root = TreeNode(data)
            self._size += 1
        else:
            self._insert_recursive(self.root, data)
    
    def _insert_recursive(self, node, data):
        """Helper method for recursive insertion"""
        if data < node.data:
            if node.left is None:
                node.left = TreeNode(data)
                self._size += 1
            else:
                self._insert_recursive(node.left, data)
        elif data > node.data:
            if node.right is None:
                node.right = TreeNode(data)
                self._size += 1
            else:
                self._insert_recursive(node.right, data)
        # If data == node.data, don't insert (no duplicates)
    
    def search(self, data):
        """
        Search for a value in the tree
        Time Complexity: O(log n) average, O(n) worst case
        
        Args:
            data: The data to search for
            
        Returns:
            bool: True if found, False otherwise
        """
        return self._search_recursive(self.root, data)
    
    def _search_recursive(self, node, data):
        """Helper method for recursive search"""
        if node is None:
            return False
        
        if data == node.data:
            return True
        elif data < node.data:
            return self._search_recursive(node.left, data)
        else:
            return self._search_recursive(node.right, data)
    
    def delete(self, data):
        """
        Delete a value from the tree
        Time Complexity: O(log n) average, O(n) worst case
        
        Args:
            data: The data to delete
            
        Returns:
            bool: True if deleted, False if not found
        """
        if not self.search(data):
            return False
        
        self.root = self._delete_recursive(self.root, data)
        self._size -= 1
        return True
    
    def _delete_recursive(self, node, data):
        """Helper method for recursive deletion"""
        if node is None:
            return None
        
        if data < node.data:
            node.left = self._delete_recursive(node.left, data)
        elif data > node.data:
            node.right = self._delete_recursive(node.right, data)
        else:
            # Node with only one child or no child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            # Node with two children: Get inorder successor
            min_larger_node = self._find_min(node.right)
            node.data = min_larger_node.data
            node.right = self._delete_recursive(node.right, min_larger_node.data)
        
        return node
    
    def _find_min(self, node):
        """Find the minimum value node in a subtree"""
        current = node
        while current.left:
            current = current.left
        return current
    
    def find_min(self):
        """
        Find the minimum value in the tree
        Time Complexity: O(log n) average
        
        Returns:
            The minimum value, or None if tree is empty
        """
        if self.root is None:
            return None
        return self._find_min(self.root).data
    
    def find_max(self):
        """
        Find the maximum value in the tree
        Time Complexity: O(log n) average
        
        Returns:
            The maximum value, or None if tree is empty
        """
        if self.root is None:
            return None
        
        current = self.root
        while current.right:
            current = current.right
        return current.data
    
    def inorder_traversal(self):
        """
        Perform inorder traversal (Left -> Root -> Right)
        Returns sorted order for BST
        Time Complexity: O(n)
        
        Returns:
            list: List of values in sorted order
        """
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node, result):
        """Helper method for inorder traversal"""
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.data)
            self._inorder_recursive(node.right, result)
    
    def preorder_traversal(self):
        """
        Perform preorder traversal (Root -> Left -> Right)
        Time Complexity: O(n)
        
        Returns:
            list: List of values in preorder
        """
        result = []
        self._preorder_recursive(self.root, result)
        return result
    
    def _preorder_recursive(self, node, result):
        """Helper method for preorder traversal"""
        if node:
            result.append(node.data)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)
    
    def postorder_traversal(self):
        """
        Perform postorder traversal (Left -> Right -> Root)
        Time Complexity: O(n)
        
        Returns:
            list: List of values in postorder
        """
        result = []
        self._postorder_recursive(self.root, result)
        return result
    
    def _postorder_recursive(self, node, result):
        """Helper method for postorder traversal"""
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.data)
    
    def height(self):
        """
        Get the height of the tree
        Time Complexity: O(n)
        
        Returns:
            int: Height of the tree (0 for empty tree)
        """
        return self._height_recursive(self.root)
    
    def _height_recursive(self, node):
        """Helper method for calculating height"""
        if node is None:
            return 0
        
        left_height = self._height_recursive(node.left)
        right_height = self._height_recursive(node.right)
        
        return 1 + max(left_height, right_height)
    
    def is_empty(self):
        """
        Check if the tree is empty
        Time Complexity: O(1)
        
        Returns:
            bool: True if tree is empty, False otherwise
        """
        return self.root is None
    
    def size(self):
        """
        Get the number of nodes in the tree
        Time Complexity: O(1)
        
        Returns:
            int: Number of nodes in the tree
        """
        return self._size
    
    def clear(self):
        """
        Remove all nodes from the tree
        Time Complexity: O(1)
        """
        self.root = None
        self._size = 0
    
    def __len__(self):
        """Return the size of the tree"""
        return self.size()
    
    def __contains__(self, data):
        """Check if value exists using 'in' operator"""
        return self.search(data)
    
    def __str__(self):
        """String representation of the tree"""
        if self.is_empty():
            return "BinarySearchTree([])"
        return f"BinarySearchTree({self.inorder_traversal()})"
    
    def __repr__(self):
        """Official string representation"""
        return self.__str__()


# Example usage and practical application
if __name__ == "__main__":
    # Example: City rating system (sorted by rating)
    print("=" * 60)
    print("BINARY SEARCH TREE - City Ratings Example")
    print("=" * 60)
    
    # Using ratings as keys for demonstration
    city_ratings = BinarySearchTree()
    
    # Insert city ratings
    print("\n⭐ Adding city ratings:")
    ratings = [85, 92, 78, 95, 88, 70, 90]
    cities = ["Mumbai", "Delhi", "Kolkata", "Bangalore", "Chennai", "Jaipur", "Hyderabad"]
    
    for rating, city in zip(ratings, cities):
        city_ratings.insert(rating)
        print(f"  ✓ Added: {city} (Rating: {rating})")
    
    print(f"\n📊 Total cities: {city_ratings.size()}")
    print(f"📏 Tree height: {city_ratings.height()}")
    
    # Search for a rating
    print("\n🔍 Searching for rating 92:")
    found = city_ratings.search(92)
    print(f"  → Found: {found}")
    
    # Find min and max ratings
    print(f"\n📉 Minimum rating: {city_ratings.find_min()}")
    print(f"📈 Maximum rating: {city_ratings.find_max()}")
    
    # Get sorted ratings (inorder traversal)
    print(f"\n📋 Ratings in sorted order:")
    sorted_ratings = city_ratings.inorder_traversal()
    print(f"  → {sorted_ratings}")
    
    # Delete a rating
    print("\n🗑️ Removing rating 78:")
    city_ratings.delete(78)
    print(f"  ✓ Deleted. Updated ratings: {city_ratings.inorder_traversal()}")
    
    # Different traversals
    print("\n🔄 Tree Traversals:")
    print(f"  Preorder:  {city_ratings.preorder_traversal()}")
    print(f"  Inorder:   {city_ratings.inorder_traversal()}")
    print(f"  Postorder: {city_ratings.postorder_traversal()}")
