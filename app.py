import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
import io
import requests
import json

st.set_page_config(layout="wide")
st.title("YouTube Sentiment Analysis (Telugu/English/Transliterated)")

load_dotenv()
hf_token = os.getenv("HF_API_TOKEN")

if hf_token is None:
    st.error("Hugging Face API Token (HF_API_TOKEN) not found in your environment variables or .env file.")
    st.warning("Please create a .env file in the same directory as app.py and add HF_API_TOKEN='your_token_here'")
    st.stop()

API_BASE_URL = "https://gajula21-telugu-sentiment-api.hf.space"
API_PREDICT_PATH = "/sentiment"
API_URL = f"{API_BASE_URL}{API_PREDICT_PATH}"

label_mapping = {
    "LABEL_0": "Negative",
    "LABEL_1": "Neutral",
    "LABEL_2": "Positive",
    "Positive": "Positive",
    "Neutral": "Neutral",
    "Negative": "Negative"
}

def query_sentiment_api(payload, hf_token):
    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 422:
             st.error(f"API Request Error: 422 Unprocessable Entity. Data payload validation failed.")
             try:
                 detail = response.json()
                 st.json(detail)
             except json.JSONDecodeError:
                 st.error(f"API returned 422 but response body is not valid JSON: {response.text}")
             return None

        response.raise_for_status()

        api_response_data = response.json()

        if isinstance(api_response_data, dict) and 'sentiments' in api_response_data and isinstance(api_response_data['sentiments'], list) and all(isinstance(item, str) for item in api_response_data['sentiments']):
             return api_response_data['sentiments']
        else:
             st.warning(f"API response has unexpected format: {api_response_data}")
             return None

    except requests.exceptions.RequestException as e:
        st.error(f"API Request Error: {e}")
        if e.response is not None:
             st.error(f"Status Code: {e.response.status_code}")
             try:
                  st.json(e.response.json())
             except json.JSONDecodeError:
                  st.error(f"Response body: {e.response.text}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred during the API call: {e}")
        return None


st.header("Analyze a Single Comment")
single_comment = st.text_area("Enter a YouTube comment:", height=100, key="single_comment_input")

if st.button("Analyze Single Comment"):
    if single_comment.strip() == "":
        st.warning("Please enter a comment.")
    else:
        if not single_comment.strip():
             st.warning("Please enter a non-empty comment.")
             st.stop()

        api_request_payload = {"comments": [single_comment.strip()]}

        api_sentiment_list = query_sentiment_api(api_request_payload, hf_token)

        if api_sentiment_list is not None and api_sentiment_list:
            if isinstance(api_sentiment_list, list) and api_sentiment_list and isinstance(api_sentiment_list[0], str):
                 predicted_sentiment = api_sentiment_list[0]
                 display_label = label_mapping.get(predicted_sentiment, predicted_sentiment)

                 st.write(f"### Sentiment: {display_label}")

            else:
                 st.warning(f"API returned unexpected format for single result: {api_sentiment_list}")
        elif api_sentiment_list is not None and not api_sentiment_list:
             st.warning("API returned empty results list.")


st.markdown("---")

st.header("Analyze Multiple Comments (Upload File)")
uploaded_file = st.file_uploader("Upload a text file (.txt) with one comment per line", type=["txt"])

if uploaded_file is not None:
    stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
    comments_list = [line.strip() for line in stringio if line.strip()]

    if not comments_list:
        st.warning("The uploaded file is empty or contains only blank lines.")
    else:
        st.write(f"Analyzing {len(comments_list)} comments...")
        results = []

        batch_api_request_payload = {"comments": comments_list}

        if not batch_api_request_payload.get("comments"):
             st.warning("No valid comments found in the uploaded file after filtering.")
             st.stop()


        st.text("Calling API with batch...")
        batch_sentiment_list = query_sentiment_api(batch_api_request_payload, hf_token)

        if batch_sentiment_list is not None:
            if isinstance(batch_sentiment_list, list) and len(batch_sentiment_list) == len(comments_list):
                st.text("Processing results...")
                progress_bar = st.progress(0)
                status_text = st.empty()
                for i, comment_text in enumerate(comments_list):
                     predicted_sentiment = batch_sentiment_list[i]

                     display_label = label_mapping.get(predicted_sentiment, predicted_sentiment)

                     # --- Modified: Removed Score column for file analysis ---
                     results.append({
                         "Comment": comment_text,
                         "Sentiment": display_label
                     })
                     # --- End Modification ---

                     progress_bar.progress((i + 1) / len(comments_list))
                     status_text.text(f"Processed {i + 1}/{len(comments_list)} comments.")

                progress_bar.empty()
                status_text.text("Batch Analysis Complete!")

            else:
                 st.error(f"Batch analysis failed: API returned unexpected response format or count. Expected list of {len(comments_list)} items, got {len(batch_sentiment_list) if isinstance(batch_sentiment_list, list) else type(batch_sentiment_list)}.")
                 for comment_text in comments_list:
                      results.append({
                         "Comment": comment_text,
                         "Sentiment": "Analysis Failed (API Response Error)",
                         # Score intentionally omitted
                      })

        else:
            st.error("Batch analysis API request failed.")
            for comment_text in comments_list:
                 results.append({
                    "Comment": comment_text,
                    "Sentiment": "Analysis Failed (API Request Error)",
                    # Score intentionally omitted
                 })


        if results:
            results_df = pd.DataFrame(results)
            st.subheader("Batch Analysis Results")
            st.dataframe(results_df, height=300)

            csv_data = results_df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="Download Results as CSV",
                data=csv_data,
                file_name="sentiment_results.csv",
                mime="text/csv",
            )