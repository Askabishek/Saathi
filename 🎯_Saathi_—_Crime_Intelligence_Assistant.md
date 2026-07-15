# 🎯 Saathi — Crime Intelligence Assistant

Saathi is a multimodal crime intelligence assistant built with a modern AI stack. It leverages structured data (SQL), unstructured knowledge (RAG), and voice capabilities (STT/TTS) to provide comprehensive crime-related insights.

## 🚀 Features
- **Multimodal Interaction**: Supports text and voice input/output.
- **Structured Intelligence**: NL-to-SQL engine for querying the crime database.
- **Unstructured Knowledge**: RAG-based retrieval for safety tips and reports.
- **Voice Suite**: Whisper for speech-to-text and gTTS for text-to-speech.
- **Interactive UI**: Built with Streamlit for a seamless user experience.

## 🛠️ Stack
- **LLM**: GPT-5-mini (via Manus Proxy)
- **STT**: Groq Whisper
- **TTS**: gTTS
- **Database**: SQLite (Structured), ChromaDB (Vector/Unstructured)
- **Embeddings**: Sentence-Transformers (all-MiniLM-L6-v2)
- **Frontend**: Streamlit

## 📂 Project Structure
```
saathi/
├── app.py              # Streamlit UI
├── pipeline.py         # Core single pipeline
├── tools/
│   ├── sql_tool.py     # NL-to-SQL
│   ├── rag_tool.py     # Semantic search
│   └── voice_tool.py   # STT + TTS
├── data/
│   ├── crime_db.sqlite # Structured DB
│   └── seed_data.py    # Synthetic data generator
├── embeddings/         # Chroma vector store
└── requirements.txt    # Dependencies
```

## 🏃 How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   streamlit run saathi/app.py
   ```
