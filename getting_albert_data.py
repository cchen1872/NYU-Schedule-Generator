import requests
response = requests.get(f"https://schedge.a1liu.com/2022/fa/search?query=computer+architecture%20&full=true&school=uy&subject=cs")
for elem in response.json():
    print(elem["name"])
response.close()



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