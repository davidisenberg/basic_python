


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
    keys = {"}":"{","]":"[",")":"("}

    for s in input:
        if s in keys:
            if len(stack)==0:
                return False
            if stack[-1] != keys[s]:
                return False
            stack.pop()
        else:
            stack.append(s)
    return len(stack)==0


def canAttendMeetings(intervals: List[List[int]]) -> bool:
    
    intervals.sort(key = lambda x: x[0])

    for i in range(1, len(intervals)):
        if intervals[i-1][1] > intervals[i][0]:
            return False
    return True

def canAttendMeetings2(intervals: List[List[int]]) -> bool:

    intervals.sort(key = lambda x: x[0])

    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i-1][1]:
            return False
    return True

def canAttendMeetings(intervals: List[List[int]]) -> bool:

    intervals.sort(key = lambda x: x[0])

    for i in range(1, len(intervals)):
        if(intervals[i-1][1] > intervals[i][0]):
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
    val = heapq.heappop(li)
    result.append(val)

    heapq.heappush(li,2)

    val = heapq.heappop(li)
    result.append(val)

    val = heapq.heappop(li)
    result.append(val)

    result.append(heapq.nsmallest(3,li))

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

    while left<right :
        mid = left + (right-left) // 2

        if(nums[mid] == target):
            return mid
        if(nums[mid] > target):
            right = mid
        else:
            left = mid + 1
        
    return -1
        
def queue() -> List[int]:
    from collections import deque
    result = []
    queue = deque()

    #add 1,2 to queue
    #remove first 1
    #extend [ 4 5]
    #remove first 2


    queue.append(1)
    queue.append(2)
    result.append(queue.popleft())
    queue.extend([3,4])
    result.append(queue.popleft())
    result.append(queue.popleft())

    return result
    

# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
# class Solution:
#     def rangeSumBST(self, root: Optional[TreeNode], low: int, high: int) -> int:
    