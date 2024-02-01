import logging
import sys
import os.path

from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)

# Ensure the root logger is set to DEBUG to see all messages
logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler(sys.stdout)], format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Setup logging with the module's name
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Set 'httpcore' logging to INFO only
logging.getLogger('httpcore').setLevel(logging.INFO)



# check if storage already exists
PERSIST_DIR = "./storage"
if not os.path.exists(PERSIST_DIR):
    # load the documents and create the index
    documents = SimpleDirectoryReader("data").load_data()
    index = VectorStoreIndex.from_documents(documents=documents, show_progress=True)
    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

query_engine = index.as_query_engine()
response = query_engine.query("What did the author do growing up?")
print(response)
