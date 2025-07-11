## Topic Explorer Agent

The **Topic Explorer Agent** accepts a user-defined topic, uses **SerpAPI** to fetch the top relevant articles, and generates **concise summaries** using an LLM. Ideal for rapid research and content exploration.

### 🔍 Features

* Fetches 3 relevant articles for any topic
* Summarizes article content using Generative AI
* Outputs clean, easy-to-read summaries for fast insights

### 🛠️ Tech Stack

* Python · SerpAPI · LangChain · Gemini AI or Hugging Face LLMs

### 🚀 How It Works

1. Enter a topic
2. Agent queries SerpAPI for top results
3. Scrapes and summarizes content using an LLM
4. Returns a clean summary list

---

Let me know if you'd like a code usage example or Streamlit UI notes added!


# Python Project Setup

## Description

This Python project requires specific dependencies that are best managed in a virtual environment. A virtual environment helps to isolate project dependencies from the global Python environment.

## Requirements

- Python 3.x or above
- pip (Python package installer)

## Setup Instructions

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/your-project-name.git
cd your-project-name
```

### 2. Clone the Repository
`python3 -m venv venv`

### 3. Create Virtual Enviroment
`source venv/bin/activate`

### 4. Activate the Virtual Environment
`source venv/bin/activate`

### 5. Install Project Dependencies
`pip install -r requirements.txt`

### 6. Create .env
create `.env` file and install environment variables

### 7. Running Project
# Project uses streamlit, run streamlit locally
`streamlit run main.py`
