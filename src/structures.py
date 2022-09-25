


from typing import List

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

    keys = { '}':'{',']':'[',')':'('}

    for i in input:
        if i in keys:
            if len(stack) == 0:
                return False
            if stack[-1] != keys[i]:
                return False
            stack.pop()
        else:
            stack.append(i)
    
    return len(stack) == 0

def canAttendMeetings2(intervals: List[List[int]]) -> bool:
    
    intervals.sort(key=lambda x:x[0])
    
    for i in range(1, len(intervals)): 
        curr = intervals[i]
        prev = intervals[i-1]
        
        if curr[0] < prev[1]: 
            return False
        
    return True 

def canAttendMeetings2(intervals: List[List[int]]) -> bool:

    intervals.sort(key = lambda x: x[0])

    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i-1][1]:
            return False
    return True

def canAttendMeetings(intervals: List[List[int]]) -> bool:

    intervals.sort(key=lambda x: x[0])

    for i in range(1, len(intervals)):
        prev_end = intervals[i-1][1]
        curr_start = intervals[i][0]

    

        if prev_end > curr_start:
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

def heap() -> List[int]:

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


def capital_case(x):
    return x.capitalize()