# [P-8.64] Implement the binary tree ADT using the array-based representation described in Section 8.3.2.

from typing import Any, List, Self

class ArrayBinaryTree:
    """
    Array-based implementation of a Binary Tree ADT.
    Positions are represented by integer indices.
    """

    # Initialization

    def __init__(self) -> None:
        """Initialize an empty binary tree."""
        self._data: List[Any] = []
        self._size: int = 0

    # Basic Utilities

    def __len__(self) -> int:
        """Returns the number of elements in the tree."""
        return self._size

    def is_empty(self) -> bool:
        """Returns True if the tree is empty."""
        return len(self) == 0

    # Accessors

    def root(self) -> int | None:
        """Returns the position of the root or None if empty."""
        return None if self.is_empty() else 0

    def parent(self, p: int) -> int | None:
        """Returns the parent position of p or None if p is root."""
        p = self._validate(p)
        return None if self.root() == p else (p - 1) // 2

    def left(self, p: int) -> int | None:
        """Returns the left child of p or None if it does not exist."""
        p = self._validate(p)
        left = 2 * p + 1
        return None if left >= len(self._data) or self._data[left] is None else left

    def right(self, p: int) -> int | None:
        """Returns the right child of p or None if it does not exist."""
        p = self._validate(p)
        right = 2 * p + 2
        return None if right >= len(self._data) or self._data[right] is None else right

    def sibling(self, p: int) -> int | None:
        """Returns the sibling of p or None if no sibling exists."""
        p = self._validate(p)
        if self.is_root(p):
            return None
        parent = self.parent(p)
        if self.left(parent) == p:
            return self.right(parent)
        return self.left(parent)

    def children(self, p: int) -> List[int | None]:
        """Returns a list containing the left and right child of p."""
        p = self._validate(p)
        return [self.left(p), self.right(p)]

    def num_children(self, p: int) -> int:
        """Returns the number of children of p."""
        p = self._validate(p)
        count = 0
        if self.left(p) is not None:
            count += 1
        if self.right(p) is not None:
            count += 1
        return count

    def is_root(self, p: int) -> bool:
        """Returns True if p is the root of the tree."""
        p = self._validate(p)
        return self.root() == p

    def is_leaf(self, p: int) -> bool:
        """Returns True if p has no children."""
        return self.left(p) is None and self.right(p) is None

    def depth(self, p: int) -> int:
        """Returns the depth of position p."""
        p = self._validate(p)
        if self.is_root(p):
            return 0
        return 1 + self.depth(self.parent(p))

    def subtree_height(self, p: int) -> int:
        """Returns the height of the subtree rooted at p."""
        p = self._validate(p)
        if self.is_leaf(p):
            return 0

        left = self.left(p)
        right = self.right(p)

        left_height: int = self.subtree_height(left) if left is not None else 0
        right_height: int = self.subtree_height(right) if right is not None else 0

        return 1 + max(left_height, right_height)

    def height(self) -> int:
        """Returns the height of the tree."""
        p = self.root()
        if p is None:
            return -1
        return self.subtree_height(p)

    # Update Operations

    def add_root(self, e: Any) -> int:
        """Adds a root to an empty tree and returns its position."""
        if not self.is_empty():
            raise ValueError("Tree is not empty.")
        self._ensure_capacity(0)
        self._data[0] = e
        self._size = 1
        return 0

    def add_left(self, p: int, e: Any) -> int:
        """Adds a left child to position p and returns its position."""
        p = self._validate(p)
        if self.left(p) is not None:
            raise ValueError("Already includes left node")
        left = 2 * p + 1
        self._ensure_capacity(left)
        self._data[left] = e
        self._size += 1
        return left

    def add_right(self, p: int, e: Any) -> int:
        """Adds a right child to position p and returns its position."""
        p = self._validate(p)
        if self.right(p) is not None:
            raise ValueError("Already includes right node")
        right = 2 * p + 2
        self._ensure_capacity(right)
        self._data[right] = e
        self._size += 1
        return right

    def replace(self, p: int, e: Any) -> None:
        """Replaces the element stored at position p."""
        p = self._validate(p)
        self._data[p] = e

    def delete(self, p: int) -> Any:
        """Deletes the node at position p and returns its element."""
        p = self._validate(p)

        if self.num_children(p) == 2:
            raise ValueError("Position has two children")

        element = self._data[p]
        child_index = self.left(p) if self.left(p) is not None else self.right(p)

        if child_index is not None:
            self._move_subtree(child_index, p)
        else:
            self._data[p] = None

        self._size -= 1
        return element

    def attach(self, p: int, t1: ArrayBinaryTree, t2: ArrayBinaryTree) -> None:
        """Attaches trees t1 and t2 as left and right subtrees of p."""
        p = self._validate(p)
        if self.left(p) is not None or self.right(p) is not None:
            raise ValueError(f"{p} must be a leaf.")

        if t1 is not None:
            self._copy_subtree(t1, t1.root(), 2 * p + 1)
        if t2 is not None:
            self._copy_subtree(t2, t2.root(), 2 * p + 2)

    # Utilities

    def _validate(self, p: int) -> int:
        """Validates position p."""
        if self.is_empty() or p >= len(self._data) or self._data[p] is None:
            raise ValueError("Position index is invalid.")
        return p

    def _ensure_capacity(self, i: int) -> None:
        """Ensures the underlying array can store index i."""
        current_length: int = len(self._data)
        if i >= current_length:
            self._data.extend(
                [None for _ in range(current_length, max(2 * current_length, i + 1))]
            )

    def _move_subtree(self, source_index: int, destination_index: int) -> None:
        """Moves a subtree from source_index to destination_index."""
        if source_index >= len(self._data) or self._data[source_index] is None:
            return

        self._data[destination_index] = self._data[source_index]
        self._data[source_index] = None

        self._move_subtree(2 * source_index + 1, 2 * destination_index + 1)
        self._move_subtree(2 * source_index + 2, 2 * destination_index + 2)

    def _copy_subtree(self, source: ArrayBinaryTree, src_p: int, dest_p: int) -> None:
        """Copies a subtree from source into this tree."""
        queue = [(src_p, dest_p)]
        while queue:
            s, d = queue.pop(0)
            if s < len(source._data) and source._data[s] is not None:
                self._ensure_capacity(d)
                self._data[d] = source._data[s]
                self._size += 1
                queue.append((2 * s + 1, 2 * d + 1))
                queue.append((2 * s + 2, 2 * d + 2))

    # Display

    def __str__(self) -> str:
        """Returns a string representation of the tree."""
        if self.is_empty():
            return "Empty Tree"

        result: List[str] = []
        for i, val in enumerate(self._data):
            if val is not None:
                parent = self.parent(i) if i != 0 else None
                left = self.left(i)
                right = self.right(i)
                result.append(
                    f"Index {i}: {val} (parent: {parent}, left: {left}, right: {right})"
                )
        return "\n".join(result)

def run_tests():
    t = ArrayBinaryTree()

    print("is_empty:", t.is_empty())
    print("len:", len(t))
    print()

    print("Add root: A")
    root = t.add_root("A")
    print("root index:", root)
    print("is_root(root):", t.is_root(root))
    print("len:", len(t))
    print()

    print("Add left and right children: B, C")
    l = t.add_left(root, "B")
    r = t.add_right(root, "C")
    print("left index:", l)
    print("right index:", r)
    print("num_children(root):", t.num_children(root))
    print()

    print("Leaf and sibling checks")
    print("is_leaf(B):", t.is_leaf(l))
    print("sibling(B):", t.sibling(l))
    print()

    print("Replace right child with C_New")
    t.replace(r, "C_New")
    print("right value:", t._data[r])
    print()

    print("Depth and height")
    print("depth(B):", t.depth(l))
    print("height:", t.height())
    print()

    print("Delete test")
    t.add_left(l, "D")
    print("Added left child D to B")
    print("len before delete:", len(t))
    removed = t.delete(l)
    print("removed:", removed)
    print("new value at index 1:", t._data[1])
    print("len after delete:", len(t))
    print()

    print("Attach test")
    leaf = t.right(root)
    t1 = ArrayBinaryTree()
    t2 = ArrayBinaryTree()
    t1.add_root("X")
    t2.add_root("Y")

    t.attach(leaf, t1, t2)
    print("attached trees at index:", leaf)
    print("len:", len(t))
    print("tree:")
    print(t)
    print()

    print("Exception tests")

    try:
        t.add_root("Duplicate")
    except ValueError as e:
        print("Caught exception on add_root:", e)

    try:
        t.delete(root)
    except ValueError as e:
        print("Caught exception on delete(root):", e)

    print()

run_tests()