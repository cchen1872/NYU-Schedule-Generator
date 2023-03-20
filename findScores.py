import datetime

def findCourseScore(course):
    score = 1
    for section in course.times:
        curr_gap = (section[0] - datetime.datetime(1,1,1,12,tzinfo=datetime.timezone.utc)) % datetime.timedelta(days=1)
        if curr_gap > datetime.timedelta(minutes=30):
            score /= (curr_gap / datetime.timedelta(minutes=30))
    return score

def findScores(course_list):
    for elem in course_list:
        elem.score = findCourseScore(elem)

def updateScore(curr_score, new_course):
    return curr_score / new_course.score