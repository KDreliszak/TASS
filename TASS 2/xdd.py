import gmplot
import webbrowser
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

text = open('simplemaps-worldcities-basic.csv', 'r', encoding="utf8").read()
lines = text.split('\n')

cities = []
for l in lines:
    try:
        line = l.split(',')
        cities.append([float(line[2]), float(line[3]), float(line[4]), line[0]])
    except:
        pass
print(cities[4743])
mymap = gmplot.GoogleMapPlotter(52.232222, 21.008333, 6)

colors = ['red', 'brown', 'yellow', 'green', 'blue']
#cmap = LinearSegmentedColormap.from_list('name', colors, [0, 1000, 10000, 30000, 50000])
#col1 = cmap(np.linspace(0,1,10000))
norm = plt.Normalize(0, 10000)

for c in cities:
    #mymap.addradpoint(c[0], c[1], c[2]/50, 'red')
#    print(c)
#    mymap.scatter(c[0], c[1], '#3B0B39', size=c[2]/50, marker=False)

#mymap.plot(lat, lon, 'cornflowerblue', edge_width=10)
#mymap.scatter(lat, lon, '#3B0B39', size=10000, marker=False)
    mymap.circle(c[0], c[1], c[2]/100, 'blue')

#mymap.scatter(lat, lon, 'k', marker=True)


mymap.draw('mymap.draw.html')

url = 'mymap.draw.html'
webbrowser.open_new_tab(url)
