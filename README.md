# 📝 AI-Powered Text Summarizer

A simple and effective web application that transforms lengthy articles into concise summaries using the Hugging Face API. This project was built to demonstrate rapid prototyping, problem-solving, and professional development practices for an internship assignment.

➡️ **View the Live Demo Here**

![App Screenshot](assests/Screenshot%202025-10-02%20011542.png)

<!--- Important: You will need to take a screenshot of your running Streamlit app, create an assets folder in your project, save the image as screenshot-webapp.png, and then commit it to GitHub for this image to show up. --->

## 🛠️ My Development Journey & Learnings

This project's goal was to demonstrate resourcefulness and the ability to ship a simple but functional AI application. Here's the story of how it was built.

### 💡 What I Tried

My plan was to first build a robust command-line tool to perfect the backend logic for calling the API and handling errors. Once the core was solid, I would wrap it in a polished Streamlit UI to create an interactive and shareable web app.

### 💥 What Broke

**API Limitations**: My first request with a long article was rejected by the server with a 400 Bad Request error. I quickly realized the API had a maximum input length that wasn't immediately obvious from the docs.

**Environment Mismatch**: I spent time debugging a ModuleNotFoundError because my code editor was using my global Python interpreter instead of my project's specific Conda environment, so it couldn't find the libraries I had installed.

### 🔧 How I Fixed It

**API Limitations**: I implemented defensive code to truncate the input text to a safe length before sending it to the API. The UI now also warns the user if their text is too long, improving the experience.

**Environment Mismatch**: I learned how to properly configure the Python interpreter in VS Code (Ctrl+Shift+P -> Select Interpreter). This was a key lesson in maintaining consistent development environments.

### 🌱 What I Learned

- The value of a CLI-first approach for separating backend logic from the UI.
- How to debug real-world API limitations and write resilient code to handle them.
- The importance of managing Python environments consistently across different tools.

## 🌟 Features Implemented

- **Core Summarization**: Leverages the `facebook/bart-large-cnn` model via the Hugging Face Inference API.
- **Clean Web UI**: Built with Streamlit, providing a clean and naturally responsive layout for desktop and mobile.
- **User Feedback**: The UI includes a real-time character counter, input length warnings, and a loading spinner (`st.spinner`) to inform the user during processing.
- **Robust Backend**: The core logic is separated into a professional-grade command-line tool (`summarizer_cli.py`) with argument parsing and proper error handling.
- **Easy Copy-Paste**: The final summary is displayed in a text box for easy copying.
- **Secure Configuration**: API keys are managed securely using a `.env` file for local development and repository secrets for deployment.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- A Hugging Face Account & API Key

### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd <your-repository-folder>
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment file:**
   Create a `.env` file in the project root and add your API key:
   ```env
   HF_API_KEY="your_hugging_face_api_key_here"
   ```

4. **Run the web app:**
   ```bash
   streamlit run app.py
   ```

## 💻 Usage

### Web Interface
1. Paste your article into the main text area.
2. Click the "Generate Summary" button.
3. View and copy the AI-generated summary from the results box.

### Command-Line Interface
```bash
# Summarize from a local file
python summarizer_cli.py --file my_article.txt

# Summarize from pasted text (pipe)
echo "Your long text here..." | python summarizer_cli.py
```

## 🔮 Future Enhancements

This project demonstrates a solid foundation. Future improvements could include:

- **Model Selection**: Allow users to choose from different summarization models in the UI.
- **URL Input**: Add a feature to summarize an article directly from a URL.
- **Export Functionality**: Allow users to download the summary as a `.txt` or `.pdf` file.

## 🙏 Acknowledgments

- **Hugging Face**: For their incredible models and accessible Inference API.
- **Streamlit**: For making it so simple to build beautiful data apps in Python.