"""
DocGist — Localization & Internationalization Module (translations.py)
Provides bilingual support (English and Hindi) for:
1. User interface labels, headings, buttons, and disclaimers.
2. Comprehensive Hindi translations for preset sample analyses and mock outputs.
3. Bilingual exportable markdown report generation.
"""

from typing import Any, Dict, List, Optional

UI_STRINGS = {
    "English": {
        "phase_badge": "PHASE 6 ACTIVE • BILINGUAL & UX POLISH",
        "app_title": "DocGist — Understand Before You Sign",
        "app_subtitle": "AI-assisted clause scrutiny for students & families: PG agreements, internships, and scholarships.",
        "ai_engine": "AI Engine",
        "live_cloud": "Live Cloud",
        "free_demo": "Free Demo",
        "legal_disclaimer_title": "⚠️ Important Legal Disclaimer:",
        "legal_disclaimer_body": "DocGist is an educational reading aid and decision-support tool. It **does not provide legal advice**, legal representation, or formal opinions. A green indicator reflects absence of immediate high-risk signals based on detected text—it is not a certification of legal validity or safety. Always consult a legal professional before executing binding legal documents.",
        "step1_title": "1. Provide Document Content",
        "input_method_label": "Choose how you want to provide your document:",
        "input_upload": "📄 Upload PDF Document",
        "input_paste": "✍️ Paste Text Directly",
        "input_presets": "📚 Try Sample Presets",
        "upload_caption": "Upload a PDF file. Text is extracted locally in RAM using `pypdf`.",
        "upload_label": "Upload PDF Document",
        "paste_label": "Paste document text here:",
        "paste_placeholder": "Paste the full text of your agreement, notice, or letter here...",
        "preset_label": "Select a pre-loaded sample document:",
        "char_count_label": "Content Length: **{chars}** characters | **{words}** words",
        "analyze_btn": "🔍 Analyze Document",
        "reset_btn": "🔄 Reset / Clear",
        "step2_title": "2. Document Analysis & Risk Assessment",
        "tab_summary": "📋 5-Point Summary",
        "tab_risks": "⚠️ Risk & Clause Breakdown",
        "tab_eligibility": "🎓 Profile Eligibility Check",
        "summary_heading": "Key Highlights at a Glance",
        "summary_caption": "Factual 5-point extraction powered by AI reading comprehension.",
        "risks_heading": "Clause-by-Clause Risk Evaluation (Evidence-Based)",
        "high_risk_metric": "🚨 High Risk Clauses",
        "caution_metric": "⚠️ Cautionary Terms",
        "standard_metric": "🟢 Clear / Standard Clauses",
        "risk_guardrail_caption": "🛡️ **Anti-Hallucination Guardrail:** Every risk must be backed by an exact quotation. DocGist programmatically verifies each quote against the document text. A green indicator reflects clear/standard terms—it does **not** certify that the document is legally safe. Always consult a legal professional before signing.",
        "flagged_suffix": "flagged",
        "badge_high_risk": "🚨 HIGH RISK / HARSH CLAUSE",
        "badge_caution": "⚠️ CAUTION / RESTRICTIVE",
        "badge_standard": "✅ CLEAR / STANDARD",
        "exact_quote_label": "Exact document text:",
        "eligibility_heading": "Personalized Eligibility Analysis",
        "evaluating_profile_ribbon": "Evaluating Stated Criteria Against Your Profile:",
        "sidebar_tip": "💡 Tip: You can modify any student profile value in the left sidebar to see instant eligibility recalculations.",
        "criteria_breakdown_heading": "🔍 Clause-by-Clause Criterion Breakdown",
        "criteria_caption": "Each criterion is verified directly against document evidence and matched to your profile.",
        "doc_requirement_label": "Document Requirement:",
        "user_profile_label": "Your Selected Profile:",
        "assessment_label": "Assessment:",
        "exact_clause_label": "Exact document clause:",
        "mandatory_doc_notes": "📋 Mandatory Documentation & Verification Notes:",
        "eligibility_disclaimer": "⚠️ Automated profile matching is based strictly on explicit text extracted from the document. Actual admission, appointment, or scholarship sanction remains subject to physical certificate verification by the administering authority.",
        "tenancy_not_applicable": "ℹ️ **Tenancy / General Contract:** Eligibility evaluation is designed for Scholarship Notices and Internship Offers. Rental agreements and general tenancy contracts apply equally to all tenants without academic, income, or category prerequisites.",
        "parties_label": "👥 Identified Parties:",
        "dates_label": "📅 Key Dates & Deadlines:",
        "financials_label": "💰 Financial Terms:",
        "missing_label": "⚠️ Missing or Unclear Details:",
        "facts_heading": "📌 Extracted Key Facts & Boundary Checks",
        "empty_warning": "Please provide or upload document text before analyzing.",
        "short_warning": "⚠️ The provided text is too brief ({chars} characters) to constitute a standard legal agreement. Please paste or upload the full document.",
        "download_report_btn": "📥 Download Analysis Report (Markdown)",
        "privacy_box_text": "🔒 **Privacy & Data Architecture:**\n• PDF parsing happens in local RAM via `pypdf`. Files are never written to a server disk, database, or cloud bucket.\n• When Gemini API is enabled, document text is processed under official Google Cloud data protection terms.\n• Documents are encapsulated inside strict untrusted data boundaries to guard against prompt injection.\n• No personal user profiles or contract data are logged or retained permanently."
    },
    "हिंदी (Hindi)": {
        "phase_badge": "चरण 6 सक्रिय • द्विभाषी (हिंदी/अंग्रेजी) एवं उन्नत अनुभव",
        "app_title": "DocGist (डॉकगिस्ट) — हस्ताक्षर करने से पहले समझें",
        "app_subtitle": "छात्रों और परिवारों के लिए AI-सक्षम दस्तावेज़ विश्लेषण: पीजी/किराया अनुबंध, इंटर्नशिप और छात्रवृत्ति।",
        "ai_engine": "AI इंजन",
        "live_cloud": "लाइव जेमिनी",
        "free_demo": "मुफ़्त डेमो",
        "legal_disclaimer_title": "⚠️ महत्वपूर्ण कानूनी अस्वीकरण (Disclaimer):",
        "legal_disclaimer_body": "DocGist एक शैक्षणिक अध्ययन सहायता और निर्णय-समर्थन उपकरण है। यह **कोई कानूनी सलाह**, कानूनी प्रतिनिधित्व या औपचारिक राय प्रदान नहीं करता है। हरा (Green) संकेत केवल यह दर्शाता है कि प्रस्तुत पाठ में कोई कठोर शर्त नहीं मिली—यह दस्तावेज़ की कानूनी वैधता या सुरक्षा का प्रमाण पत्र नहीं है। किसी भी कानूनी दस्तावेज़ पर हस्ताक्षर करने से पहले हमेशा कानूनी विशेषज्ञ से परामर्श लें।",
        "step1_title": "1. दस्तावेज़ सामग्री प्रदान करें",
        "input_method_label": "दस्तावेज़ प्रदान करने का तरीका चुनें:",
        "input_upload": "📄 पीडीएफ दस्तावेज़ अपलोड करें",
        "input_paste": "✍️ दस्तावेज़ का पाठ यहाँ पेस्ट करें",
        "input_presets": "📚 नमूना दस्तावेज़ आज़माएँ",
        "upload_caption": "पीडीएफ फाइल अपलोड करें। टेक्स्ट स्थानीय रूप से `pypdf` द्वारा रैम (RAM) में निकाला जाता है।",
        "upload_label": "पीडीएफ दस्तावेज़ अपलोड करें",
        "paste_label": "दस्तावेज़ का पाठ यहाँ पेस्ट करें:",
        "paste_placeholder": "अपने अनुबंध, नोटिस या प्रस्ताव पत्र का पूरा पाठ यहाँ पेस्ट करें...",
        "preset_label": "पहले से लोड किया गया नमूना दस्तावेज़ चुनें:",
        "char_count_label": "सामग्री की लंबाई: **{chars}** अक्षर | **{words}** शब्द",
        "analyze_btn": "🔍 दस्तावेज़ का विश्लेषण करें",
        "reset_btn": "🔄 रीसेट करें / नया दस्तावेज़",
        "step2_title": "2. दस्तावेज़ विश्लेषण एवं जोखिम मूल्यांकन",
        "tab_summary": "📋 5-पॉइंट सारांश",
        "tab_risks": "⚠️ जोखिम एवं खंड विश्लेषण",
        "tab_eligibility": "🎓 प्रोफ़ाइल पात्रता जाँच",
        "summary_heading": "एक नज़र में मुख्य बिंदु",
        "summary_caption": "AI पठन समझ द्वारा संचालित तथ्यात्मक 5-बिंदु विश्लेषण।",
        "risks_heading": "खंड-दर-खंड साक्ष्य-आधारित जोखिम मूल्यांकन",
        "high_risk_metric": "🚨 उच्च जोखिम वाले खंड",
        "caution_metric": "⚠️ सावधानी योग्य शर्तें",
        "standard_metric": "🟢 स्पष्ट एवं सामान्य शर्तें",
        "risk_guardrail_caption": "🛡️ **एंटी-हैलुसिनेशन सुरक्षा:** प्रत्येक जोखिम के समर्थन में दस्तावेज़ से लिया गया सटीक उद्धरण (कोटेशन) होना अनिवार्य है। DocGist प्रत्येक कोटेशन को मूल दस्तावेज़ पाठ से सत्यापित करता है। हरा संकेत दस्तावेज़ के कानूनी रूप से सुरक्षित होने की पुष्टि नहीं करता। हस्ताक्षर करने से पहले हमेशा कानूनी विशेषज्ञ से सलाह लें।",
        "flagged_suffix": "चिह्नित",
        "badge_high_risk": "🚨 उच्च जोखिम / कठोर खंड",
        "badge_caution": "⚠️ सावधानी / प्रतिबंधात्मक शर्त",
        "badge_standard": "✅ स्पष्ट एवं मानक शर्त",
        "exact_quote_label": "दस्तावेज़ से सटीक उद्धरण (Exact Quote):",
        "eligibility_heading": "व्यक्तिगत प्रोफ़ाइल पात्रता मूल्यांकन",
        "evaluating_profile_ribbon": "आपकी सक्रिय प्रोफ़ाइल के विरुद्ध दस्तावेज़ शर्तों की जाँच:",
        "sidebar_tip": "💡 सुझाव: बाईं ओर साइडबार में अपनी प्रोफ़ाइल बदलकर आप तुरंत वास्तविक समय में परिणाम देख सकते हैं।",
        "criteria_breakdown_heading": "🔍 शर्त-दर-शर्त पात्रता मिलान",
        "criteria_caption": "प्रत्येक मानदंड को दस्तावेज़ के साक्ष्य से जाँचा गया है और आपकी प्रोफ़ाइल से मिलाया गया है।",
        "doc_requirement_label": "दस्तावेज़ की अनिवार्यता:",
        "user_profile_label": "आपकी चुनी हुई प्रोफ़ाइल:",
        "assessment_label": "मूल्यांकन एवं कारण:",
        "exact_clause_label": "दस्तावेज़ का मूल खंड:",
        "mandatory_doc_notes": "📋 आवश्यक दस्तावेज़ एवं सत्यापन टिप्पणियाँ:",
        "eligibility_disclaimer": "⚠️ स्वचालित प्रोफ़ाइल मिलान पूरी तरह दस्तावेज़ में लिखे पाठ पर आधारित है। छात्रवृत्ति या नौकरी की अंतिम स्वीकृति मूल प्रमाणपत्रों के भौतिक सत्यापन के बाद ही संबंधित प्राधिकरण द्वारा दी जाती है।",
        "tenancy_not_applicable": "ℹ️ **किराया / सामान्य अनुबंध:** पात्रता जाँच केवल छात्रवृत्ति और इंटर्नशिप के लिए है। किराया अनुबंध सभी हस्ताक्षरकर्ताओं पर समान रूप से लागू होता है और इसमें जाति, आय या शैक्षणिक वर्ष की कोई पाबंदी नहीं होती।",
        "parties_label": "👥 पहचाने गए पक्ष (Parties):",
        "dates_label": "📅 मुख्य तिथियाँ एवं समय सीमा:",
        "financials_label": "💰 वित्तीय शर्तें (किराया/वेतन/जुर्माना):",
        "missing_label": "⚠️ गायब या अस्पष्ट विवरण:",
        "facts_heading": "📌 निकाले गए मुख्य तथ्य एवं सीमा जाँच",
        "empty_warning": "कृपया विश्लेषण करने से पहले दस्तावेज़ प्रदान करें या अपलोड करें।",
        "short_warning": "⚠️ प्रदान किया गया पाठ कानूनी अनुबंध के विश्लेषण के लिए बहुत छोटा है ({chars} अक्षर)। कृपया पूरा दस्तावेज़ प्रदान करें।",
        "download_report_btn": "📥 विश्लेषण रिपोर्ट डाउनलोड करें (Markdown)",
        "privacy_box_text": "🔒 **गोपनीयता एवं डेटा सुरक्षा वास्तुकला:**\n• पीडीएफ निष्कर्षण आपके कंप्यूटर की रैम (RAM) में `pypdf` द्वारा स्थानीय रूप से होता है। फाइलें कभी भी सर्वर डिस्क या डेटाबेस में सहेजी नहीं जातीं।\n• जेमिनी API का उपयोग करते समय पाठ आधिकारिक गूगल क्लाउड डेटा नीतियों के तहत संसाधित होता है।\n• प्रॉम्ट इंजेक्शन से सुरक्षा के लिए दस्तावेज़ को सख्त सीमाओं में सुरक्षित रखा जाता है।\n• कोई भी व्यक्तिगत प्रोफ़ाइल डेटा कभी स्थायी रूप से सुरक्षित नहीं किया जाता।"
    }
}


# ==============================================================================
# HINDI SAMPLE ANALYSES (High-Quality Localized Mock Data)
# Note: exact_quote remains verbatim in the original document language
# so that programmatic quotation verification continues to pass 100%!
# ==============================================================================
HINDI_SAMPLE_ANALYSES = {
    "PG / Rental Agreement (Sample)": {
        "document_type": "पीजी / किराया अनुबंध (PG / Rental Agreement)",
        "document_type_confidence": "उच्च (नियम आधारित)",
        "five_point_summary": [
            "मासिक किराया ₹12,000 है जो प्रत्येक महीने की 1 तारीख तक देय है; विलंब पर ₹200 प्रतिदिन का जुर्माना लगेगा।",
            "वापसी योग्य सुरक्षा जमा ₹36,000 (3 महीने के किराए के बराबर) निर्धारित की गई है।",
            "मकान खाली करते समय कमरे की स्थिति पर विचार किए बिना जमा राशि से 20% की अनिवार्य पेंटिंग व सफाई कटौती होगी।",
            "6 महीने की सख्त लॉक-इन अवधि लागू है; समय से पहले खाली करने पर पूरी ₹36,000 की सुरक्षा जमा राशि जब्त कर ली जाएगी।",
            "मकान मालिक बिना कोई कारण बताए केवल 24 घंटे की मौखिक सूचना पर किराएदार को निकालने का एकतरफा अधिकार रखता है।"
        ],
        "identified_parties": "श्री राजेश शर्मा (मकान मालिक) एवं रोहन वर्मा (किराएदार)",
        "key_dates_or_deadlines": "प्रारंभ 1 अगस्त 2026; 6 माह की लॉक-इन अवधि; प्रत्येक माह की 1 तारीख देय तिथि",
        "financial_terms": "किराया: ₹12,000/माह; सुरक्षा जमा: ₹36,000; विलंब शुल्क: ₹200/दिन; अनिवार्य सफाई कटौती: 20%",
        "missing_critical_details": "रखरखाव रसीद जारी करने की समय सीमा और बिजली/पानी मीटर की अलग रीडिंग के नियम स्पष्ट रूप से दर्ज नहीं हैं।",
        "risks": [
            {
                "level": "red",
                "title": "24 घंटे की एकतरफा बेदखली नोटिस (Unilateral Eviction)",
                "explanation": "मानक किराया समझौतों में कम से कम 30 दिनों का लिखित नोटिस देना अनिवार्य होता है। 24 घंटे का मौखिक नोटिस किराएदार को अचानक बेघर होने के गंभीर जोखिम में डालता है।",
                "exact_quote": "The Landlord reserves the absolute right to terminate this tenancy with 24 hours verbal notice without assigning any reason. The Tenant must vacate immediately."
            },
            {
                "level": "red",
                "title": "समय से पूर्व निकलने पर संपूर्ण सुरक्षा जमा की जब्ती",
                "explanation": "6 महीने के लॉक-इन पीरियड को तोड़ने पर पूरे 3 महीने की जमा राशि (₹36,000) जब्त करना अत्यधिक दंडात्मक और अनुचित है।",
                "exact_quote": "The Tenant is subject to a strict 6-month lock-in period. If the Tenant vacates before 6 months, the entire security deposit of INR 36,000 shall stand forfeited with no dispute allowed."
            },
            {
                "level": "yellow",
                "title": "अनिवार्य 20% सफाई एवं पेंटिंग कटौती",
                "explanation": "कमरे की वास्तविक स्थिति को देखे बिना स्वचालित कटौती किराएदार की सुरक्षा जमा राशि से ₹7,200 का सीधा नुकसान करती है।",
                "exact_quote": "A mandatory 20% painting and deep cleaning fee shall be deducted from the security deposit regardless of premises condition upon vacating."
            },
            {
                "level": "yellow",
                "title": "संरचनात्मक सीपेज और बड़ी मरम्मत का खर्च किराएदार पर",
                "explanation": "आवासीय पट्टे के कानूनी नियमों के अनुसार संरचनात्मक सीलन और बड़ी मरम्मत की जिम्मेदारी मकान मालिक की होती है।",
                "exact_quote": "All major and minor repairs, including plumbing, electrical fixtures, and structural seepage, shall be borne exclusively by the Tenant."
            },
            {
                "level": "green",
                "title": "मासिक किराया और विलंब शुल्क का स्पष्ट उल्लेख",
                "explanation": "मूल किराया और विलंब शुल्क की गणना स्पष्ट रूप से निर्धारित की गई है, जिससे बाद में कोई अस्पष्ट या मनमाना बिलिंग विवाद नहीं होगा।",
                "exact_quote": "Monthly rent shall be INR 12,000 payable in advance on or before the 1st of every calendar month. Delay will attract a penalty of INR 200 per day."
            }
        ],
        "eligibility": {
            "applicable": False,
            "overall_summary": "किराया अनुबंध सभी हस्ताक्षरकर्ता किराएदारों पर समान रूप से लागू होता है।",
            "criteria_list": [],
            "notes_or_caveats": "किराया समझौतों पर कोई छात्र प्रोफ़ाइल प्रतिबंध लागू नहीं होते हैं।"
        }
    },

    "Internship Offer Letter (Sample)": {
        "document_type": "इंटर्नशिप प्रस्ताव पत्र (Internship Offer Letter)",
        "document_type_confidence": "उच्च (नियम आधारित)",
        "five_point_summary": [
            "सॉफ्टवेयर इंजीनियरिंग इंटर्न का पद 1 अगस्त 2026 से 3 महीने की निश्चित अवधि के लिए दिया गया है।",
            "प्रत्येक माह के प्रोजेक्ट कार्य पूर्ण होने पर ₹15,000 प्रति माह का निश्चित वजीफा (Stipend) दिया जाएगा।",
            "24 महीने का व्यापक वैश्विक गैर-प्रतिस्पर्धा (Non-Compete) खंड इंटर्न को किसी भी सॉफ्टवेयर या AI कंपनी में काम करने से रोकता है।",
            "3 महीने पूरे होने से पहले इंटर्नशिप छोड़ने पर प्रशिक्षण लागत के नाम पर ₹50,000 का भारी जुर्माना लगाया जाएगा।",
            "अवधि के दौरान बनाए गए सभी कोड, बौद्धिक संपदा और प्रोजेक्ट विचार कंपनी की अनन्य संपत्ति रहेंगे।"
        ],
        "identified_parties": "एपेक्स टेक इनोवेशंस प्राइवेट लिमिटेड एवं अनन्या पटेल (उम्मीदवार)",
        "key_dates_or_deadlines": "आरंभ तिथि 1 अगस्त 2026; कुल अवधि 3 महीने",
        "financial_terms": "मासिक वजीफा: ₹15,000; समय से पूर्व छोड़ने पर जुर्माना: ₹50,000",
        "missing_critical_details": "छुट्टी की नीति, कार्य के घंटे और व्यक्तिगत निजी प्रोजेक्ट्स के स्वामित्व के नियम स्पष्ट रूप से परिभाषित नहीं हैं।",
        "risks": [
            {
                "level": "red",
                "title": "अत्यधिक कठोर 2 वर्ष का वैश्विक गैर-प्रतिस्पर्धा खंड",
                "explanation": "इंटर्नशिप समाप्त होने के 24 महीने बाद तक दुनिया भर में सॉफ्टवेयर या AI क्षेत्र में काम करने पर रोक लगाना बेहद कठोर है और भारतीय अनुबंध अधिनियम (धारा 27) के तहत आमतौर पर गैर-कानूनी माना जाता है।",
                "exact_quote": "For a period of 24 months after the end of this internship, the intern shall not seek employment, freelance, or consult for any company worldwide operating in the software or artificial intelligence sector."
            },
            {
                "level": "red",
                "title": "समय से पूर्व छोड़ने पर ₹50,000 का भारी जुर्माना बॉन्ड",
                "explanation": "समय से पहले छोड़ने पर ₹50,000 (3 महीने के कुल वजीफे से भी अधिक!) की मांग करना एक छात्र के लिए बंधुआ स्थिति पैदा करता है।",
                "exact_quote": "If the intern leaves or terminates the internship prior to the completion of the 3-month tenure, the intern shall pay a liquidated penalty of INR 50,000 for training costs."
            },
            {
                "level": "yellow",
                "title": "वजीफे का भुगतान 'कार्य पूरा होने' की शर्त पर निर्भर",
                "explanation": "काम किए गए घंटों के बजाय 'काम पूरा होने पर' भुगतान की शर्त कंपनी को मनमाने ढंग से वजीफा रोकने की गुंजाइश देती है।",
                "exact_quote": "You will receive a fixed stipend of INR 15,000 per month upon completion of each month's deliverables."
            },
            {
                "level": "green",
                "title": "3 महीने का स्पष्ट कार्यकाल निर्धारित",
                "explanation": "इंटर्नशिप की अवधि और आरंभ तिथि बिना किसी अनिश्चितकालीन विस्तार के स्पष्ट रूप से परिभाषित की गई है।",
                "exact_quote": "The internship duration is 3 months. You will receive a fixed stipend of INR 15,000 per month upon completion of each month's deliverables."
            }
        ],
        "eligibility": {
            "applicable": True,
            "overall_summary": "सॉफ्टवेयर इंजीनियरिंग इंटर्नशिप, 3 महीने की अवधि, 1 अगस्त 2026 से आरंभ।",
            "criteria_list": [
                {
                    "criterion": "पद एवं तकनीकी क्षेत्र (Target Role & Field)",
                    "document_requirement": "कंप्यूटर विज्ञान और तकनीकी पृष्ठभूमि के छात्रों के लिए उपयुक्त सॉफ्टवेयर इंजीनियरिंग इंटर्न पद",
                    "exact_quote": "We are pleased to offer you the position of Software Engineering Intern starting August 1, 2026."
                },
                {
                    "criterion": "कार्यकाल एवं उपलब्धता (Duration & Availability)",
                    "document_requirement": "3 महीने की पूर्णकालिक अवधि और नियत प्रोजेक्ट कार्य",
                    "exact_quote": "The internship duration is 3 months. You will receive a fixed stipend of INR 15,000 per month upon completion of each month's deliverables."
                }
            ],
            "notes_or_caveats": "सुनिश्चित करें कि आपका विश्वविद्यालय/कॉलेज शैक्षणिक सत्र के दौरान 3 महीने की पूर्णकालिक इंटर्नशिप उपस्थिति की अनुमति देता है।"
        }
    },

    "Scholarship Notice (Sample)": {
        "document_type": "छात्रवृत्ति अधिसूचना (Scholarship Notice)",
        "document_type_confidence": "उच्च (नियम आधारित)",
        "five_point_summary": [
            "शैक्षणिक सत्र 2026-27 के लिए आधिकारिक राज्य मेरिट-कम-मीन्स उच्च शिक्षा छात्रवृत्ति अधिसूचना।",
            "केवल मान्यता प्राप्त संस्थान से 2nd या 3rd वर्ष के पूर्णकालिक B.Tech / B.E. / तकनीकी छात्रों के लिए उपलब्ध।",
            "उम्मीदवार का वैध अधिवास प्रमाण पत्र (Domicile) के साथ महाराष्ट्र का स्थायी निवासी होना अनिवार्य है।",
            "सत्यापित जाति प्रमाण पत्र धारक SC, ST और OBC श्रेणी के उम्मीदवारों के लिए आरक्षित।",
            "परिवार की कुल वार्षिक सकल आय ₹2,50,000 से कम होनी चाहिए तथा तहसीलदार द्वारा प्रमाणित होना अनिवार्य है।"
        ],
        "identified_parties": "उच्च शिक्षा विभाग (प्राधिकरण) एवं पात्र छात्र आवेदक",
        "key_dates_or_deadlines": "शैक्षणिक सत्र 2026-27; आवेदन जमा करने की नियत तिथि",
        "financial_terms": "80% ट्यूशन फीस में छूट तथा ₹20,000 वार्षिक निर्वाह भत्ता",
        "missing_critical_details": "छात्रवृत्ति नवीनीकरण मानदंड (आगामी वर्षों में आवश्यक न्यूनतम CGPA या उपस्थिति प्रतिशत) का उल्लेख नहीं है।",
        "risks": [
            {
                "level": "yellow",
                "title": "सख्त दस्तावेज़ अनिवार्यता (तहसीलदार द्वारा जारी आय प्रमाण पत्र)",
                "explanation": "गैर-अधिकृत स्थानीय निकायों द्वारा जारी आय प्रमाण पत्र आवेदन को बिना किसी सुधार अवसर के तुरंत खारिज कर देंगे।",
                "exact_quote": "Total annual household gross income from all sources must not exceed INR 2,50,000 per annum. Income certificate issued by Tahsildar is mandatory."
            },
            {
                "level": "yellow",
                "title": "महाराष्ट्र का स्थायी अधिवास (Domicile) अनिवार्य",
                "explanation": "अन्य राज्यों के छात्र जो महाराष्ट्र में पढ़ाई कर रहे हैं, वे इस योजना के लिए पूरी तरह अपात्र हैं।",
                "exact_quote": "The candidate must be a permanent resident of Maharashtra holding a valid state domicile certificate."
            },
            {
                "level": "green",
                "title": "छात्रवृत्ति लाभों का स्पष्ट विवरण",
                "explanation": "सूचना में बिना किसी छिपे शुल्क के 80% ट्यूशन फीस माफी और ₹20,000 वार्षिक भत्ते की स्पष्ट गारंटी दी गई है।",
                "exact_quote": "Approved scholars will receive 80% tuition waiver plus INR 20,000 annual maintenance allowance."
            }
        ],
        "eligibility": {
            "applicable": True,
            "overall_summary": "महाराष्ट्र के 2nd/3rd वर्ष के इंजीनियरिंग छात्रों (SC/ST/OBC) के लिए छात्रवृत्ति जिनकी वार्षिक पारिवारिक आय ₹2.5 लाख से कम है।",
            "criteria_list": [
                {
                    "criterion": "पाठ्यक्रम एवं शैक्षणिक वर्ष (Course & Year)",
                    "document_requirement": "मान्यता प्राप्त संस्थान से 2nd या 3rd वर्ष में पूर्णकालिक B.Tech / B.E. / व्यावसायिक डिग्री",
                    "exact_quote": "Candidate must be enrolled full-time in B.Tech / B.E. / Professional Degree in their 2nd or 3rd year of study at an accredited university."
                },
                {
                    "criterion": "राज्य अधिवास (Domicile State)",
                    "document_requirement": "वैध राज्य अधिवास प्रमाण पत्र धारक महाराष्ट्र का स्थायी निवासी",
                    "exact_quote": "The candidate must be a permanent resident of Maharashtra holding a valid state domicile certificate."
                },
                {
                    "criterion": "सामाजिक श्रेणी (Social Category)",
                    "document_requirement": "सत्यापित जाति प्रमाण पत्र धारक SC, ST एवं OBC वर्ग के उम्मीदवार",
                    "exact_quote": "Open to candidates from SC, ST, and OBC categories with verified caste certificates."
                },
                {
                    "criterion": "वार्षिक पारिवारिक आय सीमा (Annual Income Cap)",
                    "document_requirement": "तहसीलदार द्वारा प्रमाणित पारिवारिक वार्षिक सकल आय ₹2,50,000 से अधिक नहीं होनी चाहिए",
                    "exact_quote": "Total annual household gross income from all sources must not exceed INR 2,50,000 per annum. Income certificate issued by Tahsildar is mandatory."
                }
            ],
            "notes_or_caveats": "तहसीलदार द्वारा प्रमाणित आय प्रमाण पत्र और महाराष्ट्र अधिवास (Domicile) प्रमाण पत्र अनिवार्य रूप से आवश्यक हैं।"
        }
    }
}


# ==============================================================================
# LOCALIZATION HELPERS
# ==============================================================================
def get_text(key: str, lang: str = "English") -> str:
    """Safely retrieves a localized string by key and language."""
    catalog = UI_STRINGS.get(lang, UI_STRINGS["English"])
    return catalog.get(key, UI_STRINGS["English"].get(key, key))


def get_localized_analysis(analysis_dict: Dict[str, Any], sample_key: Optional[str], lang: str) -> Dict[str, Any]:
    """
    Returns an analysis dictionary adapted for the selected language.
    If Hindi is selected and a matching high-quality preset exists, uses the localized content.
    Always maintains verbatim exact_quote fields so programmatic verification passes.
    """
    if lang != "हिंदी (Hindi)":
        return analysis_dict

    if sample_key and sample_key in HINDI_SAMPLE_ANALYSES:
        return HINDI_SAMPLE_ANALYSES[sample_key]

    return analysis_dict


def generate_downloadable_report(
    analysis_data: Dict[str, Any],
    doc_type: str,
    user_profile: Dict[str, str],
    risks_list: List[Dict[str, Any]],
    eligibility_result: Dict[str, Any],
    lang: str = "English"
) -> str:
    """
    Generates a comprehensive, clean Markdown summary report that users can
    download and take with them or share with parents/mentors.
    """
    is_hindi = (lang == "हिंदी (Hindi)")
    sep = "=" * 60

    if is_hindi:
        lines = [
            f"# DocGist (डॉकगिस्ट) — दस्तावेज़ विश्लेषण रिपोर्ट",
            f"**दस्तावेज़ प्रकार:** {doc_type}",
            f"**विश्लेषण तिथि:** तत्काल सत्र",
            f"\n{sep}\n",
            "## 📌 कानूनी अस्वीकरण (Disclaimer)",
            "DocGist एक अध्ययन एवं निर्णय-समर्थन उपकरण है। यह कोई औपचारिक कानूनी सलाह नहीं है। किसी भी अनुबंध पर हस्ताक्षर करने से पहले कानूनी विशेषज्ञ से अवश्य परामर्श लें।\n",
            f"\n{sep}\n",
            "## 📋 5-पॉइंट मुख्य सारांश",
        ]
        for i, pt in enumerate(analysis_data.get("five_point_summary", []), 1):
            lines.append(f"{i}. {pt}")

        lines.append(f"\n{sep}\n## ⚠️ जोखिम एवं खंड मूल्यांकन")
        for r in risks_list:
            lvl = str(r.get("level", "")).upper()
            title = r.get("title", "")
            exp = r.get("explanation", "")
            quote = r.get("exact_quote", "")
            lines.append(f"\n### [{lvl}] {title}")
            lines.append(f"- **व्याख्या:** {exp}")
            lines.append(f"- **मूल उद्धरण:** \"{quote}\"")

        if eligibility_result.get("applicable", False):
            lines.append(f"\n{sep}\n## 🎓 प्रोफ़ाइल पात्रता जाँच")
            lines.append(f"**समग्र स्थिति:** {eligibility_result.get('overall_status', '')}")
            lines.append(f"**छात्र प्रोफ़ाइल:** {user_profile.get('course')} | {user_profile.get('year')} | {user_profile.get('state')} | {user_profile.get('category')} | {user_profile.get('income')}\n")
            for crit in eligibility_result.get("criteria_breakdown", []):
                lines.append(f"- **{crit.get('criterion')}:** {crit.get('verdict')} ({crit.get('reason')})")

        lines.append(f"\n{sep}\n*DocGist द्वारा जनरेटेड — शून्य-डेटा-संग्रहण गारंटी के साथ।*\n")

    else:
        lines = [
            f"# DocGist — Document Analysis Report",
            f"**Document Type:** {doc_type}",
            f"**Generated:** Active Session",
            f"\n{sep}\n",
            "## 📌 Important Legal Disclaimer",
            "DocGist is an educational reading aid and decision-support tool. It does NOT provide legal advice. Always consult a qualified legal professional before signing binding documents.\n",
            f"\n{sep}\n",
            "## 📋 5-Point Executive Summary",
        ]
        for i, pt in enumerate(analysis_data.get("five_point_summary", []), 1):
            lines.append(f"{i}. {pt}")

        lines.append(f"\n{sep}\n## ⚠️ Evidence-Based Risk Evaluation")
        for r in risks_list:
            lvl = str(r.get("level", "")).upper()
            title = r.get("title", "")
            exp = r.get("explanation", "")
            quote = r.get("exact_quote", "")
            lines.append(f"\n### [{lvl}] {title}")
            lines.append(f"- **Explanation:** {exp}")
            lines.append(f"- **Exact Quote:** \"{quote}\"")

        if eligibility_result.get("applicable", False):
            lines.append(f"\n{sep}\n## 🎓 Profile Eligibility Evaluation")
            lines.append(f"**Overall Status:** {eligibility_result.get('overall_status', '')}")
            lines.append(f"**Candidate Profile:** {user_profile.get('course')} | {user_profile.get('year')} | {user_profile.get('state')} | {user_profile.get('category')} | {user_profile.get('income')}\n")
            for crit in eligibility_result.get("criteria_breakdown", []):
                lines.append(f"- **{crit.get('criterion')}:** {crit.get('verdict')} ({crit.get('reason')})")

        lines.append(f"\n{sep}\n*Generated by DocGist — Zero-Permanent-Storage Architecture.*\n")

    return "\n".join(lines)
