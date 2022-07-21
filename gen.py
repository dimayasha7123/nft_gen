from typing import Dict
from PIL import Image
import yaml
import os


with open('probs.yaml', 'rb') as file:
    probs = yaml.load(file, yaml.Loader)

export_path = r'./export/'
output_path = r'./output/'


fileList = os.listdir(export_path)

imageDict = dict()
for file in fileList:
    imageDict[file[0:len(file)-4]] = Image.open(export_path + file)


# l1 = Image.open("./export3/Баллончик-краски.png")
# l2 = Image.open("./export3/Кисть-для-предмета.png")

# output = Image.new("RGBA", l1.size)
# output = Image.alpha_composite(output, l1)
# output = Image.alpha_composite(output, l2)

# output.save("./output/test1.png")