from findConstraints import findConstraints, CourseNode
from findScores import findScores
from kv_max_heap import KVMaxHeap
import copy
import datetime

class ScheduleNode:
    def __init__(self, courses, constraints, credits, score):
        self.courses = courses
        self.constraints = constraints
        self.credits = credits
        self.score = score


def getCourseList():
    res = []
    res.append(CourseNode("Comp Networking", [(datetime.datetime(2023, 1, 23, 17, 0, 0, 0), datetime.datetime(2023, 1, 23, 18, 20, 0, 0)), (datetime.datetime(2023, 1, 25, 17, 0, 0, 0), datetime.datetime(2023, 1, 25, 18, 20, 0, 0))], 3))
    res.append(CourseNode("Comp Networkin", [(datetime.datetime(2023, 1, 24, 17, 0, 0, 0), datetime.datetime(2023, 1, 24, 18, 20, 0, 0)), (datetime.datetime(2023, 1, 26, 17, 0, 0, 0), datetime.datetime(2023, 1, 26, 18, 20, 0, 0))], 3))
    res.append(CourseNode("Comp Networkin", [(datetime.datetime(2023, 1, 24, 17, 0, 0, 0), datetime.datetime(2023, 1, 24, 18, 20, 0, 0)), (datetime.datetime(2023, 1, 26, 17, 0, 0, 0), datetime.datetime(2023, 1, 26, 18, 20, 0, 0))], 3))
    return res
def main():
    ##GRAB COURSES FROM DATABASE
    ##MUST CHANGE
    ##MUST CHANGE
    ##MUST CHANGE
    course_list = getCourseList()
    findConstraints(course_list)
    for elem in course_list:
        print(elem.name, elem.constraints)
    findScores(course_list)
    best_courses = findTenBest(course_list)
    while not best_courses.isEmpty():
        print(best_courses.extractMax())
    # display_courses(best_courses)

def findTenBest(course_list):
    frontier = KVMaxHeap()
    result = KVMaxHeap()
    explored = set()

    for i in range(10):
        result.add(0,None)
    for i in range(len(course_list)):
        key = course_list[i].credits - course_list[i].score
        print("CONSTRAINTS", i, course_list[i].constraints)
        new_node = ScheduleNode({i}, copy.deepcopy(course_list[i].constraints), course_list[i].credits, course_list[i].score)
        frontier.add(key, new_node)
        if -key < result.getMaxKey():
            result.extractMax()
            result.add(-key, {i})
    
    print("FRONTIER", frontier.arr)

    while not frontier.isEmpty():
        print(result.arr)
        # print("FRONTIER", len(frontier.arr))
        top = frontier.extractMax()

        explored.add(tuple(top[1].courses))
        # print("EXPLORED", top[1].courses, top[1].constraints, explored, tuple(top[1].courses))
        for i in range(len(course_list)):
            if i not in top[1].constraints:
                # print("PAIR", top[1].courses, i)
                
                course_credits = top[1].credits + course_list[i].credits
                courses = top[1].courses.union({i})
                if course_credits <= 18 and tuple(courses) not in explored:
                    constraints = top[1].constraints.union(course_list[i].constraints)
                    score = top[1].score / course_list[i].score
                    key = course_credits - score
                    frontier.add(key, ScheduleNode(courses, constraints, course_credits, score))
                    if -key < result.getMaxKey():
                        result.extractMax()
                        result.add(-key, courses)
    return result
                



main()
