import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import json
import datetime
from sentence_transformers import SentenceTransformer, util
from utils import extract_sections_from_pdf, load_persona

print("[INFO] Loading model...")
model_path = "model/all-MiniLM-L6-v2"
model = SentenceTransformer(model_path)
print("[INFO] Model loaded.")

input_dir = "input/"
persona_path = os.path.join(input_dir, "persona.json")
persona = load_persona(persona_path)

# Build persona description from persona and job_to_be_done fields
try:
    role = persona["persona"]["role"]
except KeyError:
    role = persona.get("persona", {}).get("role") or persona.get("persona", "") or "Unknown Role"

try:
    task = persona["job_to_be_done"]["task"]
except KeyError:
    task = persona.get("job_to_be_done", {}).get("task") or "No task provided"

persona_description = f"{role}. {task}"

# Encode persona description vector once
persona_vector = model.encode(persona_description, convert_to_tensor=True)

# Get list of PDF files mentioned in persona['documents']
pdf_files = [doc["filename"] for doc in persona.get("documents", [])]

extracted_sections = []
subsection_analysis = []

for pdf_file in pdf_files:
    pdf_path = os.path.join(input_dir, pdf_file)
    if not os.path.isfile(pdf_path):
        print(f"[WARNING] PDF file not found: {pdf_file}, skipping.")
        continue

    # Extract sections per page with titles and text
    sections = extract_sections_from_pdf(pdf_path)

    for section in sections:
        # Compute similarity score of section text vs persona description
        sec_vec = model.encode(section["text"], convert_to_tensor=True)
        score = util.pytorch_cos_sim(persona_vector, sec_vec)[0][0].item()

        extracted_sections.append({
            "document": pdf_file,
            "section_title": section["section_title"],
            "page_number": section["page_number"],
            "score": score
        })

# Sort sections by descending score
extracted_sections.sort(key=lambda x: x["score"], reverse=True)

# Assign importance ranks to top 5 (or less)
top_sections = extracted_sections[:5]
for idx, sec in enumerate(top_sections, start=1):
    sec["importance_rank"] = idx

# Build subsection analysis with refined_text and page number
for sec in top_sections:
    subsection_analysis.append({
        "document": sec["document"],
        "refined_text": sec["section_title"] + ": " + sec.get("text", "")[:500],  # Limit to 500 chars
        "page_number": sec["page_number"]
    })

# Prepare final JSON output
output = {
    "metadata": {
        "input_documents": pdf_files,
        "persona": role,
        "job_to_be_done": task,
        "processing_timestamp": datetime.datetime.now().isoformat()
    },
    "extracted_sections": [
        {
            "document": sec["document"],
            "section_title": sec["section_title"],
            "importance_rank": sec["importance_rank"],
            "page_number": sec["page_number"]
        }
        for sec in top_sections
    ],
    "subsection_analysis": subsection_analysis
}

# Save output JSON in output/ folder
os.makedirs("output", exist_ok=True)
with open("output/output.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4)

print("[INFO] Analysis complete. Output saved to output/output.json.")
