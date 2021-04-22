import time

#简单装饰器
def display_time(func): #func是要装饰的函数的形参
    def wrapper():
        t1 = time.time()
        func()
        t2 = time.time()
        print(t2-t1)
    return wrapper


def is_prime(num):
    if num < 2:
        return False
    elif num==2:
        return True
    else:
        for i in range(2,num):
            if num % i ==0:
                return False
        return True
@display_time
def prime_nums():
    for i in range(2,10001):
        if is_prime(i):
            print(i)
# prime_nums()


#可以返回值的装饰器
def display_time(func):
    def wrapper():
        t1 = time.time()
        result = func()
        t2 = time.time()
        print(t2-t1)
        return result
    return wrapper

def is_prime(num):
    if num < 2:
        return False
    elif num == 2:
        return True
    else:
        for i in range(2,num):
            if num % i ==0:
                return False
        return True
@display_time
def prime_nums_one():
    count = 0
    for i in range(2,10000):
        if is_prime(i):
            print(i)
            count += 1
    return count
# print(prime_nums_one())

#装饰器传递参数
def display_time(func):
    def wrapper(*args):
        t1 = time.time()
        result = func(*args)
        t2 = time.time()
        print(t2-t1)
        return result
    return wrapper

def is_prime(num):
    if num < 2:
        return False
    elif num == 2:
        return True
    else:
        for i in range(2,num):
            if num % i==0:
                return False
        return True

@display_time
def prime_nums_two(num):
    count = 0
    for i in range(2,num):
        if is_prime(i):
            print(i)
            count += 1
    return count

# print(prime_nums_two(10001))

import math
def func_get_prime(n):
  return filter(lambda x: not [x%i for i in range(2, int(math.sqrt(x))+1) if x%i ==0], range(2,n+1))
 
print (*func_get_prime(10000))