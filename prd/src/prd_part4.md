[[PB]]

# 12. Build Plan, Testing and Demo

## 12.1 Sprint plan

![Prototype build plan](fig/d6_sprints.png){width=6.2in}

| Sprint | Weeks | Deliverable | Linked requirements |
|---|---|---|---|
| S0 | 0–4 | Design system; clickable Figma flows for all 10 screens | All screens |
| S1 | 2–6 | Data model, synthetic data generator, ingestion and validation | DR-01 to DR-10, FR-90 to FR-92 |
| S2 | 4–8 | Benchmarking Cockpit + peer engine | FR-10 to FR-15, AI-01 |
| S3 | 8–12 | Quote & Renewal Desk (upload, extract, review, compare, approve) | FR-20 to FR-26, AI-04 |
| S4 | 10–14 | AI Simulation Lab + renewal forecast + model card | FR-30 to FR-35, AI-02, AI-03 |
| S5 | 12–16 | Portfolio home, vendor/TPA, zero-login nudges | FR-01 to FR-06, FR-40 to FR-56 |
| S6 | 14–18 | GTM Command Centre + business simulator | FR-70 to FR-83 |
| S7 | 18–20 | Security hardening, audit log, pilot demo script | NFR-01 to NFR-09, FR-93 to FR-95 |

This aligns with the report roadmap: Benchmarking Cockpit MVP by month 5, broker pilots from month 3, Quote Desk by months 4–8 (report Section 13.2).

## 12.2 Acceptance tests

| Test | Method | Pass criterion |
|---|---|---|
| Quote extraction accuracy | 50 real insurer quotes (from pilots), hand-labelled | ≥95% of fields correct |
| Renewal forecast | Back-test on pilot clients' last 2 renewals | Mean error ≤5 pts |
| Simulator realism | Compare scenario estimate with the insurer's revised quote | Within ±2 pts on ≥70% of scenarios |
| Peer-set privacy | Automated test on every refresh | Zero cohorts shown with < 10 companies |
| Policy Q&A | 100-question test set per pilot client | ≥90% correct, with correct clause citation |
| Usability | 5 account managers complete a renewal pack unaided | Median time < 2 hours; SUS score ≥70 |
| Security | External vulnerability scan before pilot | No high or critical findings open |

## 12.3 Broker demo script (15 minutes)

1. **Portfolio Home (2 min):** "Here are your 38 clients; 7 renew in 90 days, 2 at high risk."
2. **Benchmarking Cockpit (4 min):** open Acme Tech; show claims ratio 18 points above peers and a +18.9% forecast.
3. **Simulation Lab (3 min):** apply a 10% parents' co-pay and a 1% room-rent cap; premium per life falls 15.3%.
4. **Quote Desk (4 min):** drop in five quote PDFs; show extraction, flags and the draft recommendation.
5. **Close (2 min):** "Let's run this on three of your clients for 90 days and measure the hours saved."

# 13. Success Metrics

| Metric | Definition | Pilot target | Source |
|---|---|---|---|
| Renewal prep time | Hours per renewal pack vs baseline | −50% | Report KPI 13.4 |
| Extraction accuracy | Correct fields ÷ total fields | ≥95% | Report 7.3 |
| Forecast error | Mean absolute error, pts | ≤5 | Report 7.3 |
| Broker weekly active users | Active users ÷ licensed users | ≥70% by day 60 | Report 11.1 |
| Employee activation | Employees acting on ≥1 nudge ÷ eligible | ≥60% | Report 13.4 |
| Insights accepted without edits | Accepted ÷ shown | ≥80% | Report Appendix C |
| Pilot-to-paid conversion | Paid ÷ pilots | ≥50% | Report 13.4 |
| Time to first value | Contract to first client live | ≤30 days | Report 11.1 |

# 14. Risks, Assumptions and Open Questions

## 14.1 Prototype risks

| Risk | Impact | Mitigation |
|---|---|---|
| Synthetic data makes models look better than reality | Over-confidence in AI accuracy | Label every screen "synthetic"; re-test on pilot data before any client claim |
| Too few real quotes to test extraction | Cannot prove ≥95% accuracy | Collect 50 quotes in the first two pilots as a condition of the pilot |
| Brokers reluctant to share data | Benchmark pool stays small | Start with portfolio benchmarking (works with one broker); pooled-data clause in contracts |
| Scope creep from custom requests | Delays | Apply the report's product governance rule: core / configurable / paid custom / reject |
| Regulatory boundary on comparison | Legal risk | Broker-facing only; legal opinion before launch |

## 14.2 Assumptions

- NivoTime's existing Flex, TPA-integration and analytics code can be reused for data ingestion and dashboards; the extent is not yet confirmed (report Appendix B).
- Pilot brokers will provide anonymised claims and census data under a data-processing agreement.
- Pricing and business-case figures follow report assumptions A1–A14 and are illustrative.

## 14.3 Open questions for NivoTime

1. Which of the described features (benchmarking dashboard, vendor management, quote comparison) already exist in code, and in what state?
2. How many insurers and TPAs send data in a usable format today?
3. Which CRM, if any, is in use, so S8 can connect to it?
4. Who will own the product (product manager) and the AI models during the pilot?

# 15. Traceability Matrix

| Report recommendation (section) | PRD requirements | Screen | KPI |
|---|---|---|---|
| Benchmarking Cockpit with co-pay, size, family, SI filters (7.2, 7.4) | FR-10 to FR-15, AI-01 | S2 | Insights accepted ≥80% |
| Quote & Renewal Desk with AI extraction (7.2, 7.3) | FR-20 to FR-26, AI-04 | S3 | Accuracy ≥95%; prep time −50% |
| Plan simulator and renewal forecast (7.3) | FR-30 to FR-35, AI-02, AI-03 | S4 | Forecast error ≤5 pts |
| Vendor/TPA management (7.2) | FR-40 to FR-44 | S5 | SLA compliance trend |
| Zero-login engagement (11.2) | FR-50 to FR-56 | S6 | Activation ≥60% |
| Advisory & consulting layer (7.2, 9.5) | FR-60 to FR-63 | S7 | Advisory packs sold |
| Cold-start data plan (7.5) | DR-01 to DR-10, FR-90 to FR-92 | S10 | Consent coverage 100% |
| Regulatory guardrails (7.7) | FR-23 note, FR-53, NFR-02 to NFR-06 | All | Zero incidents |
| Segmentation, TAM/SAM/SOM, ICP (8.2–8.4) | FR-70, FR-72, Section 5.10 | S8 | Named accounts contacted |
| Funnel and sales engine (10.1, 10.4) | FR-71, FR-73, FR-74 | S8 | Pilot-to-paid ≥50% |
| Financial case and sensitivity (13.3) | FR-80 to FR-83 | S9 | Break-even by Year 3 |
| Governance and AI review (12.4, 13.6) | AI-G1 to AI-G5, FR-93 to FR-95 | S10 | Override rate tracked |

[[PB]]

# Appendix A: Synthetic Data Specification

| Field | Generation rule |
|---|---|
| industry | Categorical: IT 28%, manufacturing 22%, BFSI 16%, pharma 12%, retail 12%, professional services 10% |
| employees | Log-normal around 650, clipped to 250–2,000 |
| avg_age | Industry base (IT 30 … manufacturing 37) + normal noise (sd 2.5) |
| family | E 15%, E+S+2C 50%, E+S+2C+P 35% |
| sum_insured | ₹3L 35%, ₹5L 45%, ₹10L 20% |
| copay_parents | 0/10/20% (only where parents are covered) |
| room_rent | 1% 45%, 2% 30%, no cap 25% |
| premium_per_life | Base × age × family × SI × room-rent × co-pay × city factors × noise; calibrated to mean ₹2,234 |
| claims_ratio | 78% base + parents-without-co-pay +10 pts + no cap +4 pts + age effect + noise scaled by group size |
| renewal_loading | 12% trend + credibility-weighted claims effect + plan effects + noise |
| engagement | Normal around 44% (sd 12%) |

*The generator and model code (Python) are kept with this document so the prototype team can reproduce every number.*

# Appendix B: Glossary

| Term | Meaning |
|---|---|
| ICR (claims ratio) | Claims paid and outstanding ÷ premium earned |
| Renewal loading | Percentage change in premium at renewal |
| Peer set | Group of comparable companies used for benchmarking (minimum 10) |
| Co-pay | Share of each claim paid by the employee or family member |
| Room-rent cap | Limit on daily hospital room charges, often a % of sum insured |
| TPA | Third-party administrator that processes health claims |
| Zero-login | Engagement through nudges and secure links, without routine portal logins |
| Model card | Short summary of a model's purpose, data, accuracy and limits |
| MAE | Mean absolute error: the average size of a forecast miss |
| White-label | Product shown under the broker's own brand |
| DPDP | Digital Personal Data Protection Act 2023 and Rules 2025 |
| MoSCoW | Must / Should / Could / Won't prioritisation |
