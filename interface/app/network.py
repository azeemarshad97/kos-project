from pyvis.network import Network
# from pyvis.options import Options
import random
import csv

IMAGES = {}


def getImages():
    """
    It opens the csv file, reads it, and puts the contents into a dictionary.
    """
    try:
        with open("logo.csv") as f:
            reader = csv.reader(f)
            tab = list(reader)
        for t in tab:
            IMAGES[t[0]] = t[1]
    except:
        pass


def getRandomColor():
    """
    It generates a random color in hexadecimal format.
    :return: A random color in hexadecimal format.
    """
    random_number = random.randint(0, 16777215)
    hex_number = str(hex(random_number))
    hex_number = '#'+hex_number[2:]
    return hex_number


def getColumn(num, mylist):
    """
    It takes a list of lists and returns a list of the values in the column specified by the second
    argument
    
    :param num: the column number you want to get
    :param mylist: the list of lists
    :return: A list of the values in the column of the list.
    """
    return [x[num] for x in mylist]


def unique(mylist):
    """
    It takes a list as input, converts it to a set, and then returns a list of the unique elements in
    the original list
    
    :param mylist: the list you want to make unique
    :return: A list of unique elements from the list mylist.
    """
    return list(set(mylist))


def addNodes(net, facts):
    """
    It takes a network and a list of facts, and adds nodes to the network for each unique node in the
    facts
    
    :param net: the networkx graph object
    :param facts: a list of lists, each sublist is a fact
    """
    nodeList = unique(getColumn(0, facts)+getColumn(2, facts))
    for n in nodeList:
        default = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2Fd%2Fd5%2FRond_bleu_ciel.png%2F120px-Rond_bleu_ciel.png&f=1&nofb=1"
        link = IMAGES.get(n, default)
        net.add_node(n, shape="image", image=link)


def addEdges(net, facts):
    """
    It adds edges to the network, and assigns a color to each edge type
    
    :param net: the networkx graph object
    :param facts: a list of facts, each fact being a list of 3 elements: the first element is the source
    node, the second element is the edge label, and the third element is the target node
    """
    # on crée un dictionnaire qui assignera à chaque type de noeud une couleur
    d = {}
    uniqueLinks = unique(getColumn(1, facts))
    for u in uniqueLinks:
        d[u] = getRandomColor()
    for f in facts:
        net.add_edge(f[0], f[2], label=f[1], color=d[f[1]])


def displayNetwork(tab):
    """
    It takes a dataframe as input, creates a network object, adds nodes and edges to the network object,
    and then returns the html code for the network.
    
    :param tab: a list of lists, each sublist is a list of nodes and edges
    :return: The html code for the network.
    """
    getImages()
    net = Network(
        bgcolor='#FFFFFF',
        font_color='#000000',
        height='100%',
        width='100%',
        directed=True)
    addNodes(net, tab)
    addEdges(net, tab)


    # net.set_options('{ "manipulation": { "enabled": true }, "physics": { "enabled": true }, "interaction": { "multiselect": true, "navigationButtons": true }, "configure": { "enabled": true, "filter": "layout,physics", "showButton": true }, "edges": { "smooth": { "enabled": true } } }')


    # net.show("network.html")

    # change node label color
    net.set_options("""
        const options = {

            "physics": {
            "barnesHut": {
                "theta": 0.45,
                "gravitationalConstant": -26850,
                "centralGravity": 0,
                "springConstant": 0.09,
                "damping": 0.77,
                "avoidOverlap": 1
            },

            "maxVelocity": 56,
            "minVelocity": 0.75
            },

            "edges": {
            "smooth": {
                "type": "dynamic",
                "forceDirection": "none",
                "roundness": 0.5
            }
            },
            "nodes": {
                "overlap": 0.01
            },
            "interaction": {
                 "multiselect": true,
                 "navigationButtons": true
            }   
    }
    
    """)

    # net.show_buttons(filter_=['physics', 'nodes','edges'])

    # net.write_html("app/templates/network.html")

    return net.generate_html()
