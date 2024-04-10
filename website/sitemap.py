import os
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
from xml.dom import minidom

# Define the directory containing the HTML files
directory = "E:/WIKIPRJ/website/templates"

# Define the base URL of your website
base_url = "https://www.solulu4u.com/"

# Create the root element of the sitemap
urlset = Element('urlset', {'xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9'})

# Iterate over each file in the directory
for filename in os.listdir(directory):
    # Check if the file is an HTML file
    if filename.endswith(".html"):
        # Create a new URL element
        url = SubElement(urlset, 'url')

        # Add the loc (location) element
        loc = SubElement(url, 'loc')
        loc.text = base_url + filename[:-5]  # Remove the .html extension

        # Add the lastmod (last modified) element
        lastmod = SubElement(url, 'lastmod')
        lastmod.text = '2024-04-01'  # You may want to replace this with the actual last modified date

        # Add the changefreq (change frequency) element
        changefreq = SubElement(url, 'changefreq')
        changefreq.text = 'weekly'

        # Add the priority element
        priority = SubElement(url, 'priority')
        priority.text = '0.8'

# Create a new XML tree from the root element
tree = ElementTree(urlset)

# Write the XML tree to a file
tree.write("sitemap.xml", encoding='utf-8', xml_declaration=True)

# Print a success message
print("Sitemap has been successfully created and saved as sitemap.xml")
