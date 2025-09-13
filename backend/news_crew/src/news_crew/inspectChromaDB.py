import chromadb, os
from crewai.utilities.paths import db_storage_path

# Connect to CrewAI's ChromaDB
storage_path = db_storage_path()
chroma_path = os.path.join(storage_path, "knowledge")

if os.path.exists(chroma_path):
    client = chromadb.PersistentClient(path=chroma_path)
    collections = client.list_collections()

    print("ChromaDB Collections:")
    for collection in collections:
        print(f"  - {collection.name}: {collection.count()} documents")
else:
    print("No ChromaDB storage found")
