#!/usr/bin/python3 -u

from math import sin, radians, cos, asin, sqrt, sin, atan2, degrees
from aircraft import Aircraft
from queryscanner import QueryScanner

def calculate_distance_of_aircraft(lat1: float, lng1: float, lat2: float, lng2: float) -> float: 
    """
    Calculate the distance from two sets of geographic cordinates and return their distance from each other. 
    Source of equation: https://en.wikipedia.org/wiki/Great-circle_distance 
    Steps: 
    1. Convert lat and long to radian
    2. Get difference of lat long
    3. Calculate archav of two cordinates
    4. Return archave * radius of earth
    """
    
    # Check to make sure our lat and lng cordinates make sense and are of type float
    validation_list = [lat1, lng1, lat2, lng2]
    for i in validation_list: 
        if not isinstance(i, float): 
            raise Exception
        elif (i < -90 or i > 90) or (i > 180 or i < -180):
            raise Exception

    # Convert lat and lng to radians
    lat1, lat2, lng1, lng2 = map(radians, [lat1, lat2, lng1, lng2])

    d_long = lng2 - lng1
    d_lat = lat2 - lat1

    # Find the angle 
    a = sin(d_lat/2)**2 + cos(lat1) * cos(lat2) * sin(d_long/2)**2
    r_earth = 3958.8 # Radius of Earth w/ decimal for more accuracy
    if a < 0: 
        raise Exception
    c = 2 * asin(sqrt(a))

    return c * r_earth

"""double CalcPeilung(double breite1, double laenge1, double breite2, double laenge2) {
// Berechnet die Peilung von breite1/laenge1 zu breite2/laenge2 in Grad
// Ausgabe Peilung in Grad
// Matthias Busse 25.11.2014 Version 1.0
breite1 = gtor(breite1);
laenge1 = gtor(laenge1);
breite2 = gtor(breite2);
laenge2 = gtor(laenge2);  // Winkel berechnen
  double peil = atan2(sin(laenge2-laenge1)*cos(breite2), (cos(breite1)*sin(breite2))-(sin(breite1)*cos(breite2)*cos(laenge2-laenge1)));
  peil = rtog(peil); // in Grad umrechnen
  peil = fmod((peil + 360.0), 360); // mod macht -90 zu 270
  return peil;
}

double gtor(double fgrad){ // Grad in Rad umwandeln
  return(fgrad * PI / 180);
}

double rtog(double frad){ // Rad in Grad umwandeln
  return(frad * 180.0 / PI);
}"""
def calculate_direction_of_aircraft(lat1: float, lng1: float, lat2: float, lng2: float) -> float: 
    # Check to make sure our lat and lng cordinates make sense and are of type float
    validation_list = [lat1, lng1, lat2, lng2]
    for i in validation_list: 
        if not isinstance(i, float): 
            raise Exception
        elif (i < -90 or i > 90) or (i > 180 or i < -180):
            raise Exception

    # Convert lat and lng to radians
    lat1, lat2, lng1, lng2 = map(radians, [lat1, lat2, lng1, lng2])

    peil=atan2(sin(lng2-lng1)*cos(lat2), (cos(lat1)*sin(lat2))-(sin(lat1)*cos(lat2)*cos(lng2-lng1)))
    peil=(degrees(peil)+360)%360
    return peil

if __name__ == '__main__':
    q = QueryScanner("http://localhost")
    aircraft = q.get_all_aircraft()

    maxDist=0.1
    for i in aircraft:
        #print('Info:')         
        #print(i.lat)
        #print(i.lng)
        if i.lng is not None and i.lat is not None:
            #print(i)
            dist = calculate_distance_of_aircraft(51.866528, 8.469980, i.lat, i.lng)
            peil = calculate_direction_of_aircraft(51.866528, 8.469980, i.lat, i.lng)
            if dist > maxDist:
                maxDist=dist
                maxPeil=peil
            #print(dist)
    
    print (maxDist)
    print (maxPeil)