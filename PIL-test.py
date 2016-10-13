from PIL import Image, ImageFont, ImageDraw

img = Image.open('1151067.jpg')

draw = ImageDraw.Draw(img)

font = ImageFont.truetype('DejaVuSerif.ttf',35)

sample_text = 'It\'s not a twist-off!\n( grunting): Come on!'
draw.text((25, 500),sample_text,(255,255,255), font = font)

img.save('1151067-new.jpg')