import requests
response = requests.get(f"https://nyu.a1liu.com/api/campus")
res = []
for elem in response.json()['campuses']:
    TF = input(elem)
    if TF != "":
        res.append(elem)

print(res)