def extract_highlight(doc):
    annots = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        annotations = page.annots()

        if annotations:
            for annot in annotations:
                if annot.type[0] == 8:
                    rect = annot.rect  # Bounding box (fitz.Rect object: x0, y0, x1, y1)
                    # Extract the highlighted text (clips to the annotation's rectangle)
                    highlighted_text = page.get_text("text", clip=rect).strip()
                    highlight = {
                        "page_num": page_num + 1,
                        "rect": rect,
                        "text": highlighted_text,
                    }
                    annots.append(highlight)

    annots.sort(key=lambda h: (h["page_num"], h["rect"].y1))
    return annots
