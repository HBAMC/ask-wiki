# Ask Wiki & Charts

Use AI to query Wiki content

![ask_wiki](https://raw.githubusercontent.com/HBAMC/ask-wiki/master/ask_wiki.gif)


![ask_charts](https://raw.githubusercontent.com/HBAMC/ask-wiki/master/ask_charts.gif)

## Usage

### Clone project

    git clone git@github.com:HBAMC/ask-wiki.git && cd ask-wiki

### Install dependencies

    pip install -r requirements.txt

### Download LLM model

    wget https://huggingface.co/vicuna/ggml-vicuna-7b-1.1/resolve/main/ggml-vic7b-q5_0.bin .

### Build local embedding cache

    # Put all *.txt files to /data directory
    python embedding.py

### Query

    # CLI
    python query.py

    # Web UI
    python ask_wiki.py
