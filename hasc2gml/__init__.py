from osgeo import ogr
from osgeo import osr
import math

key_ncols  = "ncols"
key_nrows  = "nrows"
key_xll    = "xll"
key_yll    = "yll"
key_side   = "side"
key_nodata = "no_data"
key_angle  = "angle"

ncols  = None
nrows  = None
xll    = None
yll    = None
side   = None
nodata = ""
angle  = None

def readHeaderLine(line, key, valType, optional = False):
    
    error = False
    token = line.split()[0]
    value = line.split()[1]
    
    if token.upper() != key.upper():
        if not optional:
            print ("Error, not an hexagonal ASCII raster file. " + 
                "Expected " + key + " but read " + token)
        return None
    
    if type(1) == valType:
        try:
            return int(value)
        except Exception:
            error = True
    
    elif type(1.0) == valType:
        try:
            return float(value)
        except Exception:
            error = True
            
    else:
        return value
        
    if error:    
        print ("Error converting the string '" + value + "' into " + valType)
        return None
    

def readHeader(file):
    
    global ncols
    global nrows
    global xll  
    global yll  
    global side 
    global nodata
    global angle
    
    # Mandatory header
    ncols  = readHeaderLine(file.readline(), key_ncols,  type(1))
    nrows  = readHeaderLine(file.readline(), key_nrows,  type(1))
    xll    = readHeaderLine(file.readline(), key_xll,    type(1.0))
    yll    = readHeaderLine(file.readline(), key_yll,    type(1.0))
    side   = readHeaderLine(file.readline(), key_side,   type(1.0))
    # Optional headers
    nextLine = file.readline()
    nodata = readHeaderLine(nextLine, key_nodata, type("a"), True)
    if nodata != "" :
        nextLine = file.readline()
    angle  = readHeaderLine(nextLine, key_angle, type(1.0),  True)
    if angle == None :
        return nextLine
    else:
        return file.readline()
    
    
def createOutputGML():
    
    driver = ogr.GetDriverByName("GML")
    outSource = driver.CreateDataSource(
        "output.gml", 
        ["XSISCHEMAURI=http://schemas.opengis.net/gml/2.1.2/feature.xsd"])
    outLayer = outSource.CreateLayer("output", None, ogr.wkbUnknown)

    newField = ogr.FieldDefn("value", ogr.OFTReal)
    outLayer.GetLayerDefn().AddFieldDefn(newField)

# Edge coordinates of an hexagon centered in (x,y) and a side of d:
#
#           [x-d/2, y+sqrt(3)*d/2]   [x+d/2, y+sqrt(3)*d/2] 
#
#  [x-d, y]                                                 [x+d, y]
#
#           [x-d/2, y-sqrt(3)*d/2]   [x+d/2, y-sqrt(3)*d/2]

    # The perpendicular distance from cell center to cell edge
    perp = math.sqrt(3) * side / 2
    print ("The perpendicular: " + str(perp))

    for i in range(0, ncols):
        for j in range(0, nrows):
            x = xll + i * 3 * side / 2
            y = yll + j * 2 * perp
            if (i % 2) != 0:
                y += perp
                
            polygon = ogr.CreateGeometryFromWkt("POLYGON ((" +
                str(x - side)     + " " +  str(y)        + ", " +
                str(x - side / 2) + " " +  str(y - perp) + ", " +
                str(x + side / 2) + " " +  str(y - perp) + ", " +
                str(x + side)     + " " +  str(y)        + ", " +
                str(x + side / 2) + " " +  str(y + perp) + ", " +
                str(x - side / 2) + " " +  str(y + perp) + ", " +
                str(x - side)     + " " +  str(y)       + "))")
            
            outFeature = ogr.Feature(feature_def=outLayer.GetLayerDefn())
            outFeature.SetGeometryDirectly(polygon)
            outFeature.SetField("value",  i + j)
            outLayer.CreateFeature(outFeature)
            
            
    
def readValues(file, line):
       
    while(line):
        
        for value in line.split():
            print(value)
        line = file.readline()
    

f = open('/home/desouslu/git/caddies-api/apps/caddies-tests/HexBasic/example.hasc', 'r')
line = readHeader(f)

print ("This is what I read")
print (str(ncols))
print (str(nrows))
print (str(xll))
print (str(yll))
print (str(side))
print (str(nodata))

print ("The values:")
readValues(f, line)

f.close()

createOutputGML()
    