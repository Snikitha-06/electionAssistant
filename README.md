# Election Process Assistant 🗳️

An interactive, AI-powered educational web application built with Flask, designed to demystify the electoral process. 

## Features
- **Interactive Timeline**: Step-by-step journey from candidate declaration to inauguration.
- **Knowledge Quiz**: Test your understanding of electoral systems and terms.
- **Glossary**: Searchable dictionary of political and electoral terminology.
- **World Comparison**: Compare the U.S. system with the UK, India, and Germany.
- **Ask Anything**: Pre-configured prompts to deep-dive into complex political topics.

## Tech Stack
- **Backend**: Python 3.11+, Flask
- **Frontend**: HTML5, Vanilla CSS, Vanilla JavaScript
- **Deployment**: Docker, Google Cloud Run, Gunicorn

---

## Step-by-Step Instructions

### Prerequisites
- Python 3.11 or higher installed on your system.

### 1. Local Development Setup

1. **Navigate to the Project Folder**
   Open your terminal or command prompt and navigate to the project directory:
   ```bash
   cd "path/to/election assistant"
   ```

2. **Create a Virtual Environment**
   It's highly recommended to use a virtual environment to manage Python dependencies securely:
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**
   - **Windows:**
     ```cmd
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**
   Install the required libraries (Flask, Gunicorn) from the requirements file:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**
   Start the Flask development server:
   ```bash
   python app.py
   ```

6. **View in Browser**
   Open your web browser and navigate to:
   `http://127.0.0.1:5000`

---

### 2. Deployment to Google Cloud Run

This application includes a `Dockerfile` and is fully configured for deployment on Google Cloud Run.

1. **Prerequisites**
   Ensure you have the [Google Cloud CLI (gcloud)](https://cloud.google.com/sdk/docs/install) installed.

2. **Authenticate with Google Cloud**
   Log in to your Google account via the CLI:
   ```bash
   gcloud auth login
   ```

3. **Set Your Project**
   Set your target project using your actual Google Cloud Project ID (e.g., `election-assistant-495109`):
   ```bash
   gcloud config set project [YOUR_PROJECT_ID]
   ```

4. **Deploy**
   Run the following command to build the Docker container and deploy it to Cloud Run automatically:
   ```bash
   gcloud run deploy election-assistant --source . --region us-central1 --allow-unauthenticated
   ```

5. **Troubleshooting Deployment Permissions**
   If you encounter a `PERMISSION_DENIED` error during the build, you need to grant the necessary IAM roles to your default Compute Engine Service Account. Run these commands:
   ```bash
   # Grant Cloud Build rights
   gcloud projects add-iam-policy-binding [YOUR_PROJECT_ID] \
       --member="serviceAccount:[PROJECT_NUMBER]-compute@developer.gserviceaccount.com" \
       --role="roles/cloudbuild.builds.builder"

   # Grant Storage Viewer rights
   gcloud projects add-iam-policy-binding [YOUR_PROJECT_ID] \
       --member="serviceAccount:[PROJECT_NUMBER]-compute@developer.gserviceaccount.com" \
       --role="roles/storage.objectViewer"
   ```
   *(Replace `[YOUR_PROJECT_ID]` and `[PROJECT_NUMBER]` with your actual project details, then run the deploy command again).*
