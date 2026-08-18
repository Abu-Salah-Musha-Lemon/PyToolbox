
### `pdf_to_markdown.py`

```python
from markitdown import MarkItDown
from google.colab import files
import os
import zipfile


def upload_pdfs():
    """Upload multiple PDF files from the user's computer."""
    uploaded = files.upload()

    pdf_files = [
        filename
        for filename in uploaded.keys()
        if filename.lower().endswith(".pdf")
    ]

    print(f"\nUploaded {len(pdf_files)} PDF file(s).")

    return pdf_files


def convert_pdfs(pdf_files):
    """Convert PDF files to Markdown."""
    md = MarkItDown()
    md_files = []

    for pdf_file in pdf_files:
        print(f"\nConverting: {pdf_file}")

        result = md.convert(pdf_file)

        output_file = os.path.splitext(pdf_file)[0] + ".md"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result.text_content)

        md_files.append(output_file)

        print(f"Saved: {output_file}")

    return md_files


def create_zip(md_files, zip_name="converted_markdown.zip"):
    """Create a ZIP file containing all Markdown files."""
    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for md_file in md_files:
            zipf.write(md_file)

    print(f"\nZIP created: {zip_name}")

    return zip_name


def main():
    # Upload PDFs
    pdf_files = upload_pdfs()

    if not pdf_files:
        print("No PDF files were uploaded.")
        return

    # Convert PDFs
    md_files = convert_pdfs(pdf_files)

    # Create ZIP
    zip_name = create_zip(md_files)

    # Download ZIP
    files.download(zip_name)


if __name__ == "__main__":
    main()
