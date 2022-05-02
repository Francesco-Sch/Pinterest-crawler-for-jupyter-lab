import requests
import asyncio
from bs4 import BeautifulSoup
from time import sleep
from PIL import Image
import io

def resize_image(src, file_path, scale_value):
    img = Image.open(io.BytesIO(src))
    imgWidth = int(img.size[0])
    imgHeight = int(img.size[1])

    if imgWidth < scale_value or imgHeight < scale_value:
        print('No down scaling neccesary')
        img.save(f'{file_path}', 'JPEG')
    
    if imgWidth > imgHeight and imgWidth > scale_value:
        new_width = int(scale_value)
        new_height = int(new_width * imgHeight / imgWidth)

        img = img.resize((new_width, new_height), Image.ANTIALIAS)

        print('Resize width')
        img.save(f'{file_path}', 'JPEG')
    
    if imgHeight > imgWidth and imgHeight > scale_value:
        new_height = int(scale_value)
        new_width = int(new_height * imgWidth / imgHeight)

        img = img.resize((new_width, new_height), Image.ANTIALIAS)

        print('Resize height')
        img.save(f'{file_path}', 'JPEG')

async def download_image(src, dir, i, scale_value):
    ErrorLevel = 0
    failed = False
    filename = src.split('/')[-1]
    if dir[-1] != "/":
        dir += "/"
    savedir = dir + filename
    src = src.replace("/236x/", "/originals/").replace("/474x/", "/originals/").replace("/736x/", "/originals/")
    while True:
        try:
            request = requests.get(src)
            # If status code is not 200, skip this image
            # Maybe this cause 403 Error, but I don't know how to handle it
            # assert request.status_code == 200
            if request.status_code != 200:
                print(f"Download {src} fail!")
                return True
           
            if scale_value:
                resize_image(request.content, savedir, scale_value)
                print(f"Download {src} done!")
            else: 
                with open(savedir, 'wb') as file:
                    file.write(request.content)
                print(f"Download {src} done!")
            break
        except Exception as e:
            print(f"{src} : Download fail! Error: {e}")
            ErrorLevel += 1
            sleep(1)
            if (ErrorLevel >= 10):
                failed = True
                print(src + ": Download fail, Skip image")
                break
    return failed


async def download_image_host(plist, dir):
    fail_image = 0
    fts = [asyncio.ensure_future(download_image(plist[i], dir, i, 1000)) for i in range(0, len(plist))]
    fail_image = await asyncio.gather(*fts)
    return fail_image

