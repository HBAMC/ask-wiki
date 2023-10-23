import gradio as gr
from bardapi import Bard

proxies = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
token = ''

bard = Bard(proxies=proxies, token=token)

with gr.Blocks(title='Ask Charts') as block:
    gr.Markdown(
        """
        # Ask Charts
        Start typing your question below to get the answers.
        """
    )

    image_path = ''
    with gr.Row():
        with gr.Column():
            def get_image_path(filepath):
                global image_path
                image_path = filepath 

            image_input = gr.Image(label="Upload Image", type='filepath')
            image_input.upload(fn=get_image_path, inputs=image_input)
    
        with gr.Column():
            def ask_charts(query: str):
                global image_path
                image = open(image_path, "rb").read()
                bard_answer = bard.ask_about_image(query, image)
                return bard_answer["content"]
        
            msg = gr.Textbox(label='Question', placeholder='Type your question here...')
            clear = gr.Button("Clear")
            chatbot = gr.Chatbot(label="History")

            def user(user_message, history):
                return gr.update(value="", interactive=False), history + [[user_message, None]]

            def bot(history):
                history[-1][1] = ask_charts(history[-1][0])
                yield history

            response = msg.submit(user, [msg, chatbot], [msg, chatbot], queue=True).then(
                bot, chatbot, chatbot
            )
            response.then(lambda: gr.update(interactive=True), None, [msg], queue=True)
            clear.click(lambda: None, None, chatbot, queue=True)

block.queue()
block.launch()
