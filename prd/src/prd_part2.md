[[PB]]

# 5. Functional Requirements by Screen

## 5.1 S1 — Portfolio Home (Broker Workspace)

![S1 Portfolio Home (synthetic data)](fig/s1_portfolio.png){width=6.4in}

**Purpose:** give the broker one view of all employer clients, upcoming renewals, risk and next actions.

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-01 | Show KPI tiles: active clients, lives on platform, renewals in next 90 days, hours saved this quarter | Must | Tiles refresh on page load; values match the underlying tables |
| FR-02 | List clients with lives, renewal date, claims ratio (ICR), renewal risk score (0–100) and next action | Must | Sortable by every column; default sort by renewal date |
| FR-03 | Colour the risk score by band (≥60 high, 40–59 medium, <40 low) and show the number next to the bar | Must | Band is never shown by colour alone |
| FR-04 | Alerts panel: AI suggestions and SLA breaches, each linking to the relevant screen | Should | Clicking an alert opens the filtered screen |
| FR-05 | Apply the broker's white-label theme (logo, colours, domain) | Must | No NivoTime branding visible to the broker's clients |
| FR-06 | Create a renewal task list automatically 90 days before each renewal | Must | Tasks appear on day T-90 with owners |

**Hours saved (FR-01)** = Σ (baseline hours per task − actual logged hours). The baseline is set during pilot onboarding (Appendix C of the report).

## 5.2 S2 — Benefits Benchmarking Cockpit (Module 1)

This is the dashboard shown in the report (Section 7.4), rebuilt here on the synthetic dataset so every number comes from the simulation in Section 7.

![S2 Benefits Benchmarking Cockpit (synthetic data)](fig/s2_cockpit.png){width=6.4in}

**Purpose:** answer the HR head's question, *"Are we paying more than similar companies, and what should we change before renewal?"*

**Filters (top bar)**

| Filter | Values | Default |
|---|---|---|
| Industry | IT services, manufacturing, BFSI, pharma, retail, professional services | Client's own industry |
| Company size | 250–750, 750–2,000, 2,000+ | Client's band |
| Family cover | Employee only; E + spouse + 2 children; E+S+2C + parents | Client's definition |
| Sum insured | ₹3 lakh, ₹5 lakh, ₹10 lakh, custom | Client's value |
| Co-pay (parents) | 0%, 10%, 20% | Client's value |
| Peer set | Auto (k-nearest neighbours) or manual | Auto, shown as "n companies" |

**KPI tiles**

| Tile | Definition | Comparison shown |
|---|---|---|
| Premium per life | Annual premium ÷ covered lives | Percentile within peer set |
| Claims ratio (ICR) | Incurred claims ÷ earned premium, last 12 months | Peer median |
| Forecast renewal load | Output of the renewal forecast model (AI-02) | ± model error range |
| Employee engagement | Employees who acted on at least one nudge or login in 90 days ÷ eligible employees | Peer median |

**Requirements**

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-10 | Filter bar with the six filters above; changes refresh all tiles and charts | Must | Refresh in < 3 seconds for a peer pool of 5,000 companies |
| FR-11 | Peer set must contain **at least 10 companies**; otherwise the filter is widened automatically and the user is told | Must | No chart ever shows a peer set < 10 |
| FR-12 | Percentile chart for six plan features (sum insured, parental cover, maternity, room-rent, OPD/wellness, premium per life) with a peer-median marker | Must | Numbers printed on bars; median marker labelled |
| FR-13 | AI renewal insights panel: 3–5 plain-language insights, each with the number behind it and a link to the Simulation Lab | Must | Every insight cites its data; broker can hide any insight |
| FR-14 | "Export benchmark pack" to PDF and PowerPoint in the broker's branding | Should | Export in < 20 seconds |
| FR-15 | Data freshness label on every tile (for example "claims to 31 Aug") | Must | Label visible on screen and in exports |

## 5.3 S3 — Quote & Renewal Desk (Module 2)

![S3 Quote & Renewal Desk (illustrative data, from the report)](fig/f5_quotes.png){width=6.4in}

![Quote document AI pipeline](fig/d3_quote_pipeline.png){width=6.4in}

**Standard quote schema (24 fields, grouped)**

| Group | Fields |
|---|---|
| Commercials | Insurer, TPA, premium, GST, policy period, payment terms |
| Cover | Sum insured, family definition, floater/individual, corporate buffer |
| Limits | Room-rent cap, ICU cap, maternity limit, new-born cover, disease-wise sub-limits |
| Cost sharing | Co-pay (employees), co-pay (parents), deductible |
| Waiting periods | Pre-existing disease, 30-day, specific illness, maternity |
| Other | Modern treatments, OPD, wellness add-ons, exclusions list |

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-20 | Upload quotes as PDF, Excel or email attachment (up to 10 per renewal) | Must | Files up to 20 MB accepted; virus-scanned |
| FR-21 | Extract all 24 fields with a confidence score per field (AI-04) | Must | Field accuracy ≥95% on the labelled test set |
| FR-22 | Send only fields with confidence < 0.85 to human review, highlighted in the grid | Must | Reviewer sees the source snippet next to the field |
| FR-23 | Comparison grid vs the expiring policy; orange box = worse than expiring, green = better | Must | Flags also shown as text labels, not colour alone |
| FR-24 | "AI value score" (0–100) per quote, combining price and coverage, with the formula visible on hover | Should | Weights editable by the broker |
| FR-25 | Renewal calendar and decision log (who chose what, when, why) | Must | Log cannot be edited after approval |
| FR-26 | Approval workflow: account manager drafts → broker MD approves → HR decides | Must | Status visible to all three roles |

**Regulatory guardrail (report Section 7.7):** the comparison is a tool for the licensed broker. It is never shown publicly to prospects, so NivoTime does not act as a web aggregator.

## 5.4 S4 — AI Simulation Lab

![S4 AI Simulation Lab (synthetic data; numbers from the simulation in Section 7)](fig/s4_simlab.png){width=6.4in}

**Purpose:** let the broker and HR test plan changes and see the likely premium impact and renewal forecast before talking to insurers.

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-30 | Sliders or dropdowns for: parents' co-pay, room-rent cap, sum insured, parents' cover, maternity limit, OPD/wellness add-on | Should | Each control shows current and new value |
| FR-31 | Waterfall chart: current premium per life → effect of each change → scenario premium | Should | Steps add up exactly to the scenario total |
| FR-32 | Renewal forecast drivers chart (share of forecast explained by each factor) | Should | Uses model explanations (AI-02) |
| FR-33 | Model card: mean error, baseline error, share within ±5 pts, test size, "human review required" | Must (if S4 built) | Values read from the latest model run, never typed in |
| FR-34 | Save up to 5 scenarios per client and compare them side by side | Should | Saved scenarios appear in the advisory pack |
| FR-35 | Show employees affected by each change (for example, number of parents affected by a co-pay) | Could | Count shown next to each change |

## 5.5 S5 — Vendor & TPA Management (Module 3)

![S5 Vendor & TPA Management (synthetic data)](fig/s5_vendor.png){width=6.4in}

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-40 | Vendor register: insurers, TPAs, wellness and diagnostic vendors, contract dates and contacts | Should | Import from Excel supported |
| FR-41 | Track cashless approval time against the **60-minute** IRDAI expectation and discharge time against **3 hours** | Should | Breaches flagged within 24 hours of data upload |
| FR-42 | Ticket tracking (open, overdue, resolved) with owner and due date | Should | Overdue tickets shown on Portfolio Home alerts |
| FR-43 | Vendor scorecard (0–100): SLA compliance 50%, ticket closure 30%, employee feedback 20% | Could | Weights editable; formula shown |
| FR-44 | Weekly trend chart of approval times per TPA with the target line | Should | Direct labels on each line |

## 5.6 S6 — Employee zero-login engagement (Module 4)

![S6 Employee zero-login flow (synthetic example)](fig/s6_zerologin.png){width=6.4in}

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-50 | Event-driven nudges: welcome, add dependants, policy card ready, renewal window, unused benefits, claim status | Should | Each event type can be switched on/off per employer |
| FR-51 | Channels: email and WhatsApp (via an approved business provider); push later | Should | Opt-out honoured within one message ("STOP") |
| FR-52 | Secure deep links: signed, single-use, expire in 72 hours | Must (if S6 built) | Expired link asks the user to log in |
| FR-53 | OTP login required for sensitive actions (adding dependants, claims detail) | Must | No health data visible without authentication |
| FR-54 | Frequency cap: max 2 nudges per employee per week | Should | Cap enforced across all event types |
| FR-55 | HR sees only aggregated engagement (activation, action rate, completion) | Must | No individual health data in HR reports |
| FR-56 | Multilingual templates (English, Hindi, plus regional languages later) | Could | Template language chosen per employee |

## 5.7 S7 — Advisory Pack Builder (Module 5)

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-60 | Assemble a renewal pack: benchmark summary, quote comparison, chosen scenario, forecast and recommendation | Should | One click from an approved scenario |
| FR-61 | Broker-branded PDF and PowerPoint output | Should | Uses the white-label theme |
| FR-62 | AI-drafted narrative, editable, with every number linked to its source | Should | Draft marked "AI draft — review before sending" until approved |
| FR-63 | Record advisory engagements for billing (₹75,000 pack, report Section 9.5) | Could | Engagement count visible to NivoTime admin |

## 5.8 S8 — GTM Command Centre (internal NivoTime dashboard)

![S8 GTM Command Centre (figures from the report; account names anonymised)](fig/s7_gtm.png){width=6.4in}

**Purpose:** show NivoTime leadership whether the go-to-market plan in the report is on track.

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-70 | Segment explorer: broker TAM (751), SAM (~600), named ABM list (100), SOM target (15 by Year 3); employer path 7.66 lakh → 150 → 18 | Could | Numbers editable; source note shown |
| FR-71 | Pipeline by stage for brokers and employers (targeted, meeting, demo, pilot, won) | Could | Pulled from the CRM (HubSpot or Zoho) nightly |
| FR-72 | ICP-scored account list: type, group-health clients, in-house tech, trigger event, score, owner, next step | Could | Score formula visible (Section 5.10) |
| FR-73 | Funnel conversion rates vs plan (report assumption A14) | Could | Variance highlighted when > 20% off plan |
| FR-74 | Lost-deal reasons summary | Could | Mandatory field when a deal is marked lost |

**Reference charts carried over from the report:**

![Illustrative Year-1 broker funnel (report Section 10.4)](fig/f11_funnel.png){width=5.6in}

![Strategic group map (report Section 5.3)](fig/f2_groupmap.png){width=5.4in}

## 5.9 S9 — Business Case Simulator (internal)

![S9 Business Case Simulator (base-case figures from the report's financial model)](fig/s8_bizsim.png){width=6.4in}

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-80 | Sliders for brokers by Year 3, direct employers, subscription price, per-account fee, cost index, advisory attach rate | Could | Results update instantly |
| FR-81 | Revenue vs incremental cost by year; operating result; LTV:CAC; break-even year | Could | Base case reproduces the report: Year-3 revenue ₹105.4 lakh, result +₹6.4 lakh |
| FR-82 | Sensitivity chart (brokers −30%, costs ±20%, prices ±20%, no advisory) | Could | Matches report Section 13.3 |
| FR-83 | Downside / base / upside presets | Could | Presets match report scenarios |

![Illustrative three-year scenarios (report Section 13.3)](fig/f9_scenarios.png){width=6in}

## 5.10 ICP scoring logic (used in S8)

| Factor | Weight | Scoring rule |
|---|---|---|
| Group-health book size | 30% | 15–60 corporate clients = full score |
| In-house technology | 25% | None or Excel only = full; partial = half; existing vendor = zero |
| Trigger event present | 25% | Lost client to tech-first broker, new digital head, licence conversion, renewal pressure |
| Relationship access | 20% | Founder contact = full; second-degree = half; cold = low |

Accounts scoring **≥80** go to founder outreach; **60–79** to sales; **<60** are deprioritised (report Sections 8.4 and 10.1).

## 5.11 S10 — Admin: data ingestion and model monitoring

![S10 Admin and model monitoring (synthetic data)](fig/s9_admin.png){width=6.4in}

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-90 | Upload census, claims and policy files; auto-map columns to the standard template (census mapping assistant) | Must | ≥90% of columns auto-mapped on pilot files |
| FR-91 | Data validation rules (dates, duplicates, missing dependants, age vs relation) | Must | Errors listed with row numbers |
| FR-92 | Consent tag on every member record; records without consent excluded from the benchmark pool | Must | 100% of records tagged before pooling |
| FR-93 | Model monitoring: extraction accuracy, share of fields sent to review, forecast error, override rate | Must | Weekly trend charts with targets |
| FR-94 | Cohort guard: count of peer sets below 10 companies (hidden from users) | Must | Guard runs on every benchmark refresh |
| FR-95 | Audit log export for DPDP and client audits | Must | Export includes user, action, object, time |
