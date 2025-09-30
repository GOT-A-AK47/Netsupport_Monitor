#!/usr/bin/env python3
"""
NetSupport Monitor - Icon Generator
Creates high-quality icons for safe and warning states
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(color, symbol, filename, size=256):
    """Create a high-quality icon"""
    # Create image with anti-aliasing
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw circle background
    margin = int(size * 0.1)
    draw.ellipse([margin, margin, size-margin, size-margin],
                 fill=color, outline="#FFFFFF", width=int(size * 0.05))

    # Draw symbol in center
    font_size = int(size * 0.6)
    try:
        # Try to use a system font
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # Fallback to default font
        font = ImageFont.load_default()

    # Get text bounding box for centering
    bbox = draw.textbbox((0, 0), symbol, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Center the text
    x = (size - text_width) // 2 - bbox[0]
    y = (size - text_height) // 2 - bbox[1]

    draw.text((x, y), symbol, fill="#FFFFFF", font=font)

    # Save as PNG first (high quality)
    png_path = filename.replace('.ico', '.png')
    img.save(png_path, "PNG")
    print(f"✅ Created: {png_path}")

    # Create multiple sizes for ICO format
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    images = []
    for icon_size in sizes:
        resized = img.resize(icon_size, Image.Resampling.LANCZOS)
        images.append(resized)

    # Save as ICO
    images[0].save(filename, format="ICO", sizes=[(img.width, img.height) for img in images],
                   append_images=images[1:])
    print(f"✅ Created: {filename}")

def main():
    """Generate all required icons"""
    print("=" * 50)
    print("NetSupport Monitor - Icon Generator")
    print("=" * 50)
    print()

    # Create safe icon (green with checkmark)
    create_icon("#28a745", "✓", "icon_safe.ico")

    # Create warning icon (red with exclamation)
    create_icon("#dc3545", "!", "icon_warning.ico")

    # Create default/neutral icon (blue)
    create_icon("#007bff", "N", "icon.ico")

    print()
    print("=" * 50)
    print("✅ Icon generation complete!")
    print("=" * 50)
    print()
    print("Generated files:")
    print("  - icon_safe.ico / .png (Green - Safe)")
    print("  - icon_warning.ico / .png (Red - Warning)")
    print("  - icon.ico / .png (Blue - Default)")

if __name__ == "__main__":
    main()