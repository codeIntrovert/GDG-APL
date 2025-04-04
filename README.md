# Set Up and Run OpenAI’s Whisper for Speech Recognition & Sentiment Analysis

This project utilizes **OpenAI’s Whisper** for **speech recognition** and applies **sentiment analysis** on transcribed text. Whisper is a powerful automatic speech recognition (ASR) system capable of transcribing and understanding audio input with high accuracy.

## **Skill Tags**

Python, APIs, Google Gemini API, AI, Voice Recognition, Speech-to-Text, Text-to-Speech (TTS), Voice Assistant, Automation, Speech Synthesis

## **Relevant Links**

Visual Studio Code: https://code.visualstudio.com/
Python: https://www.python.org/downloads/

---

## **Getting Started**

Follow these steps to set up Whisper and perform speech recognition and sentiment analysis.

### **1. Install Dependencies (500MB required)**

Whisper requires several dependencies, including PyTorch and ffmpeg. Install them before proceeding.

#### **For Windows (using Chocolatey)**

First, install Chocolatey if you haven’t (using admin shell):

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

Then, install ffmpeg using:

```powershell
choco install ffmpeg
```

#### **For Mac/Linux**

Use Homebrew:

```bash
brew install ffmpeg
```

### **2. Clone the Repository**

Download the project from GitHub:

```bash
git clone https://github.com/codeIntrovert/GDG-APL
cd ./GDG-APL/
```

### **3. Set Up Python Environment**

Create a virtual environment to manage dependencies:

```bash
py -m venv env
```

Activate the virtual environment:

- **Windows:**
  ```bash
  env\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source env/bin/activate
  ```

### **4. Install Required Packages**

```bash
pip install -r requirements.txt
```

### **5. Set Up Your API Key**

To securely store your API key, create a `.env` file in the project directory and add:

```plaintext
API_KEY=your_gemini_api_key_here
```

---

## **Usage**

### **Speech Recognition with Whisper**

Run the following command to transcribe an audio file:

```bash
py src/whisper_main.py
```

---

## **Project Structure**

```
📂 whisper-project
├── 📂 env/                     # Virtual environment
├── 📂 models/                  # Whisper models (optional)
├── 📂 data/                    # Audio files & transcripts
├── 📜 whisper_transcribe.py     # Speech-to-text script
├── 📜 sentiment_analysis.py     # Sentiment analysis script
├── 📜 requirements.txt          # Dependencies
├── 📜 README.md                 # Documentation
└── 📜 .env                      # API keys (if needed)
```

---

## **Troubleshooting**

### **Common Issues and Fixes**

#### ❌ `ModuleNotFoundError: No module named 'whisper'`

✅ Ensure you have installed Whisper:

```bash
pip install openai-whisper
```

#### ❌ `ffmpeg not found`

✅ Ensure `ffmpeg` is installed and available in your system’s PATH.  
Try running:

```bash
ffmpeg -version
```

If not found, reinstall using Chocolatey (Windows) or Homebrew (Mac/Linux).

#### ❌ API Errors with Sentiment Analysis

✅ Ensure you are using a correct API key if required (e.g., for GPT-based sentiment analysis). Store it securely in `.env`.

---

## **Additional Resources**

- **Whisper GitHub**: [https://github.com/openai/whisper](https://github.com/openai/whisper)
- **Chocolatey**: [https://chocolatey.org/](https://chocolatey.org/)
- **Google AI Studio**: [https://aistudio.google.com/](https://aistudio.google.com/)

---

## **License**

This project is licensed under the **MIT License**.

---

## **[Work in Progress]**

This project is actively being developed, and additional features will be added soon.

---

Happy Coding! 🎤➡️📜🤖
