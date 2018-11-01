from PyPDF2 import PdfFileWriter, PdfFileReader
from fpdf import FPDF
from random import random
import argparse
import os
from instagram_scraper.app import InstagramScraper
from PIL import Image

from reportlab.pdfgen import canvas

# Get the watermark file you just created
def image2pdf(path,image):
    c = canvas.Canvas(path+'/temp/'+image+'.pdf')
    im = Image.open(path+"/temp/img/"+image)
    width, height = im.size
    c.setPageSize((width, height))
    # Draw the image at x, y. I positioned the x,y to be where i like here
    c.drawImage(path+'/temp/img/'+image,0, 0)
    # Add some custom text for good measure
    c.save()


parser = argparse.ArgumentParser(description="""add dogpictures""")

parser.add_argument('dist', type=int, help="""Name of output file""")

args = parser.parse_args()

from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askinteger

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
datapath = askopenfilename() # show an "Open" dialog box and return the path to the selected file
dist = askinteger("Input", "Alle wieviel Folien?",
                                 minvalue=1, maxvalue=100)

path, filename = os.path.split(datapath)

inputpdf = PdfFileReader(open(datapath, "rb"))
pdflength = inputpdf.getNumPages()

opt = {'comments': False, 'destination': path + '/temp/img/', 'filename': None, 'filter': None,
       'include_location': False, 'interactive': False, 'latest': False,
       'latest_stamps': None, 'location': False, 'login_pass': '',
       'login_user': '', 'maximum': 20, 'media_metadata': False,
       'media_types': ['image'], 'quiet': False,
       'retain_username': False, 'retry_forever': False,
       'search_location': False, 'tag': False, 'template': '{urlname}',
       'username': ['cutest'], 'usernames': ['cutest'], 'verbose': 0}

scraper = InstagramScraper(**opt)

#scraper.login()
scraper.scrape()
writer = PdfFileWriter()
namelist = os.listdir(path + '/temp/img/')
currim = 0
print(namelist[currim])
for i in range(pdflength):
    writer.addPage(inputpdf.getPage(i))
    if i % dist == 0:
        image2pdf(path, namelist[currim])
        image = PdfFileReader(open(path + "/temp/"+namelist[currim]+".pdf", "rb"))
        image.getPage(0).scaleTo(width=inputpdf.getPage(i).mediaBox[2], height=image.getPage(0).mediaBox[3] * (
                    inputpdf.getPage(i).mediaBox[2] / image.getPage(0).mediaBox[2]))
        writer.addPage(image.getPage(0))
        currim += 1

outputStream = open(path + "/"+filename[:-4]+"-animals.pdf", "wb")
writer.write(outputStream)
outputStream.close()



