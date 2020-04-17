from pathlib import Path
from PIL import Image
import os
import shutil

size = 300, 300
source = '/Users/fi241c/dev/machine-learning/ml-capstone/original-images'
destination = '/Users/fi241c/dev/machine-learning/ml-capstone/images'

if os.path.exists(destination) and os.path.isdir(destination):
    print('Deleting destination folder' + destination)
    shutil.rmtree(destination)


Path(destination).mkdir(parents=True, exist_ok=True)

entries = os.listdir(source)
for img in entries:
  if not os.path.isfile(source + "/" + img):
    print('Skipping directory ' + source + "/" + img)
    continue

  print ('Working on ' + source + "/" + img)
  im = Image.open(source + "/" + img)
  im_resized = im.resize(size)
  im_resized.save(destination + "/"+ img)
