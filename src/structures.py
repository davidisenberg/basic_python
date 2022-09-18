


from typing import List

def valid_parens(input: str) -> bool:
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

def canAttendMeetings2(intervals: List[List[int]]) -> bool:
    
    intervals.sort(key=lambda x:x[0])
    
    for i in range(1, len(intervals)): 
        curr = intervals[i]
        prev = intervals[i-1]
        
        if curr[0] < prev[1]: 
            return False
        
    return True 

def canAttendMeetings(intervals: List[List[int]]) -> bool:

    intervals.sort(key = lambda x: x[0])

    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i-1][1]:
            return False
    return True



def capital_case(x):
    return x.capitalize()