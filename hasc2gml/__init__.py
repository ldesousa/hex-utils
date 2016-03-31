key_ncols  = "ncols"
key_nrows  = "nrows"
key_xll    = "xll"
key_yll    = "yll"
key_side   = "side"
key_nodata = "no_data"

ncols  = None
nrows  = None
xll    = None
yll    = None
side   = None
nodata = None

def readHeaderLine(line, key, valType):
    
    error = False
    token = line.split()[0]
    value = line.split()[1]
    
    if token.upper() != key.upper():
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
    
    ncols  = readHeaderLine(next(file), key_ncols,  type(1))
    nrows  = readHeaderLine(next(file), key_nrows,  type(1))
    xll    = readHeaderLine(next(file), key_xll,    type(1.0))
    yll    = readHeaderLine(next(file), key_yll,    type(1.0))
    side   = readHeaderLine(next(file), key_side,   type(1.0))
    nodata = readHeaderLine(next(file), key_nodata, type("a"))
    
    #TODO: optional headers lines
    


f = open('/home/desouslu/git/caddies-api/apps/caddies-tests/HexBasic/example.hasc', 'r')
readHeader(f)

print ("This is what I read")
print (str(ncols))
print (str(nrows))
print (str(xll))
print (str(yll))
print (str(side))
print (str(nodata))


    