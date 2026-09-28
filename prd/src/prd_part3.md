[[PB]]

# 6. AI / ML Requirements

Each model below comes from report Section 7.3. For each one, the table sets the input, the method, the output, the quality bar and what happens when the model is unsure.

| ID | Model | Method | Inputs | Output | Quality bar | Fallback / human control |
|---|---|---|---|---|---|---|
| AI-01 | Peer-group matching | k-nearest neighbours on standardised features | Industry, size, age mix, family definition, sum insured, city | Peer set of ≥10 companies | Stable peer set (≥70% overlap week to week) | Widen filters automatically; never show < 10 |
| AI-02 | Renewal cost forecast | Gradient-boosted trees; permutation or SHAP explanations | Claims ratio, demographics, plan design, group size, medical trend | Renewal loading % with range and top drivers | Mean error ≤5 pts on back-test | Show range, not a single number; broker review |
| AI-03 | Plan-design simulator | Log-linear rating relativities + AI-02 | Current plan, proposed changes | Premium impact per change | Model fit R² ≥0.85; results within ±2 pts of insurer quotes in pilot | Labelled "estimate"; insurer quote is final |
| AI-04 | Quote document AI | OCR + large language model extraction to a fixed schema | Quote PDFs and Excel files | 24 structured fields with confidence | ≥95% field accuracy | Confidence < 0.85 → human review |
| AI-05 | Claims anomaly flags | Isolation forest + rules (cost per day, length of stay) | Claims lines | Flags for review | Precision ≥50% before use with clients | Advisory only; no automatic decisions |
| AI-06 | Policy Q&A assistant | Retrieval-augmented generation over the employer's own policy documents | Policy wording, FAQs | Plain-language answer with clause citation | ≥90% answers correct on a 100-question test set | Sensitive or unclear queries go to a human |
| AI-07 | Renewal risk score | Classifier on engagement, claims trend, service issues | Account-level data | 0–100 risk of client loss | Top-decile risk captures ≥40% of actual losses (once data exists) | Shown as a prompt for action only |

**AI governance requirements**

| ID | Requirement | Priority |
|---|---|---|
| AI-G1 | Every model output shown to a client is logged (ModelRun) with version, inputs hash, reviewer and any override | Must |
| AI-G2 | A model card is visible in the product for AI-02, AI-03, AI-04 | Must |
| AI-G3 | No personal data is sent to external AI services without masking; data stays in India-region cloud where possible | Must |
| AI-G4 | Quarterly bias and accuracy review by industry, city tier and group size | Should |
| AI-G5 | Models retrained monthly once real pilot data exists; version can be rolled back | Should |

# 7. Prototype Simulation of the AI/ML Layer

No real client data was available, so the AI layer was **simulated on a synthetic dataset** to prove that the pipeline works end to end and to produce realistic screens. Treat these results as a **proof of mechanics, not proof of accuracy**. Real data will be noisier, and real errors will be higher.

## 7.1 Synthetic dataset

| Item | Value |
|---|---|
| Employer groups generated | 600 |
| Industries | IT services 168, manufacturing 132, BFSI 100, retail 74, pharma 71, professional services 55 |
| Group size | 250–2,000 employees (log-normal, median ~650) |
| Plan features | Family definition, sum insured (₹3L/5L/10L), parents' co-pay (0/10/20%), room-rent cap (1%, 2%, none), city tier |
| Calibration | Mean premium per life **₹2,234**, matching the report's ₹2,233 derived from IRDAI data (₹61,435 cr ÷ 27.51 cr lives) |
| Mean claims ratio | 81.6% (IRDAI all-health ratio: 85.34% in FY25) |
| Renewal loading | 12% medical trend + claims-experience effect weighted by group size + plan-design effects + noise |

## 7.2 Results

**AI-02 Renewal cost forecast (back-test on 150 held-out groups)**

| Measure | Result | Target |
|---|---|---|
| Mean absolute error | **1.87 percentage points** | ≤5 pts |
| Trend-only baseline (everyone gets +12%) | 5.52 pts | — |
| Improvement over baseline | **66%** | — |
| Forecasts within ±5 pts | **96%** | ≥90% |

**Forecast drivers (share of explained effect):** claims ratio 89%, average age 5%, group size 3%, family definition 1%, room-rent cap 1%. **So what:** past claims experience dominates renewal pricing. Accurate, clean claims data is the most valuable input, which supports the data-ingestion priority (FR-90 to FR-92).

**AI-01 Peer matching (sample client "Acme Tech", synthetic)**

| Measure | Client | Peer set (42 companies) |
|---|---|---|
| Premium per life | ₹2,500 | Client at 79th percentile |
| Claims ratio | 96% | Median 78% |
| Employee engagement | 36% | Median 45% |
| Forecast renewal loading | +18.9% | — |

**AI-03 Plan-design simulator (rating model fit R² = 0.954 on synthetic data)**

| Change | Estimated premium impact |
|---|---|
| 10% co-pay on parents | −4.2% |
| 20% co-pay on parents | −8.2% |
| Room-rent cap at 1% (from no cap) | −11.6% |
| Sum insured ₹5 lakh → ₹10 lakh | +24.2% |
| Remove parents' cover | −30.3% |

**AI-05 Claims anomaly flags (5,000 synthetic claims, 100 planted anomalies)**

| Approach | Flagged | Precision | Recall |
|---|---|---|---|
| Isolation forest alone | 100 | 29% | 29% |
| Isolation forest + cost-per-day rule | 75 | **56%** | **42%** |

**So what:** an unsupervised model alone flags too many genuine large claims. The hybrid approach passes the 50% precision bar, but flags must stay **advisory**, reviewed by a person, exactly as the report's guardrails require.

**AI-04 and AI-06** use language models and cannot be meaningfully simulated without real documents. Their acceptance test is defined in Section 12: 50 labelled insurer quotes and 100 policy questions collected during pilots.

## 7.3 Synthetic data and model pipeline

| Stage | What happens | Tool (prototype) |
|---|---|---|
| Generate | Create employer groups, plans, claims with known rules | Python (NumPy, pandas) |
| Store | Load into the prototype database | SQLite / PostgreSQL |
| Train | Fit AI-01 to AI-03 and AI-05 | scikit-learn |
| Evaluate | Hold-out back-test; write metrics to ModelRun | scikit-learn metrics |
| Serve | Screens read metrics and predictions from the database | Streamlit / FastAPI |
| Replace | Swap synthetic data for consented pilot data, retrain, compare | Same pipeline |

[[PB]]

# 8. Data Requirements

## 8.1 Data model

![Core data model](fig/d5_datamodel.png){width=6.4in}

## 8.2 Key data fields

| ID | Entity | Key fields | Source | Sensitivity |
|---|---|---|---|---|
| DR-01 | EmployerAccount | Industry, employees, city, renewal date, broker | Broker CRM / onboarding form | Business |
| DR-02 | PlanDesign | Sum insured, family definition, co-pays, room-rent, sub-limits | Policy schedule | Business |
| DR-03 | Member | Relation, age band, consent flags (no names in benchmark pool) | HR census | **Personal** |
| DR-04 | Claim | Amount, length of stay, diagnosis group, status, turnaround minutes | TPA MIS file | **Sensitive health data** |
| DR-05 | Quote / QuoteTerm | 24 schema fields, confidence, reviewer | Insurer quotes | Business |
| DR-06 | Vendor / SLAEvent | SLA type, minutes, ticket status | TPA reports, tickets | Business |
| DR-07 | BenchmarkCohort | Filters, company count (≥10), percentiles | Computed | Anonymised |
| DR-08 | Nudge | Event, channel, sent, actioned | Engagement engine | Personal |
| DR-09 | ModelRun | Model, version, output, reviewer, override | Platform | Internal |
| DR-10 | AuditLog | User, action, object, time | Platform | Internal |

## 8.3 Data sourcing plan (solving the "cold start", report Section 7.5)

| Phase | Source | Enables |
|---|---|---|
| Prototype | Synthetic data (this document) | Demos, UI testing, pipeline proof |
| Pilot (months 3–6) | Each broker's own anonymised book | Portfolio benchmarking within one broker |
| Scale (months 6–18) | Pooled, consented, anonymised data across brokers | True market peer benchmarks |
| Ongoing | Public IRDAI/GI Council aggregates; annual benefits survey | Market context and plan-design data |

**Data rules**

- Benchmarks use only records with a consent tag (FR-92) and cohorts of ≥10 companies (FR-11).
- Health data (claims) is kept at diagnosis-group level in the benchmark pool; no individual-level health data leaves the client's own workspace.
- Retention: follow the DPDP Rules timeline, with core obligations from 14 May 2027 (report Section 3.2); logs kept at least one year and CERT-In logs for 180 days.

# 9. Non-Functional Requirements

| ID | Area | Requirement | Priority |
|---|---|---|---|
| NFR-01 | Performance | Dashboards load in < 3 s; filter changes refresh in < 3 s; quote extraction < 60 s per document | Must |
| NFR-02 | Security | HTTPS only on a branded domain; role-based access (Section 2); encryption at rest and in transit | Must |
| NFR-03 | Authentication | SSO for broker and HR users; OTP for employees; session timeout 30 minutes | Must |
| NFR-04 | Privacy | DPDP-aligned consent, purpose limitation, data-processing agreements with brokers; breach response plan | Must |
| NFR-05 | Incident reporting | Cyber incidents reported within 6 hours (CERT-In) | Must |
| NFR-06 | Audit | Immutable audit log for data access, approvals and AI outputs | Must |
| NFR-07 | Availability | 99.5% monthly uptime for the pilot; daily backups | Should |
| NFR-08 | Accessibility | WCAG 2.1 AA contrast; values never shown by colour alone; keyboard navigation | Should |
| NFR-09 | White-label | Broker logo, colours and domain configurable without code | Must |
| NFR-10 | Scalability | 50 brokers, 2,000 employer accounts, 1.5 million lives without redesign | Could |
| NFR-11 | Localisation | English first; Hindi and regional languages for employee nudges | Could |
| NFR-12 | Data residency | Cloud region in India preferred for client data | Should |

# 10. Technology Recommendations for the Prototype

| Layer | Prototype (weeks 0–20) | Production path |
|---|---|---|
| Clickable design | Figma (all 10 screens, linked flows) | Design system reused |
| Front end | Streamlit (fast, Python-native) | React + a charting library |
| Back end / API | FastAPI | FastAPI or Node.js |
| Database | SQLite → PostgreSQL | Managed PostgreSQL |
| AI/ML | scikit-learn, XGBoost; cloud OCR + LLM API for quotes | Same, with model registry |
| Internal dashboards | Power BI or Looker Studio (GTM and business simulator) | Embedded BI |
| CRM | HubSpot (free/starter) or Zoho CRM | Same |
| Messaging | Email + WhatsApp Business API (sandbox) | Approved provider |
| Hosting | India-region cloud; synthetic data only | Hardened cloud, ISO 27001 path |

**Recommended data flow for the go-to-market stack (report Section 12.1):** lead sources → CRM → marketing automation → sales → customer success → BI dashboard.

# 11. Dashboard and Chart Catalogue

Every chart in the prototype, the question it answers, and how it is built.

| Chart ID | Screen | Question it answers | Chart type | Data | Interaction |
|---|---|---|---|---|---|
| C-01 | S1 | Which clients need attention first? | Table with inline risk bars | Accounts, renewal dates, risk score | Sort, click to open client |
| C-02 | S2 | Are we above or below peers? | KPI tiles with percentile | Premium, ICR, forecast, engagement | Filter bar |
| C-03 | S2 | Where does our plan sit feature by feature? | Horizontal percentile bars + median marker | Peer percentiles | Hover shows peer values |
| C-04 | S3 | Which quote is best and what got worse? | Comparison grid with flags | 24 quote fields | Click field to see source text |
| C-05 | S4 | What do plan changes save? | Waterfall | Simulator output | Sliders update live |
| C-06 | S4 | What drives the renewal forecast? | Horizontal bars (driver share) | Model explanations | Hover shows definition |
| C-07 | S5 | Are TPAs meeting IRDAI timelines? | Line chart with 60-min target line | Weekly median approval time | Toggle TPA |
| C-08 | S5 | Which vendors perform worst? | Scorecard table | SLA, tickets, feedback | Sort |
| C-09 | S6 | Are employees engaging? | KPI tiles + funnel (sent → opened → actioned) | Nudge log | Filter by event type |
| C-10 | S8 | How big is each segment? | Horizontal bars TAM → SAM → ABM → SOM | Report sizing | Edit assumptions |
| C-11 | S8 | Is the pipeline on plan? | Grouped bars by stage and path | CRM stages | Filter by quarter |
| C-12 | S8 | Where do we sit vs competitors? | Strategic group scatter | Report Section 5.3 | Static |
| C-13 | S9 | When does the suite break even? | Grouped bars revenue vs cost | Business model | Sliders |
| C-14 | S9 | Which lever matters most? | Diverging sensitivity bars | Model sensitivities | Static per scenario |
| C-15 | S10 | Are the models healthy? | Line with target line | Accuracy and error by week | Toggle model |

**Chart design rules:** one y-axis per chart; numbers printed on or next to bars; colour never used alone to carry meaning; a validated colour palette for series; brand purple and green reserved for navigation and headers.
