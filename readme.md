**Project NEMO**

**Steps to Run the Project:**

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/project.git

2. **Create and Activate Virtual Environment:**
    ```bash
    python -m venv nemo
    source nemo/bin/activate  # For Linux/Mac
    nemo\Scripts\activate.bat  # For Windows

3. **Install Requirements:**
    ```bash
    pip install -r requirements.txt

4. **Make a Pod:**
    - Recommended Configuration:
        - RTX A6000
        - 48GB VRAM
        - 50GB RAM
        - 8 vCPU
5. **Install Ollama:**
    ```bash
    curl -fsSL https://ollama.com/install.sh | sh

6. **Run Ollama Server:**
    ```bash
    ollama serve

7. **Download Model:**
    ```bash
    ollama run mixtral:8x7b-instruct-v0.1-q5_K_M

8. **Download Ngrok:**
    ```bash 
    curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc |  tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" |  tee /etc/apt/sources.list.d/ngrok.list && apt update &&  apt install ngrok

9. **ADD NGROK Autentication Token:**
    ```bash
    ngrok config add-authtoken YOUR-TOKEN-HERE


10. **Add Ngrok URL to .env file:**
    ```bash
    NGROK_URL= https://your-ngrok-url

11. **Run Streamlit Server:**
    ```bash
    streamlit run interface.py

**Note:**

- Make sure to replace YOUR-USERNAME and project with your actual GitHub username and project name respectively.
- Ensure that you have proper permissions and necessary dependencies installed before executing the commands.
- For detailed instructions, refer to the documentation or project wiki.


