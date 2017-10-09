from math import *

#Global variables

distance_to_destination = 0             
desired_heading = 0                                 #to go to destination, head this way


my_lat = 0                                          #Read from GPS sensor
my_long = 0

togoto_lat = 0                                      #Determined depending on robot algorithm
togoto_long = 0

#GPS_Function********************************************************

def Get_GPS(cmd):
	
	##initialize GPS before use
	
    session = gps.gps("localhost", "2947")
    session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

    while True:

        try:
            report = session.next()
		# Wait for a 'TPV' report and display the current time
		# To see all report data, uncomment the line below
		# print report
            if report['class'] == 'TPV':
               
                    if hasattr(report, 'lat'):
                        my_lat = report.lat


                    if hasattr(report,'lon'):
                        resp = report.lon
                        
    
    
#GPS_Function_End***************************************************



#clac_dist_btw_coord************************************************

def clac_dist_btw_coord(my_lat, my_long, lat2, long2):
    
    R = 6371000
    
    lat1 = radians(lat1)
    long1 = radians(long1)
    lat2 = radians(lat2)
    long2 = radians(long2)

    delta_lat = lat1 - lat2
    delta_long = long1 - long2
    
    
    a = pow(sin(delta_lat/2) , 2) + cos(lat1) * cos(lat2) * pow(sin(delta_long/2) , 2)
	c = 2 * atan2( sqrt(a) , sqrt(1 - a) )
    distance = R * c
    
    desired_heading = atan2( (sin(delta_long) * cos(lat2)) , (cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(delta_long)) )


#clac_dist_btw_coord_End************************************************



if __name__=="__main__":        

    #in the robot code, assign values to togoto_lat and togoto_long depending on where you want the robot to go :)

    clac_dist_btw_coord(my_lat, my_long, togoto_lat, togoto_long)

