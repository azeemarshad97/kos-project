from parsemodules.parser import *
from parsemodules.location_parser import *


def get_value(element):
    return element[0]


def get_type(element):
    return element[1]


def get_object_callables(obj):
    for callable_element in dir(obj):
        if callable_element[:1] != "_":
            print(callable_element)


def change_extension(file_name, new_extention):
    # remove old extention
    file_name_without_extention = file_name[:file_name.rfind(".")+1]
    # concat the new extention
    new_name = file_name_without_extention+new_extention
    return new_name


def containsH5(line):
    if "</h5>" in line:
        return True
    else:
        return False


def develop(elements):
    res = []
    if len(elements) == 2 and isinstance(elements[1], str):
        elements = [elements]
    for element in elements:
        if element[1] == "persons":
            for el in element[0]:
                res.append(el)
        else:
            res.append(element)
    return res


def createTriplet(res):
    triplets = []
    first = res.pop(0)
    first_value = get_value(first)
    triplets.append([first_value, "type", get_type(first)])
    for element in res:
        triplets.append([first_value, get_type(element), get_value(element)])
    return triplets
