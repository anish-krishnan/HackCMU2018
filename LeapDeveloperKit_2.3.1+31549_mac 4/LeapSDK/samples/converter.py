import math

def convertToVector(L):
    #palm coordinates 
    xp,yp,zp = L[0]
    newList = []
    for i in range(1,len(L)):
        #finger coordinates 
        xf,yf,zf = L[i]
        unitVector = math.sqrt((xf -xp)**2 + (yf - yp)**2 + (zf - zp)**2)
        vector = [(xf - xp)/(unitVector), (yf-yp)/(unitVector), (zf-zp)/(unitVector)]
        newList.append(vector)
    return newList 
    
