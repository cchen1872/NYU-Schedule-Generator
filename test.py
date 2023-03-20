from interval_tree import IntervalTree
import datetime

tree = IntervalTree()
tree.add(datetime.datetime(2023, 1,16,10,0), datetime.datetime(2023, 1,16,11,50))
print(tree.add(datetime.datetime(2023, 1,16,10,0), datetime.datetime(2023, 1,16,11,50)))