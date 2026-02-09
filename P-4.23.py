# [P-4.23] Implement a recursive function with signature find(path, filename) that
# reports all entries of the file system rooted at the given path having the
# given file name.

import os

def find(path: str, filename: str) -> list[str]:
  """
  Recursively traverses the file system starting at 'path' to find all
  occurrences of 'filename'.

  The function performs a depth-first search (DFS) through the directory 
  tree. If a subdirectory is encountered, it calls itself recursively. 
  If a file matches the target filename, its path is recorded.

  Args:
    path: The starting directory path (string).
    filename: The exact name of the file to search for (string).

  Returns:
    A list of strings containing the paths to all matching files.
    Returns an empty list if no matches are found or if access is denied.
  """
  files_list = []
  
  try:
    entries = os.listdir(path)
  except (FileNotFoundError, PermissionError):
    # Handle cases where path doesn't exist or permission is restricted
    return []

  for entry in entries:
    record = os.path.join(path, entry)
    
    if os.path.isdir(record):
      files_list.extend(find(record, filename))
    elif os.path.isfile(record) and entry == filename:
      files_list.append(record)
      
  return files_list

path = input('path: ')
filename = input('filename: ')

results = find(path, filename)

if results:
  for file_path in results:
    print(file_path)
else:
    print("No matching files found.")