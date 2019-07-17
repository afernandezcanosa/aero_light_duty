"""
This code snippet parses latitude and longitude from the serial port of 
Comma AI Grey Panda CAN shield with high-precision GPS antenna
References: 
    - https://github.com/commaai/panda
    - https://www.u-blox.com/sites/default/files/products/documents/u-blox8-M8_ReceiverDescrProtSpec_%28UBX-13003221%29_Public.pdf
"""
import time
from panda import Panda

def lat_longitude_from_serial(gps):
    try:
        gngll = gps.find('$GNGLL')
        
        lat_start_deg = gngll + 7
        lat_end_deg = lat_start_deg + 2
        lat_start_min = lat_end_deg
        lat_end_min = lat_start_min + 8    
        n_or_s = gps[lat_end_min + 1]
        
        if n_or_s == 'N':
            lat = (float(gps[lat_start_deg:lat_end_deg]) + float(gps[lat_start_min:lat_end_min])/60)
        else:
            lat = -(float(gps[lat_start_deg:lat_end_deg]) + float(gps[lat_start_min:lat_end_min])/60)
        
        long_start_deg = lat_end_min + 3
        long_end_deg = long_start_deg + 3
        long_start_min = long_end_deg
        long_end_min = long_start_min + 8    
        e_or_w = gps[long_end_min + 1]
    
        if e_or_w == 'E':
            long = (float(gps[long_start_deg:long_end_deg]) + float(gps[long_start_min:long_end_min])/60)
        else:
            long = -(float(gps[long_start_deg:long_end_deg]) + float(gps[long_start_min:long_end_min])/60)  
    except:
        lat = None
        long = None
    return [lat, long]

if __name__ == "__main__":
    p = Panda()
    port = 1
    p.serial_clear(port)
    
    while True:
        time.sleep(0.4)
        gps = p.serial_read(port)
        print(gps)
        lat, long = lat_longitude_from_serial(gps)
        print(lat, long)