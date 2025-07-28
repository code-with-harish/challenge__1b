# Challenge 1B – Persona-Driven Document Intelligence

This project processes PDF documents and extracts relevant information based on a given **persona profile**. It uses local models, supports full offline execution, and provides structured JSON output under 60 seconds.

---

## 🧠 Features

- ⚡ Fast & CPU-only execution (≤ 60s)
- 📄 PDF segmentation and section analysis
- 🧍 Persona-driven section relevance scoring
- 📦 Fully Dockerized and offline compatible
- ✅ Output: Structured JSON summary

---

## 📁 Folder Structure

```
challenge1b/
│
├── input/                  # Place input PDF files here
├── output/                 # Extracted JSON results will be stored here
├── model/                  # Contains pre-downloaded SentenceTransformer model
├── main.py                 # Main execution script
├── utils.py                # Utility functions
├── persona.json            # Defines persona-specific interest weights
├── requirements.txt        # Python dependencies
└── Dockerfile              # Docker build config
```

---

## 🚀 How to Run (Offline Compatible)

### Step 1: Build Docker Image

```bash
docker build -t challenge1b .
```

### Step 2: Run Inference

Make sure your input PDFs are inside the `input/` folder.

```bash
docker run --rm ^
  -v "%cd%/input:/app/input" ^
  -v "%cd%/output:/app/output" ^
  challenge1b
```

> 💡 Replace `^` with `\` if using Unix/Mac shell.

---

## 📥 Persona Format (`persona.json`)

```json
{
  "persona_name": "Investor",
  "interests": {
    "Financial Highlights": 0.9,
    "Sustainability": 0.5,
    "Risks": 0.7
  }
}
```

You can define any number of interest areas and assign weights (0–1).

---

## 📦 Dependencies

- Python 3.10
- PyMuPDF
- SentenceTransformers (`all-MiniLM-L6-v2`)
- torch (CPU only)

---

© Challenge 1B — Adobe Hackathon
