import numpy as np
import pylab as plt
from matplotlib import animation

france = [['Yvoire ( F , dép. Haute-Savoie , arr. Thonon-les-Bains , ct. Sciez )', 'place'], ['Yvoy ( es ) re', 'place'], ['le seigneur de -', 'descriptions'], [[[['Saint-Jeoire ( de )', 'descriptions'], 'person']], 'voir']]

suisse = [['Appenzell , ( CH , ct. )', 'place'], ['Apensept', 'place']]



def place(element):
    place_parsed = []

    if '(' in element[0][0]:
        splited = element[0][0].split()
        place = [splited[0],"place"]
        place_parsed.append(place)

        if 'CH ,' in element[0][0]:
            place_parsed.append(["Suisse", "inCountry"])

            if 'ct.' in element[0][0]:

                # case where both canton and commun are Geneve
                if 'ct. et com.' in element[0][0]:
                    index = splited.index('com.')+1
                    resource_tmp = splited[index]
                    if resource_tmp != ')':
                        place_parsed.append([resource_tmp, "canton"])
                        place_parsed.append([resource_tmp, "common"])
                    if 'distr.' in element[0][0]:
                        index = splited.index('distr.') + 1
                        resource_tmp = splited[index]
                        if resource_tmp != ')':
                            place_parsed.append([resource_tmp, "district"])

                else:
                    index = splited.index('ct.')+1
                    resource_tmp = splited[index]
                    if resource_tmp != ')':
                        place_parsed.append([resource_tmp, "canton"])
                        if 'com.' in element[0][0]:
                            index = splited.index('com.') + 1
                            resource_tmp = splited[index]
                            if resource_tmp != ')':
                                place_parsed.append([resource_tmp, "common"])
                        if 'distr. et com.' in element[0][0]:
                            index = splited.index('com.') + 1
                            resource_tmp = splited[index]
                            if resource_tmp != ')':
                                place_parsed.append([resource_tmp, "district"])
                        elif 'distr.' in element[0][0]:
                            index = splited.index('distr.') + 1
                            resource_tmp = splited[index]
                            if resource_tmp != ')':
                                place_parsed.append([resource_tmp, "district"])
                            elif resource_tmp == ')':
                                place_parsed.append([splited[0], "district"])

                    elif resource_tmp == ')':
                        place_parsed.append([splited[0], "canton"])


        if 'F ,' in element[0][0]:
            place_parsed.append(["France", "inCountry"])

            if 'dép.' in element[0][0]:
                index = splited.index('dép.')+1
                resource_tmp = splited[index]
                place_parsed.append([resource_tmp, "inDépartement"])

        if 'I ,' in element[0][0]:
            place_parsed.append(["Italie", "inCountry"])

            if 'rég.' in element[0][0]:
                index = splited.index('rég.')+1
                resource_tmp = splited[index]
                place_parsed.append([resource_tmp, "inRégion"])

    place_parsed.append(element[1:])

    return place_parsed


print(place(france))

print(place(suisse))
