#this code extracts gps data and etc emeded in image
import sys
import pyexiv2

metadata = pyexiv2.ImageMetadata(sys.argv[1]+".jpg")
metadata.read()

tag1=metadata['Exif.Image.ProcessingSoftware']
tag2=metadata['Exif.Image.DocumentName']
tag3=metadata['Exif.Image.ImageDescription']
tag4=metadata['Exif.Image.Make']
f=open(sys.argv[1]+".txt",'w')
f.write(tag1.raw_value)
f.write('\n')
f.write(tag2.raw_value)
f.write('\n')
f.write(tag3.raw_value)
f.write('\n')
f.write(tag4.raw_value)
