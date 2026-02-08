# [P-6.32] Give a complete ArrayDeque implementation of the double-ended queue
# ADT as sketched in Section 6.3.2.

from typing import Any

class Empty(Exception):
  pass

class ArrayDeque:
  """
  Double-ended queue implementation using a circular array for storage.
  """

  DEFAULT_CAPACITY = 10

  def __init__(self) -> None:  
    """Initializes an empty deque with a default capacity."""
    self._data = [None] * ArrayDeque.DEFAULT_CAPACITY
    self._size = 0
    self._front = 0

  def __len__(self) -> int:
    """Returns the number of elements currently in the deque."""
    return self._size

  def is_empty(self) -> bool:
    """Returns True if the deque contains no elements."""
    return self._size == 0

  def first(self) -> object:
    """
    Returns (but does not remove) the element at the front of the deque.

    Raises:
      Empty: If the deque is empty.
    """
    if self.is_empty():
      raise Empty('Queue is empty')
    return self._data[self._front]

  def last(self) -> object:
    """
    Returns (but does not remove) the element at the back of the deque.

    Raises:
      Empty: If the deque is empty.
    """
    if self.is_empty():
      raise Empty('Queue is empty')
    back = (self._front + self._size - 1) % len(self._data)
    return self._data[back]

  def delete_first(self) -> Any:
    """
    Removes and returns the first element of the deque.

    The front index is shifted circularly to the right.

    Raises:
      Empty: If the deque is empty.
    """
    if self.is_empty():
      raise Empty('Queue is empty')
    answer = self._data[self._front]
    self._data[self._front] = None
    self._front = (self._front + 1) % len(self._data)
    self._size -= 1
    return answer

  def delete_last(self) -> Any:
    """
    Removes and returns the last element of the deque.

    Raises:
      Empty: If the deque is empty.
    """
    if self.is_empty():
      raise Empty('Queue is empty')
    back = (self._front + self._size - 1) % len(self._data)
    answer = self._data[back]
    self._data[back] = None
    self._size -= 1
    return answer

  def add_last(self, e: Any) -> None:
    """
    Adds an element to the back of the deque.

    If the underlying array is full, its capacity is doubled.
    """
    if self._size == len(self._data):
      self.resize(2 * len(self._data))
    avail = (self._front + self._size) % len(self._data)
    self._data[avail] = e
    self._size += 1

  def add_first(self, e: Any) -> None:
    """
    Adds an element to the front of the deque.

    The front index is shifted circularly to the left. If the underlying 
    array is full, its capacity is doubled.
    """
    if self._size == len(self._data):
      self.resize(2 * len(self._data))

    self._front = (self._front - 1) % len(self._data)
    self._data[self._front] = e
    self._size += 1

  def resize(self, cap: int) -> None:
    """
    Resizes the underlying array to a new capacity.

    This method re-aligns the elements so that the front of the deque 
    starts at index 0 in the new array.
    """
    old = self._data
    self._data = [None] * cap
    walk = self._front
    for k in range(self._size):
      self._data[k] = old[walk]
      walk = (1 + walk) % len(old)
    self._front = 0

def test_array_deque() -> None:
  """Execute a series of tests to verify ArrayDeque functionality."""
  d = ArrayDeque()

  print("is_empty:", d.is_empty())
  print("len:", len(d))
  print()

  print("Add last: 1, 2, 3")
  d.add_last(1)
  d.add_last(2)
  d.add_last(3)
  print("first:", d.first())
  print("last:", d.last())
  print("len:", len(d))
  print()

  print("Add first: 0")
  d.add_first(0)
  print("first:", d.first())
  print("last:", d.last())
  print("len:", len(d))
  print()

  print("Delete first")
  print("removed:", d.delete_first())
  print("first:", d.first())
  print("len:", len(d))
  print()

  print("Delete last")
  print("removed:", d.delete_last())
  print("last:", d.last())
  print("len:", len(d))
  print()

  print("Fill to trigger resize")
  for i in range(4, 20):
    d.add_last(i)

  print("first:", d.first())
  print("last:", d.last())
  print("len:", len(d))
  print()

  print("Emptying deque")
  while not d.is_empty():
    d.delete_first()

  print("is_empty:", d.is_empty())
  print("len:", len(d))
  print()

  print("Exception test")
  try:
    d.delete_first()
  except Empty as e:
    print("Caught exception:", e)

test_array_deque()