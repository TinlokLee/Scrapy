
from functools import wraps
import time
import threading

def deco(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        my_thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        my_thread.start()
    return wrap

@deco
def foo(x, y):
    t = 0
    while t < 3:
        t += 1
        print('x:{}, y:{}'.format(x, y))
        time.sleep(2)
foo(666, 999)


class User:
    ''' 属性监听 '''
    #q = [i for i in range(10000)]
    q = [1,2,3]
    def __init__(self):
        self.money = 100000
        self.name = 'lee'
    
    def __setattr__(self, name, value):
        if name == 'money' and value < 0:
            raise ValueError('money < 0')
        print('set %s to %s' % (name, value))
        object.__setattr__(self, name, value)
    
    def __getattribute__(self, name):
        print('get %s ' % name)
        return object.__getattribute__(self, name)
        
    def func(x, y):
        return x ** y

a = User()
print(User.__dict__)
print(a.__dict__)




# # x = 0.5
# # while x != 1.0:
# #     print(x)
# #     x += 0.1  #  BUG

# res = []
# for x in range(10):
#     res.append(x**2)
# print(res)
    



# import os
# def print_dir_content(sPath):
#     s_dir = os.path.abspath(sPath)
#     arr_file = [os.path.join(s_dir, s) for s in os.listdir(s_dir)]
#     arr = [s for s in arr_file if os.path.isfile(s)]
#     return arr


# def quick_sort(nd):
#     if nd == []: return []
#     else:
#         mid = nd[0]
#         less = quick_sort([i for i in nd[1:] if less < mid])
#         greter = quick_sort([i for i in nd[1:] if greter >= mid])
#     return less + [mid] + greter
# lst = []
# print(quick_sort(lst))

# def bu_sort(arr):


# def func():
#     lst = []
#     for i in range(5):
#         def bar(x, i=i):
#             return x*i
#         lst.append(bar)
#     return lst
# for m in func():
#     print(m(1))

# def func(items, num):
#     return zip(*[iter(items)]*num)
# print(func(range(9), 3))from functools import wraps

