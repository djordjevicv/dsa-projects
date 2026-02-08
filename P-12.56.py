# [P-12.56] Implement a nonrecursive, in-place version of the quick-sort algorithm, as
# described at the end of Section 12.3.2.

import random
from typing import List

def inplace_quick_sort(S: List[int], a: int, b: int) -> None:
  """
  Sorts the list S in-place using a nonrecursive quick-sort algorithm.

  Uses an explicit stack to simulate recursion.
  """
  
  if a >= b:
    return

  stack = []
  stack.append((a, b))

  while stack:
    a, b = stack.pop()

    if a >= b:
      continue

    pivot = S[b]
    left = a
    right = b - 1

    while left <= right:
      while left <= right and S[left] < pivot:
        left += 1
      while left <= right and pivot < S[right]:
        right -= 1
      if left <= right:
        S[left], S[right] = S[right], S[left]
        left, right = left + 1, right - 1

    S[left], S[b] = S[b], S[left]

    stack.append((a, left - 1))
    stack.append((left + 1, b))

input_list = [ random.randint(1, 100) for _ in range(40) ]
input_list_length = len(input_list)

print(f'Random list: {input_list}')
inplace_quick_sort(input_list, 0, input_list_length - 1)
print(f'Sorted list: {input_list}')