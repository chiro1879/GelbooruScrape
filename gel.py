from pygelbooru import Gelbooru
from dotenv import load_dotenv
import requests
import asyncio
import os

load_dotenv()

# Gelbooru('API_KEY', 'USER_ID')
gelbooru = Gelbooru(os.getenv("API_KEY"), os.getenv("USER_ID"))
tags = os.getenv('tags', '')
tags = tags.split(',')
exclude_tags = os.getenv('exclude_tags', '')
exclude_tags = exclude_tags.split(',')
mode = 'debug' # Possible Modes: randomdown, batchdown, randomlink, batchlink

async def fileex(filename):
    for root, dirs, files in os.walk("."):
        if filename in files:
            return os.path.join(root, filename)
    return None

async def download_file(url):
    filename = os.path.basename(url)
    
    fileexist = await fileex(filename)
    
    if fileexist is None:
        response = requests.get(url)

        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f"File downloaded: {filename}")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
    else:
        print("File already exists in " + fileexist)

async def main():
    print("Searching for posts with tags: "+ str(tags))
    match mode:
        case 'randomdown':
            results = await gelbooru.random_post(tags=tags, exclude_tags=exclude_tags)
            print("Downloading "+str(x))
            await download_file(str(x))
        case 'batchdown':
            t = -1
            results = await gelbooru.search_posts(tags=tags, exclude_tags=exclude_tags, page=0)
            loop = True
            while loop == True:
                t = t+1
                results = await gelbooru.search_posts(tags=tags, exclude_tags=exclude_tags, page=t)
                print(str(len(results))+" Posts found")
                if len(results) == 0:
                    loop = False
                else:
                    for x in results:
                        print(str(x))
                        await download_file(str(x))
        case 'randomlink':
            results = await gelbooru.random_post(tags=tags, exclude_tags=exclude_tags)
            print(str(x))
        case 'batchlink':
            t = -1
            results = await gelbooru.search_posts(tags=tags, exclude_tags=exclude_tags, page=0)
            loop = True
            while loop == True:
                t = t+1
                results = await gelbooru.search_posts(tags=tags, exclude_tags=exclude_tags, page=t)
                if len(results) == 0:
                    loop = False
                else:
                    for x in results:
                        print(str(x))
        case 'debug':
            print("The program will now output debug info")
            print(os.getenv("API_KEY"), os.getenv("USER_ID"))
            print(tags)
            print(exclude_tags)
        case _:
            print("Mode incorrectly set")

    print("Done! Enjoy your stuff!")
          
asyncio.run(main())