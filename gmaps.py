import math
class maps:

	def __init__(self, centerLat, centerLng, zoom ):
		self.center = (float(centerLat),float(centerLng))
		self.zoom = int(zoom)
		self.points = []
		self.coloricon = 'http://chart.apis.google.com/chart?cht=mm&chs=12x16&chco=FFFFFF,XXXXXX,000000&ext=.png'

	def addpoint(self, ele):
		self.points.append(ele)
                	
	#create the html file which inlcude one google map and all points
	def draw(self, htmlfile):
		f = open(htmlfile,'w')
		f.write('<html>\n')
		f.write('<head>\n')
		f.write('<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />\n')
		f.write('<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>\n')

                f.write('<style type="text/css">\n')
                f.write('  .labels { \n')
                f.write('    color: white;\n')
                f.write('    background-color: red;\n')
                f.write('    font-family: \"Lucida Grande\", \"Arial\", sans-serif;\n')
                f.write('    font-size: 10px;\n')
                f.write('    text-align: center;\n')
                f.write('    width: 10px;\n')     
                f.write('    white-space: nowrap;\n')
                f.write('  }\n')
                f.write('</style>\n')
                
                f.write('<title>Google Maps - pygmaps </title>\n')
		f.write('<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>\n')
		f.write('<script type="text/javascript">\n')
		f.write('\tfunction initialize() {\n')
		self.drawmap(f)
		self.drawpoints(f)
		f.write('\t}\n')
		f.write('</script>\n')
		f.write('</head>\n')
		f.write('<body style="margin:0px; padding:0px;" onload="initialize()">\n')
		f.write('\t<div id="map_canvas" style="width: 100%; height: 100%;"></div>\n')
		f.write('</body>\n')
		f.write('</html>\n')		
		f.close()

	def drawpoints(self,f):
                i = 0
		for point in  self.points:
			self.drawpoint(f, point)


	#############################################
	# # # # # # Low level Map Drawing # # # # # # 
	#############################################
	def drawmap(self, f):
		f.write('\t\tvar centerlatlng = new google.maps.LatLng(%f, %f);\n' % (self.center[0],self.center[1]))
		f.write('\t\tvar myOptions = {\n')
		f.write('\t\t\tzoom: %d,\n' % (self.zoom))
		f.write('\t\t\tcenter: centerlatlng,\n')
		f.write('\t\t\tmapTypeId: google.maps.MapTypeId.ROADMAP\n')
		f.write('\t\t};\n')
		f.write('\t\tvar map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);\n')
		f.write('\n')

	def drawpoint(self,f, p):
                lat = p[1]
                lon = p[2]
                fname = p[3]
                addr = p[4]
                color = p[5]
		f.write('\t\tvar latlng = new google.maps.LatLng(%f, %f);\n'%(lat,lon))
		f.write('\t\tvar img = new google.maps.MarkerImage(\'%s\');\n' % (self.coloricon.replace('XXXXXX',color)))
		f.write('\t\tvar marker = new google.maps.Marker({\n')    
                f.write('\t\tposition: latlng \n')
		f.write('\t\t});\n')

                f.write('\t\tvar iw = new google.maps.InfoWindow({\n')
                f.write('\t\tcontent: \'%s\' \n' %addr)
                f.write('\t\t});\n')
                f.write('\t\tgoogle.maps.event.addListener(marker, \"click\", function (e) { \n')
                #f.write('\t\tiw.setContent(\'%s\'); \n' %(fname))
                f.write('\t\tiw.setContent(\'<IMG BORDER=\"0\" ALIGN=\"Right\" width=\"500\" SRC=\"%s\"> \"%s\"\"%s\"\'); \n' %(fname, p[0], addr))
                f.write('\t\tiw.open(map, this); });\n')
		f.write('\t\tmarker.setMap(map);\n')
                f.write('\n')                
                
