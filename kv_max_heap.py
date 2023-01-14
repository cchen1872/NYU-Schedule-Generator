import math

class KVMaxHeap:
    def __init__(self):
        self.arr = [None]
    def add(self, key, val):
        idx = len(self.arr)
        self.arr.append((key, val))
        while idx > 1 and self.arr[idx][0] > self.arr[idx // 2][0]:
            self.arr[idx], self.arr[idx // 2] = self.arr[idx // 2], self.arr[idx]
            idx //= 2
    def extractMax(self):
        res = self.arr[1]
        self.arr[1] = self.arr[-1]
        self.arr.pop()
        
        idx = 1
        while 2 * idx < len(self.arr):
            curr = self.arr[idx][0]
            left = self.arr[2 * idx][0]
            if 2 * idx + 1 == len(self.arr):
                right = -math.inf
            else:
                right = self.arr[2 * idx + 1][0]
            
            if left >= right:
                if left > curr:
                    self.arr[idx], self.arr[2 * idx] = self.arr[2 * idx], self.arr[idx]
                    idx *= 2
                else:
                    break
            elif right > curr:
                new_idx = 2 * idx + 1
                self.arr[idx], self.arr[new_idx] = self.arr[new_idx], self.arr[idx]
                idx = new_idx
            else:
                break
        return res
    def isEmpty(self):
        return len(self.arr) == 1

    def len(self):
        return len(self.arr) - 1

    def getMaxKey(self):
        # print(self.arr)
        return self.arr[1][0]