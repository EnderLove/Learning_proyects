import math

def square(n):

    square_side = int(math.sqrt(n))
    for i in range (square_side):
        print ("# " * square_side)

def rectangle(a, b):
    for i in range (a):
        print("# " * b)

def main():

    loop = 0

    while loop == 0:
        draw = input("What you want to draw?\n a) Square\n b) Rectangle\n")
        if draw == "a":
            n = int(input("Square Area = "))
            square(n)
        elif draw == "b":
            b = int(input("b side = "))
            a = int(input("a side = "))
            rectangle(a, b)
    
        loop = int(input("want to draw another shape? 0/1"))

main()