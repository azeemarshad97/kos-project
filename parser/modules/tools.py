def treduce(tab, init, func):
    for el in tab:
        init = func(init, el)
    return init


def tplus(a, b):
    return a+b


def tparselist(tab):
    res = None
    if len(tab) == 1:   # ['el']
        res = [tab[0]]
    elif len(tab) == 2:  # ['el', ',']
        res = [tab[0]]
    else:
        res = [tab[0]]+tab[2]
    return res


def ttolist(element):
    res = None
    if not isinstance(element, list):
        res = [element]
    else:
        res = element
    return res


def tcreateTriplet(res):
    '''this function will create triplets with just the data structure obtained after the parsing'''
    triplets = []
    first = res.pop(0) 
    triplets.append([first[0],"type",first[1]])
    for element in res:
        if element[1] not in ["voir aussi", "voir"]:
            triplets.append([first[0],element[1],element[0]])
            triplets.append([element[0], "type", element[1]])
        else:
            for content in element[0]:
                triplets.append([first[0],element[1],content[0]])
                triplets.append([content[0],"type",content[1]])
    return triplets
    # displayNetwork(triplets)


def twriteContent(demof, textln, res):
    '''will write the content in the html demo file'''
    demof.write(textln+"\n")
    for element in res:
        demof.write(str(element)+"<br>")


def twriteRDFHeader(f):
    f.write("""
@prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:   <http://www.w3.org/2000/01/rdf-schema#> .
@prefix :   <http://example.org/> .

""")


def tfromLinkToRDFAttribut(link):
    res = link
    if link == "type":
        res = "rdfs:type"
    return res


def tfromTripletToRDFs(triplets):
    '''Take a list of triplets (format: ["subject","link","goal"]) and modify them'''
    f = open("index.rdf","w")
    # create header
    twriteRDFHeader(f)
    for triplet in triplets:
        triplet[0] = ":"+triplet[0]
        triplet[2] = ":"+triplet[2]
        triplet[1] = tfromLinkToRDFAttribut(triplet[1])
        RDFTriplet = triplet[0]+" "+triplet[1]+" "+triplet[2]+"\n"
        f.write(RDFTriplet)

