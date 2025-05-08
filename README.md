# YouTube Sentiment Analysis (Telugu/English/Transliterated) - Streamlit App

This repository contains the code for a Streamlit web application designed to perform sentiment analysis on YouTube comments in Telugu, English, and transliterated text. The application acts as a client, sending comments to an external FastAPI hosted on Hugging Face Spaces for analysis.

## Repository Contents

- `app.py`: The main Streamlit application script.
- `requirements.txt`: Lists the Python dependencies required to run this Streamlit app (`streamlit`, `requests`, etc.).
- `.gitignore`: Specifies files and directories that Git should ignore (crucially, your `.env` file).
- `.env` (Local only - not in repo): File to store your Hugging Face API Token when running locally.

## Setup and Running Locally

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/gajula21/youtube-sentiment-telugu-app.git](https://github.com/gajula21/youtube-sentiment-telugu-app.git)
    cd youtube-sentiment-telugu-app
    ```

2.  **Set up a virtual environment (Recommended):**
    ```bash
    # Using venv (built-in Python module)
    python -m venv venv
    # Activate the environment
    # On Windows:
    # venv\Scripts\activate
    # On macOS/Linux:
    # source venv/bin/activate

    # Or using conda
    # conda create -n sentiment-app python=3.9
    # conda activate sentiment-app
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file:** In the root of the `youtube-sentiment-telugu-app` folder, create a file named `.env`. Add your Hugging Face API Token to it in the following format:
    ```
    HF_API_TOKEN="YOUR_ACTUAL_HF_TOKEN_HERE"
    ```
    Replace `"YOUR_ACTUAL_HF_TOKEN_HERE"` with your real token. **Ensure this file is listed in your `.gitignore` and is NOT committed to GitHub.**

5.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```
    The app will open in your browser.

## Deployment

This application is designed to be easily deployed on platforms like Streamlit Community Cloud or Hugging Face Spaces.

**Crucially, when deploying, you MUST add your `HF_API_TOKEN` as a secret environment variable on the deployment platform.** Refer to the specific platform's documentation for how to add secrets (e.g., Streamlit Cloud settings, Hugging Face Space settings -> Repository secrets).

*(Optional: Add a link to your deployed app here if it's public)*

## API Used

This application relies on an external FastAPI hosted on Hugging Face Spaces for the sentiment analysis inference.

* **API Endpoint:** [https://gajula21-telugu-sentiment-api.hf.space/sentiment](https://gajula21-telugu-sentiment-api.hf.space/sentiment) 

This repository only contains the client-side Streamlit application code.

## Related Projects

* **Model Development Notebooks:** The repository containing the notebooks used to train and test the sentiment model.
    [https://github.com/gajula21/youtube-sentiment-notebooks](https://github.com/gajula21/finetune_sentiment_telugu) 
* **Hosted API:** The Hugging Face Space hosting the FastAPI sentiment analysis API.
    [https://huggingface.co/spaces/gajula21/telugu-sentiment-api](https://huggingface.co/spaces/gajula21/telugu-sentiment-api) 
