import os
import random
from datetime import datetime
from PIL import Image, ImageEnhance

# Base directory (where this script is located)
base_dir = os.path.dirname(os.path.abspath(__file__))
input_dir = os.path.join(base_dir, "icons")     # Directory containing input icons
output_dir = os.path.join(base_dir, "results")  # Directory for saving generated wallpapers

# Create the output directory if it does not exist
os.makedirs(output_dir, exist_ok=True)

# Parameters
# --------------------------------------------------------
# wallpaper_width  : Width of the generated wallpaper
# wallpaper_height : Height of the generated wallpaper
# icon_size        : Size (in pixels) to which each icon will be resized
# icon_angle       : Rotation angle (applied uniformly to all icons)
# spacing          : Distance between icon centers in the grid
# --------------------------------------------------------
wallpaper_width = 3840
wallpaper_height = 2160
icon_size = 130
icon_angle = -20
spacing = 220

# Generate output filename with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = os.path.join(output_dir, f"{timestamp}_wallpaper.png")

# Load icons from the input directory
icons = []
for f in os.listdir(input_dir):
    if f.lower().endswith(".png"):
        icons.append(os.path.join(input_dir, f))

# Create background (purple tone)
wallpaper = Image.new("RGB", (wallpaper_width, wallpaper_height), "#cc77dd")

# Determine number of rows and columns
rows = wallpaper_height // spacing + 2
cols = wallpaper_width // spacing + 2
used_icons = set()

# Place icons on the wallpaper
for row in range(rows):
    for col in range(cols):
        # Prevent adjacent duplicates by temporarily tracking used icons
        available_icons = [i for i in icons if i not in used_icons]
        if not available_icons:
            used_icons.clear()
            available_icons = icons[:]
        icon_path = random.choice(available_icons)
        used_icons.add(icon_path)

        # Process the icon (resize and rotate)
        with Image.open(icon_path).convert("RGBA") as icon:
            icon = icon.resize((icon_size, icon_size), Image.LANCZOS)
            icon = icon.rotate(icon_angle, expand=True)

            # Checkerboard pattern: shift every other row by half the spacing
            x_offset = (spacing // 2) if row % 2 else 0

            x = col * spacing + x_offset
            y = row * spacing
            wallpaper.paste(icon, (x, y), icon)

# Slightly reduce saturation (e.g., 80%)
enhancer = ImageEnhance.Color(wallpaper)
wallpaper = enhancer.enhance(0.8)

# Save the wallpaper
wallpaper.save(output_file)
print(f"Wallpaper saved: {output_file}")