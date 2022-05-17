import sys
import subprocess
from modules.module import *

# prend le nom du fichier
name = sys.argv[1]
newname = name[:-4]+"html"

# conversion en html
subprocess.run(["pandoc", name, "-o", newname])

# conversion en triplets
text = open(newname, "r").readlines()

ignor = True
tab = []

for line in text:
    # first we ignor what's before the h5
    if containsH5(line):
        ignor = False
    else:
        if ignor == False and not containsH5(line):
            res = parser.parse(line)
            if res != None:
                tab.append(createTriplet(res))

print(tab)
