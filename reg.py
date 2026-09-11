import os
import pickle
import faiss
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import ollama

PDF_FOLDER = "data/planner_pdf_map"   # ✅ Use textbook folder only
VECTOR_PATH = "vector_db"

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Cache
index = None
texts = None


# ---------- TEXT CHUNKING ----------
def split_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks


# ---------- LOAD AND SPLIT PDF WITH SUBJECT ----------
def load_pdfs():
    texts = []

    for file in os.listdir(PDF_FOLDER):
        if file.endswith(".pdf"):

            path = os.path.join(PDF_FOLDER, file)

            # ✅ Clean subject name
            subject = file.replace(".pdf", "").lower()

            try:
                reader = PdfReader(path)

                for page in reader.pages:
                    text = page.extract_text()

                    if text:
                        chunks = split_text(text)

                        for chunk in chunks:
                            texts.append({
                                "text": chunk,
                                "subject": subject
                            })

            except Exception as e:
                print(f"Error reading {file}: {e}")
                continue

    return texts


# ---------- CREATE VECTOR DATABASE ----------
def create_vector_db():
    texts = load_pdfs()

    if len(texts) == 0:
        print("❌ No text found in PDFs")
        return

    # ✅ Extract only text for embedding
    only_texts = [t["text"] for t in texts]

    embeddings = model.encode(only_texts)
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    os.makedirs(VECTOR_PATH, exist_ok=True)

    faiss.write_index(index, f"{VECTOR_PATH}/index.faiss")

    with open(f"{VECTOR_PATH}/texts.pkl", "wb") as f:
        pickle.dump(texts, f)

    print("✅ Vector DB created successfully")


# ---------- LOAD VECTOR DB ----------
def load_vector_db():
    global index, texts

    if index is None:
        index = faiss.read_index(f"{VECTOR_PATH}/index.faiss")

        with open(f"{VECTOR_PATH}/texts.pkl", "rb") as f:
            texts = pickle.load(f)

    return index, texts


# ---------- ASK RAG (FILTER BY SUBJECT) ----------
def ask_rag(question, subject=None):
    index, texts = load_vector_db()

    query_embedding = model.encode([question])
    query_embedding = np.array(query_embedding).astype("float32")

    D, I = index.search(query_embedding, k=15)

    context = ""

    for i in I[0]:
        chunk_data = texts[i]

        # ✅ FILTER by subject
        if subject and chunk_data["subject"] != subject.lower():
            continue

        context += chunk_data["text"] + "\n"

    # ✅ Handle no match
    if context.strip() == "":
        return "❌ No relevant answer found in selected subject."

    prompt = f"""
You are an AI tutor helping Tamil Nadu 12th standard students.

Use ONLY the textbook context below to answer.

Context:
{context}

Question:
{question}

Rules:
- Do not guess
- If answer not found, say "Not found in textbook"
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]


# ---------- CHAPTER EXTRACTION ----------
def extract_chapters(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return []

    try:
        reader = PdfReader(pdf_path)
        chapters = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                lines = text.split("\n")

                for line in lines:
                    line = line.strip()

                    if any(word in line.lower() for word in ["chapter", "unit", "lesson", "topic"]):
                        chapters.append(line)

        chapters = list(dict.fromkeys(chapters))  # remove duplicates
        return chapters[:20]

    except Exception as e:
        print(f"Error extracting chapters: {e}")
        return []


# ---------- STUDY PLAN ----------
def generate_study_plan(subject, days, hours, pdf_path):

    if not os.path.exists(pdf_path):
        return f"❌ PDF not found for {subject}"

    chapters = extract_chapters(pdf_path)

    if len(chapters) == 0:
        prompt = f"""
Create a study plan for {subject}

Days: {days}
Hours/day: {hours}

Include:
- Topics
- Practice
- Revision
"""
    else:
        chapter_list = "\n".join(chapters)

        prompt = f"""
Create a study plan

Subject: {subject}

Chapters:
{chapter_list}

Days: {days}
Hours/day: {hours}
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]


# ---------- BUILD VECTOR DB ----------
if __name__ == "__main__":
    create_vector_db()
