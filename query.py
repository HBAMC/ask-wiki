import langchain
from langchain.chains import RetrievalQA
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.llms import LlamaCpp
from langchain.vectorstores import Chroma

langchain.verbose = False

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

llm = LlamaCpp(
    model_path='./ggml-vic7b-q5_0.bin',
    stop=['### Human:'],
    callback_manager=callback_manager,
    n_ctx= 20000,
    verbose=True,
    use_mlock=True,
    n_gpu_layers=12,
    n_threads=4,
    n_batch=1000
)
llm.client.verbose = False

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
docsearch = Chroma(persist_directory='./.chroma_cache', embedding_function=embeddings)

qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever(), return_source_documents=True)

prompt = ''
while True:
    prompt = input('\n\n❓>>> ')
    if prompt == 'quit':
        print('\n\nBye!\n')
        break

    result = qa({'query': prompt})
    # print(result['result'])