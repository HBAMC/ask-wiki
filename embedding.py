from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import DirectoryLoader

loader = DirectoryLoader('./data', glob='**/*.txt')
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=500)
split_docs = text_splitter.split_documents(documents)

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
docsearch = Chroma.from_documents(split_docs, embeddings, persist_directory='./.chroma_cache')
docsearch.persist()
