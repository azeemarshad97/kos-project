# from tools import tcreateTriplet
from parsemodule.parser import *
from modules.network import *

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
    '''this function will create triplets with just the data structure obtained after the parsing'''
    res = develop(res)
    triplets = []
    first = res.pop(0) 
    triplets.append([first[0],"type",first[1]])
    for element in res:
        if element[1] not in ["voir aussi", "voir"]:
            triplets.append([first[0],":"+element[1],element[0]])
            triplets.append([element[0], "rdf:type", element[1]])
        else:
            for content in element[0]:
                content = develop(content)
                if len(content) == 1:
                    triplets.append([first[0],":"+element[1],content[0][0]])
                    triplets.append([content[0][0],"rdf:type",content[0][1]])
                else:
                    triplets.append([first[0],":"+element[1],content[0][0]])
                    triplets.append([content[0][0],"rdf:type",content[0][1]])
                    triplets.append([first[0],":"+element[1],content[1][0]])
                    triplets.append([content[1][0],"rdf:type",content[1][1]])
    return triplets
