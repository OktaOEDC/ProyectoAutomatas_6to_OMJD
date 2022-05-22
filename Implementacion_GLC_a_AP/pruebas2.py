from operator import index
from PIL import Image, ImageFont, ImageDraw


qi = 'a'
qc = ['b','c','d']
qa = 'e'
my_image = Image.open('Implementacion_GLC_a_AP/AP_no_texto.png')
font = ImageFont.truetype("arial.ttf", 20)
image_editable = ImageDraw.Draw(my_image)
image_editable.text((225,150), qi, (12, 12, 13), font=font)
i = 0
while i < len(qc):
    image_editable.text((400,225+ (20*i)), qc[i], (12, 12, 13), font=font)
    i+=1
image_editable.text((225,400), qa, (12, 12, 13), font=font)
my_image.show()
my_image.save('Implementacion_GLC_a_AP/AP_texto.png')