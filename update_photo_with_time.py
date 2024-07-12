from PIL import Image, ImageDraw, ImageFont

def new_photo(current_time):
    # Load the image
    image_path = 'myphoto.jpg'
    image = Image.open(image_path)

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Load a font
    try:
        font = ImageFont.truetype("alarm clock.ttf", 100)  # You can use other font files as well
    except IOError:
        font = ImageFont.load_default()

    # Calculate the position to draw the text (centered)
    text_bbox = draw.textbbox((0, 0), current_time, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    width, height = image.size
    position = (width - text_width - 20, height - text_height - 50)

    # Draw the text on the image
    draw.text(position, current_time, (255, 255, 255), font=font)

    # Save the image with the clock
    output_image_path = 'image_with_clock.jpg'
    image.save(output_image_path)
    return output_image_path

# Optionally, show the image
# image.show()
