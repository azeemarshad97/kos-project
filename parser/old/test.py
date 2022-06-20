from modules.pipeline_module import *


# New class
# creating parent class
class Parent:
    BloodGroup = 'A'
    Gender = 'Male'
    Hobby = 'Chess'


# creating child class
class Child(Parent):
    BloodGroup = 'A+'
    Gender = 'Female'

# onto = get_ontology_from_file("ontology_v3.owl")


# program to create class dynamically
  
# constructor
def constructor(self, arg):
    self.constructor_arg = arg


# method
def displayMethod(self, arg):
    print(arg)


# class method
@classmethod
def classMethod(cls, arg):
    print(arg)


# creating class dynamically
Geeks = type("Geeks", (Parent, ), {
    # constructor
    "__init__": constructor,
    # data members
    "string_attribute": "Geeks 4 geeks !",
    "int_attribute": 1706256,
    # member functions
    "func_arg": displayMethod,
    "class_func": classMethod
})

# creating objects
obj = Geeks("constructor argument")
# print(obj.constructor_arg)
# print(obj.string_attribute)
# print(obj.int_attribute)
# obj.func_arg("Geeks for Geeks")
# Geeks.class_func("Class Dynamically Created !")
# print(obj)
# get_object_callables(obj)




c1 = Child()

# print(c1)
# get_object_callables(c1)
print(type(c1).__bases__)
print(type(obj).__bases__)
