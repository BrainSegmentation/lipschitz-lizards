# lipschitz-lizards

labelme.py instructions:
    format: python3 labelimage.py <type> <arguments> -i <image file> -s <scale>
    scale is optional parameter set to 3
    if type is "txt":
    format: python3 labelimage.py txt -m <magnet.txt> -t <tissue.txt> ...
    if type is "labelme":
    format: python3 labelimage.py labelme -j <labels.json> ...

Currently, all output files are generated in the output directory. It would be
easy to make it output them somewhere else with other names, at the potential
cost of having more command line arguments.
