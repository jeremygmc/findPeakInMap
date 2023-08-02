# Write your algorithm in this function.
# Except for import statements, all other code must be within the findHighPoint function or additional helper functions

def findHighPoint(given_map):
  W = given_map.W
  H = given_map.H
  
  ini_max = [0, 0, 0]
  
  return splitSquaresFindPeak(given_map, W, H, size_of_square=round(0.1 * H), start_x=0, start_y=0, end_x=W, end_y=H, max=ini_max)

def findHighest(given_map, W, H, max):
  current_max, x, y = max, max[1], max[2]
  if (x-1 >= 0):
    left = given_map.getElevation(x-1, y)
    if left > max[0]:
      max = [left, x-1, y]
  if (x+1 <= W):
    right = given_map.getElevation(x+1, y)
    if right > max[0]:
      max = [right, x+1, y]
  if (y-1 >= 0):
    down = given_map.getElevation(x, y-1)
    if down > max[0]:
      max = [down, x, y-1]
  if (y+1 <= H):
    up = given_map.getElevation(x, y+1)
    if up > max[0]:
      max = [up, x, y+1]
  if current_max == max:
    return current_max
  else:
    return findHighest(given_map, W, H, max)

def splitSquaresFindPeak(given_map, W, H, size_of_square, start_x, start_y, end_x, end_y, max):
    current_max = max
    if size_of_square >= 5:
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                if x % size_of_square == 0 and y % size_of_square == 0:
                    ele = given_map.getElevation(x, y)
                    if ele > max[0]:
                        max = [ele, x, y]
    if current_max == max:
        max = findHighest(given_map, W, H, max)
        return (max[1], max[2])
    else:
        new_X = max[1] + size_of_square
        new_Y = max[2] + size_of_square
        if (new_X > W):
            new_X = W
        if (new_Y > H):
            new_Y = H
    return splitSquaresFindPeak(given_map, W, H, int(size_of_square//10), max[1], max[2], new_X, new_Y, max)
