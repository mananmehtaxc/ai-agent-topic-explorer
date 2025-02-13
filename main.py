
# prompt: the first tool is for searching the internet and getting URLs, and the second tool is for reading those URLs.

from duckduckgo_search import DDGS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
import requests
import streamlit as st
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# # Load environment variables from .env file
# load_dotenv()
# api_key = os.getenv("GOOGLE_API_KEY")
# if api_key is None:
#     raise ValueError("API_KEY is not set in the .env file.")

# print("API Key:", api_key)

def search_ddgs_and_store(query, num_results=10):
  """Searches DuckDuckGo and stores results in an array.

  Args:
    query: The search query.
    num_results: The maximum number of results to retrieve.

  Returns:
    An array of search result dictionaries.
  """
  search_results = []
  results = DDGS().text(query, region='wt-wt', safesearch='Moderate', timelimit='y', max_results=num_results)  # fetch results from DDGS

  # Iterate through the results and extract relevant information
  for i,result in enumerate(results): # extract title, snippet, and URL
        search_results.append(result)

  return search_results



# summarize text from url
def summarize_url(url,api_key,model):
  """Reads a URL, fetches content, and creates a summary using Google AI LLM.

  Args:
    url: The URL to process.

  Returns:
    A summary of the URL content.
  """
  try:
    # Fetch the content of the URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the text content
    text = soup.get_text()

    if model == "Google Gemini":
        # Initialize the Gemini model
        llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)
    
    if model == "OpenAI":
        # Initialize OpenAi Model
        llm = ChatOpenAI(openai_api_key=api_key)

    # Generate the summary
    summary = llm.predict(f"Summarize the following text: {text}")

    return summary

  except requests.exceptions.RequestException as e:
    print(f"Error fetching URL {url}: {e}")
    return None
  except Exception as e:
    print(f"Error processing URL {url}: {e}")
    return None

# Page title
st.set_page_config(page_title='🦜🔗 Topic Explored App')
st.title('🦜🔗 Topic Explorer App')

# Query text
topic = st.text_input('Enter your topic:', placeholder = 'Please provide a topic to explore')
results_count = st.slider("Pick a number", 3, 10)
use_model = st.selectbox("Pick one", ["Google Gemini", "OpenAI"])
model_api_key = st.text_input('Model API Key:', type='password', disabled=not(topic))

# Example usage
# topic = "What is the latest news on AI safety research?"
# urls = search_ddgs_and_store(topic,3)  # Get the top 3 URLs
# print(urls)


with st.form('myform', clear_on_submit=True):
   # input google api key
   summaries = []
   submitted = st.form_submit_button('Submit', disabled=not(topic and results_count))
   if submitted and model_api_key:
      with st.spinner("Searching..."):
         urls = search_ddgs_and_store(topic,results_count)
         for url in urls:
            summary = summarize_url(url['href'], model_api_key, use_model)
            if summary:
               summaries.append(summary)

# if len(summaries):
#    st.info(summary)
for index, summary in enumerate(summaries):
   st.info(f"""
           Summary for Title {urls[index]['title']}:

           {summary}
           """)
   st.link_button(f"Source: {urls[index]['title']}", urls[index]['href'])
#    st.info(summary)
#    st.info("-"*20)
  # print(f"{index}: {urls[index]['title']}")
  # print(f"Summary {index}: {summary}")
  # print title of given index and correspoind summary
#    print(f"Summary for Title {urls[index]['title']}: (Link:{urls[index]['href']})")
#    print(summary)
#    print("-" * 20)
