# TODO: faire un remplacement "\(,\)\(<\/[^>]\+>\) -> \2\1"
# TODO: faire un remplacement "\(<\/[^>]\+>\) \([^,]\) -> \2,\1"

def final_format(text):
    return text.replace(" >", ">").replace("\n","").replace("\xa0"," ").replace("</em >","<em>")

def text_format(line):
    return line.replace(" >", ">").replace("\n","").replace("\xa0"," ").replace("</em >","<em>")

def isOpenParagraphOnly(line):
    return (line.count("<p>") > 0 and line.count("</p>") == 0)

def isCloseParagraphOnly(line):
    return (line.count("<p>") == 0 and line.count("</p>") > 0)

def isNoParagraph(line):
    return (line.count("<p>") == 0 and line.count("</p>") == 0)

def joinTilNextCloseParagraph(text, linenumber):
    i = linenumber+1
    while(i < len(text)):
        if isCloseParagraphOnly(text[i]):
            return text_format(" ".join(text[linenumber:i+1]))
        i += 1

def concatParagraph(text):
    res = []
    for linenumber, line in enumerate(text):
        if isOpenParagraphOnly(line):
            res.append(joinTilNextCloseParagraph(text, linenumber))
        elif isCloseParagraphOnly(line) or isNoParagraph(line):
            pass
        else:
            res.append(line)
    return res

def open_and_format(file_name):
    """This function will recieve a file name and will open it. Then it will perform a formattage and get the text back"""
    f = open(file_name)
    res = ""
    for line in f.readlines():
       res += text_format(line) 
    return final_format(res)

def open_and_format2(file_name):
    """This function will recieve a file name and will open it. Then it will perform a formattage and get the text back"""
    f = open(file_name)
    res = []
    for line in f.readlines():
       res.append(text_format(line))
    return res

# def open_and_format3(file_name):
    # """This function will recieve a file name and will open it. Then it will perform a formattage and get the text back"""
    # f = open(file_name, "r")
    # text = concatParagraph(f.readlines())
    # f2 = open("exp2.html", "w")
    # for line in text:
       # f2.write(text_format(line)+"\n")

# open_and_format3("exp.html")
