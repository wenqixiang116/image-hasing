from image_hashing import whash, colorhash
from PIL import Image
import numpy as np

# Create a dummy image
img = Image.new('RGB', (100, 100), color='red')
print(f"ColorHash: {colorhash(img)}")
print(f"WHash: {whash(img)}")
