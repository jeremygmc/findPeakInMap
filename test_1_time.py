from urllib.request import urlretrieve
import os

# represents a map class
class Map:
  def __init__(self, fpath, delay=0.00075):
    self._elevations, self.W, self.H = self._read_map(fpath)
    self._counter = 0
    self.delay = delay

  def reset_counter(self):
    self._counter = 0

  def _read_map(self, fpath):
    elevations = []
    with open(fpath, 'r') as f:
      for l in f:
        tokens = l.strip().split()
        elevations.append([int(tok) for tok in tokens])
    return elevations, len(elevations), len(elevations[0])
  
  # returns the elevation of (x,y)
  def getElevation(self, x, y):
    '''
    x and y should be integer
    '''

    if x < 0 or x >= self.W or y < 0 or y >= self.H:
      self.reset_counter()
      raise Exception("Sorry, coordinate out of bound x={}, y={}. Boundary 0 <= x < {}, 0 <= y < {}".format(x, y, self.W, self.H))
    self._counter += 1
    if self.delay > 0:
      import time
      time.sleep(self.delay)
    return self._elevations[x][y]

  @property
  def counter(self):
    return self._counter

# ------------------------------------------------------------------------------
# check if answer is OK (returns None if OK, else returns an error msg)
def get_error_message(answer):
  if answer == None:
    return "Error : your function returned None. It should return a list/tuple of 2 integers."
  elif type(answer) not in [list, tuple]:
    return "Error : your function returned something other than a list/tuple. It should return a list of 2 integers."
  elif len(answer) != 2:
    return "Error : your function returned a list/tuple of fewer than, or more than 2 elements. It should return a list/tuple of exactly 2 integers."
  elif not all(isinstance(i, int) for i in answer):  # check if all elements in answer are int
    return "Error : your function returned a list/tuple of elements, but not all of them are integers. It should return a list/tuple of exactly 2 integers."
  else:
    return None  # no problem, no error msg

# ------------------------------------------------------------------------------    
# returns quality score of an answer
def compute_quality_score(answer, given_map, threshold=0.001):
  '''
    The quality score is equal to the elevation that the designed algorithm found.
    However, this quality score will be reduced by a punishment ratio.
  '''
  W = given_map.W
  H = given_map.H
  counter = given_map.counter
  elevation = given_map.getElevation(answer[0], answer[1])
  total_points = W * H
  punishment_factor = 0
  if counter / total_points > threshold:
    punishment_factor = counter / total_points
  return max(elevation - elevation * 10 * punishment_factor, 0)

# Download a map
def download(url, file):
    if os.path.isfile(file):
        print(file + " already downloaded. You can see it if you click on the folder icon at the left")
    else:
        print("Downloading file " + file + " ...", end="")
        urlretrieve(url,file)
        print("OK")
        
from findPeakInMap import *

# Test case
file_name = "map1.txt"  # <---- CHANGE CSV FILE NAME HERE to use a different map

import time, copy
# (1) ----- prepare data ------
print("(1) Reading data from " + file_name + " now...\n")
given_map = Map(file_name)

# (2) ----- run the test case ------
print("(2) Starting timer...")
print("Calling your function now using the map read from " + file_name)
start_time = time.time()
answer = findHighPoint(given_map) # calls your function 
time_taken = time.time() - start_time
print("Stopping timer...")
print("Execution time " + str(time_taken) + " seconds.\n")    # display time lapsed

# (3) ----- correctness testing code ------ 
print("(3) Checking your answer...")
error_message = get_error_message(answer)

if error_message == None:
  # all is good
  print("Your function returned a valid answer")
  quality_score = compute_quality_score(answer, given_map)
  print("Returned coordinate:", answer)
  print("Elevation (height):", given_map.getElevation(answer[0], answer[1]))
  print("Quality score:", quality_score)
else:
  # there is an error
  print("Your function is not correctly written :-(")
  print(error_message)