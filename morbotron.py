import requests
import smtplib as smtp
from pprint import pprint
from PIL import Image, ImageFont, ImageDraw
import shutil
import requests

# gets quote and image from frinkiac
def get_quote():
    res = {}
    r = requests.get("https://morbotron.com/api/random")
    # Check if our request had a valid response.
    if r.status_code == 200:
        json = r.json()
        pprint(json)
        image_urls = []
        caption = "\n".join([subtitle["Content"] for subtitle in json["Subtitles"]])
        res.update({'quote': caption})
        for nearby in json["Nearby"]:
            nearby_episode = str(nearby['Episode'])
            nearby_timestamp = str(nearby['Timestamp'])
            image_url = nearby_episode + '/' + nearby_timestamp
            
            image_urls.append(image_url)

        res.update({'images': image_urls})
        # Extract the episode number and timestamp from the API response
        # and convert them both to strings.
#        timestamp, episode, _ = map(str, json["Frame"].values())
#        localFileName = episode+'-'+timestamp
        # Combine each line of subtitles into one string.
#        res_list.append()
        return res


# saves image to local directory
def save_image(media):
    url = 'https://morbotron.com/img/' + media
    response = requests.get(url, stream = True)

    with open('images/' + '-'.join(media.split('/')) + '.jpg', 'wb') as f:
        shutil.copyfileobj(response.raw, f)


# saves a new image with quote
def make_meme(quote, image):
    image = '-'.join(image.split('/'))
    newLineCount = len(quote.split('\n'))
    textFont = ImageFont.truetype('Simpsonfont.ttf',35)
    img = Image.open('images/'+image + '.jpg')
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
    
    img.save('images/'+image + '-quoted.jpg')


res = get_quote()

for image in res['images']:
    save_image(image)
make_meme(res['quote'], res['images'][3])
"""
r = requests.get('https://morbotron.com/api/caption?e=S03E04&t=432681')
json = r.json()

pprint(json)
"""