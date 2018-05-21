######################
# WCZYTYWANIE DANYCH #
######################


def read_file(text):
    text = open(text, 'r', encoding="utf8").read()
    lines = text.split('\n')
    return lines


def read_passengers(list, text):
    lines = text.split('\n')
    for l in lines:
        try:
            line = l.split(';')
            if not (line[2] == ""):
                list.append([line[1], line[2], int(line[3].replace(" ", "")), line[0]])
        except:
            pass
    return list


# liczba pasazerow per lotnisko (europa, ameryka, reszta swiata)
passengers = []
passengers.append(read_passengers(passengers, open('european-airports-2015.csv', 'r').read()))
passengers.append(read_passengers(passengers, open('american-airport-traffic-trends-2015.csv', 'r').read()))
passengers.append(read_passengers(passengers, open('row-airports-database-2015.csv', 'r').read()))


# miasta - polozenie i populacja
lines = read_file('simplemaps-worldcities-basic.csv')
cities = []
for l in lines:
    try:
        line = l.split(',')
        cities.append([float(line[2]), float(line[3]), float(line[4]), line[1], line[0], line[5]])
    except:
        pass


# miasta i lotniska w ich okolicy
lines = read_file('airports.dat.txt')
airports = []
for l in lines:
    try:
        line = l.replace('"', '').split(',')
        if len(line[4]) == 3 and not(line[2] == ""):
            airports.append([line[1], line[4], line[2], line[3]])
    except:
        pass


###################
# LACZENIE DANYCH #
###################


# loty = pasazerowie per lotnisko + lotniska
loty = []
for p in passengers:
    for a in airports:
        if p[1] == a[1]:
            powtorka = False
            for lot in loty:
                if lot[0] == a[2]:
                    lot[1] = lot[1] + p[2]
                    powtorka = True
                    break
            if not powtorka:
                loty.append([a[2], p[2], a[3], p[3], a[1]])
            break


# wskaznik = pasazerowie per lotnisko (miato) / populacji miast
from difflib import SequenceMatcher
from operator import itemgetter

data = []
airportsPosition = {}
wsk = []
a = 0
for l in loty:
    b = False
    for c in cities:
        if (l[0] == c[3] or l[0] == c[4]) and (l[2] == c[5] or l[3] == c[5]):
        #if (SequenceMatcher(None, l[0], c[3]).ratio() > 0.65 or SequenceMatcher(None, l[0], c[4]).ratio() > 0.65) and (l[2] == c[5] or l[3] == c[5]):
            data.append([c[0], c[1], float(l[1])/float(c[2]), c[3], l[1], c[2], l[4]])
            airportsPosition[l[4]] = [c[0], c[1]]
            b = True
            break
    if not b:
        a += 1
data.sort(key=itemgetter(2))

print("Max wsk:", data[-1][2], data[-2][2], data[-3][2], data[-4][2], data[-5][2], data[-6][2], data[-7][2], data[-8][2], data[-9][2], data[-10][2])

# polaczenia miedzymiastowe i polozenie miast
lines = read_file('routes.dat.txt')
routes = []
for l in lines:
    try:
        line = l.split(',')
        if line[2] in airportsPosition and line[4] in airportsPosition:
            routes.append([line[2], line[4]])
    except:
        pass


########
# MAPA #
########


import gmplot
import webbrowser
from matplotlib.colors import Normalize, rgb2hex, LinearSegmentedColormap


def color(c):

    colors = ['purple', 'blue', 'green', 'yellow', 'orange','orange','orange', 'tomato', 'tomato','tomato','tomato', 'red','red','red','red']
    cmap = LinearSegmentedColormap.from_list('name', colors, 300)
    #cmap = cm.jet
    rgb = cmap(c)

    return(rgb2hex(rgb))


mymap = gmplot.GoogleMapPlotter(52.232222, 21.008333, 6)
mymap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"

wsk_max = 100
wsk_norm = Normalize(vmin=data[0][2], vmax=wsk_max)

for d in data:
    try:
        if d[2] >= 2:
            mymap.circle(d[0], d[1], radius=min(wsk_norm(d[2]), 1) * 100000, c=color(wsk_norm(d[2])))
            mymap.marker(d[0], d[1], c=color(wsk_norm(d[2])), title=d[3] + ", " + str(d[2]))
        #if d[6] in wsp_new:
            #mymap.marker(d[0], d[1], c=color(wsk_norm(d[2])), title=str(wsp_new[d[6]]) + ", " + d[3] + ", " + str(d[2]))
            # wspolczynnik posrednictwa
            # mymap.circle(d[0], d[1], radius=min(wsk_norm(d[2] * wsp_new[d[6]]), 1) * 500000, c=color(wsk_norm(d[2] * wsp_new[d[6]])))
            # wspolczynnik posrednictwa
            #mymap.circle(d[0], d[1], radius=min(wsk_norm(d[2] * wsp_new[d[6]]), 1) * 10000000, c=color(wsk_norm(d[2] * wsp_new[d[6]])))
    except:
        pass


mymap.draw('mapa.html')
webbrowser.open_new_tab('mapa.html')

