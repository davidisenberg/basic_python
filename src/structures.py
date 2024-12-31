
from typing import List, Optional
from collections import defaultdict

def valid_parens2(input: str) -> bool:
    from collections import deque
    keys = { '}':'{', ']':'[',')':'('}
    stack = deque()

    for s in input:
        if s in keys:
            if len(stack) == 0:
                return False
            if stack[-1] == keys[s]:
                stack.pop()
        else:
            stack.append(s)
    return len(stack) == 0

def valid_parens(input: str) -> bool:

    from collections import deque

    dict = { "}":"{", ")":"(","]":"["}
    stack = deque()

    for s in input:
        if s in dict:
            if len(stack) == 0:
                return False
            if stack[-1] != dict[s]:
                return False
            stack.pop()
        else:
            stack.append(s)
    return len(stack) == 0




def canAttendMeetings2(intervals: List[List[int]]) -> bool:

    intervals.sort(key = lambda x: x[0])

    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i-1][1]:
            return False
    return True


    # intervals.sort(key = lambda x: x[0])
    # for i in range(0, len(intervals)-1):
    #     if intervals[i][1] > intervals[i+1][0]:
    #         return False
    # return True

def canAttendMeetings(intervals: List[List[int]]) -> bool:

    intervals.sort(key= lambda x: x[0])
    for i in range(0, len(intervals)-1):
        if intervals[i][1] > intervals[i+1][0]:
            return False
    return True
        

   


def movingAverage2(list: List[int], w: int = 3) -> List[float]:

    result = []
    
    sum = 0
    for i in range(0,w):
        sum = sum + list[i]

    result.append(sum/w)
    for i in range(w, len(list),1):
        sum = sum + list[i] - list[i-w]
        result.append(sum/w)

    return result

def movingAverage3(list: List[int], w: int = 3) -> List[float]:

    import numpy as np

    result = []
    
    for i in range(0, len(list)-w+1,1):
        sum = np.sum(list[i:i+w])
        result.append(sum/w)

    return result



def heap2() -> List[int]:

    result = []
    li = [5, 7, 9, 1, 3, 8 ]
    #return top - 1
    #pop and return it - 1
    #push 2
    #pop and return it - 2
    #pop and return it - 3
    #3 smallest - return 5,7,8

    import heapq
    heapq.heapify(li)

    result.append(li[0])

    result.append(heapq.heappop(li))

    heapq.heappush(li,1)

    result.append(heapq.heappop(li))
    result.append(heapq.heappop(li))
    result.append(heapq.nsmallest(3,li))

    return result


    return result

def heap() -> List[int]:
    result = []
    li = [5, 7, 9, 1, 3, 8 ]
    import heapq

    heapq.heapify(li)
       
    
    #return top - 1
    result.append(li[0])
    #pop and return it - 1
    result.append(heapq.heappop(li))
    
    #push 2
    heapq.heappush(li, 2)

    #pop and return it - 2
    result.append(heapq.heappop(li))

    #pop and return it - 3
    result.append(heapq.heappop(li))

    #3 smallest - return 5,7,8
    result.append(heapq.nsmallest(3,li))

    return result

def capital_case(x):
    return x.capitalize()

def islands2( grid : List[List[int] ]) -> int:
    visited = set()
    num_islands = 0

    def dfs(grid, row, col):
        #nonlocal visited            

        if (row,col) in visited:
            return


        visited.add((row,col))
        if grid[row][col] != 1:
            return

        if row > 0:
            dfs(grid, row -1, col)
        if row < len(grid)-1:
            dfs(grid, row+1, col)
        if col > 0:
            dfs(grid, row, col-1)
        if col < len(grid[0]) -1:
            dfs(grid, row, col+1 )


    for row, rowlist in enumerate(grid):
        for col, val in enumerate(rowlist):
            if val == 1:
                if (row,col) not in visited:
                    num_islands = num_islands + 1
                    dfs(grid, row, col)
    
    return num_islands

def islands( grid : List[List[int] ]) -> int:
    
    num_islands = 0
    visited = set()

    def dfs(grid, row: int, col: int):
        
        if (row,col) in visited:
            return

        visited.add((row,col))
        
        if grid[row][col] == 1:
            if row > 0:
                dfs(grid, row-1, col)
            if col>0:
                dfs(grid, row, col-1)
            if row < len(grid)-1:
                dfs(grid, row+1, col)
            if col < len(grid[0])-1:
                dfs(grid, row, col+1)

    for row in range(0, len(grid)):
        for col in range(0, len(grid[0])):
            if (row, col) not in visited:
                if grid[row][col] == 1:
                    num_islands = num_islands+1
                    dfs(grid, row, col)
    
    return num_islands









def search2(nums : List[int], target : int):

    left = 0
    right = len(nums)

    while left < right:
        mid = left + (right-left) // 2

        if(nums[mid] == target):
            return mid
        
        if(nums[mid] >= target):
            right = mid
        
        else:
            left = mid + 1
    
    return -1
        
def search(nums: List[int], target: int) -> int:

    left = 0
    right = len(nums)

    while left < right:
        mid = left + (right-left)//2

        if nums[mid] == target:
            return mid
        if nums[mid] > target:
            right = mid
        else:
            left = mid +1
    return -1

        
def queue2() -> List[int]:
    from collections import deque
    result = []
    queue = deque()

    #add 1,2 to queue
    #remove first 1
    #extend [ 3 4]
    #remove first 2


    queue.append(1)
    queue.append(2)
    result.append(queue.popleft())
    queue.extend([3,4])
    result.append(queue.popleft())
    result.append(queue.popleft())

    return result

def queue() -> List[int]:
  
    result = []
    from collections import deque
    queue = deque()

    #add 1,2 to queue
    #remove first 1
    #extend [ 3 4]
    #remove first 2
    queue.append(1)
    queue.append(2)
    result.append(queue.popleft())
    queue.extend([3,4])
    result.append(queue.popleft())
    result.append(queue.popleft())



    return result
    

class TreeNode2:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class TreeNode:
    def __init__(self, val=0, left = None, right=None):
        self.val = val
        self.left = left
        self.right = right




#    7
#  4   

class DiameterCalc:

    def __init__(self):
        self.diameter = 0

    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0

        self.longest_path(root)
        return self.diameter


    def longest_path(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
    
        left = self.longest_path(root.left)
        right = self.longest_path(root.right)
        val =  1+max(left, right)
        self.diameter = max(self.diameter, left+right)
        return val

def in_order_traversal_2(root: Optional[TreeNode]) -> List[int]:
    
    return in_order_traversal(root.left) + [root.val] + in_order_traversal(root.right) if root else []

def in_order_traversal2(root: Optional[TreeNode]) -> List[int]:
    
    res = []
    def traverse(root: Optional[TreeNode]):

        if root.left: traverse(root.left)
        res.append(root.val)
        if root.right: traverse(root.right)
    if root: traverse(root)
    return res

def in_order_traversal(root: Optional[TreeNode]) -> List[int]:
    
    res = []
    def traverse(root: Optional[TreeNode]):

        if root.left: traverse(root.left)
        res.append(root.val)
        if root.right: traverse(root.right)
    if root: traverse(root)
    return res


def ocean_view2(heights: List[int]) -> List[int]:

    left_view = 0
    right_view = 0
    left_list = []
    right_list = []
    already_there = set()

    for i in range(0,len(heights)):
        if heights[i] > left_view:
            left_list.append(i)
            left_view = heights[i]
            already_there.add(i)
    for i in range(len(heights)-1,-1,-1):
        if i in already_there:
            break
        if heights[i] > right_view:
            right_list.append(i)
            right_view = heights[i]
    right_list.reverse()
    left_list.extend(right_list)
    return left_list


# There are n buildings in a line. You are given an integer array heights of size n that represents the heights of the buildings in the line.
# The ocean is to the right of the buildings. A building has an ocean view if the building can see the ocean without obstructions. Formally, a building has an ocean view if all the buildings to its right have a smaller height.
# Return a list of indices (0-indexed) of buildings that have an ocean view, sorted in increasing order.
# Example 1:
# Input: heights = [4,2,3,1]
# Output: [0,2,3]
# Explanation: Building 1 (0-indexed) does not have an ocean view because building 2 is taller.

# Example 2:

# Input: heights = [4,3,2,1]
# Output: [0,1,2,3]
# Explanation: All the buildings have an ocean view.
# Example 3:

# Input: heights = [1,3,2,4]
# Output: [3]
# Explanation: Only building 3 has an ocean view.

def ocean_view(heights: List[int]) -> List[int]:

    left_list = []
    right_list = []
    max_height = 0

    items = set()
    

    for i in range(0, len(heights)):
        height = heights[i]
        if height > max_height:
            max_height = height
            left_list.append(i)
            items.add(i)
    
    max_height=0
    for i in range(len(heights)-1,-1,-1):
        if i in items:
            break
        height = heights[i]
        if height > max_height:
            max_height = height
            right_list.append(i)
    
    right_list.reverse()
    left_list.extend(right_list)
    
    return left_list

def merge_sort2(list: List[int]):

    if len(list) <= 1:
        return list
    
    else:
        mid = len(list)//2
        listA = merge_sort(list[0:mid])
        listB = merge_sort(list[mid:])
        result = merge(listA, listB)
    
    return result

def merge_sort(list: List[int]):

    if len(list) < 2:
        return list
    
    mid = len(list)//2
    listA = merge_sort(list[0:mid])
    listB = merge_sort(list[mid:])
    return merge(listA, listB)


def merge2(listA: List[int], listB: List[int]) -> List[int]:
    a = 0
    b = 0
    result = []
    while a < len(listA) or b < len(listB):
        if a == len(listA):
            result.append(listB[b])
            b = b + 1
            
        elif b == len(listB):
            result.append(listA[a])
            a = a+1
            
        elif listA[a] < listB[b]:
            result.append(listA[a])
            a = a + 1
        else:
            result.append(listB[b])
            b = b + 1
        
    return result


def merge(listA: List[int], listB: List[int]) -> List[int]:
  
  result = []
  a = 0
  b = 0

  while a < len(listA) or b < len(listB):
      if a >= len(listA):
        result.append(listB[b])
        b = b+1
      elif b>= len(listB):
        result.append(listA[a])
        a = a+1
      elif  listA[a] > listB[b]:
        result.append(listB[b])
        b = b+1
      else:
        result.append(listA[a])
        a = a+1

  return result
    

    
        
        
def two_sum2(list: List[int], target: int ) -> List[int]:

    cache = {}

    for i, item in enumerate(list):
        if target-item in cache:
            return [cache[target-item], i ]
        else:
            cache[item] = i

    return []

def two_sum(list: List[int], target: int ) -> List[int]:

    cache = {}

    for i, item in enumerate(list):
        if target-item in cache:
            return [cache[target-item], i ]
        cache[item] = i

def max_profit2( prices: List[int]) -> int:
    import sys
    profit = 0
    curr_min = sys.maxsize

    for i in range(0, len(prices),1):
        if prices[i] < curr_min:
            curr_min = prices[i]
        else:
            profit = max(prices[i] - curr_min, profit)
            
    return profit


def max_profit( prices: List[int]) -> int:
   
    if len(prices) <= 1:
       return 0
   
    min = prices[0]
    max_profit = 0

    for i in range(1, len(prices)):
        if prices[i] < min:
           min = prices[i]
        elif prices[i] - min > max_profit:
            max_profit = prices[i] -min
    return max_profit

def others(self) ->int:
    str = "abcdef"
    print(str[0:2] == "ab")
    import sys
    a = sys.maxsize













