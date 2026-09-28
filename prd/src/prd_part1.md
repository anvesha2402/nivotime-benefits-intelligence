[[PB]]

# Document Control

| Item | Detail |
|---|---|
| Document | Product Requirements Document (PRD): Benefits Intelligence Suite, dashboard and prototype |
| Product | NivoTime Benefits Intelligence Suite (proposed in the Live Company Project report) |
| Version | 1.0, September 2026 |
| Prepared by | Anvesha, PGDM (E-Business) 2025–27, WeSchool |
| Status | Draft for prototype build and broker-pilot demo |
| Parent document | *From Services Breadth to Benefits Intelligence*, Live Company Project Report (Sections 7, 9–13, 15) |
| Data used | Public market data from the report; **synthetic data** for all screens and AI/ML simulations. No real client data. |

**How to read requirement IDs**

| Prefix | Meaning |
|---|---|
| FR-xx | Functional requirement (what the product must do) |
| AI-xx | AI / ML model requirement |
| DR-xx | Data requirement |
| NFR-xx | Non-functional requirement (security, speed, privacy, usability) |
| **Priority** | **Must** = needed for the pilot prototype; **Should** = strongly wanted; **Could** = nice to have; **Won't (now)** = later phase |

# 1. Purpose, Scope and Objectives

## 1.1 Why this document exists

- The Live Company Project report recommends that NivoTime build an **AI-powered Benefits Intelligence Suite** and sell it mainly through mid-size insurance brokers (report, Sections 7–9).
- This PRD turns that recommendation into a **buildable specification**: every screen, chart, user flow, data field and AI model the prototype needs, with acceptance criteria.
- It covers two things:
  1. The **customer-facing product** used by brokers, HR teams, employees and vendors.
  2. The **internal NivoTime dashboards** (go-to-market command centre and business-case simulator) that track whether the strategy is working.

## 1.2 Prototype objectives

Kept separate, as in the report: what the prototype must *do*, and how we will *measure* whether it works.

**Product objectives**

1. Let a broker compare a client's benefits with a peer group, filtered by co-pay, company size, industry, family cover and sum insured.
2. Turn 4–6 insurer quotes (PDF or Excel) into one structured comparison with flagged differences.
3. Simulate the premium effect of plan changes and forecast next year's renewal loading.
4. Track insurer, TPA and wellness vendor service levels in one place.
5. Reach employees through nudges without requiring routine logins.
6. Give NivoTime management one view of segments, pipeline and business-case scenarios.

**Measurement and validation objectives**

1. Renewal pack preparation time falls by **≥50%** in pilot (report KPI, Section 13.4).
2. Quote field extraction accuracy is **≥95%**; low-confidence fields go to human review.
3. Renewal forecast error is **within ±5 percentage points** on back-tested renewals.
4. **≥70%** of broker users are active weekly by day 60; **≥60%** employee activation.
5. **≥50%** of pilots convert to paid contracts (report Appendix C).

## 1.3 Scope

| In scope (prototype) | Out of scope (later phases) |
|---|---|
| Broker Workspace: portfolio, cockpit, quote desk, simulation lab, advisory packs | Native mobile apps (responsive web only) |
| HR/CFO views (read-only benchmark, forecast, engagement) | Live insurer API integrations (file upload used instead) |
| Employee zero-login nudge flow (demo channel) | Bima Sugam integration (roadmap item, report Section 13.2) |
| Vendor/TPA SLA tracking | Payments, billing and invoicing |
| Internal GTM Command Centre and business simulator | GCC / ZOYAME localisation |
| Admin: data ingestion, consent tags, model monitoring | Production-grade ISO 27001 controls (designed for, not certified) |

## 1.4 Guiding principles (from the report)

- **AI for work, not as a label:** every AI feature must replace a measurable manual task.
- **Broker-first, white-label:** the broker's brand faces the client; NivoTime stays in the background.
- **Human in the loop:** no AI output reaches a client without broker review.
- **Privacy by design:** anonymised benchmarks, minimum peer set of 10 companies, DPDP-ready consent tags.
- **Configure, don't customise:** industry needs are met by templates and settings, not separate code.

# 2. Users and Personas

| Persona | Role | Main goal | Top pain today | Key screens |
|---|---|---|---|---|
| **Rohit**, Broker MD | Economic buyer at a mid-size broker | Look as sharp as tech-first brokers; keep clients | Losing clients to Plum/Pazcare-type brokers | Portfolio home, GTM-style reports |
| **Meera**, Account manager | Daily user at the broker | Renewal pack in hours, not weeks | Re-typing quotes; no peer data | Cockpit, Quote Desk, Simulation Lab |
| **Anita**, CHRO / Total Rewards | Employer decision maker | Prove benefits are competitive; control premium | Renewal surprises; spreadsheets | HR benchmark snapshot, forecast |
| **Vikram**, CFO | Employer economic influencer | Predictable benefits cost | No forward view of renewal | Forecast, scenario summary |
| **Priya**, Employee | End user | Understand and use benefits easily | Forgets benefits; portal fatigue | Zero-login nudges, deep links |
| **TPA coordinator** | Vendor user | Meet SLAs, close tickets | Scattered requests | Vendor portal |
| **NivoTime leadership** | Internal | Know if the strategy is working | No pipeline or segment view | GTM Command Centre, business simulator |
| **NivoTime admin / analyst** | Internal | Clean data, healthy models | Messy files; no monitoring | Admin & model monitoring |

**Roles and permissions (summary)**

| Capability | Broker MD | Account manager | HR / CFO | Employee | Vendor | NivoTime admin |
|---|---|---|---|---|---|---|
| View client benchmarks | All clients | Assigned clients | Own company | — | — | Anonymised only |
| Upload quotes and data | — | Yes | Census only | — | SLA data | Yes |
| Run simulations | Yes | Yes | View shared scenarios | — | — | Yes |
| Approve client-facing pack | Yes | Draft only | Approve decision | — | — | — |
| See individual employee data | No | Limited (renewal tasks) | Own employees | Own record | Claim status only | No (anonymised) |
| GTM and business dashboards | — | — | — | — | — | Yes |

# 3. Product Overview

## 3.1 Architecture

![Proposed architecture of the Benefits Intelligence Suite (from the report)](fig/f3_architecture.png){width=6.2in}

## 3.2 Information architecture

![Sitemap of the prototype](fig/d1_sitemap.png){width=6.4in}

## 3.3 Screen inventory

| # | Screen | Users | Module | Priority |
|---|---|---|---|---|
| S1 | Portfolio Home | Broker MD, account manager | Broker Workspace | Must |
| S2 | Benefits Benchmarking Cockpit | Broker, HR, CFO | M1 | Must |
| S3 | Quote & Renewal Desk | Account manager | M2 | Must |
| S4 | AI Simulation Lab | Broker, HR | M1/M2 + AI layer | Should |
| S5 | Vendor & TPA Management | Broker, HR, vendor | M3 | Should |
| S6 | Employee zero-login flow | Employee | M4 | Should |
| S7 | Advisory pack builder | Broker | M5 | Should |
| S8 | GTM Command Centre | NivoTime leadership | Internal | Could |
| S9 | Business Case Simulator | NivoTime leadership | Internal | Could |
| S10 | Admin: ingestion and model monitoring | NivoTime admin | Platform | Must |

# 4. Key User Journeys

## 4.1 Renewal preparation (the core journey)

![Renewal preparation swimlane](fig/d2_renewal_flow.png){width=6.4in}

| Step | Actor | What happens | System response | Target time |
|---|---|---|---|---|
| 1 | Platform | Renewal date is 90 days away | Alert on Portfolio Home; task list created | Automatic |
| 2 | Account manager | Requests census, claims and quotes | Secure upload links sent to HR and insurers | 5 min |
| 3 | HR client | Uploads census and claims | Validation and column mapping; errors shown | 10 min |
| 4 | AI layer | Forecast and benchmark | Cockpit refreshed; renewal loading forecast | < 1 min |
| 5 | Account manager | Uploads 5 insurer quotes | Quote AI extracts terms into the standard schema | < 60 s per quote |
| 6 | Account manager | Reviews low-confidence fields only | Comparison grid with flags | 15 min |
| 7 | Account manager | Runs 2–3 plan scenarios | Premium impact and trade-offs | 10 min |
| 8 | Broker MD / HR | Approves recommendation | Pack generated; decision logged | 15 min |

**Target:** a full renewal pack in **under 2 hours of working time**, against a manual baseline of about 30 hours per account (report assumption A13).

## 4.2 Broker onboarding

![Broker onboarding journey (from the report)](fig/f12_onboarding.png){width=6.2in}

## 4.3 Employee zero-login engagement

![Zero-login engagement flow](fig/d4_zerologin_flow.png){width=6.4in}
