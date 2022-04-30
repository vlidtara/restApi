import itertools as iter

items = [
    {
        "name": "test",
        "price": 3.33
    }
]

from users import Users

test_list = [
    Users(2,"ssss","eeeeee"),
    Users(3,"bob","3000")
]

for i in test_list:
    print(i.id, i)
a = iter.takewhile(lambda x : x["name"] == "test", items)
print(next(a))

# l2 = [2]

# if l2:
#     print("list is not empty")
# else:
#     print("list is empty")