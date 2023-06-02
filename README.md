# Ask Wiki

Use AI to query Wiki content

![screenshot](https://raw.githubusercontent.com/HBAMC/ask-wiki/master/screenshot.gif?token=GHSAT0AAAAAAB4TUAT2YIMITRYI4QJRC6CMZDZSVLQ)

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
    python web.py
