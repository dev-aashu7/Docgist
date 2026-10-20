# DocGist — Understand Before You Sign 📑
## Complete Prototype Reference Report & Hackathon PPT Blueprint

> **How to use this document:** This report is structured so you can directly copy-paste bullet points, architecture diagrams, workflows, and talking points onto your PowerPoint / Canva / Google Slides deck, while also serving as your technical reference sheet during Judge Q&A.

---

## 1. Executive Summary & Elevator Pitch

- **Project Name:** DocGist — *Understand Before You Sign*
- **One-Line Tagline:** A privacy-first, bilingual (English/Hindi) AI document scrutiny tool that helps students and families spot hidden traps, verify exact clauses, and check personal eligibility before signing PG agreements, internship offers, or scholarship notices.
- **Target Audience:** College students, first-time renters, fresh graduates, and non-English-speaking parents across India.
- **Core Innovation:** Unlike generic AI chat wrappers that summarize vaguely or hallucinate legal advice, **DocGist enforces Evidence-Based Clause Scrutiny**—every flagged risk and eligibility rule is backed by a verbatim quotation that is programmatically verified against the raw document text in local RAM.

---

## 2. The Problem Statement (Why DocGist Matters)

Every year, millions of students move to new cities for college or internships and sign legally binding documents without understanding the fine print:
1. **Predatory PG / Rental Agreements:** Hidden clauses like *24-hour verbal eviction*, *mandatory 20% cleaning deductions*, or *100% deposit forfeiture* during a 6-month lock-in period cost students tens of thousands of rupees.
2. **Exploitative Internship Offer Letters:** Unfair *₹50,000 training penalty bonds*, *2-year global non-compete restrictions*, and stipends tied subjectively to "deliverable completion."
3. **Complex Scholarship Notices:** Strict multi-layered eligibility rules (Degree + Year + Domicile State + Caste Category + Tahsildar-certified Income Ceiling) cause mass application rejections over minor documentary mismatches.
4. **Language & Jargon Barriers:** Documents are written in dense English legalese, making it difficult for students and their Hindi-speaking parents to review terms together.
5. **AI Hallucination & Privacy Risks:** Uploading sensitive personal contracts to generic chatbots risks permanent data logging and fabricated legal conclusions.

---

## 3. Recommended 10-Slide Hackathon PPT Structure

| Slide # | Slide Title | Key Content to Put on Slide | Visual / Graphic to Include |
| :--- | :--- | :--- | :--- |
| **Slide 1** | **Title Slide** | **DocGist — Understand Before You Sign** <br> *AI-Powered Evidence-Based Document Scrutiny for Students & Families* | App logo, tagline, team name |
| **Slide 2** | **The Real-World Problem** | • Predatory PG lock-ins & deposit forfeitures <br> • ₹50k internship penalty bonds & global non-competes <br> • Confusing scholarship eligibility rules & language barriers | 3 icons: Home (PG), Briefcase (Internship), Graduation Cap (Scholarship) |
| **Slide 3** | **Why Existing Tools Fail** | • Lawyers are expensive for ₹12k/month PG leases <br> • Generic LLMs hallucinate clauses & store private contracts <br> • English-only interfaces exclude parents from decision-making | Comparison table: *Manual Reading vs. Generic Chatbots vs. DocGist* |
| **Slide 4** | **Meet DocGist (Our Solution)** | • **5-Point Plain Summary** + **Boundary Fact Cards** <br> • **Red / Yellow / Green Risk Scoring** with **Verified Exact Quotes** <br> • **Dynamic Student Profile Eligibility Engine** <br> • **1-Click English / हिंदी Toggle & Report Export** | Full screenshot of the DocGist main dashboard |
| **Slide 5** | **System Architecture & Workflow** | • Local RAM PDF Parsing (`pypdf`) -> Prompt Injection Firewall -> Gemini Structured Output (`Pydantic`) -> Algorithmic Quote Verifier (`SequenceMatcher`) | System Architecture Flowchart (Section 4) |
| **Slide 6** | **Deep Dive 1: Anti-Hallucination Engine** | • AI must cite an exact verbatim quote for every risk <br> • Python verifies the quote against raw text (Exact -> Normalized -> Fuzzy >= 85%) <br> • Quotes stay verbatim even in Hindi mode! | Screenshot of a Red Risk Card showing `✅ Verbatim Quote Verified` |
| **Slide 7** | **Deep Dive 2: Personalized Eligibility Check** | • 5-Factor Student Profile (Course, Year, State, Category, Income) <br> • Instant recalculation without re-calling the LLM <br> • Never guesses missing rules (*"Need more information"*) | Screenshot of the `🎓 Profile Eligibility Check` tab (Green vs. Red state) |
| **Slide 8** | **Privacy, Security & Reliability** | • **Zero-Storage Guarantee:** `io.BytesIO` in RAM, zero databases <br> • **Indirect Prompt Injection Defense:** `<UNTRUSTED_DOCUMENT_CONTENT>` tags <br> • **100% Uptime:** Multi-model cascade + offline heuristic engine | Shield icon + 3 security pillars |
| **Slide 9** | **Quality Assurance & Testing** | • Built across 7 structured engineering phases <br> • **44 Automated Unit & UI Tests (`pytest` + Streamlit `AppTest`)** passing in `< 5s` <br> • Handles scanned PDFs (0 text), encrypted PDFs, and short inputs | Screenshot of terminal showing `44 passed in 4.79s` |
| **Slide 10** | **Future Scope & Impact** | • Local OCR (`Tesseract`) for scanned camera photos <br> • Regional language expansion (Marathi, Tamil, Telugu, Bengali) <br> • Counter-clause generator to help students negotiate fair terms | Roadmap timeline graphic |

---

## 4. Detailed Breakdown of Core Features & Internal Working

### 4.1 Local PDF Extraction & Validation (`pdf_processor.py`)
- **How it works:** Reads uploaded PDF bytes directly from memory using `io.BytesIO` and `pypdf.PdfReader`.
- **Edge Cases Handled:**
  1. **Encrypted PDFs:** Checks `reader.is_encrypted` and prompts the user to unlock the file first.
  2. **Scanned Image PDFs (No OCR):** If a PDF has pages (`page_count > 0`) but zero extractable text (`len(full_text) == 0`), it detects that the file is a camera scan and gracefully explains that OCR is not yet supported, guiding the user to the **"Paste Text Directly"** option.
  3. **Corrupted Files:** Catches `PdfReadError` without crashing the server.
  4. **Built-in Test PDF Generators:** Functions `create_sample_text_pdf()` and `create_blank_scanned_pdf_simulation()` construct valid PDF binary streams from scratch in memory so users and judges can test PDF uploads with one click.

### 4.2 Structured Gemini AI & Prompt Defense (`gemini_analyzer.py`)
- **Official SDK & Schema Enforcement:** Uses `google-genai` (`genai.Client`) with `response_mime_type="application/json"` and Pydantic's `DocumentAnalysisSchema`. This guarantees the AI always returns deterministic fields:
  - `document_type` & `document_type_confidence`
  - `five_point_summary` (strictly normalized to 5 bullet points)
  - Boundary Fact Cards: `identified_parties`, `key_dates_or_deadlines`, `financial_terms`, and `missing_critical_details`
  - `risks` (List of `RiskClauseSchema`)
  - `eligibility` (`DocumentEligibilitySchema`)
- **Indirect Prompt Injection Firewall:** User documents are treated as untrusted data. `build_analysis_prompt()` isolates the text inside `<UNTRUSTED_DOCUMENT_CONTENT>` tags, and `SYSTEM_INSTRUCTION` explicitly forbids executing any instructions found inside those tags.
- **High-Availability Model Cascade:** Automatically attempts `gemini-3.8-flash` -> `gemini-2.0-flash` -> `gemini-1.5-flash`. If no API key is provided or cloud traffic spikes (`HTTP 503`/`429`), it seamlessly transitions to `mock_analyze_document()` so live demos never fail.

### 4.3 Evidence-Based Risk Scoring & Algorithmic Quote Verifier (`verify_quotation`)
- **Tricolor Risk Classification:**
  - 🚨 **Red (High Risk / Harsh):** Unilateral 24-hour eviction, 100% deposit forfeiture, ₹50,000 exit penalty bonds, 2-year global non-competes.
  - ⚠️ **Yellow (Caution / Restrictive):** Mandatory 20% painting deductions, stipend tied to subjective deliverables, strict Tahsildar certificate mandates.
  - 🟢 **Green (Clear / Standard):** Explicit monthly rent/stipend amounts and fixed tenure durations. *(Includes a mandatory legal guardrail stating that Green does **not** certify a contract as legally safe).*
- **3-Tier Quote Verification Algorithm:**
  Every risk and eligibility rule must include an `exact_quote`. Python validates it in 3 steps:
  1. **Tier 1 (Exact Match):** Checks if the exact string (ignoring surrounding quotes/ellipses) is a substring of the document (`similarity = 1.0` -> Green Badge `✅ Verbatim Document Quote Verified`).
  2. **Tier 2 (Whitespace/Case Normalized Match):** Collapses line breaks and multiple spaces from PDF formatting (`re.sub(r'\s+', ' ', text)`). If matched, awards Green Badge (`✅ Verbatim Quote Verified (Normalized)`).
  3. **Tier 3 (Sliding-Window Fuzzy Match):** Uses `difflib.SequenceMatcher` across sliding windows of the document. If similarity >= 85%, shows a Yellow Badge; if < 85%, flags a Red Badge (`❌ Quote Unverified — Potential AI Paraphrase/Hallucination`).

### 4.4 Dynamic Student Profile Eligibility Engine (`evaluate_profile_eligibility`)
- Evaluates scholarship notices and internship offers against 5 sidebar attributes:
  1. **Course / Degree** (e.g., *B.Tech / B.E.* vs. *B.Com / BBA*)
  2. **Current Year of Study** (e.g., *2nd/3rd Year* vs. *1st Year*)
  3. **Permanent Domicile State** (e.g., *Maharashtra* vs. *Delhi*)
  4. **Reservation Category** (e.g., *SC / ST / OBC* vs. *General*)
  5. **Annual Family Gross Income** (e.g., *Below ₹2.5 Lakhs* vs. *₹5–8 Lakhs*)
- **Instant Client-Side Reactivity:** Modifying any dropdown in the left sidebar recalculates the entire eligibility breakdown instantaneously without making redundant API calls.
- **Context Awareness:** Automatically detects PG/Rental agreements and marks eligibility as `"Not Applicable"` since tenancy contracts apply equally to all signers.

### 4.5 Bilingual Internationalization & Report Exporter (`translations.py`)
- **Complete UI Catalog (`UI_STRINGS`):** Over 55 UI keys translated across English and conversational Devanagari Hindi (`हिंदी (Hindi)`).
- **Cross-Language Quote Preservation:** When Hindi is active, explanations and summaries are presented in Hindi, while `exact_quote` remains in the original document language so that `verify_quotation()` continues to pass 100% of the time.
- **Portable Markdown Report (`generate_downloadable_report`):** Compiles a clean, shareable `.md` report in memory containing the legal disclaimer, 5-point summary, risk breakdown with quotes, and student profile eligibility results.
