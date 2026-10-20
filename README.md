# DocGist — Understand Before You Sign 📑

DocGist is a privacy-first, AI-assisted web application designed for students and families to understand complex documents (**PG/rental agreements**, **scholarship notices**, and **internship offers**) before signing them.

Built with **Python**, **Streamlit**, **pypdf**, and the official **Google GenAI SDK (`google-genai`)**.

---

## 🚀 Quickstart Guide (Windows)

### 1. Open Terminal (PowerShell or Command Prompt)
Navigate to the project folder:
```powershell
cd C:\Users\study\.gemini\antigravity\scratch\docgist
```

### 2. Install Required Packages
```powershell
pip install -r requirements.txt
```

### 3. Run the Web Application
```powershell
python -m streamlit run app.py
```
Streamlit will launch and open your default browser at `http://localhost:8501`.

### 4. Run the Full Automated Test Suite (All 7 Phases)
```powershell
python -m pytest -v
```
Or run individual phase test scripts:
```powershell
python test_phase1.py
python test_phase2.py
python test_phase3.py
python test_phase4.py
python test_phase5.py
python test_phase6.py
python test_phase7.py
```

---

## 🔑 Gemini API Setup (Optional)

DocGist supports both **Live Gemini AI Analysis** and a **Free Local Demo Mode**:
1. **Via Web Interface (Easiest):** Paste your key into the **"Gemini API Key"** field in the left sidebar. It stays only in your active browser session memory.
2. **Via Environment Variable:**
   ```powershell
   $env:GEMINI_API_KEY="AIzaSy..."
   ```
3. **Via Streamlit Secrets:** Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and add:
   ```toml
   GEMINI_API_KEY = "AIzaSy..."
   ```
4. **No API Key?** No problem! DocGist automatically falls back to the built-in offline heuristic engine so you can demo all UI features, risk verifications, and bilingual presets completely free.

---

## 📂 Project Structure

```
docgist/
├── .streamlit/
│   ├── config.toml           # Production UI theme, 10MB upload cap & XSRF security
│   └── secrets.toml.example  # Template for configuring GEMINI_API_KEY safely
├── app.py                    # Main Streamlit web app (Bilingual UI, PDF upload, tabs, report export)
├── gemini_analyzer.py        # Official google-genai SDK integration, Pydantic schemas, quote verifier & eligibility engine
├── pdf_processor.py          # Local RAM PDF text extraction (pypdf) & scanned/encrypted document checks
├── translations.py           # Bilingual English/Hindi string catalogs, localized presets & Markdown report builder
├── sample_data.py            # Realistic sample contracts & structured analysis outputs
├── test_phase1.py            # Phase 1 UI foundation tests
├── test_phase2.py            # Phase 2 PDF extraction & edge-case tests
├── test_phase3.py            # Phase 3 Gemini API, schema & prompt-injection defense tests
├── test_phase4.py            # Phase 4 evidence-based risk & verbatim quote verification tests
├── test_phase5.py            # Phase 5 personalized profile eligibility tests
├── test_phase6.py            # Phase 6 bilingual (Hindi/English) & report export tests
├── test_phase7.py            # Phase 7 end-to-end security, privacy, edge-case & deployment readiness suite
├── requirements.txt          # Minimal, beginner-friendly dependencies
├── .gitignore                # Protects .env and secrets.toml from being committed to Git
└── README.md                 # Complete documentation, deployment guide & hackathon pitch notes
```

---

## 🎯 Features Completed Across All 7 Phases

### Phase 1: Clean, Mobile-Friendly Interface
- Responsive layout with intuitive tabs (`📋 5-Point Summary`, `⚠️ Risk & Clause Breakdown`, `🎓 Profile Eligibility Check`).
- Prominent legal disclaimer clarifying that DocGist is an educational reading aid, not legal counsel.

### Phase 2: Local PDF Extraction & Validation (`pypdf`)
- Extracts text strictly in local RAM without writing files to disk.
- Detects scanned/image-only PDFs (0 extractable characters) and explains that OCR is not supported yet, guiding users to paste text directly.
- Gracefully handles password-protected and corrupted files.

### Phase 3: Secure Gemini API Integration (`google-genai`)
- Uses the official `genai.Client` with structured Pydantic `response_schema` (`DocumentAnalysisSchema`).
- Encapsulates document text inside `<UNTRUSTED_DOCUMENT_CONTENT>` tags with strict system instructions to defeat indirect prompt injection.
- Automatically cascades across candidate Gemini models (`gemini-3.8-flash`, `gemini-2.0-flash`, `gemini-1.5-flash`) and falls back offline if rate-limited.

### Phase 4: Evidence-Based Risk Assessment & Anti-Hallucination Guardrail
- Flags clauses with **Red** (High Risk), **Yellow** (Caution), and **Green** (Standard/Clear) indicators.
- Programmatically verifies every AI-extracted `exact_quote` against the raw document text (`verify_quotation()`), displaying a live verification badge (`✅ Verbatim Quote Verified`).
- Explicitly reminds users that a Green indicator does not certify a document as legally safe.

### Phase 5: Personalized Student Profile Eligibility Engine
- Matches stated document criteria against the user's sidebar profile (**Course**, **Year**, **Domicile State**, **Category**, **Family Income**).
- Recalculates eligibility in real time when any sidebar dropdown changes.
- Marks missing criteria as *"Need more information"* instead of guessing, and marks rental agreements as *"Not Applicable"*.

### Phase 6: Bilingual Support (English / हिंदी) & Exportable Reports
- Instant sidebar toggle between **English** and **हिंदी (Hindi)**.
- Keeps `exact_quote` in its original verbatim document language during Hindi mode so algorithmic quote verification remains 100% accurate.
- One-click **📥 Download Analysis Report (Markdown)** button to share findings with parents or mentors.

### Phase 7: End-to-End Testing, Edge-Case Hardening & Deployment Readiness
- Validates short/unusable text inputs (`< 20` characters) with clear guidance.
- Enforces zero hardcoded secrets, zero database/disk writes, and `.streamlit/config.toml` security settings.

---
