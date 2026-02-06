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

def student_info(**data):
    print("\n--- Student Details ---")
    print("Data type of argument:", type(data))  # It will be a dict
    
    # Iterate through the dictionary items
    for key, value in data.items():
        print(f"{key}: {value}")

# Calling the function with keyword arguments
student_info(name="Alice", age=20, course="Physics", grade="A")
student_info(name="Bob", country="USA")

def greet(name, msg="Good morning"):
    print(f"Hello {name}, {msg}!")

greet("John")             # Uses default message
greet("Sarah", "Welcome") # Overwrites default message


numbers = [1, 2, 3, 4, 5, 6]

# MAP: Square every number in the list
# Syntax: map(function, list)
squared_numbers = list(map(lambda x: x**2, numbers))
print("Squared numbers:", squared_numbers)

# FILTER: Get only even numbers
# Syntax: filter(function, list)
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", even_numbers)

print("\n--- Grade Calculator ---")
while True:
    try:
        user_input = input("Enter marks for Maths, Phy, Chem (separated by comma) or 'q' to quit: ")
        
        if user_input.lower() == 'q':
            print("Exiting program.")
            break
        
        # Using list comprehension to convert string input to integers
        # '10,20,30' -> ['10', '20', '30'] -> [10, 20, 30]
        marks = [float(x) for x in user_input.split(',')]
        
        if len(marks) != 3:
            print("Error: Please enter exactly 3 marks.")
            continue
            
        # Calculate average
        avg = sum(marks) / len(marks)
        print(f"Average marks: {avg:.2f}") # .2f rounds to 2 decimal places

    except ValueError:
        print("Invalid input! Please enter numbers only (e.g., 80, 90, 75).")
        
import random

print("\n--- Random Module ---")

# Generate a random integer between 1 and 100
lucky_num = random.randint(1, 100)
print(f"Your lucky number today is: {lucky_num}")

# Pick a random item from a list
fruits = ["Apple", "Banana", "Cherry", "Date"]
choice = random.choice(fruits)
print(f"I picked a fruit for you: {choice}")

# Shuffle a list (like a deck of cards)
deck = [1, 2, 3, 4, 5]
random.shuffle(deck)
print(f"Shuffled deck: {deck}")        
        