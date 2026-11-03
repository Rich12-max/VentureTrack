# VentureTrack — Deployment & Hosting Guide
**Academic Mini Project 13** | **Author:** Richa Sharma (`25BAI10049`)  
**Deployment Profile:** Zero-Cost Cloud & Local Production Architecture  

---

## 1. Local Production Deployment

VentureTrack is engineered to run from the root directory on macOS, Linux, or Windows with zero external service dependencies or API credentials.

### Prerequisites
- Python 3.10 through 3.13
- Git & pip

### Step-by-Step Local Launch
```bash
# 1. Clone repository and navigate to root directory
git clone <repository-url>
cd Richa_Sharma_25BAI10049

# 2. (Recommended) Create and activate a clean virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install verified dependencies
pip install -r requirements.txt

# 4. Verify system integrity before launch
pytest tests/ -v

# 5. Launch the VentureTrack Platform
streamlit run app.py
```
*The application will automatically initialize on `http://localhost:8501`.*

---

## 2. Zero-Cost Cloud Deployment: Streamlit Community Cloud

VentureTrack can be hosted publicly on **Streamlit Community Cloud** with zero cost, zero credit cards, and zero external infrastructure requirements.

### Architecture Compatibility Audit
- **Path Resolution**: All filesystem paths in `src/config.py`, `src/cleaning.py`, and `views/` use `Path(__file__).resolve().parent.parent` relative anchors. No absolute local paths are present in runtime code.
- **Data Availability**: The Kaggle raw and cleaned datasets are committed under `data/`, requiring no external database or S3 bucket.
- **Zero Secrets / API Keys**: The application is fully self-contained. It requires no environment variables or cloud keys to function.
- **Theme Pre-configuration**: The light institutional theme is pre-configured in `.streamlit/config.toml` (`base = "light"`).

### Step-by-Step Cloud Deployment Instructions
1. **Push Repository to GitHub**:
   Ensure all files including `app.py`, `requirements.txt`, `data/`, `src/`, `views/`, and `.streamlit/config.toml` are committed and pushed to your GitHub repository:
   ```bash
   git add .
   git commit -m "feat: complete academic mini project 13 delivery"
   git push origin main
   ```
2. **Access Streamlit Community Cloud**:
   - Navigate to [share.streamlit.io](https://share.streamlit.io).
   - Sign in with your GitHub account.
3. **Configure New App**:
   - Click **"New app"**.
   - **Repository**: Select your GitHub repository (`.../Richa_Sharma_25BAI10049`).
   - **Branch**: `main` (or default branch).
   - **Main file path**: `app.py`.
   - **Advanced settings**: Python 3.11 or 3.12 (standard container).
4. **Deploy**:
   - Click **"Deploy!"**.
   - Streamlit Cloud will run `pip install -r requirements.txt` and launch the application.

---

## 3. Containerized Deployment (Docker)

For reproducible, containerized local hosting or deployment to Google Cloud Run / Render / AWS ECS, a clean Docker configuration is provided:

### Sample `Dockerfile`
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency specification
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Configure container healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Launch application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build & Run Commands
```bash
# Build Docker image
docker build -t venturetrack:latest .

# Run container on port 8501
docker run -p 8501:8501 venturetrack:latest
```

---

## 4. Verification & Health Monitoring

The application includes an internal health check endpoint exposed automatically by Streamlit at:
```http
GET http://localhost:8501/_stcore/health
```
A returning HTTP status of `200 OK` confirms active server readiness.

