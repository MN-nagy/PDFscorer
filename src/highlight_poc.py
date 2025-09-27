import fitz

pdf_file = "/mnt/e/ArchForTests/MCQ-example.pdf"

doc = fitz.open(pdf_file)

for page_num in range(len(doc)):
    page = doc[page_num]
    annotations = page.annots()

    if annotations:
        for annot in annotations:
            if annot.type[0] == 8:
                rect = annot.rect  # Bounding box (fitz.Rect object: x0, y0, x1, y1)
                author = annot.info.get("title", "Unknown")  # Author of the annotation
                creation_date = annot.info.get(
                    "creationDate", None
                )  # Creation timestamp

                # Extract the highlighted text (clips to the annotation's rectangle)
                highlighted_text = page.get_text("text", clip=rect).strip()

                # Print or store the extracted info (customize as needed)
                print(f"Page {page_num + 1}:")
                print(f"  Author: {author}")
                print(f"  Highlighted Text: {highlighted_text}")
                print("-" * 40)

doc.close()
