# Original made by Reegan Alward

import PIL
from PIL import Image, ImageDraw

#Custom function for eye styling. These create the eye masks

def style_inner_eyes(img):
  img_size = img.size[0]
  eye_size = 70 #default
  quiet_zone = 40 #default
  mask = Image.new('L', img.size, 0)
  draw = ImageDraw.Draw(mask)
  draw.rectangle((60, 60, 90, 90), fill=255) #top left eye
  draw.rectangle((img_size-90, 60, img_size-60, 90), fill=255) #top right eye
  draw.rectangle((60, img_size-90, 90, img_size-60), fill=255) #bottom left eye
  return mask

def style_outer_eyes(img):
  img_size = img.size[0]
  eye_size = 70 #default
  quiet_zone = 40 #default
  mask = Image.new('L', img.size, 0)
  draw = ImageDraw.Draw(mask)
  draw.rectangle((40, 40, 110, 110), fill=255) #top left eye
  draw.rectangle((img_size-110, 40, img_size-40, 110), fill=255) #top right eye
  draw.rectangle((40, img_size-110, 110, img_size-40), fill=255) #bottom left eye
  draw.rectangle((60, 60, 90, 90), fill=0) #top left eye
  draw.rectangle((img_size-90, 60, img_size-60, 90), fill=0) #top right eye
  draw.rectangle((60, img_size-90, 90, img_size-60), fill=0) #bottom left eye
  return mask

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer,VerticalBarsDrawer,SquareModuleDrawer
from  qrcode.image.styles.colormasks import SolidFillColorMask


border=0
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, border=border)

qr.add_data("MECARD:N:{lastname_txt.value},{name_txt.value};NICKNAME:{nickname_txt.value};TEL:{work_phone_txt.value};TEL:{priv_phone_txt.value};TEL:{phone_txt.value};EMAIL:{mail_txt.value};BDAY:{self.birthday};URL:{url_txt.value}NOTE:{filled_txt.value};ADR:,,{street_txt.value},{city_txt.value},{state_txt.value},{zip_txt.value},{country_txt.value};;")

qr_inner_eyes_img = qr.make_image(image_factory=StyledPilImage,
                            eye_drawer=RoundedModuleDrawer(radius_ratio=1),
                            color_mask=SolidFillColorMask(back_color=(1, 255, 1), front_color=(63, 42, 86)))

qr_outer_eyes_img = qr.make_image(image_factory=StyledPilImage,
                            eye_drawer=VerticalBarsDrawer(),
                            color_mask=SolidFillColorMask(back_color=(1, 1, 1), front_color=(255, 128, 0)))

qr_img = qr.make_image(image_factory=StyledPilImage,
                       module_drawer=SquareModuleDrawer(), color_mask=SolidFillColorMask(back_color=(1, 0, 0), front_color=(255, 255, 255)))

inner_eye_mask = style_inner_eyes(qr_img)
outer_eye_mask = style_outer_eyes(qr_img)

intermediate_img = Image.composite(qr_inner_eyes_img, qr_img, inner_eye_mask)
final_image = Image.composite(qr_outer_eyes_img, intermediate_img, outer_eye_mask)
final_image.save('final_eyes_image.png')