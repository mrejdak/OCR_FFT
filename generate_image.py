import os
from PIL import Image

# Folders with font files
FONT_FOLDER = "Calibri"
LETTERS_FOLDER = "Letters"

# Margin and spacing parameters
MARGIN = 3
LINE_SPACING = 3
CHARACTER_SPACING = 1

# Mapping special characters to file names
CHARACTER_MAP = {
    " ": "space",
    ".": "dot",
    ",": "comma",
    "?": "question_mark",
    "!": "exclamation_mark"
}


def load_character(char):
    """Load a character image from disk based on character map."""
    key = CHARACTER_MAP.get(char, char)
    path = os.path.join(FONT_FOLDER, LETTERS_FOLDER, f"{key}.png")
    try:
        return Image.open(path).convert("L")
    except FileNotFoundError:
        print(f"Missing file for character: '{char}' → {path}")
        return None


def generate_text_image(text, rotation_angle=0):
    """Generate a full image representing the input text using character images."""
    lines = text.lower().split("\n")
    image_lines = []
    max_line_width = 0
    char_height = None

    for line in lines:
        characters = []
        for char in line:
            char_img = load_character(char)
            if char_img:
                if char_height is None:
                    char_height = char_img.height
                characters.append(char_img)
        if characters:
            line_width = sum(c.width for c in characters)
            line_width += (len(characters) - 1) * CHARACTER_SPACING
            max_line_width = max(max_line_width, line_width)
            image_lines.append(characters)

    if not image_lines or char_height is None:
        raise ValueError("No characters found to generate image.")

    num_lines = len(image_lines)

    # Calculate total image height and width, including bottom margin
    total_height = (
            2 * MARGIN +  # Top and bottom margins
            num_lines * char_height +
            (num_lines - 1) * LINE_SPACING
    )
    total_width = max_line_width + 2 * MARGIN

    result_image = Image.new("L", (total_width, total_height), color=255)

    y = MARGIN
    for line_chars in image_lines:
        x = MARGIN
        for i, char_img in enumerate(line_chars):
            # Paste character image at (x, y)
            result_image.paste(char_img, (x, y))
            x += char_img.width
            if i < len(line_chars) - 1:
                x += CHARACTER_SPACING
        # Move to next line (down)
        y += char_height + LINE_SPACING

    if rotation_angle != 0:
        result_image = result_image.rotate(rotation_angle, expand=True, fillcolor=255)

    return result_image


# Example usage
sample_text = """lorem ipsum dolor sit amet, consectetur adipiscing elit. nullam gravida vel metus vitae scelerisque. ut
quis augue eu erat bibendum egestas. sed a dui feugiat, pretium mi quis, fringilla quam. etiam hendrerit
quis leo non pulvinar. maecenas eleifend fringilla justo. cras aliquam auctor urna at facilisis. pellentesque
non egestas quam. sed mollis odio ac massa ornare porttitor. in sagittis dui eu hendrerit laoreet.
pellentesque ullamcorper gravida imperdiet. aliquam at purus sed ipsum consectetur porta id vel libero."""

image = generate_text_image(sample_text, 20)
image.save(os.path.join(FONT_FOLDER, "lorem_ipsum_rotated.png"))
image.show()