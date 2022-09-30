import json
# https://python-scripts.com/json#about-json
data = {
    "president": {
        "name": "Zaphod Beeblebrox",
        "species": "Betelgeusian"
    }
}

# with open("data_file.json", "w") as write_file:
#     json.dump(data, write_file)
#
json_string = json.dumps(data)
# print(json_string)

# json_string = json.dumps(data, indent=4)
# print(json_string)

# with open("data_file.json", "r") as read_file:
#     data2 = json.load(read_file)

# print(data)
# print(data2)
# d=dict(data)
# print(d,type(d))
#
# print(d["president"]["name"])

# json_string = """
# {
#     "researcher": {
#         "name": "Ford Prefect",
#         "species": "Betelgeusian",
#         "relatives": [
#             {
#                 "name": "Zaphod Beeblebrox",
#                 "species": "Betelgeusian"
#             }
#         ]
#     }
# }
# """
#
# data = json.loads(json_string)
# print(data)

d2='MOEX ROSN s 6 333.3 3127736446.0 179748.0 205949.0 2750.0 2549.0 20 333.45 55.0 333.5 32.0 333.55 169.0 333.6 31.0 333.65 180.0 333.7 96.0 333.75 176.0 333.8 312.0 333.85 82.0 333.9 199.0 333.95 172.0 334.0 1940.0 334.05 23.0 334.1 225.0 334.15 196.0 334.2 61.0 334.25 99.0 334.3 22.0 334.35 112.0 334.4 124.0 20 333.3 45.0 333.25 5.0 333.2 105.0 333.15 237.0 333.1 158.0 333.05 156.0 333.0 254.0 332.95 213.0 332.9 327.0 332.85 57.0 332.8 242.0 332.75 28.0 332.7 89.0 332.65 103.0 332.6 136.0 332.55 22.0 332.5 250.0 332.45 22.0 332.4 158.0 332.35 116.0 '

a=d2.split()
print(a)
asks=[]
bids=[]
# asks=(a,b for a,b )
ind=11
for i in range(int(a[10])):
    asks.append((float(a[ind]), float(a[ind + 1])))
    ind+=2
for i in range(int(a[ind])):
    bids.append((float(a[ind+1]), float(a[ind + 2])))
    ind+=2

ask=asks[0][0]
bid=bids[0][0]

asks=tuple(asks)
bids=tuple(bids)

print(asks)
print(bids)
print(ask)
print(bid)
dat=dict(i=a[1],p=a[0],l=float(a[4]),a=float(ask),b=float(bid),vl=float(a[5]),bvl=float(a[6]),avl=float(a[7]),kbo=int(float(a[8])),kao=int(float(a[9])), asks=asks,bids=bids)
print(dat)
print(a[10])
