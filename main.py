
# prompt: the first tool is for searching the internet and getting URLs, and the second tool is for reading those URLs.

from duckduckgo_search import DDGS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
import requests
import streamlit as st
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import time
from serpapi import GoogleSearch

# # Load environment variables from .env file
# load_dotenv()
# api_key = os.getenv("GOOGLE_API_KEY")
# if api_key is None:
#     raise ValueError("API_KEY is not set in the .env file.")

# print("API Key:", api_key)
@st.cache_data(show_spinner=False)
def search_query_and_store(query, serpapi_apiKey, num_results=3):
  """Searches using SerpAPI and stores results in an array, with retry on rate limit.

  Args:
    query: The search query.
    num_results: The maximum number of results to retrieve.
    max_retries: Maximum number of retries on rate limit.

  Returns:
    An array of search result dictionaries.
  """

  search_results = []
  retries = 0
  # serpapi_api_key = os.getenv("SERPAPI_API_KEY")
  if not serpapi_apiKey:
    st.error("SERPAPI_API_KEY not set in environment variables.")
    return []

  while retries < 5:
    try:
      params = {
        "q": query,
        "num": num_results,
        "api_key": serpapi_apiKey,
        "engine": "google",
      }
      search = GoogleSearch(params)
      results = search.get_dict()
      organic_results = results.get("organic_results", [])
      for result in organic_results[:num_results]:
        # Each result is a dict with 'title' and 'link'
        search_results.append({
          "title": result.get("title", ""),
          "href": result.get("link", "")
        })
      return search_results
    except Exception as e:
      if "rate limit" in str(e).lower():
        wait_time = 2 ** retries
        print(f"Rate limited by SerpAPI. Retrying in {wait_time} seconds...")
        time.sleep(wait_time)
        retries += 1
      else:
        print(f"Error searching SerpAPI: {e}")
        break
  st.error("SerpAPI rate limit reached or error occurred. Please try again later.")
  return []



# summarize text from url
def summarize_url(url,api_key,model):
  """Reads a URL, fetches content, and creates a summary using Google AI LLM.

  Args:
    url: The URL to process.

  Returns:
    A summary of the URL content.
  """
  try:
    #mode name
    modelname = "gemini-2.5-flash"
    # Fetch the content of the URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the text content
    text = soup.get_text()

    if model == "Google Gemini":
        # Initialize the Gemini model
        llm = ChatGoogleGenerativeAI(model=modelname, google_api_key=api_key)
    
    if model == "OpenAI":
        # Initialize OpenAi Model
        llm = ChatOpenAI(openai_api_key=api_key)

    # Generate the summary
    summary = llm.invoke(f"Summarize the following text: {text}")

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
results_count = st.slider("Pick a number", 3, 10, 3, help="Number of results to fetch fro search engine", disabled=not topic)
use_model = st.selectbox("Pick one", ["Google Gemini", "OpenAI"])
model_api_key = st.text_input('AI Model API Key:', type='password', disabled=not(topic))
serpapi_api_key = st.text_input('SerpAPI API Key:', type='password', disabled=not(topic))

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
        #  urls = search_query_and_store(topic,results_count)
         urls = search_query_and_store(topic, serpapi_api_key, results_count)
         for url in urls:
            summary = summarize_url(url['href'], model_api_key, use_model)
            if summary:
               summaries.append(summary)

# if len(summaries):
#    st.info(summary)
for index, summary in enumerate(summaries):
   st.info(f"""
           Summary for Title {urls[index]['title']}:

           {summary.content if hasattr(summary, 'content') else summary}
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

