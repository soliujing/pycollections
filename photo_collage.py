from PIL import Image
import os

# input folder containing the images
input_folder = "/Users/jing_liu/Downloads/in"

# output folder to store the collage pages
output_folder = "/Users/jing_liu/Downloads/out"

# image size in pixels for A4 size paper (210 x 297 mm) at 300 DPI
image_width = 2480
image_height = 3508

# number of images per collage page
num_images_per_page = 6

# margin between the images in pixels
margin = 20

# get all image files from the input folder
image_files = [f for f in os.listdir(input_folder) if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png')]

# calculate the number of pages required based on the number of images
num_pages = len(image_files) // num_images_per_page + (1 if len(image_files) % num_images_per_page > 0 else 0)

# loop through each page
for page_num in range(num_pages):
    # create a blank image for the page
    page_image = Image.new('RGB', (image_width, image_height), color='white')

    # loop through each image on the page
    for i in range(num_images_per_page):
        # calculate the index of the image in the image files list
        image_index = page_num * num_images_per_page + i

        # check if the index is valid
        if image_index < len(image_files):
            # load the image from the input folder
            image_path = os.path.join(input_folder, image_files[image_index])
            image = Image.open(image_path)

            # calculate the size of the image after adding the margin
            new_width = image_width // 3 - margin * 2
            new_height = image_height // 2 - margin * 2
            
            # Determine orientation of image (portrait or landscape)
            if image.size[0] > image.size[1]:
                # Landscape image
                image = image.rotate(270, expand=True)  # Rotate to portrait orientation

            # resize the image while keeping the aspect ratio
            image.thumbnail((new_width, new_height))

            # calculate the position of the image on the page
            x_offset = (i % 3) * (new_width + margin) + margin
            y_offset = (i // 3) * (new_height + margin) + margin

            # paste the image onto the page
            page_image.paste(image, (x_offset, y_offset))
    
    # save the collage page in the output folder
    page_path = os.path.join(output_folder, f"collage_{page_num+1}.jpg")
    page_image.save(page_path)
