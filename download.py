from sentence_transformers import SentenceTransformer

# Model name
model_name = "all-MiniLM-L6-v2"
output_path = "model/" + model_name

print("[INFO] Downloading model...")
model = SentenceTransformer(model_name)
model.save(output_path)
print(f"[INFO] Model saved to {output_path}")
