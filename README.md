# Content Intelligence Engine 🚀

An asynchronous, AI-powered pipeline that transforms raw event media into platform-ready marketing assets. Built with Python, FastAPI, Next.js, and Google Gemini.

## 🌟 Overview

The Content Intelligence Engine automates the heavy lifting of event marketing. It ingests folders of images and videos, uses a Vision-Language Model (VLM) to select the highest-quality "hero moments," and orchestrates a multi-agent workflow to generate professional case studies, social media posts, and voice-overs.

### **Core Features**
- **Explainable Media Selection:** Uses `gemini-2.5-flash` to score assets (1-10) for technical quality and marketing utility.
- **Multi-Modal Production:** Automatically samples video keyframes and generates high-quality audio voice-overs using LiveKit TTS.
- **Hierarchical Agents:**
  - **Analyst:** Drafts 300-word deep-dive case studies.
  - **Creator:** Generates high-engagement LinkedIn and Instagram content.
  - **QA Agent:** Self-reflects to prevent hallucinations and ensure metadata grounding.
- **SaaS Architecture:** Secure JWT-based authentication, multi-tenant data isolation, and cloud storage integration (Supabase).
- **Interactive Dashboard:** Modern Next.js interface for real-time tracking and human-in-the-loop asset review.

---

## 🏗️ Architecture

```text
content-design-engine/
├── frontend/             # Next.js 15 Dashboard (React, Tailwind, Lucide)
├── src/
│   ├── api/              # FastAPI REST Service & JWT Auth
│   ├── ingestion/        # Media scanning & Video keyframe extraction
│   ├── selection/        # Explainable VLM scoring logic
│   ├── agents/           # Analyst, Creator, QA, and Voice Agents
│   ├── orchestration/    # Async background workflow loop
│   └── database/         # SQLAlchemy models & Supabase Storage
├── main.py               # Unified CLI/Server entry point
└── requirements.txt      # Backend dependencies
```

---

## 🚀 Getting Started

### **1. Prerequisites**
- Python 3.10+
- Node.js 18+
- Google Gemini API Key

### **2. Backend Setup**
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Create a .env file:
# GEMINI_API_KEY=your_key
# OPENAI_API_KEY=your_key (for Voice/TTS)
# SUPABASE_URL=...
# SUPABASE_SERVICE_ROLE_KEY=...
```

### **3. Frontend Setup**
```bash
cd frontend
npm install
```

### **4. Launch**
```bash
# Terminal 1: Start Backend
python main.py serve

# Terminal 2: Start Dashboard
cd frontend
npm run dev
```

---

## 🛠️ Go-To-Market Roadmap

- [x] **Stage 1: Cloud Pivot** (FastAPI, Postgres, Async Tasks).
- [x] **Stage 2: Multi-Modal Mastery** (Video, Brand RAG, Voice-Over).
- [x] **Stage 3: SaaS Dashboard** (Interactive review UI).
- [ ] **Phase 4: Commercialization** (Stripe integration, Team collaboration).

---

## 📜 License
MIT License. Built for the Sovereign AI era.
