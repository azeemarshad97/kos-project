from pyvis.network import Network
# from pyvis.options import Options
import random
import csv

IMAGES = {}


def getImages():
    try:
        with open("logo.csv") as f:
            reader = csv.reader(f)
            tab = list(reader)
        for t in tab:
            IMAGES[t[0]] = t[1]
    except:
        pass


def getRandomColor():
    random_number = random.randint(0, 16777215)
    hex_number = str(hex(random_number))
    hex_number = '#'+hex_number[2:]
    return hex_number


def getColumn(num, mylist):
    return [x[num] for x in mylist]


def unique(mylist):
    return list(set(mylist))


def addNodes(net, facts):
    nodeList = unique(getColumn(0, facts)+getColumn(2, facts))
    for n in nodeList:
        default = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2Fd%2Fd5%2FRond_bleu_ciel.png%2F120px-Rond_bleu_ciel.png&f=1&nofb=1"
        link = IMAGES.get(n, default)
        net.add_node(n, shape="image", image=link)


def addEdges(net, facts):
    # on crée un dictionnaire qui assignera à chaque type de noeud une couleur
    d = {}
    uniqueLinks = unique(getColumn(1, facts))
    for u in uniqueLinks:
        d[u] = getRandomColor()
    for f in facts:
        net.add_edge(f[0], f[2], label=f[1], color=d[f[1]])


def displayNetwork(tab):
    getImages()
    net = Network(
            bgcolor='#FFFFFF',
            font_color='#000000',
            height='100%',
            width='100%',
            directed=True)
    addNodes(net, tab)
    addEdges(net, tab)

    net.set_options('{ "manipulation": { "enabled": true }, "physics": { "enabled": true }, "interaction": { "multiselect": true, "navigationButtons": true }, "configure": { "enabled": true, "filter": "layout,physics", "showButton": true }, "edges": { "smooth": { "enabled": false } } }')
    net.show("network.html")
