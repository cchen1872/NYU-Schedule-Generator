import requests
def getCourseDetails(username):
    response = requests.get(f'http://127.0.0.1:8000/courses/?username={username}')
    course_details = []
    for course in response.json():
        course_details.append((course['name'], course['school'], course['subject']))
    return course_details
