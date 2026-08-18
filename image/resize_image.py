"""
PyForge - Image Resizer

Resize one or multiple images while preserving aspect ratio.

Supported formats:
- JPG / JPEG
- PNG
- WEBP
- BMP
- TIFF
"""

from PIL import Image
import os
import zipfile
import argparse


SUPPORTED_FORMATS = (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff")


def resize_image(input_file, output_file, width=None, height=None):
    """
    Resize an image while preserving its aspect ratio.

    If only width is provided, height is calculated automatically.
    If only height is provided, width is calculated automatically.
    If both are provided, the image is resized to exactly those dimensions.
    """

    image = Image.open(input_file)

    original_width, original_height = image.size

    if width and height:
        new_size = (width, height)

    elif width:
        ratio = width / original_width
        new_height = int(original_height * ratio)
        new_size = (width, new_height)

    elif height:
        ratio = height / original_height
        new_width = int(original_width * ratio)
        new_size = (new_width, height)

    else:
        raise ValueError("You must provide width or height.")

    resized = image.resize(new_size, Image.Resampling.LANCZOS)

    resized.save(output_file)

    return new_size


def resize_images(input_folder, output_folder, width=None, height=None):
    """
    Resize all supported images in a folder.
    """

    os.makedirs(output_folder, exist_ok=True)

    output_files = []

    for filename in os.listdir(input_folder):

        if not filename.lower().endswith(SUPPORTED_FORMATS):
            continue

        input_file = os.path.join(input_folder, filename)

        name, extension = os.path.splitext(filename)

        output_file = os.path.join(
            output_folder,
            f"{name}_resized{extension}"
        )

        try:
            new_size = resize_image(
                input_file,
                output_file,
                width=width,
                height=height
            )

            output_files.append(output_file)

            print(
                f"✓ {filename} → "
                f"{new_size[0]}x{new_size[1]}"
            )

        except Exception as error:
            print(f"✗ Failed: {filename}")
            print(f"  Error: {error}")

    return output_files


def create_zip(files, zip_name):
    """
    Create a ZIP archive containing the resized images.
    """

    with zipfile.ZipFile(
        zip_name,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zipf:

        for file in files:
            zipf.write(
                file,
                arcname=os.path.basename(file)
            )

    print(f"\n✓ ZIP created: {zip_name}")


def main():

    parser = argparse.ArgumentParser(
        description="Resize multiple images."
    )

    parser.add_argument(
        "input_folder",
        help="Folder containing the images"
    )

    parser.add_argument(
        "--output",
        default="resized_images",
        help="Output folder"
    )

    parser.add_argument(
        "--width",
        type=int,
        help="Target width"
    )

    parser.add_argument(
        "--height",
        type=int,
        help="Target height"
    )

    parser.add_argument(
        "--zip",
        action="store_true",
        help="Create a ZIP file"
    )

    args = parser.parse_args()

    if not args.width and not args.height:
        parser.error(
            "Provide --width or --height."
        )

    output_files = resize_images(
        input_folder=args.input_folder,
        output_folder=args.output,
        width=args.width,
        height=args.height
    )

    print(
        f"\n✓ Resized {len(output_files)} image(s)."
    )

    if args.zip and output_files:

        zip_name = "resized_images.zip"

        create_zip(
            output_files,
            zip_name
        )


if __name__ == "__main__":
    main()
