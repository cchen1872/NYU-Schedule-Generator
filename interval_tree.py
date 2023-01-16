import copy
import datetime
BLACK = True
RED = False

class TimeSlot:
    def __init__(self, start, end):
        self.start = start # Time Object
        self.end = end # Time Object
        self.duration = end - start # TimeDelta Object

class IntervalTree:
    class RedBlackNode:
        def __init__(self, start, end, color = RED):
            self.ts = TimeSlot(start, end)
            self.left = None #RedBlackNode Object
            self.right = None #RedBlackNode Object
            self.parent = None #RedBlackNode Object
            self.latest = end #Maximum end time in subtree rooted at self
            self.color = color #Boolean (RED/BLACK)
        
        def rotateLeft(self, tree):
            L = self
            R = self.right
            if R is None:
                return L
            elif L.parent is None:
                tree.head = R
                R.parent = None 
            else:
                if L is L.parent.left:
                    L.parent.left = R
                else:
                    L.parent.right = R
                R.parent = L.parent

            #Remaking Connections
            L.right = R.left
            L.parent = R
            R.left = L

            #Updating Inteval Augmented Data
            R.latest = L.latest
            if L.right is not None:
                L.latest = max(L.ts.end, L.right.latest)
            else:
                L.latest = L.ts.end
            
            return R
        
        def rotateRight(self, tree):
            R = self
            L = self.left
            if L is None:
                return R
            elif R.parent is None:
                tree.head = L
                L.parent = None
            else:
                if R is R.parent.left:
                    R.parent.left = L
                else:
                    R.parent.right = L
                L.parent = R.parent
            
            #Remaking Connections
            R.left = L.right
            R.parent = L
            L.right = R

            #Updating Interval Augmented Data
            L.latest = R.latest
            if R.right is not None:
                R.latest = max(R.ts.end, R.right.latest)
            else:
                R.latest = R.ts.end
            
            return L

        def getRelatives(self):
            # Returns Orientation and parent, grandparent, and uncle of self
            # If no parent exists, returns a -1
            # If no grandparent exists, and self is left child, returns 0
            # If no grandparent exists, and self is right child, returns 1
            # If parent is left child and self is left child, returns 2
            # If parent is left child and self is right child, returns 3
            # If parent is right child and self is left child, returns 4
            # If parent is right child and self is right child, returns 5
            res = 0
            if self.parent is None:
                return -1, None, None, None

            if self is self.parent.right:
                res += 1
            
            if self.parent.parent is None:
                return res, self.parent, None, None

            if self.parent is self.parent.parent.left:
                res += 2
                uncle = self.parent.parent.right
            else:
                res += 4
                uncle = self.parent.parent.left
            
            return res, self.parent, self.parent.parent, uncle     

        def replace(self, other, tree):
            if self.parent is not None and self.parent is not other:
                if self is self.parent.left:
                    self.parent.left = None
                else:
                    self.parent.right = None

            if other.parent is None:
                tree.head = self
            elif other.parent is not self:
                if other is other.parent.left:
                    other.parent.left = self
                else:
                    other.parent.right = self

            color = self.color

            if other.left is not self:
                self.left = other.left
                if self.left is not None:
                    self.left.parent = self
            if other.right is not self:
                self.right = other.right
                if self.right is not None:
                    self.right.parent = self
            if other.parent is not self:
                self.parent = other.parent
            self.color = other.color
            self.latest = max(self.latest, other.latest)
            return color

        def findSmallest(self):
            curr = self
            while curr.left is not None:
                curr = curr.left
            return curr 
        
        def getChildrenColor(self):
            l = BLACK if self.left is None else self.left.color
            r = BLACK if self.left is None else self.right.color
            return l, r
        
        

                
    def __init__(self):
        self.head = None #RedBlackNode

    def add(self, start, end):
        if start >= end:
            return False
        new_node = self.RedBlackNode(start, end)

        #Interval Tree Overlap Checking and Implementation
        if self.head is None:
            self.head = new_node
            self.head.color = BLACK
            return True

        curr = self.head
        loop = True
        while curr is not None and loop:
            loop = False
            if (start < curr.ts.start and end > curr.ts.start) \
                or (end > curr.ts.end and start < curr.ts.end): 

                break
                
            elif end < curr.ts.start:
                if curr.left is None:
                    curr.left = new_node
                    new_node.parent = curr
                else:
                    curr = curr.left
                    loop = True

            elif curr.left is not None and start < curr.left.latest:
                break
            elif curr.right is None:
                curr.right = new_node
                new_node.parent = curr
            else:

                curr = curr.right
                loop = True
        
        if new_node.parent is None: #If there was a time conflict in the Interval Tree
            return False
        else:
            
            curr = new_node.parent
            while curr is not None:
                curr.latest = max(new_node.latest, curr.latest)
                curr = curr.parent

        #Maintaining Red-Black Tree
        curr = new_node
        loop = True
        # print("COLOR:", new_node.color)
        while loop and curr.parent is not None and curr.color == RED and curr.parent.color == RED:
            case, parent, grandparent, uncle = curr.getRelatives()
            loop = False
            # print("case:", case)
            if 0 <= case <= 1:
                curr.parent.color = BLACK
            elif uncle is not None and uncle.color == RED:
                parent.color = BLACK
                uncle.color = BLACK
                grandparent.color = RED
                curr = grandparent
                loop = True
            elif case <= 3:
                if case == 3:
                    parent.rotateLeft(self)
                    parent, curr = curr, parent

                grandparent.rotateRight(self)
                parent.color = BLACK
                grandparent.color = RED
                
            else:
                if case == 4:
                    parent.rotateRight(self)    
                    parent, curr = curr, parent
                
                grandparent.rotateLeft(self)
                parent.color = BLACK
                grandparent.color = RED

        self.head.color = BLACK
        return True
    
    def find(self, start):
        curr = self.head
        while curr is not None:
            if curr.ts.start < start:
                curr = curr.right
            elif curr.ts.start == start:
                return curr
            else:
                curr = curr.left
        return None


    def bstDelete(self, node):
        if node is None:
            return None
        if node.right is not None:
            target = node.right.findSmallest()
            res = self.bstDelete(target)
            leaf = target.parent
            dir = target is leaf.left
            color = target.replace(node, self)
            if res is None:
                return color, leaf, dir
            else:
                return res
        elif node.left is not None:
            color = node.left.replace(node, self)
            return color, node.left, True

    def redBlackJustify(self, color, parent, dir):
        sibling = None
        close = None
        far = None
        if parent is not None:
            if dir: 
                node = parent.left
                sibling = parent.right
                if sibling is not None:
                    close = sibling.left
                    far = sibling.right
                else:
                    close = None
            else:
                node = parent.right
                sibling = parent.left
                if sibling is not None:
                    close = sibling.right
                    far = sibling.left

        print(parent)

        if color == RED:
            if node is not None:
                node.color = BLACK
        elif far is not None and far.color == RED:
            if dir:
                parent.rotateLeft(self)
            else:
                parent.rotateRight(self)
            
            sibling.color = parent.color
            parent.color = BLACK
            far.color = BLACK

            parent = sibling
            dir = parent.parent is not None and parent is parent.parent.left
            if parent.color == BLACK:
                self.redBlackJustify(parent.color, parent.parent, dir)

        elif close is not None and close.color == RED:
            if not dir:
                sibling.rotateLeft(self)
            else:
                sibling.rotateRight(self)

            sibling.color = RED
            close.color = BLACK
            self.redBlackJustify(color, parent, dir)


        elif parent is not None and parent.color == RED:
            parent.color = BLACK
            sibling.color = RED
        elif sibling is not None and sibling.color == RED:
            if dir:
                parent.rotateLeft(self)
            else:
                parent.rotateRight(self)

            parent.color = RED
            sibling.color = BLACK
            self.redBlackJustify(color, parent, dir)
        elif parent is not None:
            sibling.color = RED

            dir = parent.parent is not None and parent is parent.parent.left
            self.redBlackJustify(parent.color, parent.parent, dir) 
        
    def correctLatest(self, node):
        if node.parent is not None and node.parent.right is node:
            node.parent.latest = node.parent.ts.end
            self.correctLatest(node.parent)

    def remove(self, start):
        target = self.find(start)
        self.correctLatest(target)
        tup = self.bstDelete(target)
        if tup is not None:
            color, parent, dir = tup
            self.redBlackJustify(color, parent, dir) 
        elif target is not None:
            if target.parent is not None:
                parent = target.parent
                if target is parent.left:
                    dir = True
                    parent.left = None
                else:
                    dir = False
                    parent.right = None
                self.redBlackJustify(target.color, parent, dir)
            else:
                self.head = None
        return target

    def traverse(self):
        def display(node):
            if node.left is not None:
                print('L')
                display(node.left)
            print("BLACK" if node.color else "RED", node.ts.start, node.ts.end)
            if node.right is not None:
                print('R')
                display(node.right)
        if self.head is not None:
            display(self.head)

# tree = IntervalTree()
# tree.add(16,17)
# tree.add(0,1)
# tree.add(-2,-1)
# tree.add(5,6)
# tree.add(22,23)
# tree.add(2,3)
# tree.add(7,8)
# # tree.add(26,27)

# tree.remove(22)

# # tree2 = copy.deepcopy(tree)
# # tree2.add(9,10)
# tree.traverse()
# # print("_____________________________")
# # tree2.traverse()


