from selenium import webdriver
import requests
import os
import argparse
import shutil
from selenium.webdriver.common.by import By


dir_name="Data-test"

# Create an argument parser to handle the flag
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--delete', action='store_true', help='Delete the data directory')
args = parser.parse_args()

# Delete the data directory if the flag is provided
if args.delete:
    shutil.rmtree(dir_name)

# Set up the Selenium webdriver (make sure you have the appropriate browser driver installed)
driver = webdriver.Chrome()

# Navigate to the website
driver.get("https://texample.net/tikz/examples/")

# Get feature header
features_header = driver.find_element(By.ID, "features")

# Get features section
features_section = features_header.find_element(By.XPATH, '..')

# Find all link elements within the features section
link_elements = features_section.find_elements(By.TAG_NAME, "a")

for feature in link_elements:
    # Navigate to the feature page
    driver.get(feature.get_attribute("href"))

    # Get feature header
    gallery = driver.find_element(By.CLASS_NAME, "gallery")

    # Find all examples within the features section
    examples = gallery.find_elements(By.TAG_NAME, "dt")

    for example in examples:
        # Find all examples within the features section
        link_example = example.find_elements(By.TAG_NAME, "a")

        driver.get(link_example[0].get_attribute("href"))

        # Get Image
        image_element = driver.find_elements(By.CLASS_NAME, "galleryimage")[0]
        image_element = image_element.find_elements(By.TAG_NAME, "img")[0]

        image_url = image_element.get_attribute('src')

        # Create a directory to store the downloaded images
        if not os.path.exists(os.path.join(dir_name, 'images')):
            os.makedirs(os.path.join(dir_name, 'images'))

        # Get the name
        image_name = os.path.basename(image_url)

        # Download the image using requests
        response = requests.get(image_url)

        # Save the image to a file
        with open(os.path.join(dir_name, f'images/{image_name}'), 'wb') as file:
            file.write(response.content)




# Download and save each image
for index, element in enumerate(image_elements):
    # Get the source URL of the image
    image_url = element.get_attribute('src')

    # Download the image using requests
    response = requests.get(image_url)

    # Save the image to a file
    with open(f'images/image{index}.jpg', 'wb') as file:
        file.write(response.content)

# Close the browser
driver.quit()