#!/usr/local/anaconda3/bin/python3

from PIL import Image, ImageDraw
import sys
import re
import os
import tkinter as tk
from tkinter import messagebox

# Function to sort filenames with numbers
def sort_files_from_args(files):
    # Regex to match filenames with numbers, ignoring the extension
    number_pattern = re.compile(r'(\d+)')
    
    # Custom sorting key to extract the numeric part of the filename
    def extract_number(file_name):
        match = number_pattern.search(file_name)
        if match:
            return int(match.group(0))
        # If no number is found, return a high value to push non-numbered files to the end
        return float('inf')

    # Sort the files based on the extracted number
    sorted_files = sorted(files, key=extract_number)
    
    # Print the sorted file list
    print("Sorted files:")
    for file in sorted_files:
        print(file)
    
    # Extract the path from the first file (assuming all files are in the same directory)
    output_path = os.path.dirname(sorted_files[0]) if sorted_files else ''
    
    # Return sorted file list and the output path
    return sorted_files, output_path

# Function to rotate images
def rotate_image(image, degrees):
    return image.rotate(degrees, expand=True)

# Function to draw a dashed line
def draw_dashed_line(draw, start_pos, end_pos, dash_length=15, gap_length=10, line_width=2):
    total_length = ((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5
    dashes = int(total_length // (dash_length + gap_length))
    for i in range(dashes + 1):
        start = (
            start_pos[0] + i * (dash_length + gap_length) * (end_pos[0] - start_pos[0]) / total_length,
            start_pos[1] + i * (dash_length + gap_length) * (end_pos[1] - start_pos[1]) / total_length
        )
        end = (
            start[0] + dash_length * (end_pos[0] - start_pos[0]) / total_length,
            start[1] + dash_length * (end_pos[1] - start_pos[1]) / total_length
        )
        draw.line([start, end], fill=(204,204,204), width=line_width)

# Load PNG files (adjust filenames if needed)

if len(sys.argv) < 9:  # We need at least 8 files plus the script name
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showerror("Error", "Not enough files provided. Please provide at least 8 image files.")
    print("Usage: zine.py <file1> <file2> ... <file8>")
    sys.exit(1)
else:
    # Pass all arguments except the script name
    png_files, output_path = sort_files_from_args(sys.argv[1:])

# Load scissors image
has_scissors = True

try:
    # Attempt to open the image and convert it
    scissors_image = Image.open('scissors.png').convert('RGBA')
except FileNotFoundError:
    # Set the flag to False if the file is not found
    has_scissors = False

# Open images
images = [Image.open(png).convert('RGB') for png in png_files]

# Create a blank canvas with the appropriate size (assuming all images are the same size)
image_width, image_height = images[0].size

# Create a new blank image for the zine layout
canvas_width = image_width * 4  # 4 images side by side
canvas_height = image_height * 2  # 2 rows (top half and bottom half)

zine_canvas = Image.new('RGB', (canvas_width, canvas_height), (255, 255, 255))  # White background

# Paste the images for the bottom half (pages 1, 2, 3, 4) - normal orientation
zine_canvas.paste(images[1], (0, image_height))  # Page 1 (bottom-left)
zine_canvas.paste(images[2], (image_width, image_height))  # Page 2
zine_canvas.paste(images[3], (image_width * 2, image_height))  # Page 3
zine_canvas.paste(images[4], (image_width * 3, image_height))  # Page 4 (bottom-right)

# Rotate and paste the images for the top half (pages 8, 7, 6, 5) - 180 degrees rotation
zine_canvas.paste(rotate_image(images[0], 180), (0, 0))  # Page 8 (top-left, rotated)
zine_canvas.paste(rotate_image(images[7], 180), (image_width, 0))  # Page 7
zine_canvas.paste(rotate_image(images[6], 180), (image_width * 2, 0))  # Page 6
zine_canvas.paste(rotate_image(images[5], 180), (image_width * 3, 0))  # Page 5 (top-right, rotated)

# Draw the regular dotted lines between pages
draw = ImageDraw.Draw(zine_canvas)

# Set the spacing for dotted lines (e.g., every 10 pixels)
dot_spacing = 10
line_width = 1  # Fine line

# Draw horizontal dotted line between top and bottom halves
for x in range(0, canvas_width, dot_spacing):
    draw.line([(x, image_height), (x + dot_spacing / 2, image_height)], fill=(204,204,204), width=line_width)

# Draw vertical dotted lines between pages
for y in range(0, canvas_height, dot_spacing):
    draw.line([(image_width, y), (image_width, y + dot_spacing / 2)], fill=(204,204,204), width=line_width)
    draw.line([(image_width * 2, y), (image_width * 2, y + dot_spacing / 2)], fill=(204,204,204), width=line_width)
    draw.line([(image_width * 3, y), (image_width * 3, y + dot_spacing / 2)], fill=(204,204,204), width=line_width)

# Draw a dashed line between the top-right corner of page1 and the top-left corner of page4
start_pos = (image_width - 1, image_height)
end_pos = (image_width * 3, image_height)
draw_dashed_line(draw, start_pos, end_pos, dash_length=15, gap_length=10, line_width=2)

if (has_scissors):
    # Add the scissors image at both ends of the dashed line
    scissors_resized = scissors_image.resize((30, 30))  # Resize the scissors image

    # Paste scissors on the left, rotated 180 degrees and moved to the right by 20 pixels
    scissors_rotated = scissors_resized.rotate(180, expand=True)
    zine_canvas.paste(scissors_rotated, (image_width - 3, image_height - 15), scissors_rotated)

    # Paste scissors on the right, moved to the left by 20 pixels
    zine_canvas.paste(scissors_resized, (image_width * 3 - 25, image_height - 15), scissors_resized)

# Save the zine layout as a PDF with the new features
zine_canvas.save(os.path.join(output_path, 'zine_layout.pdf'), 'PDF')
