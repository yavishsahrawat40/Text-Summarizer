import os
import sys
import requests
import argparse
import logging
from dotenv import load_dotenv


def setup_logging():
    """Configure a basic logger."""
    # Log to stderr so that stdout can be used for the summary result
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s', stream=sys.stderr)

def setup_parser():
    """Configure the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="Summarize text using the Hugging Face API.",
        epilog="If no file is provided, text will be read from standard input."
    )
    parser.add_argument(
        "-f", "--file",
        metavar="PATH",
        type=str,
        help="Path to a text file to summarize."
    )
    return parser

# --- Core Logic ---

def load_config():
    """Load environment variables and return a config dict."""
    load_dotenv()
    api_token = os.getenv("HF_API_KEY")
    model = os.getenv("HF_MODEL", "facebook/bart-large-cnn")

    if not api_token:
        logging.error("Hugging Face API Key not found. Please set HF_API_KEY in your .env file.")
        sys.exit(1)

    api_url = f"https://api-inference.huggingface.co/models/{model}"
    return {"api_token": api_token, "api_url": api_url}

def read_input_text(file_path):
    """Read text from a file or from stdin."""
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            logging.error(f"File not found at '{file_path}'.")
            sys.exit(1)
    else:
        logging.info("No file provided. Reading from standard input...")
        return "".join(sys.stdin.readlines())

def query_api(text, api_url, api_token):
    """Send text to the API and return a dictionary with the summary or an error."""
    headers = {"Authorization": f"Bearer {api_token}"}
    
    MAX_INPUT_LENGTH = 5000 
    if len(text) > MAX_INPUT_LENGTH:
        logging.warning("Input text exceeds max length. Truncating to %d characters.", MAX_INPUT_LENGTH)
        text = text[:MAX_INPUT_LENGTH]

    payload = {"inputs": text}

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return {"summary": None, "error": f"API request failed. Details: {e}"}
    except ValueError:
        return {"summary": None, "error": f"Could not decode JSON. Raw response: {response.text}"}

    if isinstance(data, list) and data and "summary_text" in data[0]:
        return {"summary": data[0]["summary_text"], "error": None}

    return {"summary": None, "error": f"Unexpected API response format. Details: {data}"}

# --- Main Execution ---

def main():
    """Main entry point for the CLI summarizer tool."""
    setup_logging()
    parser = setup_parser()
    args = parser.parse_args()
    
    config = load_config()
    article_text = read_input_text(args.file)

    if not article_text.strip():
        logging.error("No input text provided. Exiting.")
        sys.exit(1)

    logging.info("Sending text to the summarization API...")
    result = query_api(article_text, config["api_url"], config["api_token"])

    # This is the corrected logic
    if result["error"]:
        logging.error(result["error"])
        sys.exit(1)
    else:
        # Print the final result to standard output (stdout)
        print(result["summary"])
        sys.exit(0)

if __name__ == "__main__":
    main()