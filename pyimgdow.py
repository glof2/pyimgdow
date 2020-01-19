import grequests
import requests
import datetime
import os
from colorama import init, Fore
from bs4 import BeautifulSoup

# Colorama init (Without this the colors won't change)
init()


# Exception handler for grequests
def exception_handler(request, exception):
    print(Fore.RED, "Request failed", request.url, Fore.WHITE)


# Class beggining
class ImageDownload():
    def __init__(self):
        self.headers = {
            "UserAgent": "CoolUSERagentasdasad"
        }
        self.time = datetime.datetime.now().strftime("%H%M%S")

# Grab links from the site
    def getlinks(self, link):
        res = requests.get(link, headers=self.headers).text
        soup = BeautifulSoup(res, "html.parser")
        soup = BeautifulSoup(soup.prettify(), "html.parser")

        images = soup.findAll("img")
        links = []

        for link in images:
            try:
                links.append(link["src"])
            except KeyError:
                print(Fore.RED, "No 'src' in this img tag...: ", Fore.WHITE)
        return links

# Download images from a list of links
    def downloadimages(self, links, savenames=False, imgname="image",
                       foldername="images"):
        rs = [grequests.get(link) for link in links]
        i = 0
        imagenames = []

        for link in grequests.imap(rs, size=16,
                                   exception_handler=exception_handler):
            # Continue only for 200 response
            if int(link.status_code) == 200:
                print(Fore.GREEN, link.status_code, link.url, Fore.WHITE)
            else:
                print(Fore.RED, link.status_code, link.url, Fore.WHITE)
                continue

            # Creating file name and path
            filename = f"{imgname}{i}"
            filename_ = os.path.join(foldername, filename)

            # Getting rid of the "/" at the end of the link if it's there
            link_ = link.url.rstrip("/")

            #
            if savenames:
                imagenames.append(filename)

            # Making sure the folder is there
            os.makedirs(foldername, exist_ok=True)

            # Download images:
            # png
            if ".png" in link_:
                with open(f"{filename_}.png", "wb") as f:
                    f.write(link.content)
            # jpg
            elif ".jpg" in link_:
                with open(f"{filename_}.jpg", "wb") as f:
                    f.write(link.content)
            # gif
            elif ".gif" in link_:
                with open(f"{filename_}.gif", "wb") as f:
                    f.write(link.content)
            # tif
            elif ".tif" in link_:
                with open(f"{filename_}.tif", "wb") as f:
                    f.write(link.content)
            # svg
            elif ".svg" in link_:
                with open(f"{filename_}.svg", "wb") as f:
                    f.write(link.content)
            # other
            else:
                with open(f"{filename_}.jpg", "wb") as f:
                    print(Fore.YELLOW, "Unsupported file type. Saving as .jpg")
                    print(" Please report the file type at ",
                          "https://github.com/glof2/pyimgdow", Fore.WHITE)
                    f.write(link.content)
            i += 1
        if savenames:
            return imagenames


if __name__ == "__main__":
    print("""
          ┌────────────────────┐
          │  Pyimgdow library  │
          │    Version v0.1    │
          └────────────────────┘
          """)
