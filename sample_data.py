"""
Sample data for DocGist Phase 1.
Provides realistic sample documents and structured mock analyses for:
1. PG / Rental Agreement
2. Internship Offer
3. Scholarship Notice
"""

SAMPLE_DOCUMENTS = {
    "PG / Rental Agreement (Sample)": """HOUSE / PG RENTAL AGREEMENT

This Agreement is made on this 1st day of August, 2026, between Mr. Rajesh Sharma (Landlord) and Rohan Verma (Tenant).

1. PREMISES & RENT:
The Landlord agrees to let out Room 204 at Green View Residency. Monthly rent shall be INR 12,000 payable in advance on or before the 1st of every calendar month. Delay will attract a penalty of INR 200 per day.

2. SECURITY DEPOSIT & FORFEITURE:
The Tenant deposits a sum of INR 36,000 (3 months rent) as refundable security deposit.
Clause 2(b): "A mandatory 20% painting and deep cleaning fee shall be deducted from the security deposit regardless of premises condition upon vacating."

3. LOCK-IN PERIOD:
Clause 3(a): "The Tenant is subject to a strict 6-month lock-in period. If the Tenant vacates before 6 months, the entire security deposit of INR 36,000 shall stand forfeited with no dispute allowed."

4. TERMINATION & IMMEDIATE VACATION:
Clause 4(c): "The Landlord reserves the absolute right to terminate this tenancy with 24 hours verbal notice without assigning any reason. The Tenant must vacate immediately."

5. MAINTENANCE & REPAIRS:
Clause 5: "All major and minor repairs, including plumbing, electrical fixtures, and structural seepage, shall be borne exclusively by the Tenant."
""",

    "Internship Offer Letter (Sample)": """APEX TECH INNOVATIONS PVT LTD
Offer of Internship

Date: July 15, 2026
Candidate: Ananya Patel

Dear Ananya,
We are pleased to offer you the position of Software Engineering Intern starting August 1, 2026.

1. DURATION & STIPEND:
The internship duration is 3 months. You will receive a fixed stipend of INR 15,000 per month upon completion of each month's deliverables.

2. NON-COMPETE RESTRICTION:
Clause 5: "For a period of 24 months after the end of this internship, the intern shall not seek employment, freelance, or consult for any company worldwide operating in the software or artificial intelligence sector."

3. RESIGNATION & PENALTY BOND:
Clause 7: "If the intern leaves or terminates the internship prior to the completion of the 3-month tenure, the intern shall pay a liquidated penalty of INR 50,000 for training costs."

4. INTELLECTUAL PROPERTY:
All inventions, source code, and project ideas conceived by the intern during this term remain the exclusive property of the Company.
""",

    "Scholarship Notice (Sample)": """STATE MERIT-CUM-MEANS HIGHER EDUCATION SCHOLARSHIP 2026-27
Department of Higher Education

ELIGIBILITY NOTIFICATION:
Applications are invited from deserving students pursuing technical degrees.

1. ELIGIBLE COURSES & YEAR:
Clause 1: "Candidate must be enrolled full-time in B.Tech / B.E. / Professional Degree in their 2nd or 3rd year of study at an accredited university."

2. DOMICILE REQUIREMENT:
Clause 2: "The candidate must be a permanent resident of Maharashtra holding a valid state domicile certificate."

3. CATEGORY & RESERVATION:
Clause 3: "Open to candidates from SC, ST, and OBC categories with verified caste certificates."

4. ANNUAL FAMILY INCOME CAP:
Clause 4: "Total annual household gross income from all sources must not exceed INR 2,50,000 per annum. Income certificate issued by Tahsildar is mandatory."

5. SCHOLARSHIP BENEFIT:
Approved scholars will receive 80% tuition waiver plus INR 20,000 annual maintenance allowance.
"""
}

SAMPLE_ANALYSES = {
    "PG / Rental Agreement (Sample)": {
        "document_type": "PG / Rental Agreement",
        "document_type_badge": "Rental Agreement",
        "five_point_summary": [
            "Monthly rent is INR 12,000 payable by the 1st of each month with a late fee of INR 200/day.",
            "Refundable security deposit is INR 36,000 (equivalent to 3 months of rent).",
            "A mandatory 20% cleaning deduction is taken from the deposit upon vacating regardless of wear or cleanliness.",
            "A strict 6-month lock-in period applies; early departure forfeits the entire INR 36,000 deposit.",
            "Landlord claims unilateral authority to evict with 24 hours verbal notice without stating a reason."
        ],
        "risks": [
            {
                "level": "red",
                "title": "Unilateral 24-Hour Eviction Notice",
                "explanation": "Standard rental agreements require at least 30 days written notice. A 24-hour verbal notice leaves the tenant vulnerable to abrupt homelessness.",
                "exact_quote": "The Landlord reserves the absolute right to terminate this tenancy with 24 hours verbal notice without assigning any reason. The Tenant must vacate immediately."
            },
            {
                "level": "red",
                "title": "Total Security Deposit Forfeiture on Early Exit",
                "explanation": "Forfeiting the entire 3 months deposit (INR 36,000) for breaking a lock-in period is unusually punitive.",
                "exact_quote": "The Tenant is subject to a strict 6-month lock-in period. If the Tenant vacates before 6 months, the entire security deposit of INR 36,000 shall stand forfeited with no dispute allowed."
            },
            {
                "level": "yellow",
                "title": "Mandatory 20% Deposit Deduction",
                "explanation": "Automatic deduction regardless of actual condition eliminates incentive for careful tenancy and reduces returned deposit by INR 7,200.",
                "exact_quote": "A mandatory 20% painting and deep cleaning fee shall be deducted from the security deposit regardless of premises condition upon vacating."
            },
            {
                "level": "yellow",
                "title": "Tenant Liable for Structural Seepage & Major Repairs",
                "explanation": "Structural seepage and major repairs are legally the landlord's responsibility in customary residential leasing.",
                "exact_quote": "All major and minor repairs, including plumbing, electrical fixtures, and structural seepage, shall be borne exclusively by the Tenant."
            },
            {
                "level": "green",
                "title": "Explicit Monthly Rent & Late Fee Amount",
                "explanation": "The basic rent and late fee calculation are explicitly quantified, avoiding vague variable billing.",
                "exact_quote": "Monthly rent shall be INR 12,000 payable in advance on or before the 1st of every calendar month. Delay will attract a penalty of INR 200 per day."
            }
        ],
        "identified_parties": "Mr. Rajesh Sharma (Landlord) and Rohan Verma (Tenant)",
        "key_dates_or_deadlines": "Commencing August 1, 2026; 6-month lock-in period; Rent due on 1st of month",
        "financial_terms": "Rent: INR 12,000/month; Deposit: INR 36,000; Late fee: INR 200/day; Mandatory cleaning deduction: 20%",
        "missing_critical_details": "Receipt timeline for maintenance and separate sub-meter electricity billing rules are not explicitly recorded.",
        "eligibility": {
            "applicable": False,
            "message": "Eligibility checks are specific to Scholarship Notices and Internship Offers."
        }
    },

    "Internship Offer Letter (Sample)": {
        "document_type": "Internship Offer Letter",
        "document_type_badge": "Internship Offer",
        "five_point_summary": [
            "Position offered: Software Engineering Intern starting August 1, 2026 for a 3-month duration.",
            "Monthly stipend is fixed at INR 15,000 per month payable upon deliverable completion.",
            "Broad 24-month global non-compete clause restricts working in software or AI anywhere in the world.",
            "Heavy financial penalty bond of INR 50,000 imposed if the intern leaves before completing 3 months.",
            "All intellectual property and code conceived during the term belong entirely to the company."
        ],
        "risks": [
            {
                "level": "red",
                "title": "Overly Restrictive 2-Year Global Non-Compete",
                "explanation": "Restricting an intern from working anywhere in software or AI for 24 months post-internship is extremely aggressive and generally unenforceable under Indian contract law (Section 27 of ICA).",
                "exact_quote": "For a period of 24 months after the end of this internship, the intern shall not seek employment, freelance, or consult for any company worldwide operating in the software or artificial intelligence sector."
            },
            {
                "level": "red",
                "title": "INR 50,000 Early Exit Penalty Bond",
                "explanation": "Demanding a penalty of INR 50,000 (more than 3 months of stipend!) if you leave early creates unfair entrapment for a student.",
                "exact_quote": "If the intern leaves or terminates the internship prior to the completion of the 3-month tenure, the intern shall pay a liquidated penalty of INR 50,000 for training costs."
            },
            {
                "level": "yellow",
                "title": "Stipend Conditional on 'Deliverables Completion'",
                "explanation": "Phrasing payment as 'upon completion of deliverables' rather than monthly hours worked allows subjective withholding of stipend.",
                "exact_quote": "You will receive a fixed stipend of INR 15,000 per month upon completion of each month's deliverables."
            },
            {
                "level": "green",
                "title": "Clear 3-Month Fixed Tenure Defined",
                "explanation": "The internship duration and start date are clearly specified without indefinite probationary extensions.",
                "exact_quote": "The internship duration is 3 months. You will receive a fixed stipend of INR 15,000 per month upon completion of each month's deliverables."
            }
        ],
        "identified_parties": "Apex Tech Innovations Pvt Ltd and Ananya Patel (Candidate)",
        "key_dates_or_deadlines": "Starting August 1, 2026; 3-month duration",
        "financial_terms": "Stipend: INR 15,000/month; Early departure penalty bond: INR 50,000",
        "missing_critical_details": "Leave policy, working hours, and IP ownership of personal/hobby side projects are not defined.",
        "eligibility": {
            "applicable": True,
            "overall_summary": "Software Engineering Internship starting August 1, 2026 for 3 months duration.",
            "criteria_list": [
                {
                    "criterion": "Target Role & Field",
                    "document_requirement": "Software Engineering Intern position suited for computer science and technical students",
                    "exact_quote": "We are pleased to offer you the position of Software Engineering Intern starting August 1, 2026."
                },
                {
                    "criterion": "Duration & Availability",
                    "document_requirement": "Full-time 3-month duration with fixed deliverables",
                    "exact_quote": "The internship duration is 3 months. You will receive a fixed stipend of INR 15,000 per month upon completion of each month's deliverables."
                }
            ],
            "notes": "Verify if your university permits 3-month full-time internship attendance during academic terms."
        }
    },

    "Scholarship Notice (Sample)": {
        "document_type": "Scholarship Notice",
        "document_type_badge": "Scholarship Notice",
        "five_point_summary": [
            "Official State Merit-cum-Means Higher Education Scholarship for the 2026-27 academic year.",
            "Exclusively covers full-time B.Tech, B.E., or Professional Degree students in Year 2 or Year 3.",
            "Requires permanent residency in Maharashtra with a valid state domicile certificate.",
            "Caste/Category criteria restricted to SC, ST, and OBC applicants with verified certificates.",
            "Family gross income must be strictly below INR 2,50,000 per annum certified by a Tahsildar."
        ],
        "risks": [
            {
                "level": "yellow",
                "title": "Strict Documentation Mandate (Tahsildar Income Proof)",
                "explanation": "Income certificates issued by unauthorized local bodies will lead to immediate rejection without a re-application window.",
                "exact_quote": "Total annual household gross income from all sources must not exceed INR 2,50,000 per annum. Income certificate issued by Tahsildar is mandatory."
            },
            {
                "level": "yellow",
                "title": "Strict Domicile Restriction to Maharashtra",
                "explanation": "Students studying in Maharashtra but whose domicile is another state are completely ineligible.",
                "exact_quote": "The candidate must be a permanent resident of Maharashtra holding a valid state domicile certificate."
            },
            {
                "level": "green",
                "title": "Explicit Benefit Structure Provided",
                "explanation": "The notice clearly commits to 80% tuition waiver plus INR 20,000 maintenance allowance without hidden fees.",
                "exact_quote": "Approved scholars will receive 80% tuition waiver plus INR 20,000 annual maintenance allowance."
            }
        ],
        "identified_parties": "Department of Higher Education (Authority) and Eligible Student",
        "key_dates_or_deadlines": "Academic session 2026-27; application submission deadlines",
        "financial_terms": "80% tuition fee waiver plus INR 20,000 annual maintenance allowance",
        "missing_critical_details": "Renewal criteria (minimum CGPA/attendance required in subsequent years) are unstated.",
        "eligibility": {
            "applicable": True,
            "overall_summary": "State Merit-cum-Means Scholarship for 2nd/3rd year Engineering students residing in Maharashtra from SC/ST/OBC categories with income under ₹2.5 Lakhs.",
            "criteria_list": [
                {
                    "criterion": "Course & Year",
                    "document_requirement": "Full-time B.Tech / B.E. / Professional Degree in 2nd or 3rd year",
                    "exact_quote": "Candidate must be enrolled full-time in B.Tech / B.E. / Professional Degree in their 2nd or 3rd year of study at an accredited university."
                },
                {
                    "criterion": "Domicile State",
                    "document_requirement": "Permanent resident of Maharashtra holding valid state domicile certificate",
                    "exact_quote": "The candidate must be a permanent resident of Maharashtra holding a valid state domicile certificate."
                },
                {
                    "criterion": "Social Category",
                    "document_requirement": "Open to candidates from SC, ST, and OBC categories with verified caste certificates",
                    "exact_quote": "Open to candidates from SC, ST, and OBC categories with verified caste certificates."
                },
                {
                    "criterion": "Annual Income Cap",
                    "document_requirement": "Household gross income must not exceed INR 2,50,000 per annum certified by Tahsildar",
                    "exact_quote": "Total annual household gross income from all sources must not exceed INR 2,50,000 per annum. Income certificate issued by Tahsildar is mandatory."
                }
            ],
            "notes": "Tahsildar-certified income proof and Maharashtra domicile certificate are strictly mandatory."
        }
    }
}
