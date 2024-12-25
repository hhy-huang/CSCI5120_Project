# Implementation of CSCI5120 project

# 1. GraphRAG-Ollama

For more details on the GraphRAG implementation, please refer to the [GraphRAG paper](https://arxiv.org/pdf/2404.16130).

## 🌟 Features

- **Local Model Support:** Leverage local models with Ollama for LLM and embeddings.
- **Cost-Effective:** Eliminate dependency on costly OpenAPI models.
- **Easy Setup:** Simple and straightforward setup process.

## 📦 Installation and Setup

Follow these steps to set up this repository and use GraphRag with local models provided by Ollama :


1. **Create and activate a new conda environment:  (please stick to the given python version 3.10 for no errors)**
    ```bash
    conda create -n graphrag-ollama-local python=3.10
    conda activate graphrag-ollama-local
    ```

2. **Install Ollama:**
    - Visit [Ollama's website](https://ollama.com/) for installation instructions.
    - Or, run:
    ```bash
    curl -fsSL https://ollama.com/install.sh | sh #ollama for linux
    pip install ollama
    ```

3. **Download the required models using Ollama, we can choose from (mistral,gemma2, qwen2) for llm and any embedding model provided under Ollama:**
    ```bash
    ollama pull mistral  #llm
    ollama pull nomic-embed-text  #embedding
    ```

4. **Clone the repository:**
    ```bash
    git clone https://github.com/TheAiSingularity/graphrag-local-ollama.git
    ```

5. **Navigate to the repository directory:**
    ```bash
    cd graphrag-local-ollama/
    ```

6. **Install the graphrag package ** This is the most important step :**
    ```bash
    pip install -e .
    ```


7. **Create the required input directory: This is where the experiments data and results will be stored - ./ragtest**
    ```bash
    mkdir -p ./ragtest/input
    ```
    
8. **Copy sample data folder input/  to  ./ragtest. Input/ has the sample data to run the setup. You can add your own data here in .txt format.**
    ```bash
    cp input/* ./ragtest/input
    ```
    
9. **Initialize the ./ragtest folder to create the required files:**
    ```bash
    python -m graphrag.index --init --root ./ragtest
    ```

10. **Move the settings.yaml file, this is the main predefined config file configured with ollama local models :**
    ```bash
    cp settings.yaml ./ragtest
    ```

Users can experiment by changing the models. The llm model expects language models like llama3, mistral, phi3, etc., and the embedding model section expects embedding models like mxbai-embed-large, nomic-embed-text, etc., which are provided by Ollama. You can find the complete list of models provided by Ollama here https://ollama.com/library, which can be deployed locally. The default API base URLs are http://localhost:11434/v1 for LLM and http://localhost:11434/api for embeddings, hence they are added to the respective sections. 

![LLM Configuration](<Screenshot 2024-07-09 at 3.34.31 AM-1.png>)

![Embedding Configuration](<Screenshot 2024-07-09 at 3.36.28 AM.png>)

11. **Run the indexing, which creates a graph:**
    ```bash
    python -m graphrag.index --root ./ragtest
    ```

12. **Run a query: Only supports Global method** 
    ```bash
    python -m graphrag.query --root ./ragtest --method global "What is machine learning?"
    ```

**Graphs can be saved which further can be used for visualization by changing the graphml to "true" in the settings.yaml :**
    
    snapshots:
    graphml: true
    
**To visualize the generated graphml files, you can use : https://gephi.org/users/download/ or the script provided in the repo visualize-graphml.py :**

Pass the path to the .graphml file to the below line in visualize-graphml.py:

    graph = nx.read_graphml('output/20240708-161630/artifacts/summarized_graph.graphml') 

13. **Visualize .graphml :**

    ```bash
    python visualize-graphml.py
    ```


- Original GraphRAG repository by Microsoft: [GraphRAG](https://github.com/microsoft/graphrag)
- Ollama: [Ollama](https://ollama.com/)


# 2. API_qwen Project

## Project Overview
API_qwen is a project that utilizes Alibaba's qwen large model for data preprocessing. The project aims to clean news text data by calling the qwen_Turbo API, thereby enhancing data quality and preparing it for subsequent data analysis and machine learning tasks.

## Features
- Reads news text data from `input.txt`.
- Calls the qwen_Turbo API for data preprocessing.
- Outputs the cleaned news text to `cleaned_output.txt`.

## Installation
Ensure you have Python installed and the following dependencies:

```bash
pip install requests
```

Configuration
Before running the project, make sure you have set up the following environment variables:
QWEN_API_KEY: Your qwen_Turbo API key.
QWEN_API_ENDPOINT: The endpoint URL of the qwen_Turbo API.

Usage
Save the news text data that needs cleaning to input.txt, then run the following command:
python qwen_text_from_file.py
The project will automatically call the qwen_Turbo API and output the cleaned text to cleaned_output.txt.

# 3.Firecrawl Project

## Project Overview
Firecrawl is a Python-based project designed to crawl text data from target web pages by utilizing the Firecrawl API. It allows users to specify the URLs and CSS elements of the web pages they wish to scrape, and it outputs the crawled data in a structured format.

## Features
- Crawls text data from specified web pages.
- Accepts URLs and CSS selectors as input.
- Outputs crawled data in a file for further processing.

## Technology Stack
- Python
- Firecrawl API

## Installation
To get started with Firecrawl, ensure you have Python installed on your system.

Configuration
Before running the crawler, you need to prepare an input.txt file that contains the URLs and CSS elements you want to scrape.

Usage
To run the Firecrawl program, execute the following command in your terminal:
python crawl.py

The program will read the input.txt file, crawl the specified web pages, and output the crawled data to already_crawled.txt, which can then be used as input for the qwen_API project for data cleaning.

Authors
HUANG Haoyu, QI Xixian, WANG Mingshuo, WU Siyuan, YANG Junjie