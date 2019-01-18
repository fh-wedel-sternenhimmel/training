import glob, os
from PIL import Image
from xml.dom import minidom

process_id = 1
process_dirs = [
    "./Positiv/OnePersonPositivLeft/",
    "./Positiv/OnePersonPositiveRight/",
    "./Negativ/OnePersonNegativLeft/",
    "./Positiv/TwoPositiveLeft/",
    "./Positiv/TwoPositiveRight/",
    "./Positiv/21_09/",
    "./Positiv/TestBilderTemp_21-09/",
    "./training_1/",
    "./training_2/"
]

# Directory where the data will reside, relative to 'darknet.exe'
path_data = 'data/trainingset/'

# Percentage of images to be used for the test set
percentage_test = 10

# Create and/or truncate train.txt and test.txt
file_train = open('./trainingset/train.txt', 'a+')
file_test = open('./trainingset/test.txt', 'a+')

counter = 1
index_test = round(100 / percentage_test)
for process_dir in process_dirs:
    for pathAndFilename in glob.iglob(os.path.join(process_dir, "*.png")):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))

        if os.path.exists(process_dir + title + '.xml') == False:
            continue

        # Convert JPG
        im = Image.open(pathAndFilename)
        rgb_im = im.convert('RGB')
        rgb_im.save('./trainingset/' + str(process_id).zfill(5) + '.jpg')

        # Read XML
        mydoc = minidom.parse(process_dir + title + '.xml')
        size = mydoc.getElementsByTagName('size')
        objects = mydoc.getElementsByTagName('object')

        # Calculate Format
        width = float(size[0].getElementsByTagName('width')[0].firstChild.data)
        height = float(size[0].getElementsByTagName('height')[0].firstChild.data)

        file = open('./trainingset/' + str(process_id).zfill(5) + '.txt', 'w')

        for obj in objects:
            name = obj.getElementsByTagName('name')[0].firstChild.data
            bndbox = obj.getElementsByTagName('bndbox')[0]
            xmin = float(bndbox.getElementsByTagName('xmin')[0].firstChild.data)
            ymin = float(bndbox.getElementsByTagName('ymin')[0].firstChild.data)
            xmax = float(bndbox.getElementsByTagName('xmax')[0].firstChild.data)
            ymax = float(bndbox.getElementsByTagName('ymax')[0].firstChild.data)

            dw = 1.0 / width
            dh = 1.0 / height
            x = ((xmin + xmax) / 2.0) * dw
            y = ((ymin + ymax) / 2.0) * dh
            w = (xmax - xmin) * dw
            h = (ymax - ymin) * dh

            if name == "hand":
                name = "0"
            # elif name == "head":
            #     name = "1"
            # elif name == "person":
            #     name = "2"
            else:
                continue

            file.write(name + " " + str(x) + " " + str(y) + " " + str(w) + " " + str(h) + "\n")

        file.close()

        if counter == index_test:
            counter = 1
            file_test.write(path_data + str(process_id).zfill(5) + '.jpg' + "\n")
        else:
            file_train.write(path_data + str(process_id).zfill(5) + '.jpg' + "\n")
            counter = counter + 1

        process_id += 1;
