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
import gmaps
 
def concat (a, b):
        return a + b

class image_info:
        def __init__(self, pathv, fnamev, rename_bool):
                self.pathv = pathv
                self.rename_bool = rename_bool
                self.ab_fname = pathv + fnamev
                self.format = fnamev[-4:]                
                img = Image.open(self.ab_fname, 'r')
                self.exif_data = img._getexif()
                img.close()
                self._set_time_field()
                self._set_GPS_fields()
                if self.rename_bool == "True":
                        self._set_newname()
                        self._rename()
                

        def print_info(self):
                print self.get_info()
        
        def get_info(self):
                if self.rename_bool == "True":
                        newname = self.newname
                else:
                        newname = self.ab_fname
                newname = newname.replace("\\", "/")
                return (self.time, self.lat, self.lon, newname, self.addr)
                        
        def _print_tags_vals(self):
                if self.exif_data == None:
                        print "exif_data is none"
                        return
                for (k, v) in self.exif_data.iteritems():
                        print '%s: %s' %(TAGS.get(k), v)

        def _get_field(self, field):
                if self.exif_data == None:
                        return None
                for (k,v) in self.exif_data.iteritems():
                        if TAGS.get(k) == field:
                                return v

        def _get_gps_field(self, field):
                for (k,v) in self.gps_data.iteritems():
                        if GPSTAGS.get(k) == field:
                                return v
	
        def _set_time_field(self):
                if self.exif_data == None:
                        return None
                
                val = self._get_field('DateTimeOriginal')
                self.time = val.replace(':', '').encode("ascii")

        def _get_gps_val(self, field):
                val = None
                gps_val = self._get_gps_field(field)
                gps_ref = self._get_gps_field(field + 'Ref')
                if gps_val and gps_ref:
                        val = self._convert_to_degress(gps_val)
                if field == 'GPSLatitude' and gps_ref == 'S':                     
                    val = 0 - val
                elif field == 'GPSLongitude' and gps_ref == 'W':
                    val = 0 - val
                return val                

        def _set_address(self):
                if self.lat == None or self.lon == None:
                        self.addr = ""
                        self.short_addr = ""
                        return
                g = geocoder.google([self.lat, self.lon], method='reverse')
                self.addr = g.address
                self._set_short_address()

        def _set_short_address(self):
                s = self.addr.split(",")
                s.reverse()
                s.pop()
                addr = re.sub("[0-9]", "", reduce(concat,s))
                addr = self._clean_fname(addr)
                self.short_addr = addr

        def _set_GPS_fields(self):
                self.gps_data = self._get_field('GPSInfo')

                if self.gps_data == None:
                        return
                self.lat = self._get_gps_val('GPSLatitude')
                self.lon = self._get_gps_val('GPSLongitude')    
                self._set_address()
                
        def _set_newname(self):
                if (self.addr != None):
                        newname = self.time + self.short_addr
                        self.newname = self.pathv + self._clean_fname(newname) + self.format
        def _rename(self):
                print("rename: ")
                print("original name: ")
                print self.ab_fname
                print("new name: ")
                print self.newname
        
                if self.ab_fname == self.newname:
                        return
                try:
                        os.rename(self.ab_fname, self.newname)

                except OSError as e:
                        print e.errno
                        print e.filename
                        print e.strerror

        def _clean_fname(self, f):
                t = ''
                for i in f:
                        if i != '/' and i != ':' and i != '*' and i != '?' and i!='"' and i!='<' and i!='>' and i != '|' and i != '\\':
                                t =  t + i
                return t.decode("utf-8", "ignore").encode("ascii", "ignore")

                        
	
        def _convert_to_degress(self, value):
                d0 = value[0][0]
                d1 = value[0][1]
                d = float(d0) / float(d1)

                m0 = value[1][0]
                m1 = value[1][1]
                m = float(m0) / float(m1)

                s0 = value[2][0]
                s1 = value[2][1]
                s = float(s0) / float(s1)

                return d + (m / 60.0) + (s / 3600.0)

