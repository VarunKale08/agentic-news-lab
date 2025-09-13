import chromadb
import os
from crewai.utilities.paths import db_storage_path

# Path to CrewAI storage
storage_path = db_storage_path()
chroma_path = os.path.join(storage_path, "knowledge")

print(f"Looking inside: {chroma_path}")

client = chromadb.PersistentClient(path=chroma_path)
collections = client.list_collections()

if not collections:
    print("⚠️ No collections found.")
else:
    print("✅ Collections:")
    for col in collections:
        print(f" - {col.name}")
        print(f"   → Document count: {col.count()}")
        # Show a sample
        docs = col.peek()
        for d in docs:
            print("   Sample:", d)
