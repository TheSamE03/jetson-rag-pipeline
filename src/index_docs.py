import os
from rag import ShopManualRAG
from config import DOCS_DIR

def main():
    # Check if there are any documents to index
    if not os.listdir(DOCS_DIR):
        print(f"No documents found in {DOCS_DIR}. Please add your PDF manuals first.")
        return
    
    print("Starting document indexing process...")
    rag = ShopManualRAG()
    
    try:
        rag.index_documents()
        print("Successfully indexed all documents!")
        print(f"Documents are now ready for querying.")
    except Exception as e:
        print(f"Error during indexing: {str(e)}")

if __name__ == "__main__":
    main() 