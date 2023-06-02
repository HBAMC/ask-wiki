import queue
import threading

import gradio as gr
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.llms import LlamaCpp
from langchain.vectorstores import Chroma


class ThreadedGenerator:
    def __init__(self):
        self.queue = queue.Queue()

    def __iter__(self):
        return self

    def __next__(self):
        item = self.queue.get()
        if item is StopIteration: raise item
        return item

    def send(self, data):
        self.queue.put(data)

    def close(self):
        self.queue.put(StopIteration)

class ChainStreamHandler(StreamingStdOutCallbackHandler):
    def __init__(self, gen):
        super().__init__()
        self.gen = gen

    def on_llm_new_token(self, token: str, **kwargs):
        self.gen.send(token)


embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
docsearch = Chroma(persist_directory='./.chroma_cache', embedding_function=embeddings)

def llm_thread(g, prompt):
    try:
        llm = LlamaCpp(
            callback_manager = CallbackManager([ChainStreamHandler(g)]),
            model_path='./ggml-vic7b-q5_0.bin',
            stop=['### Human:'],
            n_ctx= 20000,
            verbose=False,
            use_mlock=True,
            n_gpu_layers=12,
            n_threads=4,
            n_batch=1000
        )
        llm.client.verbose = False

        qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever(), return_source_documents=True)
        qa({'query': prompt})
    finally:
        g.close()

def chain(prompt):
    g = ThreadedGenerator()
    threading.Thread(target=llm_thread, args=(g, prompt)).start()
    return g

with gr.Blocks(title='Ask Wiki', theme='sudeepshouche/minimalist') as demo:
    gr.Markdown(
        """
        # Ask Wiki
        Start typing question below to get the answers.
        """
    )
    msg = gr.Textbox(label='Question', placeholder='Type your question here...')
    clear = gr.Button("Clear")
    chatbot = gr.Chatbot(label="History")

    def user(user_message, history):
        return gr.update(value="", interactive=False), history + [[user_message, None]]

    def bot(history):
        history[-1][1] = ""
        for token in chain(history[-1][0] + '\n\n'):
            history[-1][1] += token
            yield history

    response = msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    response.then(lambda: gr.update(interactive=True), None, [msg], queue=False)
    clear.click(lambda: None, None, chatbot, queue=False)

demo.queue()
demo.launch()