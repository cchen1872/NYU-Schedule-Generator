from getCourseDetails import getCourseDetails
from findConstraints import findConstraints, addCourseToTree
from getting_albert_data import CourseNode, getCourseData, getValidCourseCombos, check
from interval_tree import TimeSlot, IntervalTree
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

# def formatCorequisites(coreq_graph, curr, visited):

def getCourseList(username='cc6956'):
    term = "sp2023"
    course_details = getCourseDetails(username)
    # course_details = [("Machine Design", "UY", "ME")]
    time_conflicts = [(datetime.datetime(2023, 1, 23, 22, 30, tzinfo=datetime.timezone.utc),datetime.datetime(2023, 1,23, 23, 00, tzinfo=datetime.timezone.utc))]
    course_data = []
    
    for name, school, subject in course_details:
        print(name)
        course_data.append(getCourseData(name, term, school, subject))
    print(course_data)
    print("LEN COURSE DATA", len(course_data[0][0]))
    tree = IntervalTree()
    for start, end in time_conflicts:
        tree.add(start, end)
    # corequisites = {}
    # for _, _, _, curr_coreq in course_details:
    #     if curr_coreq is not None:
    #         corequisites[]
    course_names = set()
    for i in range(len(course_data)):
        for j in range(len(course_data[i])):
            idx = 0
            while idx < len(course_data[i][j]):
                success = addCourseToTree(tree, course_data[i][j][idx])
                if not success:
                    course_data[i][j][idx] = course_data[i][j][-1]
                    course_data[i][j].pop()
                else:
                    for start, _ in course_data[i][j][idx].times:
                        tree.remove(start)
                    idx += 1

    print("LEN COURSE DATA", len(course_data[0][0]))

    ### IMPORTANT COREQ ALGORITHM PLANS
    ### FIND ALL CYCLES USING DFS
    ### IF CYCLE PART OF BIGGER ACYCLIC GRAPH
    ### IF NODE HAS EDGE OUT OF CYCLE,
    ### REMOVE EDGE FROM SAID 'EXIT' NODE TO THE NEXT NODE IN CYCLE TO MAKE IT DAG
    ### IF NODE HAS EDGE INTO CYCLE
    ### REMOVE CYCLIC EDGE GOING INTO 'ENTRANCE NODE' FROM ITS CYCLIC PARENT
    ### THEN RUN TOPOLOGICAL SORT TO FIND ALL CLUMPS OF COREQUISITE COURSE NAMES

    res = []
    # print(course_data[2][0][0].name)
    for i in range(len(course_data)):
        print('f',i)
        # print(i, course_data[i][0][0].name, len(course_data[i][0]))
        if len(course_data[i]) > 1:
            getValidCourseCombos(course_data[i], res)
        elif len(course_data[i]) == 1:
            res.extend(course_data[i][0])
        print("RES", res)

    # for elem in res:
    #     print([(slot[0].strftime('%m/%d/%Y %H:%M'), slot[1].strftime('%m/%d/%Y %H:%M')) for slot in elem.times])
    
    # for x in course_data:
    #     for i in x:
    #         for elem in i:
    #             print([(slot[0].strftime('%m/%d/%Y %H:%M'), slot[1].strftime('%m/%d/%Y %H:%M')) for slot in elem.times])
    #         print("_________________")
    # print([x.name for x in res])
    
        

    return res


def main():
    ##GRAB COURSES FROM DATABASE
    ##MUST CHANGE
    ##MUST CHANGE
    ##MUST CHANGE
    course_list = getCourseList()
    findConstraints(course_list)
    print(len(course_list))
    for elem in course_list:
        print(elem.name, elem.constraints,)
        for sect in elem.times:
            print(sect[0].strftime('%m/%d/%Y %H:%M'), sect[1].strftime('%m/%d/%Y %H:%M'))
    findScores(course_list)
    best_courses = findTenBest(course_list)
    res = []
    while not best_courses.isEmpty():
        res.append(best_courses.extractMax())
    for score, elem in res:
        print(score, elem)
        curr = []
        for sect in elem:
            curr.extend(course_list[sect].reg_numbers)
        # print(elem)
        check(','.join(curr))
    # display_courses(best_courses)

def findTenBest(course_list):
    frontier = KVMaxHeap()
    result = KVMaxHeap()
    explored = set()

    for i in range(10):
        result.add(0,None)
    for i in range(len(course_list)):
        key = course_list[i].credits - course_list[i].score
        # print("CONSTRAINTS", i, course_list[i].constraints)
        new_node = ScheduleNode({i}, copy.deepcopy(course_list[i].constraints), course_list[i].credits, course_list[i].score)
        frontier.add(key, new_node)
        if -key < result.getMaxKey():
            result.extractMax()
            result.add(-key, {i})
    
    # print("FRONTIER", frontier.arr)

    while not frontier.isEmpty():
        # print(result.arr)
        # print("FRONTIER", len(frontier.arr))
        top = frontier.extractMax()

        explored.add(tuple(top[1].courses))
        # print("EXPLORED", top[1].courses, top[1].constraints, explored, tuple(top[1].courses))
        for i in range(len(course_list)):
            if i not in top[1].constraints:
                
                course_credits = top[1].credits + course_list[i].credits
                courses = top[1].courses.union({i})
                if course_credits <= 18 and tuple(courses) not in explored:
                    constraints = top[1].constraints.union(course_list[i].constraints)
                    score = min(course_list[i].score, top[1].score) / max(course_list[i].score, top[1].score) 
                    key = course_credits - score
                    frontier.add(key, ScheduleNode(courses, constraints, course_credits, score))
                    # print("PAIR", top[1].courses, i, course_credits, score, key, result.getMaxKey())
                    if -key < result.getMaxKey():
                        result.extractMax()
                        result.add(-key, courses)
    return result
                



main()
