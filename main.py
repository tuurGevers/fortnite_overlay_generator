import os

from PIL import Image, ImageDraw, ImageFont
from math import ceil


def draw_description(title, draw, text, font, max_width, image_width, ):
    words = text.split(' ')
    if len(words) < 3 or len(title.split(" ")) > 2:  # If it's a single word or two words, split it in half
        text = text
    else:  # If there are more than two words, split near the middle
        split_index = ceil(len(words) / 2)
        first_half = " ".join(words[:split_index])  # Join the first half of the words
        second_half = " ".join(words[split_index:])  # Join the second half of the words
        text = first_half + "\n" + second_half

    # Center align the text
    text_position = (350, 850)
    text_anchor = "mm"

    # Draw the description text
    draw.multiline_text(text_position, text, font=font, fill="white", anchor=text_anchor)


def apply_gradient_with_manual_outline(base_image, text, font, position, gradient_colors, outline_thickness,
                                       outline_color, description_text, description_font, center_title=False):
    draw = ImageDraw.Draw(base_image)

    # Measure the size of the text to create a gradient and a mask
    text_size = draw.textsize(text, font=font)
    text_width, text_height = text_size

    # Center align the title text
    title_position = ((base_image.width - text_width) // 2, position[1])

    # Create the gradient for the text
    gradient = Image.new('RGBA', (text_width, text_height))
    for i in range(text_width):
        ratio = i / text_width
        r = ratio * gradient_colors[0] + (1 - ratio) * gradient_colors[1]
        g = ratio * gradient_colors[2] + (1 - ratio) * gradient_colors[3]
        b = ratio * gradient_colors[4] + (1 - ratio) * gradient_colors[5]
        for j in range(text_height):
            gradient.putpixel((i, j), (int(r), int(g), int(b), 255))

    # Create a mask for the text
    mask = Image.new('L', (text_width, text_height), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.text((0, 0), text, font=font, fill=255)

    # Create a temporary image for the outlined text
    temp_image = Image.new('RGBA', (text_width + outline_thickness * 2, text_height + outline_thickness * 2))
    temp_draw = ImageDraw.Draw(temp_image)

    # Draw text outline
    for adj in range(-outline_thickness, outline_thickness + 1):
        for adj_y in range(-outline_thickness, outline_thickness + 1):
            if adj != 0 or adj_y != 0:  # Skip the center position
                temp_draw.text((outline_thickness + adj, outline_thickness + adj_y), text, font=font,
                               fill=outline_color)

    # Draw the base text on top of the outline
    temp_draw.text((outline_thickness, outline_thickness), text, font=font, fill="white")

    # Apply the gradient to the text using the mask
    temp_image.paste(gradient, (outline_thickness, outline_thickness), mask)

    # Paste the outlined gradient text onto the base image at the desired position
    # Paste the outlined gradient text onto the base image at the desired position
    base_image.paste(temp_image, position, temp_image)

    # Call draw_description with image width
    draw_description(text, draw, description_text, description_font, text_size, base_image.width)

    return base_image


# Define the directory with input images and load the font
input_dir = 'input/'
output_dir = 'output/'
font_path = "currentfont.otf"
title_font_size = 68
description_font_size = 32
outline_thickness = 3
outline_color = "black"
position = (250, 750)  # Replace with the actual position

# Define your batch data
batch_data = [
    {"filename": "banana.png", "title": "Banana Peel", "description": "Slippery surprises await.", "gradient_colors": (255, 255, 0, 100, 100, 0)},
    {"filename": "boogie.png", "title": "Boogie Bandit", "description": "Dance the fight away.", "gradient_colors": (255, 105, 180, 100, 50, 100)},
    {"filename": "controller.png", "title": "Controller Steal", "description": "Seize the controls.", "gradient_colors": (0, 191, 255, 50, 50, 100)},
    {"filename": "esp.png", "title": "Hackerman", "description": "Master of digital realms.", "gradient_colors": (0, 255, 0, 0, 100, 0)},
    {"filename": "door.png", "title": "Door Knock", "description": "Phantom knocks deceive.", "gradient_colors": (128, 0, 128, 50, 0, 50)},
    {"filename": "fart.png", "title": "Fart Cushion", "description": "Emit a gaseous giggle.", "gradient_colors": (127, 255, 0, 50, 100, 50)},
    {"filename": "funny_gass.png", "title": "Funny Gas", "description": "Dizzying laughs ensue.", "gradient_colors": (255, 69, 0, 100, 69, 0)},
    {"filename": "geoguess.png", "title": "GeoGuesser", "description": "Random relocations.", "gradient_colors": (0, 206, 209, 50, 100, 100)},
    {"filename": "gnome.png", "title": "Gnomed", "description": "Tiny trickster's tease.", "gradient_colors": (255, 140, 0, 100, 60, 0)},
    {"filename": "invis_obj.png", "title": "Invisible Obstacle", "description": "Unseen barriers block.", "gradient_colors": (75, 0, 130, 25, 0, 65)},
    {"filename": "laugh grenade.png", "title": "Joke Grenade", "description": "Explosive laughter.", "gradient_colors": (255, 20, 147, 100, 20, 60)},
    {"filename": "magic.png", "title": "Magic Pockets", "description": "Pockets of disappointment.", "gradient_colors": (128, 128, 128, 50, 50, 50)},
    {"filename": "see.png", "title": "Now You See Me", "description": "Vanish and reappear.", "gradient_colors": (255, 255, 255, 100, 100, 100)},
    {"filename": "sneeze.png", "title": "Sneezing Powder", "description": "Achoo! You're stunned.", "gradient_colors": (255, 228, 181, 100, 90, 70)},
    {"filename": "temp_tp.png", "title": "Temporary TP", "description": "Teleport tactically.", "gradient_colors": (64, 224, 208, 30, 100, 90)},
    {"filename": "trap.png", "title": "Fake Loot", "description": "Tempting but treacherous.", "gradient_colors": (184, 134, 11, 70, 50, 10)}
]


# Process each image
for data in batch_data:
    # Load the image
    base_image_path = os.path.join(input_dir, data['filename'])
    if not os.path.exists(base_image_path):
        print(f"Image not found: {base_image_path}")
        continue
    base_image = Image.open(base_image_path).convert('RGBA')

    # Load the fonts
    title_font = ImageFont.truetype(font_path, title_font_size)
    description_font = ImageFont.truetype(font_path, description_font_size)
    # Determine if the title needs to be centered
    center_title = len(data['description'].split()) == 1
    # Apply the gradient and description
    base_image = apply_gradient_with_manual_outline(
        base_image,
        data['title'],
        title_font,
        position,
        data['gradient_colors'],
        outline_thickness,
        outline_color,
        data['description'],
        description_font
    )
    # Center align the title if description is a single word
    if len(data['description'].split()) == 1:
        # Measure the size of the title text
        title_width, title_height = base_image.textsize(data['title'], font=title_font)
        # Calculate the new position for the title to be center-aligned
        center_position = ((base_image.width - title_width) // 2, position[1])
        # Redraw the title with the new center position
        base_image = apply_gradient_with_manual_outline(
            base_image,
            data['title'],
            title_font,
            center_position,
            data['gradient_colors'],
            outline_thickness,
            outline_color,
            data['description'],
            description_font
        )

    # Save the output image
    output_image_path = os.path.join(output_dir, f"output_{data['filename']}")
    base_image.save(output_image_path)

print("Batch processing complete.")
