#!/usr/bin/env python
# coding: utf-8

# In[3]:


import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import qrcode

def create_info_image(title, regular_price, image_data, sale_price, url):
    
    img = Image.new('RGB', (800, 500), color='white')

    d = ImageDraw.Draw(img)
    
    local_image_path = r"C:\Users\nitin\Downloads\download.jpg"
    
    try:
        local_image = Image.open(local_image_path)
        local_image.thumbnail((150, 150))  
        img.paste(local_image, (300, 10))  # Adjust the paste position of the local image
    except Exception as e:
        print("Error while pasting local image:", e)

    font = ImageFont.truetype("arial.ttf", 25)

    border_top_color = (255, 0, 0)  
    border_bottom_color = (0, 255, 0)
    border_left_color = (0, 0, 255)  
    border_right_color = (255, 255, 0) 
    border_width = 10  

    # Top border
    d.rectangle([(0, 0), (img.width - 1, border_width)], outline=border_top_color, width=border_width)
    # Bottom border
    d.rectangle([(0, img.height - border_width), (img.width - 1, img.height - 1)],
                outline=border_bottom_color, width=border_width)
    # Left border
    d.rectangle([(0, 0), (border_width, img.height - 1)], outline=border_left_color, width=border_width)
    # Right border
    d.rectangle([(img.width - border_width, 0), (img.width - 1, img.height - 1)],
                outline=border_right_color, width=border_width)

    d.text((20, 70), f"Title: {title}", fill=(0, 0, 0), font=font)
    d.text((20, 100), f"Regular Price: {regular_price}", fill=(0, 0, 0), font=font)
    d.text((20, 130), f"Sale Price: {sale_price}", fill=(255, 0, 0), font=font)
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=2,
        border=1.5,
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    img.paste(qr_img, (20, 160))

    if image_data:
        try:
            max_width = 600
            max_height = 300
            image = Image.open(BytesIO(image_data))
            image.thumbnail((max_width, max_height))
            img.paste(image, (300, 130))
        except Exception as e:
            print("Error:", e)

    img.save("extracted_info_with_resized_image.png")

url = input()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.5",
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('h1', attrs={'class': 'single-product-title'}).text.strip()
    regular_price = soup.find('span', attrs={'id': 'regular-price'}).text.strip()
    image_url = soup.find('img', attrs={'class': 'single-product-img'}).get('src')
    sale_price = soup.find('span', attrs={'id': 'sale-price'}).text.strip()

    if image_url:
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            image_data = image_response.content
        else:
            image_data = None
    else:
        image_data = None

    create_info_image(title, regular_price, image_data, sale_price, url)
    print("Image with extracted information and resized image saved as 'banner.png'")
else:
    print("Failed to fetch the content.")


# In[ ]:




