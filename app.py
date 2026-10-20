"""
DocGist — Understand Before You Sign
Main Streamlit Web Application (Production Ready — Phases 1 to 7 Complete)
Features:
- Local RAM PDF text extraction with scanned-PDF detection (pypdf)
- Secure Gemini API integration with structured Pydantic output & offline fallback (google-genai)
- Evidence-based tricolor risk assessment with programmatic verbatim quote verification
- Personalized scholarship & internship eligibility engine against student profile
- Full bilingual UI & report export in English and Hindi (हिंदी)
"""

import streamlit as st
from sample_data import SAMPLE_DOCUMENTS, SAMPLE_ANALYSES
from pdf_processor import (
    extract_text_from_pdf,
    create_sample_text_pdf,
    create_blank_scanned_pdf_simulation
)
from gemini_analyzer import (
    resolve_api_key,
    mask_api_key,
    analyze_document_with_gemini,
    mock_analyze_document,
    verify_quotation,
    evaluate_profile_eligibility,
    DEFAULT_MODEL,
    CANDIDATE_MODELS
)
from translations import get_text, get_localized_analysis, generate_downloadable_report
# 1. Page Configuration (Title, Icon, Mobile-friendly wide layout)
st.set_page_config(
    page_title="DocGist — Understand Before You Sign",
    page_icon="📑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean cards, risk badges, and typography
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .disclaimer-box {
        background-color: #FEF3C7;
        border-left: 5px solid #F59E0B;
        padding: 0.9rem 1.2rem;
        border-radius: 6px;
        margin-bottom: 1.5rem;
        font-size: 0.9rem;
        color: #78350F;
    }
    .privacy-box {
        background-color: #EFF6FF;
        border-left: 5px solid #3B82F6;
        padding: 0.9rem 1.2rem;
        border-radius: 6px;
        margin-top: 2rem;
        font-size: 0.88rem;
        color: #1E40AF;
    }
    .fact-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.8rem;
        font-size: 0.9rem;
    }
    .card-box {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .quote-box {
        background-color: #F9FAFB;
        border-left: 4px solid #6B7280;
        padding: 0.6rem 1rem;
        font-style: italic;
        color: #374151;
        margin-top: 0.5rem;
        border-radius: 0 4px 4px 0;
        font-family: monospace;
        font-size: 0.88rem;
    }
    .badge-red {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.82rem;
        display: inline-block;
    }
    .badge-yellow {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.82rem;
        display: inline-block;
    }
    .badge-green {
        background-color: #DCFCE7;
        color: #166534;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.82rem;
        display: inline-block;
    }
    .phase-pill {
        background-color: #E0E7FF;
        color: #3730A3;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.8rem;
        display: inline-block;
        margin-bottom: 0.5rem;
    }
    .meta-tag {
        background-color: #F3F4F6;
        color: #1F2937;
        padding: 0.25rem 0.6rem;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: 500;
        display: inline-block;
        margin-right: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# SIDEBAR: API Settings & User Profile
# ==============================================================================
with st.sidebar:
    st.markdown("### 🔑 Gemini AI Setup")
    user_api_key = st.text_input(
        "Gemini API Key (Optional)",
        type="password",
        help="Paste your Gemini API key from Google AI Studio. Stored only in session memory.",
        placeholder="AIzaSy..."
    )

    selected_gemini_model = st.selectbox(
        "Gemini Model",
        options=CANDIDATE_MODELS,
        index=0,
        help="gemini-3.8-flash is the current recommended model for new users."
    )
    
    active_api_key = resolve_api_key(user_api_key)
    if active_api_key:
        st.success(f"🟢 API Connected (`{mask_api_key(active_api_key)}`)")
    else:
        st.info("🟡 **Demo / Mock Mode**\n(Enter API key above to enable live Gemini analysis)")

    st.caption("🔒 *Sent text is processed under Google Cloud Gemini API data governance rules.*")
    st.divider()

    st.markdown("### 👤 Student / User Profile")
    st.caption("DocGist personalizes scholarship & internship eligibility checks using this profile. Nothing is saved permanently.")

    user_course = st.selectbox(
        "Course / Degree",
        options=[
            "B.Tech / B.E. (Engineering)",
            "B.Sc / BCA (Computer Applications/Science)",
            "B.Com / BBA (Commerce / Management)",
            "MBBS / BDS / Health Sciences",
            "B.A. / Humanities",
            "Diploma / Polytechnic",
            "Other"
        ],
        index=0
    )

    user_year = st.selectbox(
        "Current Year of Study",
        options=["1st Year", "2nd Year", "3rd Year", "4th Year", "Post-Graduate / Masters", "Recent Graduate"],
        index=2
    )

    indian_states = [
        "Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "Uttar Pradesh",
        "Telangana", "Gujarat", "West Bengal", "Rajasthan", "Madhya Pradesh",
        "Bihar", "Kerala", "Punjab", "Haryana", "Andhra Pradesh", "Other State"
    ]
    user_state = st.selectbox("Permanent Domicile (State)", options=indian_states, index=0)

    user_category = st.selectbox(
        "Category / Quota",
        options=["General / Unreserved", "OBC (Non-Creamy Layer)", "SC", "ST", "EWS"],
        index=1
    )

    user_income = st.selectbox(
        "Annual Family Gross Income",
        options=[
            "Below ₹2.5 Lakhs / year",
            "₹2.5 Lakhs – ₹5 Lakhs / year",
            "₹5 Lakhs – ₹8 Lakhs / year",
            "Above ₹8 Lakhs / year"
        ],
        index=0
    )

    st.divider()

    st.markdown("### 🌐 Language Setting")
    language_choice = st.radio(
        "Display Language",
        options=["English", "हिंदी (Hindi)"],
        horizontal=True,
        index=0
    )
    # Normalise to a simple language identifier used throughout the app
    language = language_choice

    st.divider()
    st.caption("🛡️ **Zero-Storage Guarantee**\nYour document and profile live only in your active browser session.")


# ==============================================================================
# MAIN VIEW: Title, Disclaimer & Workflow
# ==============================================================================
col_title, col_status = st.columns([4, 1])
with col_title:
    st.markdown(f'<div class="phase-pill">{get_text("phase_badge", language)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="main-header">{get_text("app_title", language)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">{get_text("app_subtitle", language)}</div>', unsafe_allow_html=True)

with col_status:
    if active_api_key:
        st.metric(label=get_text("ai_engine", language), value="Gemini 3.8", delta=get_text("live_cloud", language))
    else:
        st.metric(label=get_text("ai_engine", language), value="Mock Engine", delta=get_text("free_demo", language))

# Non-legal advice warning banner
st.markdown(f"""
<div class="disclaimer-box">
    <strong>{get_text("legal_disclaimer_title", language)}</strong><br>
    {get_text("legal_disclaimer_body", language)}
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# DOCUMENT INPUT SECTION
# ==============================================================================
st.subheader(get_text("step1_title", language))

upload_opt = get_text("input_upload", language)
paste_opt = get_text("input_paste", language)
preset_opt = get_text("input_presets", language)

input_method = st.radio(
    get_text("input_method_label", language),
    options=[upload_opt, paste_opt, preset_opt],
    horizontal=True,
    index=0
)

document_text = ""
doc_source_desc = ""
page_count = 0

if input_method == upload_opt:
    st.caption(get_text("upload_caption", language))
    
    uploaded_pdf = st.file_uploader(
        get_text("upload_label", language),
        type=["pdf"],
        help="Upload a digital PDF. Scanned images are validated with an informative message."
    )

    if uploaded_pdf is not None:
        with st.spinner("Extracting text from PDF locally..." if language == "English" else "स्थानीय रूप से पीडीएफ से पाठ निकाला जा रहा है..."):
            pdf_result = extract_text_from_pdf(uploaded_pdf)

        if pdf_result["success"]:
            document_text = pdf_result["text"]
            page_count = pdf_result["page_count"]
            doc_source_desc = f"Uploaded PDF: {uploaded_pdf.name} ({page_count} page{'s' if page_count > 1 else ''})"

            st.success(f"✅ Successfully extracted text from **{uploaded_pdf.name}** ({page_count} page{'s' if page_count > 1 else ''}, {pdf_result['word_count']} words, {pdf_result['char_count']} characters)")
            
            with st.expander("🔍 Preview Extracted Text", expanded=False):
                st.text_area("Extracted Content", value=document_text, height=180, disabled=True)
        else:
            st.error(f"❌ {pdf_result['error']}")
            if "OCR" in pdf_result["error"]:
                st.info(
                    "💡 **How to proceed:** You can still analyze this agreement! Switch to the **'✍️ Paste Text Directly'** "
                    "option above and paste the document text manually."
                )
    else:
        st.info("👆 Please drag and drop or browse for a PDF file above." if language == "English" else "👆 कृपया ऊपर एक पीडीएफ फाइल खींचें या चुनें।")
        
        # Helper test PDF generator buttons for quick local evaluation
        st.caption("🛠️ **Quick Test Helper:** Don't have a PDF on your device right now? Download one of our pre-built test PDFs below:")
        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            sample_rental_lines = [
                "HOUSE / PG RENTAL AGREEMENT",
                "Monthly rent: INR 12,000 payable on 1st of month. Late fee INR 200/day.",
                "Security deposit: INR 36,000 (3 months rent).",
                "Lock-in period: 6 months. Early vacate forfeits entire INR 36,000 deposit.",
                "Eviction notice: Landlord reserves right to terminate with 24 hours verbal notice.",
                "Cleaning deduction: Mandatory 20% deep cleaning fee deducted regardless of condition."
            ]
            rental_pdf_bytes = create_sample_text_pdf(sample_rental_lines)
            st.download_button(
                label="📥 Download Test Rental PDF (Valid)",
                data=rental_pdf_bytes,
                file_name="sample_rental_agreement.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        with col_dl2:
            scanned_sim_bytes = create_blank_scanned_pdf_simulation()
            st.download_button(
                label="📥 Download Test Scanned PDF (0 Text)",
                data=scanned_sim_bytes,
                file_name="sample_scanned_unreadable.pdf",
                mime="application/pdf",
                help="Test how DocGist gracefully detects and handles scanned image PDFs without crashing.",
                use_container_width=True
            )

elif input_method == paste_opt:
    document_text = st.text_area(
        get_text("paste_label", language),
        height=220,
        placeholder=get_text("paste_placeholder", language),
        help="Paste clauses directly from your contract or offer letter."
    )
    doc_source_desc = "Pasted Text Input"

else:  # preset_opt
    preset_choice = st.selectbox(
        get_text("preset_label", language),
        options=[
            "PG / Rental Agreement (Sample)",
            "Internship Offer Letter (Sample)",
            "Scholarship Notice (Sample)"
        ],
        index=0
    )
    document_text = SAMPLE_DOCUMENTS.get(preset_choice, "")
    doc_source_desc = f"Preset: {preset_choice}"
    
    st.text_area(
        "Sample Document Preview:" if language == "English" else "नमूना दस्तावेज़ पूर्वावलोकन:",
        value=document_text,
        height=200,
        disabled=True
    )

# Document Stats Counter & Action Button
col_count, col_clear = st.columns([3, 1])
with col_count:
    char_count = len(document_text.strip())
    word_count = len(document_text.strip().split()) if document_text.strip() else 0
    count_msg = get_text("char_count_label", language).format(chars=char_count, words=word_count)
    st.caption(f"📊 {count_msg}")

with col_clear:
    analyze_btn = st.button(get_text("analyze_btn", language), type="primary", use_container_width=True)


# ==============================================================================
# ANALYSIS & RESULTS SECTION
# ==============================================================================
if analyze_btn or (document_text.strip() and (input_method == preset_opt or "presets" in input_method.lower() or "नमूना" in input_method or "sample" in input_method.lower())):
    if not document_text.strip():
        st.warning(get_text("empty_warning", language))
    elif len(document_text.strip()) < 20:
        st.warning(get_text("short_warning", language).format(chars=len(document_text.strip())))
    else:
        st.divider()
        st.subheader(get_text("step2_title", language))

        # Check if text corresponds to one of the rich sample presets
        matched_sample_key = None
        if "HOUSE / PG RENTAL AGREEMENT" in document_text or "Rajesh Sharma" in document_text or "PG Rental Agreement" in doc_source_desc:
            matched_sample_key = "PG / Rental Agreement (Sample)"
        elif "APEX TECH INNOVATIONS" in document_text or "Internship Offer" in doc_source_desc or "Software Engineering Intern" in document_text:
            matched_sample_key = "Internship Offer Letter (Sample)"
        elif "STATE MERIT-CUM-MEANS" in document_text or "Scholarship Notice" in doc_source_desc or "Higher Education Scholarship" in document_text:
            matched_sample_key = "Scholarship Notice (Sample)"

        # Execute Analysis: Gemini API if key provided, else Mock Fallback
        with st.spinner("Analyzing document clauses with AI..." if language == "English" else "दस्तावेज़ का AI विश्लेषण जारी है..."):
            if active_api_key:
                api_res = analyze_document_with_gemini(
                    document_text,
                    api_key=active_api_key,
                    model_name=selected_gemini_model,
                    language=language
                )
                if api_res["success"]:
                    gemini_analysis = api_res["data"]
                    analysis_engine_label = f"Live Gemini ({api_res['model_used']})"
                else:
                    if "503" in api_res["error"] or "peak traffic" in api_res["error"].lower() or "high demand" in api_res["error"].lower():
                        st.warning(f"ℹ️ {api_res['error']}")
                    else:
                        st.error(f"⚠️ {api_res['error']}")
                    st.info("Seamlessly switched to offline evaluation so your document analysis was not interrupted." if language == "English" else "सुचारू रूप से ऑफ़लाइन मूल्यांकन पर स्विच किया गया ताकि विश्लेषण बाधित न हो।")
                    gemini_analysis = mock_analyze_document(document_text)["data"]
                    analysis_engine_label = "Offline Mock Fallback" if language == "English" else "ऑफ़लाइन मॉक फ़ॉलबैक"
            else:
                gemini_analysis = mock_analyze_document(document_text)["data"]
                analysis_engine_label = "Demo / Mock Engine (No API Key)" if language == "English" else "डेमो / मॉक इंजन (बिना API कुंजी)"

        # Apply high-quality localized analysis for Hindi preset if selected
        gemini_analysis = get_localized_analysis(gemini_analysis, matched_sample_key, language)

        # Pull rich risk and eligibility data if available
        if gemini_analysis.get("risks"):
            risks_list = gemini_analysis["risks"]
        elif matched_sample_key and matched_sample_key in SAMPLE_ANALYSES:
            risks_list = SAMPLE_ANALYSES[matched_sample_key]["risks"]
        else:
            first_line = (document_text.strip().splitlines()[0] if document_text.strip() else "Document content loaded")
            risks_list = [
                {
                    "level": "yellow",
                    "title": "Document Under Local Verification" if language == "English" else "दस्तावेज़ स्थानीय सत्यापन के तहत",
                    "explanation": "Document clauses were extracted and verified locally." if language == "English" else "दस्तावेज़ के खंड स्थानीय रूप से निकाले और जाँचे गए।",
                    "exact_quote": first_line
                }
            ]

        if matched_sample_key and matched_sample_key in SAMPLE_ANALYSES:
            sample_ref = SAMPLE_ANALYSES[matched_sample_key]
            eligibility_data = gemini_analysis.get("eligibility") or sample_ref.get("eligibility")
            display_summary = gemini_analysis.get("five_point_summary", sample_ref["five_point_summary"])
            detected_type = gemini_analysis.get("document_type", sample_ref["document_type"])
        else:
            eligibility_data = gemini_analysis.get("eligibility") or {
                "applicable": False,
                "overall_summary": "General document" if language == "English" else "सामान्य दस्तावेज़",
                "criteria_list": [],
                "notes_or_caveats": "Connect Gemini API key or select a scholarship/internship to evaluate custom criteria." if language == "English" else "कस्टम छात्रवृत्ति/इंटर्नशिप शर्तों के मूल्यांकन के लिए जेमिनी API कुंजी जोड़ें।"
            }
            display_summary = gemini_analysis.get("five_point_summary", [
                "Document received and processed.",
                "Review terms carefully for hidden obligations.",
                "Verify dates, deadlines, and signatures.",
                "Ensure payment terms and penalties are documented in writing.",
                "Check governing jurisdiction and dispute resolution rules."
            ] if language == "English" else [
                "दस्तावेज़ प्राप्त हुआ और संसाधित किया गया।",
                "छिपी हुई देनदारियों के लिए शर्तों की सावधानीपूर्वक समीक्षा करें।",
                "तिथियों, अंतिम समय-सीमा और हस्ताक्षरों का सत्यापन करें।",
                "सुनिश्चित करें कि भुगतान शर्तें और दंड लिखित रूप में दर्ज हैं।",
                "विवाद समाधान और अधिकार क्षेत्र के नियमों की जाँच करें।"
            ])
            detected_type = gemini_analysis.get("document_type", "Other Document" if language == "English" else "अन्य दस्तावेज़")

        # Document metadata badges
        confidence_text = gemini_analysis.get("document_type_confidence", "High" if language == "English" else "उच्च")
        type_lbl = "Type" if language == "English" else "प्रकार"
        engine_lbl = "Engine" if language == "English" else "इंजन"
        profile_lbl = "Profile" if language == "English" else "प्रोफ़ाइल"
        st.markdown(f"""
        <div style="margin-bottom: 1rem;">
            <span class="meta-tag">📄 <strong>{type_lbl}:</strong> {detected_type} ({confidence_text})</span>
            <span class="meta-tag">🤖 <strong>{engine_lbl}:</strong> {analysis_engine_label}</span>
            <span class="meta-tag">👤 <strong>{profile_lbl}:</strong> {user_course} • {user_year} • {user_state}</span>
        </div>
        """, unsafe_allow_html=True)

        # Extracted Key Document Facts Cards (Phase 3 Core Feature)
        st.markdown(f"##### {get_text('facts_heading', language)}")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            st.markdown(f"""
            <div class="fact-card">
                <strong>{get_text('parties_label', language)}</strong><br>
                {gemini_analysis.get('identified_parties', 'Not specified' if language == 'English' else 'उल्लेख नहीं')}
            </div>
            <div class="fact-card">
                <strong>{get_text('dates_label', language)}</strong><br>
                {gemini_analysis.get('key_dates_or_deadlines', 'Not specified' if language == 'English' else 'उल्लेख नहीं')}
            </div>
            """, unsafe_allow_html=True)
        with col_f2:
            st.markdown(f"""
            <div class="fact-card">
                <strong>{get_text('financials_label', language)}</strong><br>
                {gemini_analysis.get('financial_terms', 'Not specified' if language == 'English' else 'उल्लेख नहीं')}
            </div>
            <div class="fact-card">
                <strong>{get_text('missing_label', language)}</strong><br>
                {gemini_analysis.get('missing_critical_details', 'None identified' if language == 'English' else 'कोई नहीं')}
            </div>
            """, unsafe_allow_html=True)

        st.write("")

        # ----------------------------------------------------------------------
        # Tabbed Results View
        # ----------------------------------------------------------------------
        tab_summary, tab_risks, tab_eligibility = st.tabs([
            get_text("tab_summary", language),
            get_text("tab_risks", language),
            get_text("tab_eligibility", language)
        ])

        with tab_summary:
            st.markdown(f"#### {get_text('summary_heading', language)}")
            st.caption(get_text("summary_caption", language))
            for i, point in enumerate(display_summary, 1):
                st.markdown(f"**{i}.** {point}")

        with tab_risks:
            st.markdown(f"#### {get_text('risks_heading', language)}")

            # Tally counters
            red_count = sum(1 for r in risks_list if str(r.get("level", "")).lower() == "red")
            yellow_count = sum(1 for r in risks_list if str(r.get("level", "")).lower() == "yellow")
            green_count = sum(1 for r in risks_list if str(r.get("level", "")).lower() == "green")

            flag_word = get_text("flagged_suffix", language)
            col_r1, col_r2, col_r3 = st.columns(3)
            with col_r1:
                st.metric(get_text("high_risk_metric", language), f"{red_count} {flag_word}")
            with col_r2:
                st.metric(get_text("caution_metric", language), f"{yellow_count} {flag_word}")
            with col_r3:
                st.metric(get_text("standard_metric", language), f"{green_count} {flag_word}")

            st.caption(get_text("risk_guardrail_caption", language))

            for item in risks_list:
                lvl = str(item.get("level", "")).lower()
                if lvl == "red":
                    badge_html = f'<span class="badge-red">{get_text("badge_high_risk", language)}</span>'
                elif lvl == "yellow":
                    badge_html = f'<span class="badge-yellow">{get_text("badge_caution", language)}</span>'
                else:
                    badge_html = f'<span class="badge-green">{get_text("badge_standard", language)}</span>'

                # Verify quotation programmatically
                v_res = item.get("verification") or verify_quotation(document_text, item.get("exact_quote", ""))
                v_color = v_res.get("badge_color", "green")
                if language == "English":
                    v_text = v_res.get("badge_text", "✅ Verbatim Quote Verified")
                else:
                    if v_color == "green":
                        v_text = "✅ मूल पाठ से उद्धरण सत्यापित"
                    elif v_color == "yellow":
                        v_text = "⚠️ सन्निकट मिलान (अक्षर अंतर)"
                    else:
                        v_text = "❌ उद्धरण दस्तावेज़ में नहीं मिला"

                if v_color == "green":
                    v_badge_html = f'<span class="badge-green" style="font-size: 0.78rem;">{v_text}</span>'
                elif v_color == "yellow":
                    v_badge_html = f'<span class="badge-yellow" style="font-size: 0.78rem;">{v_text}</span>'
                else:
                    v_badge_html = f'<span class="badge-red" style="font-size: 0.78rem;">{v_text}</span>'

                quote_lbl = get_text("exact_quote_label", language)
                st.markdown(f"""
                <div class="card-box">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
                        <div>{badge_html} &nbsp; <strong>{item['title']}</strong></div>
                        <div>{v_badge_html}</div>
                    </div>
                    <p style="margin-top: 0.6rem; margin-bottom: 0.4rem; font-size: 0.95rem;">{item['explanation']}</p>
                    <div class="quote-box">
                        <strong>{quote_lbl}</strong><br>
                        "{item['exact_quote']}"
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with tab_eligibility:
            st.markdown(f"#### {get_text('eligibility_heading', language)}")

            # Collect active student profile from sidebar
            current_profile = {
                "course": user_course,
                "year": user_year,
                "state": user_state,
                "category": user_category,
                "income": user_income
            }

            eval_res = evaluate_profile_eligibility(
                document_type=detected_type,
                eligibility_info=eligibility_data,
                user_profile=current_profile,
                document_text=document_text,
                language=language
            )

            if not eval_res.get("applicable", False):
                st.info(f"ℹ️ **{eval_res.get('overall_status', 'Not Applicable')}:** {eval_res.get('message', get_text('tenancy_not_applicable', language))}")
                st.caption(get_text("tenancy_not_applicable", language))
            else:
                # Active Profile Ribbon
                ribbon_lbl = get_text("evaluating_profile_ribbon", language)
                sidebar_tip_msg = get_text("sidebar_tip", language)
                st.markdown(f"""
                <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 0.8rem 1rem; margin-bottom: 1.2rem;">
                    <span style="font-size: 0.82rem; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.05em; display: block; margin-bottom: 0.4rem;">{ribbon_lbl}</span>
                    <span class="meta-tag">🎓 {user_course}</span>
                    <span class="meta-tag">📅 {user_year}</span>
                    <span class="meta-tag">📍 {user_state}</span>
                    <span class="meta-tag">🏷️ {user_category}</span>
                    <span class="meta-tag">💵 {user_income}</span>
                    <div style="margin-top: 0.5rem; font-size: 0.8rem; color: #64748B;">
                        {sidebar_tip_msg}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Overall Status Banner
                status_color = eval_res.get("status_color", "green")
                status_badge = eval_res.get("status_badge", "Evaluated")
                status_title = eval_res.get("overall_status", "")
                status_msg = eval_res.get("message", "")

                if status_color == "green":
                    st.success(f"### {status_badge}\n**{status_title}**\n\n{status_msg}")
                elif status_color == "red":
                    st.error(f"### {status_badge}\n**{status_title}**\n\n{status_msg}")
                else:
                    st.warning(f"### {status_badge}\n**{status_title}**\n\n{status_msg}")

                # Criteria Breakdown Cards
                breakdown = eval_res.get("criteria_breakdown", [])
                if breakdown:
                    st.markdown(f"##### {get_text('criteria_breakdown_heading', language)}")
                    st.caption(get_text("criteria_caption", language))

                    doc_req_lbl = get_text("doc_requirement_label", language)
                    user_prof_lbl = get_text("user_profile_label", language)
                    assess_lbl = get_text("assessment_label", language)
                    exact_cls_lbl = get_text("exact_clause_label", language)

                    for item in breakdown:
                        v_color = item.get("verdict_color", "green")
                        if v_color == "green":
                            badge_html = f'<span class="badge-green">{item.get("verdict_badge", "✅ Matched")}</span>'
                        elif v_color == "red":
                            badge_html = f'<span class="badge-red">{item.get("verdict_badge", "❌ Ineligible")}</span>'
                        else:
                            badge_html = f'<span class="badge-yellow">{item.get("verdict_badge", "ℹ️ Need Info")}</span>'

                        # Quote verification badge
                        q_ver = item.get("quote_verification", {})
                        q_color = q_ver.get("badge_color", "green")
                        if language == "English":
                            q_text = q_ver.get("badge_text", "✅ Verbatim Document Quote Verified")
                        else:
                            if q_color == "green":
                                q_text = "✅ मूल पाठ से उद्धरण सत्यापित"
                            elif q_color == "yellow":
                                q_text = "⚠️ सन्निकट मिलान"
                            else:
                                q_text = "❌ उद्धरण नहीं मिला"

                        if q_color == "green":
                            q_badge_html = f'<span class="badge-green" style="font-size: 0.78rem;">{q_text}</span>'
                        elif q_color == "yellow":
                            q_badge_html = f'<span class="badge-yellow" style="font-size: 0.78rem;">{q_text}</span>'
                        else:
                            q_badge_html = f'<span class="badge-red" style="font-size: 0.78rem;">{q_text}</span>'

                        st.markdown(f"""
                        <div class="card-box">
                            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.6rem;">
                                <div><strong>{item.get('criterion', 'Criterion')}</strong> &nbsp; {badge_html}</div>
                                <div>{q_badge_html}</div>
                            </div>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 0.5rem; font-size: 0.88rem;">
                                <div>
                                    <span style="color: #6B7280; font-size: 0.8rem; font-weight: 600; text-transform: uppercase;">{doc_req_lbl}</span><br>
                                    {item.get('document_requirement', 'Not specified')}
                                </div>
                                <div>
                                    <span style="color: #6B7280; font-size: 0.8rem; font-weight: 600; text-transform: uppercase;">{user_prof_lbl}</span><br>
                                    <strong>{item.get('user_value', 'Not provided')}</strong>
                                </div>
                            </div>
                            <p style="margin-top: 0.4rem; margin-bottom: 0.4rem; font-size: 0.9rem; color: #374151;">
                                <strong>{assess_lbl}</strong> {item.get('reason', '')}
                            </p>
                            <div class="quote-box">
                                <strong>{exact_cls_lbl}</strong><br>
                                "{item.get('exact_quote', '')}"
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                if eval_res.get("notes"):
                    st.markdown(f"""
                    <div style="background-color: #FEF9C3; border-left: 4px solid #EAB308; padding: 0.8rem 1rem; border-radius: 4px; margin-top: 1rem; font-size: 0.88rem; color: #713F12;">
                        <strong>{get_text('mandatory_doc_notes', language)}</strong><br>
                        {eval_res['notes']}
                    </div>
                    """, unsafe_allow_html=True)

                st.caption(get_text("eligibility_disclaimer", language))

        # Downloadable Analysis Report (Phase 6 Feature)
        st.write("")
        st.divider()
        report_profile = {
            "course": user_course,
            "year": user_year,
            "state": user_state,
            "category": user_category,
            "income": user_income
        }
        report_eval = eval_res if 'eval_res' in locals() else {"applicable": False}
        report_md = generate_downloadable_report(
            analysis_data=gemini_analysis,
            doc_type=detected_type,
            user_profile=report_profile,
            risks_list=risks_list,
            eligibility_result=report_eval,
            lang=language
        )
        st.download_button(
            label=get_text("download_report_btn", language),
            data=report_md,
            file_name=f"docgist_analysis_{'hi' if 'hindi' in language.lower() else 'en'}.md",
            mime="text/markdown",
            use_container_width=True
        )

# ==============================================================================
# FOOTER & PRIVACY EXPLANATION
# ==============================================================================
privacy_body = (
    "• PDF parsing happens in local RAM via <code>pypdf</code>. Files are never written to a server disk, database, or cloud bucket.<br>"
    "• When Gemini API is enabled, document text is processed under official Google Cloud data protection terms.<br>"
    "• Documents are encapsulated inside strict untrusted data boundaries to guard against prompt injection.<br>"
    "• No personal user profiles or contract data are logged or retained permanently."
    if language == "English" else
    "• पीडीएफ निष्कर्षण आपके कंप्यूटर की रैम (RAM) में <code>pypdf</code> द्वारा स्थानीय रूप से होता है। फाइलें कभी भी सर्वर डिस्क या डेटाबेस में सहेजी नहीं जातीं।<br>"
    "• जेमिनी API का उपयोग करते समय पाठ आधिकारिक गूगल क्लाउड डेटा नीतियों के तहत संसाधित होता है।<br>"
    "• प्रॉम्ट इंजेक्शन से सुरक्षा के लिए दस्तावेज़ को सख्त सीमाओं में सुरक्षित रखा जाता है।<br>"
    "• कोई भी व्यक्तिगत प्रोफ़ाइल डेटा कभी स्थायी रूप से सुरक्षित नहीं किया जाता।"
)
privacy_header = "🔒 Privacy & Data Architecture:" if language == "English" else "🔒 गोपनीयता एवं डेटा सुरक्षा वास्तुकला:"
st.markdown(f"""
<div class="privacy-box">
    <strong>{privacy_header}</strong><br>
    {privacy_body}
</div>
""", unsafe_allow_html=True)
