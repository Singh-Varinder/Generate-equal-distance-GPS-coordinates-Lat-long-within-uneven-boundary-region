
import pandas
import numpy as np
import utm
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

easting_row_1=[]
northing_col_1=[]
res=10

df = pandas.read_csv('polycord.csv')

from pyproj import Proj
pp = Proj(proj='utm',zone=43,ellps='WGS84', preserve_units=False)

xx, yy = pp(df["long"].values, df["lat"].values)
xx_r = np.array(xx)
b_east = np.append(xx_r, xx_r[0])
yy_r = np.array(yy)
b_north = np.append(yy_r, yy_r[0])

dlen= df.shape[0]
print(dlen)
c=0
llpoints=[]
gpslistdata=[]
i=0
while i<dlen:
    llpoints.append(xx_r[i])
    llpoints.append(yy_r[i])
    i+=1
while c<len(llpoints):
    gpslistdata.append(tuple(llpoints[c:c+2]))
    c+=2

nlat = (df.loc[:, ['lat']])
nlong = (df.loc[:, ['long']])
minilat = float(nlat.min())
maxlat = float(nlat.max())

minilong = float(nlong.min())
maxlong = float(nlong.max())

uorigon = utm.from_latlon(minilat, minilong)
ufirst = utm.from_latlon(maxlat, minilong)
usecond = utm.from_latlon(maxlat, maxlong)
uthird = utm.from_latlon(minilat, maxlong)

o_east = uorigon[0]
o_north = uorigon[1]
f_east = ufirst[0]
f_north = ufirst[1]
s_east = usecond[0]
s_north = usecond[1]
t_east = uthird[0]
t_north = uthird[1]

distancenorth_1 = f_north - o_north
distancenorth_2 = s_north - t_north
northoffset = distancenorth_1 / res

distanceeast_1 = t_east - o_east
distanceeast_2 = s_east - f_east
eastoffset = distanceeast_1 / res

for i in range(res + 1):
    row_1 = o_east + i * eastoffset
    easting_row_1.append(row_1)

    col_1 = o_north + i * northoffset
    northing_col_1.append(col_1)

easting = []
northing = []
for i in range(res + 1):
    nordata = northing_col_1[i]

    for i in range(res + 1):
        northing.append(nordata)
        easting.append(easting_row_1[i])

lons_lats_vect = np.column_stack((xx_r, yy_r))
polygon = Polygon(lons_lats_vect)

inpolyeast=[]
inpolynorth=[]
z=0
while z<len(easting):
    point=Point(easting[z], northing[z])
    isenclosed = point.within(polygon)

    if isenclosed == True:
         inpolyeast.append(easting[z])
         inpolynorth.append(northing[z])
    z += 1

fig, axes = plt.subplots(1,2)
ax1 = axes[0]
ax2 = axes[1]

ax1.plot((easting ), (northing), 'o')
ax1.plot(b_east, b_north)

ax2.plot((inpolyeast ), (inpolynorth ), 'o')
ax2.plot(b_east, b_north)
plt.show()
