from PIL import Image
import numpy as np
import os

# image resizing code starts here
#pulls image
imagePath = 'frontend\Images\Medicai.png'

try:
    img = Image.open(imagePath)
    filename = os.path.basename(imagePath)
except FileNotFoundError:
    # Create a new image if file doesn't exist (example)
    image = Image.new("RGB", (100, 100), color="blue")
    filename = "default_image.jpg"  # Define a custom filename for new images


# img.size and .format can get the properties of the image (it shouldn't matter too much..??)
desiredLength = 28
desiredWidth = 28
desiredDimension = (desiredLength, desiredWidth)

#prints the image and show() displays it
img = img.resize(desiredDimension)
img.show()

#saves the image into new folder
savePath = 'backend\savedImages'
os.makedirs(savePath, exist_ok=True)
savePath = os.path.join(savePath, imagePath)
print('image saved to: {savePath}')

#convert to an array
imageArray = np.array(img)
print(imageArray)
print("Array:", imageArray.shape)