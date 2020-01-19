import pyimgdow
from colorama import init, Fore

init()

download = pyimgdow.ImageDownload()

link = input("Input your link: ")
try:
    links = download.getlinks(link)
except Exception as e:
    print(Fore.RED, e, Fore.WHITE)

imgname = input("Image keyword: ")
foldername = input("Folder keyword: ")
try:
    download.downloadimages(links, imgname=imgname, foldername=foldername)
except Exception as e:
    print(Fore.RED, e, Fore.WHITE)