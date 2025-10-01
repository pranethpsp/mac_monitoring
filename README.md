# 💻 Mac System Monitor with Local AI

A proof-of-concept (POC) project for monitoring **Disk**, **Battery**, and **Memory** usage on macOS. This tool leverages local AI models through `ollama` to provide interactive system monitoring directly in your terminal.

---

## ✨ Features

* **System Monitoring**: Get real-time stats for disk space, memory usage, and battery health.
* **Local AI Integration**: Uses `ollama` to interact with powerful local language models like Llama 3 and Mistral.
* **Lightweight**: Built with Python and the efficient `psutil` library.

---

## 🛠️ Setup and Installation

Follow these steps to get the monitor up and running on your macOS machine.

### Prerequisites

* macOS
* [Homebrew](https://brew.sh/)
* Python 3.13 or later

### Installation Steps

1.  **Install Ollama**
    Use Homebrew to install the Ollama CLI.
    ```bash
    brew install ollama
    ```

2.  **Start the Ollama Service**
    Run the following command in your terminal to start the background service. It's recommended to run this in a separate terminal window.
    ```bash
    ollama serve
    ```

3.  **Download AI Models**
    Pull the required AI models. This project is configured to use `llama3` and `mistral`.
    ```bash
    ollama pull llama3:8b
    ollama pull mistral:7b-instruct
    ```

4.  **Install Python Dependencies**
    Install the necessary Python packages using pip.
    ```bash
    pip install ollama psutil
    ```

---

## 🚀 How to Run

Once the setup is complete, you can start the monitoring script.

Execute the `running_script.py` file from your terminal:
```bash
python running_script.py