import fitz  # PyMuPDF

def extract_sections_from_pdf(pdf_path):
    import fitz
    import re
    
    doc = fitz.open(pdf_path)
    sections = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]

        # Collect all spans with font sizes and text
        spans = []
        for block in blocks:
            if block['type'] == 0:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        size = span["size"]
                        if text:
                            spans.append((size, text))

        # Sort unique sizes descending, take top 2 font sizes as candidates
        sizes = sorted({s[0] for s in spans}, reverse=True)
        if not sizes:
            # fallback: entire page text
            text = page.get_text()
            sections.append({
                "section_title": f"Page {page_num + 1} content",
                "page_number": page_num + 1,
                "text": text.strip()
            })
            continue
        top_sizes = sizes[:2]

        # Find candidate titles: texts with font size in top_sizes
        candidates = [text for size, text in spans if size in top_sizes]

        # Filter candidates to likely section titles:
        filtered_titles = []
        for t in candidates:
            # Conditions for title:
            # 1. Length between 3 and 10 words
            # 2. No ending punctuation like '.' or ':'
            # 3. Mostly capitalized words or Title Case
            word_count = len(t.split())
            if 3 <= word_count <= 10:
                if not re.search(r'[.:]$', t):
                    # Check if mostly title case (first letter capital)
                    words = t.split()
                    capitalized = sum(1 for w in words if w and w[0].isupper())
                    if capitalized >= max(1, word_count // 2):
                        filtered_titles.append(t)

        filtered_titles = list(dict.fromkeys(filtered_titles))  # remove duplicates

        if not filtered_titles:
            # fallback: whole page text
            text = page.get_text()
            sections.append({
                "section_title": f"Page {page_num + 1} content",
                "page_number": page_num + 1,
                "text": text.strip()
            })
            continue

        # Split page text by these filtered titles
        page_text = page.get_text()
        pattern = "|".join([re.escape(t) for t in filtered_titles])
        splits = re.split(f"({pattern})", page_text)

        # Pair splits as (title, text)
        i = 1
        while i < len(splits):
            title = splits[i].strip()
            text_chunk = splits[i+1].strip() if i+1 < len(splits) else ""
            sections.append({
                "section_title": title,
                "page_number": page_num + 1,
                "text": text_chunk
            })
            i += 2

    return sections




def load_persona(persona_path):
    import json
    with open(persona_path, 'r', encoding='utf-8') as f:
        return json.load(f)
