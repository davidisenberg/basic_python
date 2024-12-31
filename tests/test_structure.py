import pytest
import sys

sys.path.insert(0, '../src')
from structures import capital_case, movingAverage, ocean_view, valid_parens, canAttendMeetings, \
                       heap, islands, search, queue, TreeNode, DiameterCalc, in_order_traversal, merge, merge_sort, two_sum, max_profit
from typing import Optional, List


@pytest.mark.parametrize("input,expected", [
    ("[()]", True),
    ("}{", False),
    ("())", False),
    ("[]{}()", True),
    ("()[", False),
    ("(})[]", False)
])

def test_parens(input, expected):
    assert  valid_parens(input) == expected  

@pytest.mark.parametrize("intervals_start_end,expected", [
    ([[1,3],[2,4]], False),
    ([[3,5],[1,3]], True)
])

def test_meeting_rooms(intervals_start_end, expected):
    assert  canAttendMeetings(intervals_start_end) == expected  

@pytest.mark.parametrize("list, num, expected", [
    ([1,2,3,4,5,6],2, [1.5,2.5,3.5,4.5,5.5]),
    ([1,2,3,4,5,6],3, [2,3,4,5])
])

def test_moving_average(list, num, expected):
    assert movingAverage(list, num) == expected

def test_heap():
    assert heap() == [1,1,2,3,[5,7,8]]

def test_queue():
    assert queue() == [1,2,3]

def test_capital_case():
    assert capital_case('semaphore') == 'Semaphore'

@pytest.mark.parametrize("world,num_islands", [
    ([  [ 1, 0, 0, 0],
        [ 1, 1, 0, 1],
        [ 0, 1, 0, 1],
        [ 1, 0, 1, 0]], 4),
    ([  [ 1, 0, 0, 0],
        [ 1, 1, 0, 1],
        [ 0, 1, 1, 1],
        [ 1, 0, 0, 0]],2)
])

def test_islands(world, num_islands):
    # world = [[ 1, 0, 0, 0],
    #          [ 1, 1, 0, 1],
    #          [ 0, 1, 0, 1],
    #          [ 1, 0, 1, 0]]
    assert islands(world) == num_islands


@pytest.mark.parametrize("search_list,search_val, search_expected", [
    ([0, 4, 7 , 9], 4, 1),
    ([0, 4, 7, 9], 0, 0),
    ([0, 4, 7, 9], 9, 3),
    ([0, 4, 7, 9], 7, 2),
    ([0, 4, 7, 9], 8, -1),
    ([0, 4, 7, 9], 10, -1)
])

def test_search(search_list, search_val, search_expected):
    assert search(search_list, search_val) == search_expected

def create_tree() -> Optional[TreeNode]:

    #       
    #           7
    #       5           10
    #   3          8         12
    #                 9
    three_node = TreeNode(3, None, None)    
    five_node = TreeNode(5, three_node, None)
    nine_node = TreeNode(9,None, None )
    eight_node = TreeNode(8,None, nine_node )
    twelve_node = TreeNode(12,None, None )
    ten_node = TreeNode(10,eight_node, twelve_node)
    seven_node = TreeNode(7, five_node, ten_node)
    return seven_node


def test_diameter_tree() -> int:
    root = create_tree()
    assert DiameterCalc().diameterOfBinaryTree(root) == 5

def test_inorder() -> List[int]:
    root = create_tree()
    assert in_order_traversal(root) == [3,5,7,8,9,10,12]

@pytest.mark.parametrize("heights,views", [
    ([4, 3, 2 , 1], [0,1,2,3]),
    ([1, 2, 3, 4], [0,1,2,3]),
    ([3, 2, 1, 2, 3], [0,4]),
    ([3, 2, 5, 2, 3], [0,2,4])
])

def test_view(heights, views):
    assert ocean_view(heights) == views
    

@pytest.mark.parametrize("listA, listB , merged", [
    ([0, 2],[1,3], [0,1,2,3]),
    ([0, 2,4],[1,3], [0,1,2,3,4]),
    ([7],[1,3, 10], [1,3,7,10]),
    ([],[1,3,10], [1,3,10]),
    ([4],[], [4]),
    ([],[], []),
    ([1,2,3],[4,5,6], [1,2,3,4,5,6]),
    ([4,5,6],[1,2,3], [1,2,3,4,5,6]),

])

def test_merge(listA, listB, merged):
    assert merge(listA, listB) == merged

@pytest.mark.parametrize("list, sorted", [
    ([6, 8,3,5], [3,5,6,8]),
    ([6, 8,3,5,7], [3,5,6,7,8]),
    ([2,1], [1,2]),
    ([5], [5]),
    ([], [])    

])

def test_merge_sort(list, sorted):
    assert merge_sort(list) == sorted


@pytest.mark.parametrize("list, target, twosumindices", [
    ([2,4,6,7,10],9, [0,3]),
    ([2,4,6,7,10],16, [2,4]),

])

def test_two_sum(list, target, twosumindices):
    assert two_sum(list, target) == twosumindices


@pytest.mark.parametrize("list, profit", [
    ([5,3,1,4,10,2,12],11),
    ([5,3,1,4,10,2],9),

])

def test_max_profit(list, profit):
    assert max_profit(list) == profit
