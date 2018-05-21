import pygmaps
import webbrowser

text = open('simplemaps-worldcities-basic.csv', 'r', encoding="utf8").read()
lines = text.split('\n')
print(lines)
coords = []
for l in lines:
    try:
        line = l.split(',')
        coords.append([float(line[2]), float(line[3]), float(line[4]), line[0]])
    except:
        pass
print(coords[4743])
mymap = pygmaps.maps(52.232222, 21.008333, 6)
for c in coords:
    mymap.addradpoint(c[0], c[1], c[2]/50, 'red')


mymap.draw('mymap.draw.html')

url = 'mymap.draw.html'
webbrowser.open_new_tab(url)
