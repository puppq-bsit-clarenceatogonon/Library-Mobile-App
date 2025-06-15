# syntax

# class class_name:
#     def __init__(self,a1,a2):
#         self.a1 = a1
#         self.a2 = a2
#
# a1 = input()
# a2 = input()
#
# identifier = class_name(a1, a2)

# class Person:
#     def __init__(self, name):
#         self.name = name
#         #print(f"{self.name} is created")
#     def introduce(self):
#         print(f"I am {self.name}")

# name = input("Enter your name: ")
# person_one = Person(name)

# p_one = Person("Jordan")
# p_two = Person("Clarkson")
# p_three = Person("Tejada")

list_of_people = []

# for i in range(5):
#     name = input("Enter name: ")
#     p = Person(name)
#     list_of_people.append(p)


# for person in list_of_people:
#     person.introduce()

# list_of_people = [p_one, p_two, p_three]

# for person in list_of_people:
#     print(f"I am {person.name}")


class Student:
    def __init__(self, name, course, year, section):
        self.name = name
        self.course = course
        self.year = year
        self.section = section

    def introduce(self):
        print(f"Hi, I am {self.name} taking {self.course}, from {self.year} section {self.section}")

list_of_students = []

print("Type 'done' to exit the loop.")
while True:
    name = input("Enter name: ")
    if name.lower() == "done":
        break  # exits the loop immediately

    course = input("Enter course: ")
    year = input("Enter year: ")
    section = input("Enter section: ")

    student = Student(name, course, year, section)
    list_of_students.append(student)

print("\nStudent Introductions:")
for person in list_of_students:
    person.introduce()