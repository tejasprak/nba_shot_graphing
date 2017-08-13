import csv
import requests
import matplotlib.pyplot as plt
import json

# A function that takes the output of get_shots and calculates the percent made of a shot range
def made(array):
    top = 0
    bottom = 0
    #A counter that, per shot in shot array, checks if it is made. If it is made, it adds 1 to the made counter. Either way, add one to missed counter.
    for t in array:
        if str(t[10]) == "Made Shot":
            top = top + 1
            bottom = bottom + 1
        elif str(t[10]) == "Missed Shot":
            bottom = bottom + 1
    # To prevent a division error
    if float(bottom) == 0:
        return 0
    # Calculate percentage and return it.
    return [float(top)/float(bottom), top, bottom]
#A function that takes the name and team, and outputs a formatted array with five subarrays of each different range. These subarrays contain every shot that the player took during the season
def get_shots(name2, team):
    # Declare shot arrays

    #SHOTS from 0-4FT
    z4 = []
    #SHOTS from 5-8FT
    f8 = []
    #SHOTS from 9-15
    n15 = []
    #SHOTS from 15-21
    f21 = []
    #SHOTS from 22-27
    t27 = []
    #HEAVES (Anything above)
    heaves = []

    # Open json data
    with open("teams/" + team + '.json') as json_data:
        d = json.load(json_data)
        #print(d)
    # Grab headers
    headers = d['resultSets'][0]['headers']
    # Grab the shot chart data
    shots = d['resultSets'][0]['rowSet']
    # Iterate over overy shot for this player
    for shot in shots:
        # Declare name to check if this is the player we want
        name =  shot[4]
        if name == str(name2):
            # If it is, we add the shot to its given array.
            ft = shot[16]
            if int(ft) < 5:
                z4.append(shot)
            elif int(ft) < 9:
                f8.append(shot)
            elif int(ft) < 16:
                n15.append(shot)
            elif int(ft) < 22:
                f21.append(shot)
            elif int(ft) < 28:
                t27.append(shot)
            else:
                heaves.append(shot)
    #return an array containing the formatted shots
    return [z4, f8, n15, f21, t27, heaves]

x = []
y = []
names = []
# Open CSV with our relevant players to graph for
with open('names.csv') as csvfile:
        nbalist = csv.reader(csvfile)
        g = 0
        for row in nbalist:
            # Account for the first two rows with bad data
            if g == 0 or g ==1:
                g = g + 1
                continue
            # Take out the bbref url part of the name (lol)
            nm =  row[1]
            nm = nm.split("\\")[0]
            tm = row[4]
            print nm

            if tm != "TOT":
                if tm:
                    gg = get_shots(nm, tm)
                    md = made(gg[5])
                    #This changes depending on what you want to graph
                    #0 for 0 -4 , 1 for 5-8, 2 for 9-15, 3 for 16-21, 4 for 22-27, 5 for the rest
                    if md:
                        # The cutoff of the data scattered
                        if md[2] > 20:
                                print md
                                x.append(md[2])
                                y.append(md[0])
                                names.append(nm)
colors = (0,0,0)
area = 0.5

# Some colors in an array
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.

for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

hfont = {'fontname':'Arial'}

# plot!
plt.scatter(x, y, s=area, c=tableau20[0], alpha=0.5)
plt.title('FGA over FG% from 27-the other side of the court ft', **hfont)
plt.xlabel('FGA',  **hfont)
plt.ylabel('FG%', **hfont)
i = 0

# A simple function to iterate over scattered points and add labels. Some code to cut the name into First Initial Last Name is included
for value in x:
        name = names[i]

        fname, lname = name.split(" ")
        init = fname[0]
        finalname = str(init) + ". " + lname
        string = '  '  + finalnam
        plt.annotate(string, xy=(x[i], y[i]), arrowprops=dict(), size=10, **hfont)

        i = i + 1

# Done!
plt.show()


#Useless code

#gg = get_shots(name, team)
#print name + ", " + team + " Overview"
#print made(gg[0]), " percentage from 0 to 4ft"
#print made(gg[1]), " percentage from 5ft to 8ft"
#print made(gg[2]), " percentage from 9ft to 15ft"
#print made(gg[3]), " percentage from 16ft to 21ft"
#print made(gg[4]), " percentage from 22 to 27 ft (3P range)"
#print made(gg[5]), " percentage from heaves"
