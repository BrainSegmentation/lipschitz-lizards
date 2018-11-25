import json
import os
import sys

# format: python3 labelimage.py image.tif magnet_file.txt tissue_file.txt output.json
if len(sys.argv) != 5:
    raise ValueError("Invalid number of arguments")

magnet_file = open(sys.argv[2], 'r')
tissue_file = open(sys.argv[3], 'r')
output = open(sys.argv[4], 'w+')

magnet_lines = magnet_file.readlines()
tissue_lines = tissue_file.readlines()

def label(magnet_lines, tissue_lines, output):
    # write json header
    output.write("{\n")
    output.write('\"imagePath\": \"' + sys.argv[1] + '\",\n')
    output.write('\"shapes\": [\n')
    output.write('    {\n')
    output.write('      \"line_color\": null,\n')
    output.write('\"points\": [\n')

    # write coordinates for magnets
    line = magnet_lines[0]
    line = line.split('\t')[0:-1]
    for coord in line[0:-1]:
        coords = coord.split(",")
        output.write("\t[\n")
        output.write("\t    " + str(int(coords[0]) / 3) + ",\n")
        output.write("\t    " + str(int(coords[1]) / 3))
        output.write("\t],\n")
    coord = line[-1].split(",")
    output.write("\t[\n")
    output.write("\t    " + str(int(coord[0]) / 3) + ",\n")
    output.write("\t    " + str(int(coord[1]) / 3))
    output.write("\t]\n")
    output.write("],\n")
    output.write("\"fill_color\": null,\n")
    output.write("\"label\": \"magnet-1\"\n")
    output.write("}")

    # write remainder of magnet coordinates
    for i in range(1, len(magnet_lines)):
        line = magnet_lines[i]
        output.write(",\n")
        output.write('    {\n')
        output.write('      \"line_color\": null,\n')
        output.write('\"points\": [\n')
        line = line.split('\t')[0:-1]
        for coord in line[0:-1]:
            coords = coord.split(",")
            output.write("\t[\n")
            output.write("\t    " + str(int(coords[0]) / 3) + ",\n")
            output.write("\t    " + str(int(coords[1]) / 3))
            output.write("\t],\n")
        coord = line[-1].split(",")
        output.write("\t[\n")
        output.write("\t    " + str(int(coord[0]) / 3) + ",\n")
        output.write("\t    " + str(int(coord[1]) / 3))
        output.write("\t]\n")
        output.write("],\n")
        output.write("\"fill_color\": null,\n")
        output.write("\"label\": \"magnet-" + str(i + 1) + "\"\n")
        output.write("}")

    # write tissue coordinates
    for i in range(len(tissue_lines)):
        line = tissue_lines[i]
        output.write(",\n")
        output.write('    {\n')
        output.write('      \"line_color\": null,\n')
        output.write('\"points\": [\n')
        line = line.split('\t')[0:-1]
        for coord in line[0:-1]:
            coords = coord.split(",")
            output.write("\t[\n")
            output.write("\t    " + str(int(coords[0]) / 3) + ",\n")
            output.write("\t    " + str(int(coords[1]) / 3))
            output.write("\t],\n")
        coord = line[-1].split(",")
        output.write("\t[\n")
        output.write("\t    " + str(int(coord[0]) / 3) + ",\n")
        output.write("\t    " + str(int(coord[1]) / 3))
        output.write("\t]\n")
        output.write("],\n")
        output.write("\"fill_color\": null,\n")
        output.write("\"label\": \"tissue-" + str(i + 1) + "\"\n")
        output.write("}")

    output.write("],\n")
    output.write('\"imageData\": null,\n')
    output.write("\"lineColor\": [\n")
    output.write("0, 255, 0, 128 ],\n")
    output.write("\"fillColor\": [\n")
    output.write("""    255,
        0,
        0,
        128
      ]
    }""")
    output.close()

label(magnet_lines, tissue_lines, output)
