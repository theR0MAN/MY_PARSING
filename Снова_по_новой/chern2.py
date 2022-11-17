

z=[[1,15],[2,10],[3,20],[4,40],[5,100],[6,500],[7,100],[7,1000],[9,10],[10,5]]

# importing the collections library
# for deque operations
import collections

a=dict()
a["f"]=3

# declaring the deque
lenque=7
my_deque = collections.deque([],maxlen=lenque)


my_deque.append(2)
my_deque.append(3)
my_deque.append(4)
my_deque.append(5)
my_deque.append(6)


print("The deque after appending at left: ")
print(my_deque)

print(my_deque[len(my_deque)-1])
print(my_deque[0])

print(sum(my_deque))

# print(len(my_deque))

# for i in my_deque:
#     print(i)

