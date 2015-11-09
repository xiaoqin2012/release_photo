# release_photo
photo processing
These days when we travel, we get photos from phone,  camera, friend's phone, and friend' phone. Each device has its 
own naming system, so it is hard to sort them according to the names from all devices. 
Luckily the picture files have metadata that captures the time when the picture is taken. 
I hacked down to the metadata and extracted both the time and the place the picture is taken. 
By setting date and place information into the pictures' file names, they can not only be easily sorted 
but also the places I have traveled are clearly shown up. 

In this toy too, I also mark the places extracted from the picture in the map by scanning the pictures' GPS information. At the end, a nice trip journal map is generated. While clicking on the point, the picture taken there is shown up.
To use the software, first install python and PIL library.
Run the program by given the absolute path of the album.
The program will rename all pictures in the album with date and place information.
At the end, an map.html file is generated that can be viewed in a browser. All the places in the picture will be marked on the map and by clicking the icon, the picture taken at the specific place will be pop up.
Example:
/* B:\test is the absolute path for the directory of pictures */
/* -rTrue means all the files will be renamed, if -rFalse, the files will not be renamed but a map of the trip with pictures markers will still be generated */
python photo.py -iB:\test -rTrue
