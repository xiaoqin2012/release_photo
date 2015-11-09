#!/usr/bin/python
import copy
import requests
import geocoder
import os, sys
import time
from PIL import Image
import re
from PIL.ExifTags import TAGS, GPSTAGS
from datetime import datetime
import getopt
import gmaps
import image

def concat (a, b):
        return a + b

def get_central_lat_lon(trip_info):
        lat = trip_info[0][1]
        lon = trip_info[0][2]
        return(lat, lon)

def draw_map(pathv, trip_info):
        (lat, lon) = get_central_lat_lon(trip_info)
        mymap = gmaps.maps(lat, lon, 10)
        pt = copy.deepcopy(trip_info)
        for ele in pt:
                ele = ele + ('#00FF00',)
                mymap.addpoint(ele)
        mymap.draw(pathv + 'tripmap.html')

def get_dir_info(pathv, info, rename):
        dirs = os.listdir(pathv)
        for fnamev in dirs:
                format = fnamev[-4:]
                if format == ".jpg" or format == ".JPG":
                        image_info = image.image_info(pathv, fnamev, rename)
                        info_vals = image_info.get_info()
                        info.append(info_vals)

def process_dir(dir, rename_bool, create_bool):
        fname_trip_info = dir + "trip_info.txt"
        trip_info = []
        if create_bool == False and os.path.isfile(fname_trip_info):
                f = open(fname_trip_info)
                trip_info = eval(f.read())
                f.close()

        else:
                get_dir_info(dir, trip_info, rename_bool)
                trip_info.sort(key=lambda tup: tup[0])

                if trip_info != []:
                        f = open(fname_trip_info, "w")        
                        f.write(str(trip_info))
                        f.close()
        
        draw_map(dir, trip_info)

def main(argv):
        help_str = '--inputdir inputdir --rename True'
        try:
                opts, args = getopt.getopt(argv, 'i:r:h', ['inputdir=', 'rename=', 'help'])
        except getopt.GetoptError:
                print help_str
                sys.exit(2)

        rename = False                   
        for opt, arg in opts:
                if opt in('-h', '--help'):
                        print help_str
                        sys.exit(2)
                elif opt in ('-i'):
                        dir = arg
                elif opt in ('-r'):
                        rename = arg

        if dir[-1] != '\\':
                dir = dir + '\\'

        process_dir(dir, rename, True)

if __name__ == "__main__":
   main(sys.argv[1:])  
        
#process_dir("B:\\Europe 2012 Selects\\", True, True)
