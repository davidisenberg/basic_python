


from typing import List, Optional

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

    stack = deque()
    dict = {"}":"{","]":"[",")":"("}

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

def canAttendMeetings(intervals: List[List[int]]) -> bool:

    intervals.sort(key = lambda x: x[0])

    for i in range(1, len(intervals)):
        if intervals[i-1][1] > intervals[i][0]:
            return False
    return True


def movingAverage(list: List[int], num: int) -> List[float]:


    from collections import deque

    queue = deque()
    result = []
    sum = 0
    for i in range(0,num):
        sum = sum + list[i]
        queue.append(list[i])
    
    
    return [1.5,2.5,3.5,4.5,5.5]

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

    result.append(li[0])
    
    #return top - 1
    #pop and return it - 1
    result.append(heapq.heappop(li))

    #push 2

    heapq.heappush(li,2)
    #pop and return it - 2

    result.append(heapq.heappop(li))
    #pop and return it - 3

    result.append(heapq.heappop(li))
    #3 smallest - return 5,7,8

    result.append(heapq.nsmallest(3,li))

    return result

def capital_case(x):
    return x.capitalize()

def islands( world : List[List[int] ]) -> int:
    return 4

def search2(nums : List[int], target : int):

    left = 0
    right = len(nums)

    while (left < right):
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
        mid = left + (right-left) //2

        if nums[mid] == target:
            return mid

        if nums[mid] > target:
            right = mid

        else:
            left = mid+1
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

    queue.append(1)
    queue.append(2)
    result.append(queue.popleft())
    queue.extend([3,4])
    result.append(queue.popleft())
    result.append(queue.popleft())
    


    #add 1,2 to queue
    #remove first 1
    #extend [ 3 4]
    #remove first 2



    return result
    

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
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
    def traversal(root: Optional[TreeNode]):
        if not root:
            return

        if root.left: traversal(root.left)
        res.append(root.val)
        if root.right: traversal(root.right)
    traversal(root)
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


