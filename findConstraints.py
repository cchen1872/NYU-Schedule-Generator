from interval_tree import IntervalTree, TimeSlot

def sortKey(element):
    return element.credits + min(0.001 * len(element.times), 0.999)

def addCourseToTree(tree, new_course):
    num_successes = -1
    for k in range(len(new_course.times)):
        print("ADD")
        success = tree.add(new_course.times[k][0], new_course.times[k][1])
        tree.traverse()
        if not success:
            num_successes = k
            break

    if num_successes >= 0:
        for k in range(num_successes):
            print("REMOVE", new_course.times[k][0].strftime('%m/%d/%Y %H:%M'))
            tree.remove(new_course.times[k][0])
            tree.traverse()
    return num_successes == -1
def findConstraints(course_list):
    # course_list = [CourseNode(course_list[i].name, course_list[i].times, course_list[i].credits) for i in range(len(course_list))]
    course_list.sort(reverse=True, key=sortKey)

    tree = IntervalTree()
    for i in range(len(course_list)):
        for elem in course_list[i].times:
            tree.add(elem[0], elem[1])
        for j in range(i, len(course_list)):
            if course_list[i].name != course_list[j].name:
                success = addCourseToTree(tree, course_list[j])
                if not success:
                    course_list[i].constraints.add(j)
                    course_list[j].constraints.add(i)
                else:
                    for elem in course_list[j].times:
                        print("REMOVE", elem[0].strftime('%m/%d/%Y %H:%M'))
                        tree.remove(elem[0])
                        tree.traverse()
            else:
                course_list[i].constraints.add(j)
                course_list[j].constraints.add(i)
            #     print(i, j, "SAME NAME")
            # print(i, course_list[i].constraints)
            # print(j, course_list[j].constraints)
        for elem in course_list[i].times:
            print("REMOVE", elem[0].strftime('%m/%d/%Y %H:%M'))
            tree.remove(elem[0])
            tree.traverse()
    # for i in course_list:
    #     print(i.constraints)
