import requests
import datetime
from pytz import timezone
from interval_tree import IntervalTree, TimeSlot
from findConstraints import addCourseToTree

START_TIME = datetime.datetime(year=1970, month=1, day=5, hour=0, minute=0, tzinfo=timezone('US/Eastern'))
DEFAULT_CAMPUSES = {'ePoly', 'Distance Learning/Synchronous', 'Distance Learning/Asynchronous', 'Distance Learning / Blended', 'Off Campus', 'Distance Ed (Learning Space)', 'Distance Education', 'Online'}

class CourseNode:
    def __init__(self, name, time_bounds, credits, registration_numbers, constraints = None, score = None):
        self.name = name
        self.reg_numbers = registration_numbers
        # print(type(time_bounds[0]))
        self.times = [(start, end) for start, end in time_bounds]
        self.credits = credits
        if constraints is None:
            self.constraints = set()
        else:
            self.constraints = constraints
        self.score = score

def check(string):
    response = requests.get(f"https://nyu.a1liu.com/generateSchedule/sp2023?registrationNumbers={string}")
    print(string)
    print(response.status_code)

def logSection(name, sect, sections, section_indicies, courses_added):
    curr_time_bounds = []
    for date in sect['meetings']:
        start = datetime.datetime.fromisoformat(date['beginDate'])
        duration = datetime.timedelta(minutes=date['minutesDuration'])
        
        start = datetime.datetime(year = START_TIME.year, month = START_TIME.month, day=START_TIME.day + start.weekday(), hour=start.hour, minute=start.minute, second=start.second, tzinfo=start.tzinfo)
        start = start.astimezone(tz=timezone('US/Eastern'))
        
        curr_time_bounds.append((start, start + duration))

    key = hash(tuple(curr_time_bounds))
    if key not in courses_added:
        courses_added.add(key)
        course = CourseNode(name, curr_time_bounds, sect['minUnits'], {str(sect['registrationNumber'])})
        if sect['type'] in section_indicies:
            sections[section_indicies[sect['type']]].add(course)
        else:
            section_indicies[sect['type']] = len(sections)
            sections.append({course})

def getTotalCoreqCredits(sections):
    names = set()
    total = 0
    for sect in sections:
        if sect[0].name not in names:
            total += sect[0].credits
            names.add(sect[0].name)
    return total

def getRegistrationNumbers(sections, combo_idxs):
    reg_numbers = set()
    for i in range(len(sections)):
        for num in sections[i][combo_idxs[i]].reg_numbers:
            reg_numbers.add(num)
    return reg_numbers

def getCourseData(name, semester, school, subject, campuses={"Brooklyn Campus", "ePoly"}):

    # print(f"https://nyu.a1liu.com/api/search/{semester}/?query={subject}-{school}+{name}")
    html_friendly_name = name.replace("&", "&amp")
    response = requests.get(f"https://nyu.a1liu.com/api/search/{semester}/?query={html_friendly_name} {subject}-{school}")
    # print(response.status_code)
    section_indicies = {}
    courses_added = set()
    sections = []
    print(response.json())
    for elem in response.json():
        course_name = elem['name']
        campus = elem['campus']
        # course_school = elem['school']
        # subject_code = elem['subjectCode'].lower()
        if course_name == name:
            for sect in elem['sections']:  
                if campus in campuses:   
                    logSection(course_name, sect, sections, section_indicies, courses_added)
                    if 'recitations' in sect:
                        for rec in sect['recitations']:
                            logSection(course_name, rec, sections, section_indicies, courses_added)

    response.close()
    # print([(hash(elem), hash(tuple(elem.times))) for elem in sections[1]])
    # print([[(x[0].strftime('%m/%d/%Y %H:%M'), x[1].strftime('%m/%d/%Y %H:%M')) for x in elem.times] for elem in sections[1]])
    sections = [list(sect) for sect in sections]  
    return sections

def getValidCourseCombos(sections, combo_sections = None):
    # if len(sections) == 0:
    #     return
    # elif len(sections) == 1:
    #     for elem in sections[0]:
    #         combo_sections.append(elem)
    #     return

    total_credits = getTotalCoreqCredits(sections)
    print('s', sections)
    name = sections[0][0].name
    if combo_sections is None:
        combo_sections = []
    combo_idxs = [0 for i in range(len(sections))]
    tree = IntervalTree()
    curr = 0
    while curr < len(sections):
        success = addCourseToTree(tree, sections[curr][combo_idxs[curr]])
        if success:
            print("Added ", combo_idxs[curr], " to ", curr)
            curr += 1
        else:
            combo_idxs[curr] += 1
            while combo_idxs[curr] == len(sections[curr]):
                combo_idxs[curr] = 0
                for sect in sections[curr][combo_idxs[curr]].times:
                    tree.remove(sect[0])
                curr -= 1
                combo_idxs[curr] += 1
                if curr == len(sections):
                    return None

    print(combo_idxs)
    curr = len(sections) - 1
    for sect in sections[curr][combo_idxs[curr]].times:
        tree.remove(sect[0])
    while curr >= 0:
        print(curr, combo_idxs)
        success = addCourseToTree(tree, sections[curr][combo_idxs[curr]])
        if success:
            print("ADD", curr, combo_idxs[curr])
            if curr == len(sections) - 1:
                curr_times = []
                for i in range(len(sections)):
                    for slot in sections[i][combo_idxs[i]].times:
                        curr_times.append((slot[0], slot[1]))
                curr_reg_numbers = getRegistrationNumbers(sections, combo_idxs)
                combo_sections.append(CourseNode(name, curr_times, total_credits, curr_reg_numbers))
                print("REMOVE", len(sections) - 1, combo_idxs[-1])
                for sect in sections[-1][combo_idxs[-1]].times:
                    print(sect[0].strftime('%m/%d/%Y %H:%M'))
                    tree.remove(sect[0])
                
                
            else:
                curr += 1

        combo_idxs[curr] += 1
        while combo_idxs[curr] == len(sections[curr]):
            print(curr)
            combo_idxs[curr] = -1
            print("REMOVE", curr, len(sections[curr]) - 1)
            for sect in sections[curr][-1].times:
                print(sect[0].strftime('%m/%d/%Y %H:%M'))
                tree.remove(sect[0])
            curr -= 1
            for sect in sections[curr][combo_idxs[curr]].times:
                print(sect[0].strftime('%m/%d/%Y %H:%M'))
                tree.remove(sect[0])
            tree.traverse()
            combo_idxs[curr] += 1
    return combo_sections
            
            
        


        
# getCourseData("Automatic Control", "sp2023", "uy", "me")

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