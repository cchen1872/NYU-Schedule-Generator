import requests
import datetime
from interval_tree import IntervalTree, TimeSlot

DATE_FORMAT = '%y-%m-%dT'

class CourseNode:
    def __init__(self, name, time_bounds, credits, registration_numbers, constraints = None, score = None):
        self.name = name
        self.reg_numbers = registration_numbers
        # print(type(time_bounds[0]))
        self.times = [TimeSlot(start, end) for start, end in time_bounds]
        self.credits = credits
        if constraints is None:
            self.constraints = set()
        else:
            self.constraints = constraints
        self.score = score

def logSection(name, sect, sections):
    curr_time_bounds = []
    for date in sect['meetings']:
        curr_time_bounds.append((datetime.datetime.fromisoformat(date['beginDate']), datetime.datetime.fromisoformat(date['beginDate']) + datetime.timedelta(minutes=date['minutesDuration'])))
    print(name, curr_time_bounds)
    course = CourseNode(name, curr_time_bounds, sect['minUnits'], {sect['registrationNumber']})
    if sect['type'] in sections:
        sections[sect['type']].append(course)
    else:
        sections[sect['type']] = [course]

def getCourseData(name, semester, school, subject):

    print(f"https://nyu.a1liu.com/api/search/{semester}/?query={subject}-{school}+{name}")
    response = requests.get(f"https://nyu.a1liu.com/api/search/{semester}/?query={subject}-{school}+{name}")
    print(response.status_code)
    tree = IntervalTree()
    sections = {}
    for elem in response.json():
        course_name = elem['name']
        print(course_name)
        for sect in elem['sections']:   
            logSection(course_name, sect, sections)
            if 'recitations' in sect:
                for rec in sect['recitations']:
                    logSection(course_name, rec, sections)
    print(sections)
    return sections
        
        
    response.close()

getCourseData("Automatic Control", "sp2023", "uy", "me")

# bound = 5
# idxs = [4,3,2,1,0]
# idx = 1
# nums = []
# # nums.append(1)
# total = 1
# print(idxs)
# while len(idxs) > 0:
    
#     nums.append(total)
    
#     if idx == bound:
#         if len(idxs) > 0:
#             idx = idxs.pop() + 1
#             total = max(0, total -  pow(2, idx - 1))
#             print("POP", idx)
#     else:
#         idxs.append(idx)
#         total += pow(2, idx)
#         idx += 1
#     print(idxs, idx, total)
# print(len(nums))
# print(nums)