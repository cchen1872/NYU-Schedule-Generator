from interval_tree import IntervalTree, TimeSlot

def sortKey(element):
    return element.credits + min(0.001 * len(element.times), 0.999)

def findConstraints(course_list):
    # course_list = [CourseNode(course_list[i].name, course_list[i].times, course_list[i].credits) for i in range(len(course_list))]
    course_list.sort(reverse=True, key=sortKey)

    tree = IntervalTree()
    for i in range(len(course_list)):
        for elem in course_list[i].times:
            tree.add(elem.start, elem.end)
        for j in range(i, len(course_list)):
            if course_list[i].name != course_list[j].name:
                num_successes = -1
                for k in range(len(course_list[j].times)):
                    success = tree.add(course_list[j].times[k].start, course_list[j].times[k].end)
                    if not success:
                        num_successes = k
                        break
                    else:
                        print(course_list[j].times[k].start)
                
                if num_successes >= 0:
                    course_list[i].constraints.add(j)
                    course_list[j].constraints.add(i)
                    print(course_list[i].times)
                    print(course_list[j].times)
                    for k in range(num_successes + 1):
                        print("REMOVE", course_list[j].times[k].start)
                        tree.traverse()
                        tree.remove(course_list[j].times[k].start)
                        print(i, j, "NOT SUCCESS")
                else:
                    for elem in course_list[j].times:
                        tree.remove(elem.start)
                        print(i, j, "SUCCESS")
            else:
                course_list[i].constraints.add(j)
                course_list[j].constraints.add(i)
                print(i, j, "SAME NAME")
            print(i, course_list[i].constraints)
            print(j, course_list[j].constraints)
        # for elem in course_list[i].times:
            # tree.remove(elem.start)
    for i in course_list:
        print(i.constraints)
