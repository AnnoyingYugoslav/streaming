import requests
import shutil
import os
import time
import pytesseract
from PIL import Image
from gtts import gTTS

def makeUrl(afterID, subreddit):
    newUrl = subreddit.split('/.json')[0] + "/.json?after={}".format(afterID)
    return newUrl

def downloadImage(imageUrl, imageAmount, save_dir):
    filename = os.path.join(save_dir, "1")
    extension = imageUrl.split('.')[-1]  # Extract the file extension
    if filename:
        filename = f"{filename}.{extension}"  # Include the file extension
        r = requests.get(imageUrl, stream=True)
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
            print("Successfully downloaded: " + imageUrl)
            imageAmount += 1
    if extension != 'png':
        try:
            image = Image.open(filename)
            png_filename = os.path.splitext(filename)[0] + '.png'
            image.save(png_filename, 'PNG')
            print(f"Converted to PNG: {filename} -> {png_filename}")
        except Exception as e:
            print(f"Error converting to PNG: {filename} - {str(e)}")
    return imageAmount

def runDownload():
    subreddit = "https://www.reddit.com/r/memes/new"
    limit = 1
    subJson = ''
    x = 0
    while x < limit:
        if subJson:
            url = makeUrl(subJson['data']['after'], subreddit)
        else:
            url = makeUrl('', subreddit)
        subJson = requests.get(url, headers={'User-Agent': 'MyRedditScraper'}).json()
        post = subJson['data']['children']
        postCount = range(len(post))

        for i in postCount:
            imageUrl = (post[i]['data']['url'])
            _imageUrls = []
            _imageUrls.append(imageUrl)
            x = downloadImage(_imageUrls[0], x, r'C:\Users\16bit\Desktop\syf z pulpitu\syf')
            if x == limit:
                break
def textExtract(text):
    path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    path_to_image = 'C:\\Users\\16bit\\Desktop\\syf z pulpitu\\syf\\1.png'
    pytesseract.tesseract_cmd = path_to_tesseract
    img = Image.open(path_to_image)
    extracted_text = pytesseract.image_to_string(img)
    extracted_text = extracted_text.replace('\n', '')
    print(extracted_text)
    return extracted_text

def readLoud(mtext):
    language = 'en'
    myobj = gTTS(text=mtext, lang=language, slow=False)
    myobj.save("welcome.mp3")
    os.system("start wmplayer welcome.mp3")

while True:
    mytext = ""
    runDownload()
    time.sleep(5)
    mytext = textExtract(mytext)
    time.sleep(15)
    print(mytext)
    if mytext != "":
        readLoud(mytext)
    time.sleep(5)