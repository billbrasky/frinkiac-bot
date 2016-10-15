import requests
import smtplib as smtp
from pprint import pprint
from PIL import Image, ImageFont, ImageDraw
import shutil
import requests

# gets quote and image from frinkiac
def get_quote():
    r = requests.get("https://morbotron.com/api/random")
    # Check if our request had a valid response.
    if r.status_code == 200:
        json = r.json()
        pprint(json)
        # Extract the episode number and timestamp from the API response
        # and convert them both to strings.
        timestamp, episode, _ = map(str, json["Frame"].values())
        
        localFileName = episode+'-'+timestamp
        image_url = "https://morbotron.com/meme/" + episode + "/" + timestamp
        # Combine each line of subtitles into one string.
        caption = "\n".join([subtitle["Content"] for subtitle in json["Subtitles"]])
        
        return image_url, caption, localFileName


# saves image to local directory
def save_image(media, localImage):

    response = requests.get(media, stream = True)

    with open(localImage + '.jpg', 'wb') as f:
        shutil.copyfileobj(response.raw, f)


# saves a new image with quote
def make_meme(quote, localImage):
    newLineCount = len(quote.split('\n'))
    textFont = ImageFont.truetype('Simpsonfont.ttf',35)
    img = Image.open(localImage + '.jpg')
    width, height = img.size
    draw = ImageDraw.Draw(img)
    deltaFont = 0
    textWidth, textHeight =  draw.multiline_textsize(quote, font = textFont)
    
    while textWidth < width/2 and textHeight < height/2:
        deltaFont += 5
        textFont = ImageFont.truetype('Simpsonfont.ttf', 35 + deltaFont)
        textWidth, textHeight =  draw.multiline_textsize(quote, font = textFont)
    while textWidth > width:
        deltaFont -= 5
        textFont = ImageFont.truetype('Simpsonfont.ttf', 35 + deltaFont)
        textWidth, textHeight =  draw.multiline_textsize(quote, font = textFont)
    
    baseX, baseY = ((width - textWidth)/2 , height - (20 + textHeight + newLineCount * 20) )
    shadowcolor = 'black'
    
    delta = 2
    for x in [-1, 1, 0]:
        for y in [1, -1, 0]:
            posX = baseX + delta*x
            posY = baseY + delta*y
            draw.multiline_text((posX, posY), quote, font=textFont, fill=shadowcolor, align = 'center', spacing = 20)
    
    draw.multiline_text((baseX, baseY), quote, font = textFont, align = 'center', spacing = 20)
    
    img.save(localImage + '-quoted.jpg')




media, quote, localImage = get_quote()
save_image(media, localImage)
make_meme(quote, localImage)
