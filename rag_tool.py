import chromadb
from chromadb.utils import embedding_functions
import os

class RAGTool:
    def __init__(self, persist_directory="saathi/embeddings"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        self.collection = self.client.get_or_create_collection(
            name="crime_reports",
            embedding_function=self.embedding_fn
        )
        self._seed_reports()

    def _seed_reports(self):
        # Sample unstructured reports for RAG
        reports = [
            {"id": "doc1", "text": "Recent increase in petty thefts reported near the central metro station during evening hours."},
            {"id": "doc2", "text": "New safety guidelines issued for residents in the North Suburbs following recent break-ins."},
            {"id": "doc3", "text": "Witness report: Suspect seen wearing a red hoodie near the West End vandalism site."},
            {"id": "doc4", "text": "Police increase patrols in Downtown area to combat rising vehicle thefts."},
            {"id": "doc5", "text": "Community alert: Be aware of suspicious activities in the Shopping Mall parking lot."}
        ]
        
        # Check if already seeded to avoid duplicates
        if self.collection.count() == 0:
            self.collection.add(
                documents=[r["text"] for r in reports],
                ids=[r["id"] for r in reports]
            )

    def query(self, text, n_results=2):
        results = self.collection.query(
            query_texts=[text],
            n_results=n_results
        )
        if results and results.get("documents") and len(results["documents"]) > 0:
            return results["documents"][0]
        return "No relevant documents found."

if __name__ == "__main__":
    rag = RAGTool()
    print(rag.query("theft near metro"))
