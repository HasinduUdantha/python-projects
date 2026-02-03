# # # def calAvg(a,b,c):
# # #     avg = (a + b + c) / 3
# # #     print("Average is:", avg)
    
# # # calAvg(10, 20, 30)        


# # def myFunc(*a):
# #     print(a)
# #     print("Type of a is:", type(a))
# #     b = sum(a)
# #     print("Sum is:", b)
    
# #     c=b / len(a)
# #     print("Average is:", c)
    
# # myFunc(10, 20, 30, 40, 50)    


# # def calculator(val1,val2):
    
# #     add= val1 + val2
# #     sub= val1 - val2
# #     mul= val1 * val2
# #     div= val1 / val2
    
# #     return add, sub, mul, div

# # val = calculator(100, 20)
# # print("Returned value is:", val)

# # a,b,c,d = calculator(10, 2)
# # print("Addition:", a)
# # print("Subtraction:", b)
# # print("Multiplication:", c)
# # print("Division:", d)



# # # Lambda function

# # # Syntax: lambda arguments: expression

# # def calAvg(a,b,c):
# #     avg = (a + b + c) / 3
# #     return avg

# # calAvgNew = lambda a,b,c: (a + b + c) / 3

# # val = calAvg(10, 20, 30)
# # print("Average using normal function is:", val)

# # valNew = calAvgNew(10, 20, 30)
# # print("Average using lambda function is:", valNew)


# # def calAvg(a,b,c):
# #     avg = (a + b + c) / 3
# #     print("Average using normal function is:", avg)
    
    
# # while True:    
# #     maths,phy,chem=eval(input("Enter marks of Maths, Physics and Chemistry: "))
# #     calAvg(maths,phy,chem)


# # import math # importing math module to code

# # val = math.sqrt(16) # calling the sqrt function in math module to calculate square root

# # print("Square root is:", val)    


# # import math as m # importing math module with an alias name

# # val = m.pow(2, 3) # calling the pow function in math module to calculate power

# # print("2 raised to power 3 is:", val)

# from math import sqrt, pow # importing specific functions from math module

# val1 = sqrt(25)
# val2 = pow(2, 4)    

# print("Square root of 25 is:", val1)
# print("2 raised to power 4 is:", val2)