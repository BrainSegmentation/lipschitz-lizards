import json
import os
import sys
import labelme
import pandas as pd
import numpy as np
from PIL import Image


# format: python3 labelimage.py <type> <arguments> -i <image file> -s <scale>
# scale is optional parameter set to 3
# if type is "txt":
# format: python3 labelimage.py txt -m <magnet.txt> -t <tissue.txt> ...
# if type is "labelme":
# format: python3 labelimage.py labelme -j <labels.json> ...


# Splits list into list of ordered pairs. For example:
# [1, 2, 3, 4] => [[1, 2], [3, 4]]
def to_pairs(l):
    """Yield successive pairs from l"""
    for i in range(0, len(l), 2):
        yield l[i:i + 2]


# Converts magnet and tissue text files, and an image file location,
# to a labelme json file. Writes to labels.json
def txtToJson(magnet, tissue, image):
    print("Converting text file to json...")
    f = {}
    f["imagePath"] = image
    f["shapes"] = []

    for i in range(len(magnet)):
        shape = {}
        shape["line_color"] = None
        shape["points"] = list(to_pairs(magnet[i]))
        shape["fill_color"] = None
        shape["label"] = "magnet-" + str(i + 1)
        f["shapes"].append(shape)

    for i in range(len(tissue)):
        shape = {}
        shape["line_color"] = None
        shape["points"] = list(to_pairs(tissue[i]))
        shape["fill_color"] = None
        shape["label"] = "tissue-" + str(i + 1)
        f["shapes"].append(shape)

    f["imageData"] = None
    f["lineColor"] = [0, 255, 0, 128]
    f["fillColor"] = [255, 0, 0, 128]

    with open("labels.json", "w+") as outfile:
        outfile.write(json.dumps(f, indent=4))

    print("Converted text file to json")
    return f


# Generates mask bitmaps from json file and image location. Creates masks
# in masks folder of current directory.
def jsonToMasks(f, image):
    if not os.path.isdir("masks"):
        os.mkdir("masks")

    print("Creating mask bitmaps from json...")

    img = np.array(Image.open(image))

    # Loop through all objects and create masks
    for shape in f["shapes"]:
        points = shape["points"]
        mask = labelme.utils.shape_to_mask(img.shape[:2], points)

        size = mask.shape[::-1]
        databytes = np.packbits(mask, axis=1)
        mask = Image.frombytes(mode='1', size=size, data=databytes)
        mask.save('masks/' + shape["label"] + ".bmp")

    print("Created mask bitmaps from json")


# NOTE: won't return same coordinates as original due to integer rounding
# Given json file as dictionary and scale, converts to magnet and tissue
# text data.
def jsonToTxt(f, scale):
    magnet = open('magnets.txt', 'w')
    tissue = open('tissue.txt', 'w')

    scale = 3

    # write magnets
    for i in range(len(f["shapes"]) // 2):
        shape = f["shapes"][i]
        points = shape["points"]
        magnet.write(str(points[0][0]*scale)+','+ str(points[0][1]*scale))
        for point in points[1:]:
            magnet.write('\t')
            magnet.write(str(point[0]*scale)+','+ str(point[1]*scale))
        magnet.write('\n')

    # write tissues
    for i in range(len(f["shapes"]) // 2, len(f["shapes"])):
        shape = f["shapes"][i]
        points = shape["points"]
        tissue.write(str(points[0][0]*scale)+','+ str(points[0][1]*scale))
        for point in points[1:]:
            tissue.write('\t')
            tissue.write(str(point[0]*scale)+','+ str(point[1]*scale))
        tissue.write('\n')


# Reads in data from command line arguments for txt files
def createFromTxt():
    if len(sys.argv) != 8 and len(sys.argv) != 10:
        raise ValueError("Invalid number of arguments!")

    magnet = ""
    tissue = ""
    image = ""
    scale = -1

    for i in range(2, len(sys.argv), 2):
        arg = sys.argv[i]
        if (arg == "-m" and magnet == ""):
            magnet = pd.read_csv(sys.argv[i + 1], sep="\t|,", header=None,\
                                 engine='python')
        elif (arg == "-t" and tissue == ""):
            tissue = pd.read_csv(sys.argv[i + 1], sep="\t|,", header=None,\
                                 engine='python')
        elif (arg == "-i" and image == ""):
            image = sys.argv[i + 1]
        elif (arg == "-s" and scale == -1):
            scale = int(sys.argv[i])
        else:
            raise ValueError("Invalid argument error on " + arg)

    if scale == -1:
        scale = 3

    magnet = magnet // scale
    tissue = tissue // scale
    magnet = magnet.values.tolist()
    tissue = tissue.values.tolist()

    f = txtToJson(magnet, tissue, image)
    jsonToMasks(f, image)


# Reads in data from command line arguments for json files
def createFromJson():
    if len(sys.argv) != 6 and len(sys.argv) != 8:
        raise ValueError("Invalid number of arguments!")

    f = ""
    image = ""
    scale = -1

    for i in range(2, len(sys.argv), 2):
        arg = sys.argv[i]
        if (arg == "-j" and f == ""):
            f = json.load(open(sys.argv[i + 1]))
        elif (arg == "-i" and image == ""):
            image = sys.argv[i + 1]
        elif (arg == "-s" and scale == -1):
            scale = int(sys.argv[i])
        else:
            raise ValueError("Invalid argument error on " + arg)

    if scale == -1:
        scale = 3

    jsonToTxt(f, scale)
    jsonToMasks(f, image)


def main():
    if len(sys.argv) < 6:
        if len(sys.argv) == 2 and sys.argv[1] == "help":
            print("""format: python3 labelimage.py <type> <arguments> -i <image file> -s <scale>
        scale is optional parameter set to 3
        if type is "txt":
        format: python3 labelimage.py txt -m <magnet.txt> -t <tissue.txt> ...
        if type is "labelme":
        format: python3 labelimage.py labelme -j <labels.json> ...""")
            sys.exit()
        else:
            raise ValueError("Invalid number of arguments!")

    if sys.argv[1] == "txt":
        createFromTxt()
    elif sys.argv[1] == "labelme":
        createFromJson()
    else:
        raise ValueError("Type must be \"txt\" or \"labelme\"!")


if __name__ == "__main__":
    main()

