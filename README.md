# lipschitz-lizards

labelme.py instructions:

    Example calls:
    
    python labelimage.py magnets.txt tissues.txt image.tif
    python labelimage.py magnets.txt tissues.txt image.tif -j labels.json -s 3 ...

Takes an image path, as well as its corresponding magnet and tissue text files,
and constructs a labelme-compatible json file.
