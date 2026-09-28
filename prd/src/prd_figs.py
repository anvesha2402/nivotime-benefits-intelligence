import json, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch, Circle
import numpy as np

P = "#3B3A73"; G = "#87B549"; GD = "#4F7A22"
C1, C2, C3, C4 = "#5553B5", "#E08A2E", "#3F8A3A", "#A7479A"
INK, INK2, MUTED, GRID = "#1F2130", "#4A4D5E", "#8A8FA3", "#E4E6EC"
LIGHTP, LIGHTG, BG = "#ECEBF7", "#EEF6E4", "#F4F5F8"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "figure.dpi": 200, "savefig.bbox": "tight", "savefig.pad_inches": 0.1})
OUT = "/home/claude/nivotime/prd/fig/"
S = json.load(open("/home/claude/nivotime/prd/sim.json"))
M = json.load(open("/home/claude/nivotime/final/model.json"))

def rbox(ax, x, y, w, h, fc="white", ec=GRID, lw=0.9, r=0.8):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw))
def t(ax, x, y, s, fs=6.5, c=INK, **k): ax.text(x, y, s, fontsize=fs, color=c, **k)
def screen(title, right="", w=7.0, h=4.4, H=66):
    fig = plt.figure(figsize=(w, h)); fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(0, H); ax.axis("off")
    ax.add_patch(Rectangle((0, H - 6), 100, 6, fc=P))
    t(ax, 2, H - 3, "NivoTime  |  " + title, 9, "white", fontweight="bold", va="center")
    if right: t(ax, 98, H - 3, right, 6.3, "white", va="center", ha="right")
    return fig, ax
def nav(ax, items, active, H=66):
    ax.add_patch(Rectangle((0, 0), 13, H - 6, fc="#2E2D5C"))
    for i, it in enumerate(items):
        y = H - 11 - i * 5.2
        if it == active: ax.add_patch(Rectangle((0, y - 2.2), 13, 4.4, fc=C1))
        t(ax, 1.5, y, it, 5.8, "white", va="center", fontweight="bold" if it == active else "normal")
def kpi(ax, x, y, w, h, lab, val, sub, subc=INK2):
    rbox(ax, x, y, w, h); t(ax, x + 1.3, y + h - 2.3, lab, 5.6, MUTED)
    t(ax, x + 1.3, y + h / 2 - 1, val, 11, INK, fontweight="bold", va="center"); t(ax, x + 1.3, y + 1.5, sub, 5.6, subc)
def save(fig, n): fig.savefig(OUT + n, facecolor=fig.get_facecolor()); plt.close(fig)
NAV = ["Portfolio", "Benchmarking", "Quote & Renewal", "AI Simulation Lab", "Vendors / TPA", "Engagement", "Advisory", "Admin"]

# ---------- S1 Portfolio home ----------
fig, ax = screen("Broker Workspace — Portfolio Home", "Broker: Sample Insurance Brokers Pvt Ltd (white-label)")
nav(ax, NAV, "Portfolio")
kpi(ax, 15, 48, 20, 10, "Active employer clients", "38", "+3 this quarter")
kpi(ax, 36.5, 48, 20, 10, "Lives on platform", "26,410", "72% engaged via nudges")
kpi(ax, 58, 48, 20, 10, "Renewals next 90 days", "7", "2 at high risk", C2)
kpi(ax, 79.5, 48, 18.5, 10, "Hours saved (QTD)", "212", "vs manual baseline")
rbox(ax, 15, 3, 50, 43); t(ax, 17, 43, "Clients by renewal date and risk", 7, INK, fontweight="bold")
cols = ["Client", "Lives", "Renewal", "ICR", "Risk", "Next action"]; cx = [17, 27.5, 33, 39.5, 44, 52.5]
for j, c in enumerate(cols): t(ax, cx[j], 39.5, c, 5.8, MUTED, fontweight="bold")
rows = [("Acme Tech", "439", "12 Dec", "96%", 82, "Run renewal pack"), ("Orbit Pharma", "1,120", "03 Jan", "88%", 64, "Benchmark review"),
        ("Delta Mfg", "1,840", "15 Jan", "71%", 22, "Collect census"), ("Nimbus BFSI", "760", "01 Feb", "92%", 71, "Plan simulation"),
        ("Kite Retail", "520", "18 Feb", "79%", 35, "Send nudges"), ("Vega Services", "310", "04 Mar", "84%", 48, "Quote request")]
for i, r in enumerate(rows):
    y = 35.5 - i * 5.3
    if i % 2 == 0: ax.add_patch(Rectangle((15.5, y - 2.3), 49, 4.6, fc="#FAFAFC", ec="none"))
    for j, v in enumerate(r):
        if j == 4:
            col = C2 if v >= 60 else (C1 if v >= 40 else C3)
            ax.add_patch(Rectangle((cx[j], y - 0.9), 4.5 * v / 100, 1.8, fc=col)); t(ax, cx[j] + 5.0, y, str(v), 5.6, INK, va="center")
        else: t(ax, cx[j], y, v, 5.9, INK, va="center")
rbox(ax, 67, 3, 31, 43, fc=LIGHTG, ec=G); t(ax, 69, 43, "Alerts and AI suggestions", 7, GD, fontweight="bold")
al = ["Acme Tech: ICR 96% (peer median 78%).\nForecast renewal +18.9%. Open cockpit.",
      "Nimbus BFSI: 4 employees missing\ndependant data before renewal.",
      "TPA B: cashless approvals averaging\n74 min vs 60-min IRDAI expectation.",
      "Orbit Pharma: 3 quotes received;\nextraction ready for review."]
for i, a in enumerate(al): t(ax, 69, 38.5 - i * 8.8, "• " + a, 5.9, INK, va="top", linespacing=1.35)
save(fig, "s1_portfolio.png")

# ---------- S2 Benchmarking cockpit (sim-consistent) ----------
pv = S["peer"]; cl = pv["client"]
fig, ax = screen("Benefits Benchmarking Cockpit", f"Client: Acme Tech (synthetic)  ·  Renewal in 74 days")
nav(ax, NAV, "Benchmarking")
filters = [("Industry", "IT services"), ("Company size", "250–750"), ("Family cover", "E+S+2C+P"), ("Sum insured", "₹5 lakh"),
           ("Co-pay (parents)", "0%"), ("Peer set", f"{pv['n_peers']} companies")]
for i, (k, v) in enumerate(filters):
    x = 15 + i * 14.2; rbox(ax, x, 52.5, 13.3, 5.5); t(ax, x + 1, 56.2, k, 5.2, MUTED); t(ax, x + 1, 53.9, v + " ▾", 6.3, INK, fontweight="bold")
kp = [("Premium / life", f"₹{int(cl['premium_per_life']):,}", f"{pv['prem_pct']}th percentile", C2),
      ("Claims ratio (ICR)", f"{pv['icr_client']}%", f"Peer median {pv['icr_peer_median']}%", C2),
      ("Forecast renewal load", f"+{pv['pred_renewal']}%", "Range ±1.9 pts (model MAE)", C2),
      ("Employee engagement", f"{pv['eng_client']}%", f"Peer median {pv['eng_peer_median']}%", C2)]
for i, (a, b, c, d) in enumerate(kp): kpi(ax, 15 + i * 21, 40.5, 20, 10.5, a, b, c, d)
rbox(ax, 15, 3, 45, 36); t(ax, 17, 36.3, "Where you sit vs. peers (percentile)", 6.8, INK, fontweight="bold")
items = [("Sum insured", 45), ("Parental cover", 81), ("Maternity limit", 62), ("Room-rent (no cap)", 88), ("OPD / wellness", 22), ("Premium per life", pv["prem_pct"])]
for i, (n, p) in enumerate(items):
    y = 31 - i * 4.6; t(ax, 17, y, n, 5.9, INK2, va="center")
    ax.add_patch(Rectangle((31, y - 0.9), 24, 1.8, fc="#EEF0F4")); ax.add_patch(Rectangle((31, y - 0.9), 24 * p / 100, 1.8, fc=C1))
    ax.plot([43, 43], [y - 1.4, y + 1.4], color=INK2, lw=0.8); t(ax, 55.8, y, str(p), 5.9, INK, va="center", fontweight="bold")
t(ax, 43.3, 4.5, "│ peer median", 5.2, MUTED)
rbox(ax, 62, 3, 36, 36, fc=LIGHTG, ec=G); t(ax, 64, 36.3, "AI renewal insights", 7, GD, fontweight="bold")
sm = S["simulator"]
ins = [f"1. Claims ratio is {pv['icr_client'] - pv['icr_peer_median']} pts above peers;\n    renewal forecast +{pv['pred_renewal']}%.",
       f"2. 10% co-pay on parents → est.\n    premium {sm['10% co-pay on parents']}%.",
       f"3. Room-rent cap at 1% → est.\n    premium {sm['Room-rent cap 1% (from no cap)']}%.",
       "4. OPD/wellness in bottom quartile:\n    low-cost add-on may lift engagement."]
for i, s_ in enumerate(ins): t(ax, 64, 32 - i * 7, s_, 5.9, INK, va="top", linespacing=1.35)
t(ax, 64, 4.6, "Synthetic data. Broker reviews before sharing.", 5, INK2, style="italic")
save(fig, "s2_cockpit.png")

# ---------- S4 AI Simulation Lab ----------
fig, ax = screen("AI Simulation Lab — plan design & renewal forecast", "What-if scenarios · model v0.1 (synthetic)")
nav(ax, NAV, "AI Simulation Lab")
rbox(ax, 15, 3, 24, 55); t(ax, 17, 55, "Scenario controls", 7, INK, fontweight="bold")
sl = [("Co-pay on parents", "10%", 0.33), ("Room-rent cap", "1% of SI", 0.2), ("Sum insured", "₹5 lakh", 0.4), ("Parents' cover", "Keep", 1.0),
      ("Maternity limit", "₹75,000", 0.5), ("OPD / wellness add-on", "₹1,500", 0.3)]
for i, (a, b, f) in enumerate(sl):
    y = 50 - i * 6.8; t(ax, 17, y, a, 5.9, INK2); t(ax, 37, y, b, 5.9, INK, ha="right", fontweight="bold")
    ax.add_patch(Rectangle((17, y - 3), 20, 0.8, fc="#DADDE6")); ax.add_patch(Rectangle((17, y - 3), 20 * f, 0.8, fc=C1))
    ax.add_patch(Circle((17 + 20 * f, y - 2.6), 0.9, fc="white", ec=C1, lw=1.2))
rbox(ax, 17, 4.5, 20, 4, fc=C1, ec=C1); t(ax, 27, 6.5, "Save scenario", 6.2, "white", ha="center", va="center", fontweight="bold")
# waterfall
rbox(ax, 41, 25, 57, 33); t(ax, 43, 55, "Premium per life impact (₹, estimate)", 7, INK, fontweight="bold")
base = cl["premium_per_life"]; s1 = base * (1 + sm["10% co-pay on parents"] / 100); s2 = s1 * (1 + sm["Room-rent cap 1% (from no cap)"] / 100); s3 = s2 + 1500 / 12 * 0  # OPD separate
steps = [("Current", base, None), ("Parents co-pay 10%", s1 - base, base), ("Room-rent cap 1%", s2 - s1, s1), ("Scenario", s2, None)]
x0 = 47; bw = 9; scale = 25 / 2600
for i, (n, v, st) in enumerate(steps):
    x = x0 + i * 12.5
    if st is None:
        ax.add_patch(Rectangle((x, 28.5), bw, v * scale, fc=C1)); t(ax, x + bw / 2, 28.5 + v * scale + 0.8, f"₹{v:,.0f}", 6, INK, ha="center", fontweight="bold")
    else:
        top = st * scale; ax.add_patch(Rectangle((x, 28.5 + top + v * scale), bw, -v * scale, fc=C3))
        t(ax, x + bw / 2, 28.5 + top + 0.8, f"−₹{abs(v):,.0f}", 6, INK, ha="center", fontweight="bold")
    t(ax, x + bw / 2, 27, n, 5.3, INK2, ha="center")
t(ax, 70, 38, f"Total change:\n{((s2 / base) - 1) * 100:+.1f}% per life", 7, C3, ha="center", fontweight="bold")
# drivers
rbox(ax, 41, 3, 28, 20); t(ax, 43, 20.3, "Renewal forecast drivers", 6.8, INK, fontweight="bold")
dr = list(S["drivers"].items())[:5]
for i, (n, v) in enumerate(dr):
    y = 16.5 - i * 3; t(ax, 43, y, n, 5.5, INK2, va="center")
    ax.add_patch(Rectangle((56, y - 0.7), 11 * v / 100, 1.4, fc=C4)); t(ax, 56 + 11 * v / 100 + 0.5, y, f"{v:.0f}%", 5.2, INK, va="center")
rbox(ax, 71, 3, 27, 20, fc=LIGHTG, ec=G); t(ax, 73, 20.3, "Model card (back-test)", 6.8, GD, fontweight="bold")
fc_ = S["forecast"]
mc = [f"Mean error: {fc_['mae_pp']} pts", f"Trend-only baseline: {fc_['naive_mae_pp']} pts", f"Within ±5 pts: {fc_['within_5pp']}%",
      f"Test groups: {fc_['test_n']} (synthetic)", "Human review: required"]
for i, m in enumerate(mc): t(ax, 73, 16.5 - i * 3, m, 5.9, INK, va="center")
save(fig, "s4_simlab.png")

# ---------- S5 Vendor / TPA ----------
fig, ax = screen("Vendor & TPA Management", "SLA view · last 30 days")
nav(ax, NAV, "Vendors / TPA")
kpi(ax, 15, 48, 20, 10, "Vendors managed", "14", "3 insurers · 2 TPAs · 9 wellness")
kpi(ax, 36.5, 48, 20, 10, "Cashless approvals ≤60 min", "81%", "Target 100% (IRDAI)", C2)
kpi(ax, 58, 48, 20, 10, "Discharge ≤3 hours", "88%", "Target 100% (IRDAI)", C2)
kpi(ax, 79.5, 48, 18.5, 10, "Open tickets", "23", "5 overdue", C2)
rbox(ax, 15, 3, 50, 43); t(ax, 17, 43, "Vendor scorecard", 7, INK, fontweight="bold")
cols = ["Vendor", "Type", "Cashless", "Discharge", "Tickets", "Score"]; cx = [17, 27, 36, 44.5, 53, 59]
for j, c in enumerate(cols): t(ax, cx[j], 39.5, c, 5.5, MUTED, fontweight="bold")
vr = [("TPA A", "TPA", "42 min", "2.4 h", "6", "86"), ("TPA B", "TPA", "74 min", "3.3 h", "11", "61"), ("Insurer X", "Insurer", "—", "—", "3", "79"),
      ("Insurer Y", "Insurer", "—", "—", "2", "83"), ("FitCo gyms", "Wellness", "—", "—", "1", "90"), ("LabNet", "Diagnostics", "—", "—", "0", "92")]
for i, r in enumerate(vr):
    y = 35.5 - i * 5.3
    if i % 2 == 0: ax.add_patch(Rectangle((15.5, y - 2.3), 49, 4.6, fc="#FAFAFC", ec="none"))
    for j, v in enumerate(r):
        col = C2 if (j in (2, 3) and v in ("74 min", "3.3 h")) or (j == 5 and int(v) < 70) else INK
        t(ax, cx[j], y, v, 5.9, col, va="center", fontweight="bold" if col == C2 else "normal")
rbox(ax, 67, 3, 31, 43); t(ax, 69, 43, "Cashless approval time by week (min)", 6.5, INK, fontweight="bold")
wk = np.arange(8); a = [48, 45, 44, 41, 43, 40, 42, 42]; b = [65, 70, 78, 72, 80, 76, 71, 74]
ox, oy, sx, sy = 71, 8, 24 / 7, 30 / 100
ax.plot([ox, ox + 24], [oy + 60 * sy, oy + 60 * sy], color=MUTED, lw=0.8, ls="--"); t(ax, ox + 24, oy + 60 * sy + 1, "60-min target", 5, MUTED, ha="right")
ax.plot(ox + wk * sx, oy + np.array(a) * sy, color=C1, lw=1.6); ax.plot(ox + wk * sx, oy + np.array(b) * sy, color=C2, lw=1.6)
t(ax, ox + 24.3, oy + a[-1] * sy, "TPA A", 5.5, C1, va="center"); t(ax, ox + 24.3, oy + b[-1] * sy, "TPA B", 5.5, C2, va="center")
ax.plot([ox, ox + 24], [oy, oy], color=GRID, lw=0.8)
for i in range(0, 8, 2): t(ax, ox + i * sx, oy - 2.5, f"W{i + 1}", 5, MUTED, ha="center")
save(fig, "s5_vendor.png")

# ---------- S6 Employee zero-login ----------
fig = plt.figure(figsize=(7.0, 3.9)); fig.patch.set_facecolor("white")
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(0, 56); ax.axis("off")
def phone(x, title, hdr_c):
    rbox(ax, x, 2, 24, 50, fc="#1F2130", ec="#1F2130", r=2.5); rbox(ax, x + 1, 4, 22, 45, fc="white", ec="white", r=1.5)
    ax.add_patch(Rectangle((x + 1, 43), 22, 6, fc=hdr_c)); t(ax, x + 2.5, 46, title, 6.3, "white", fontweight="bold", va="center")
phone(3, "WhatsApp · HR Benefits", "#128C7E")
rbox(ax, 5, 24, 18, 17, fc="#DCF8C6", ec="#DCF8C6")
t(ax, 6, 39.5, "Hi Priya, your benefits renewal\nwindow closes on 30 Nov.\n\nYour parents are not yet\nadded. It takes 2 minutes.\n\n▶ Add parents (secure link)", 5.6, INK, va="top", linespacing=1.4)
t(ax, 6, 21, "Sent by Acme Tech HR via\nNivoTime · reply STOP to opt out", 4.8, MUTED, va="top")
phone(38, "Acme Tech Benefits", P)
t(ax, 40, 40, "Verify it's you", 7, INK, fontweight="bold"); t(ax, 40, 36.5, "OTP sent to +91 98•••••210", 5.5, INK2)
for i in range(6): rbox(ax, 40 + i * 3.2, 30, 2.6, 3.5, ec=C1)
t(ax, 40, 26, "Sensitive action: adding\ndependants needs login.", 5.5, INK2, va="top", linespacing=1.4)
rbox(ax, 40, 7, 20, 4, fc=C1, ec=C1); t(ax, 50, 9, "Continue", 6.3, "white", ha="center", va="center", fontweight="bold")
phone(73, "Acme Tech Benefits", P)
t(ax, 75, 40, "Add parents", 7, INK, fontweight="bold")
for i, (a, b) in enumerate([("Father", "R. Sharma, 61"), ("Mother", "S. Sharma, 58"), ("Cover", "₹5 lakh, 0% co-pay"), ("Your cost", "₹0 (employer paid)")]):
    t(ax, 75, 35 - i * 5, a, 5.3, MUTED); t(ax, 75, 33 - i * 5, b, 6, INK, fontweight="bold")
rbox(ax, 75, 7, 20, 4, fc=C3, ec=C3); t(ax, 85, 9, "Confirm ✓", 6.3, "white", ha="center", va="center", fontweight="bold")
for x in [29, 64]: ax.add_patch(FancyArrowPatch((x, 27), (x + 7, 27), arrowstyle="-|>", mutation_scale=12, color=MUTED, lw=1.5))
t(ax, 32.5, 29.5, "tap", 6, MUTED, ha="center"); t(ax, 67.5, 29.5, "verified", 6, MUTED, ha="center")
save(fig, "s6_zerologin.png")

# ---------- S7 GTM command centre ----------
fig, ax = screen("GTM Command Centre (internal NivoTime view)", "Segments · ICP scoring · pipeline", H=70)
ax.set_ylim(0, 70)
rbox(ax, 2, 35, 47, 27); t(ax, 4, 59, "Market segment explorer", 7, INK, fontweight="bold")
seg = [("Broker TAM: licensed brokers", 751, 751), ("Broker SAM: mid-size, group-health book", 600, 751), ("Named ABM list (Year 1)", 100, 751),
       ("Broker SOM: signed by Year 3 (base)", 15, 751)]
for i, (n, v, m) in enumerate(seg):
    y = 54 - i * 5; t(ax, 4, y + 1.3, n, 5.5, INK2)
    ax.add_patch(Rectangle((4, y - 1.3), 36 * v / m, 1.8, fc=C1 if i < 3 else C3)); t(ax, 4 + 36 * v / m + 0.8, y - 0.4, f"{v}", 5.8, INK, va="center", fontweight="bold")
t(ax, 4, 36.5, "Employer path: 7.66 lakh EPFO establishments → 150 named → 18 by Y3", 5.4, MUTED)
rbox(ax, 51, 35, 47, 27); t(ax, 53, 59, "Pipeline by stage (Year 1 plan)", 7, INK, fontweight="bold")
stg = ["Targeted", "Meeting", "Demo", "Pilot", "Won"]; bv = [100, 30, 18, 6, 3]; ev = [150, 30, 15, 6, 4]
for i, s_ in enumerate(stg):
    x = 55 + i * 8.5; hb = bv[i] / 150 * 17; he = ev[i] / 150 * 17
    ax.add_patch(Rectangle((x, 39), 3.2, hb, fc=C1)); ax.add_patch(Rectangle((x + 3.5, 39), 3.2, he, fc=C2))
    t(ax, x + 1.6, 39 + hb + 0.6, str(bv[i]), 5, INK, ha="center"); t(ax, x + 5.1, 39 + he + 0.6, str(ev[i]), 5, INK, ha="center")
    t(ax, x + 3.3, 37, s_, 5.3, INK2, ha="center")
ax.add_patch(Rectangle((76, 56.5), 2, 1.3, fc=C1)); t(ax, 78.5, 57.1, "Brokers", 5.3, INK2, va="center")
ax.add_patch(Rectangle((85, 56.5), 2, 1.3, fc=C2)); t(ax, 87.5, 57.1, "Employers", 5.3, INK2, va="center")
rbox(ax, 2, 2, 96, 31); t(ax, 4, 30, "ICP-scored target accounts (anonymised sample)", 7, INK, fontweight="bold")
cols = ["Account", "Type", "GH clients", "In-house tech", "Trigger event", "ICP score", "Owner", "Next step"]
cx = [4, 16, 25, 37, 47, 65, 75, 84]
for j, c in enumerate(cols): t(ax, cx[j], 26.5, c, 5.4, MUTED, fontweight="bold")
acc = [("Broker 017", "Composite", "42", "None", "Lost client to tech-first broker", 91, "Founder", "Intro call"),
       ("Broker 052", "Direct", "28", "Excel only", "New digital head hired", 84, "Sales", "Health check"),
       ("Broker 103", "Direct", "35", "Partial", "Licence conversion 2026", 72, "Sales", "Webinar invite"),
       ("Employer 211", "IT, 640 staff", "—", "—", "Renewal in 4 months", 78, "Inside sales", "Benchmark snapshot"),
       ("Broker 144", "Composite", "12", "Bharatsure user", "—", 38, "—", "Deprioritise")]
for i, r in enumerate(acc):
    y = 22.5 - i * 4.2
    for j, v in enumerate(r):
        if j == 5:
            col = C3 if v >= 80 else (C1 if v >= 60 else MUTED)
            ax.add_patch(Rectangle((cx[j], y - 0.8), 6 * v / 100, 1.6, fc=col)); t(ax, cx[j] + 6.5, y, str(v), 5.5, INK, va="center")
        else: t(ax, cx[j], y, v, 5.6, INK, va="center")
save(fig, "s7_gtm.png")

# ---------- S8 Financial scenario simulator ----------
fig, ax = screen("Business Case Simulator (internal)", "Illustrative model · assumptions A1–A14", H=66)
rbox(ax, 2, 3, 25, 55); t(ax, 4, 55, "Drivers", 7, INK, fontweight="bold")
dv = [("Brokers by Year 3", "15", 0.5), ("Direct employers by Y3", "18", 0.5), ("Broker subscription", "₹1.8 L", 0.5), ("Per-account fee", "₹5,000", 0.5),
      ("Incremental cost index", "100%", 0.5), ("Advisory attach rate", "30%", 0.4)]
for i, (a, b, f) in enumerate(dv):
    y = 49 - i * 7.3; t(ax, 4, y, a, 5.8, INK2); t(ax, 25, y, b, 5.9, INK, ha="right", fontweight="bold")
    ax.add_patch(Rectangle((4, y - 3), 21, 0.8, fc="#DADDE6")); ax.add_patch(Rectangle((4, y - 3), 21 * f, 0.8, fc=C1))
    ax.add_patch(Circle((4 + 21 * f, y - 2.6), 0.9, fc="white", ec=C1, lw=1.2))
base = M["res"]["Base"]
kpi(ax, 29, 47, 22, 11, "Year-3 revenue", f"₹{base[2]['revenue'] / 1e5:.1f} L", "base case")
kpi(ax, 52.5, 47, 22, 11, "Year-3 operating result", f"+₹{base[2]['ebitda'] / 1e5:.1f} L", "break-even year: 3", C3)
kpi(ax, 76, 47, 22, 11, "LTV : CAC (broker)", f"{M['ltv_cac']:.1f}x", "excl. founder time")
rbox(ax, 29, 3, 40, 42); t(ax, 31, 42, "Revenue vs incremental cost (₹ lakh)", 6.8, INK, fontweight="bold")
ox, oy, sx, sy = 34, 8, 13, 28 / 110
for i, r in enumerate(base):
    x = ox + i * sx
    ax.add_patch(Rectangle((x, oy), 4.5, r["revenue"] / 1e5 * sy, fc=C1)); ax.add_patch(Rectangle((x + 4.8, oy), 4.5, r["cost"] / 1e5 * sy, fc="#C9CCD6"))
    t(ax, x + 2.25, oy + r["revenue"] / 1e5 * sy + 0.8, f"{r['revenue'] / 1e5:.0f}", 5.3, INK, ha="center")
    t(ax, x + 7.05, oy + r["cost"] / 1e5 * sy + 0.8, f"{r['cost'] / 1e5:.0f}", 5.3, INK, ha="center")
    t(ax, x + 4.6, oy - 2.5, f"Year {i + 1}", 5.5, INK2, ha="center")
ax.plot([ox - 1, ox + 35], [oy, oy], color=GRID, lw=0.8)
ax.add_patch(Rectangle((52, 38.5), 1.8, 1.2, fc=C1)); t(ax, 54.2, 39.1, "Revenue", 5.2, INK2, va="center")
ax.add_patch(Rectangle((61, 38.5), 1.8, 1.2, fc="#C9CCD6")); t(ax, 63.2, 39.1, "Cost", 5.2, INK2, va="center")
rbox(ax, 71, 3, 27, 42); t(ax, 73, 42, "Sensitivity: Year-3 result", 6.8, INK, fontweight="bold")
sens = [("30% fewer brokers", -22.5), ("Costs +20%", -13.4), ("No advisory", -11.6), ("Prices −20%", -5.7), ("Prices +20%", 18.4), ("Costs −20%", 26.2)]
cxz = 84.5; sc = 12 / 30
ax.plot([cxz, cxz], [6, 38], color=INK2, lw=0.8); t(ax, cxz, 4.2, "base +6.4", 5, MUTED, ha="center")
for i, (n, v) in enumerate(sens):
    y = 35 - i * 5.2
    ax.add_patch(Rectangle((cxz, y - 1), v * sc, 2, fc=C2 if v < 0 else C3))
    t(ax, 72.5, y + 2.2, n, 5.2, INK2); t(ax, cxz + v * sc + (0.6 if v > 0 else -0.6), y, f"{v:+.1f}", 5.2, INK, va="center", ha="left" if v > 0 else "right")
save(fig, "s8_bizsim.png")

# ---------- S9 Admin & model monitoring ----------
fig, ax = screen("Admin — Data Ingestion & Model Monitoring", "Governance view")
nav(ax, NAV, "Admin")
kpi(ax, 15, 48, 20, 10, "Quote extraction accuracy", "96.4%", "target ≥95%", C3)
kpi(ax, 36.5, 48, 20, 10, "Fields sent to human review", "7.8%", "low-confidence fields")
kpi(ax, 58, 48, 20, 10, "Forecast error (MAE)", f"{S['forecast']['mae_pp']} pts", "target ≤5 pts", C3)
kpi(ax, 79.5, 48, 18.5, 10, "Cohorts below k=10", "3", "hidden from users", C2)
rbox(ax, 15, 3, 42, 43); t(ax, 17, 43, "Extraction accuracy by week", 6.8, INK, fontweight="bold")
wk = np.arange(10); acc_ = [91.2, 92.5, 93.1, 94.0, 94.6, 95.2, 95.8, 96.0, 96.1, 96.4]
ox, oy, sx = 19, 8, 34 / 9; sy = 30 / 10
ax.plot([ox, ox + 34], [oy + (95 - 88) * sy, oy + (95 - 88) * sy], color=MUTED, ls="--", lw=0.8); t(ax, ox + 34, oy + 7 * sy + 1, "95% target", 5, MUTED, ha="right")
ax.plot(ox + wk * sx, oy + (np.array(acc_) - 88) * sy, color=C1, lw=1.6, marker="o", ms=2.5)
ax.plot([ox, ox + 34], [oy, oy], color=GRID, lw=0.8)
for i in range(0, 10, 3): t(ax, ox + i * sx, oy - 2.5, f"W{i + 1}", 5, MUTED, ha="center")
rbox(ax, 59, 3, 39, 43); t(ax, 61, 43, "Data pipeline status", 6.8, INK, fontweight="bold")
pl = [("Census upload — Acme Tech", "Mapped 14/14 columns", C3), ("Claims file — Orbit Pharma", "2 date formats fixed", C3),
      ("Quotes — Nimbus BFSI (5)", "2 fields need review", C2), ("Consent tags", "100% records tagged", C3),
      ("Benchmark pool refresh", "Scheduled Sun 02:00", C1), ("Audit log export", "Ready (DPDP)", C3)]
for i, (a, b, c) in enumerate(pl):
    y = 38 - i * 5.8; ax.add_patch(Circle((62, y), 0.8, fc=c)); t(ax, 64, y + 0.9, a, 5.8, INK, va="center"); t(ax, 64, y - 1.6, b, 5.2, MUTED, va="center")
save(fig, "s9_admin.png")

# ---------- D1 sitemap ----------
fig, ax = plt.subplots(figsize=(7.0, 3.9)); ax.set_xlim(0, 100); ax.set_ylim(0, 56); ax.axis("off")
def node(x, y, w, h, s, fc, tc="white", fs=6.2, bold=True):
    rbox(ax, x, y, w, h, fc=fc, ec=fc, r=0.8); t(ax, x + w / 2, y + h / 2, s, fs, tc, ha="center", va="center", fontweight="bold" if bold else "normal")
node(33, 49, 34, 5, "NivoTime Suite (single sign-on)", P, fs=6)
apps = [("Broker Workspace", 2, ["Portfolio home", "Benchmarking Cockpit", "Quote & Renewal Desk", "AI Simulation Lab", "Advisory packs"]),
        ("HR / CFO Portal", 22, ["Benchmark snapshot", "Renewal forecast", "Engagement report", "Vendor SLAs"]),
        ("Employee app", 42, ["Nudges (WhatsApp/email)", "Secure deep links", "Add dependants", "Policy Q&A assistant"]),
        ("Vendor / TPA", 62, ["SLA updates", "Tickets", "Scorecard"]),
        ("NivoTime internal", 82, ["GTM Command Centre", "Business simulator", "Admin & ingestion", "Model monitoring"])]
for name, x, kids in apps:
    node(x, 39, 16, 5, name, C1 if x < 80 else C4, fs=5.4)
    ax.plot([50, x + 8], [49, 44], color=MUTED, lw=0.7)
    for i, k in enumerate(kids):
        y = 32 - i * 6.2; node(x, y, 16, 4.6, k, LIGHTP if x < 80 else "#F5E7F2", tc=INK, fs=5.3, bold=False)
        ax.plot([x + 1, x + 1], [39, y + 2.3], color=GRID, lw=0.7)
t(ax, 0, 55, "Information architecture (sitemap)", 9, INK, fontweight="bold")
fig.savefig(OUT + "d1_sitemap.png"); plt.close(fig)

# ---------- D2 renewal swimlane ----------
fig, ax = plt.subplots(figsize=(7.0, 4.0)); ax.set_xlim(0, 100); ax.set_ylim(0, 58); ax.axis("off")
lanes = [("HR client", "#F4F5F8"), ("Broker account manager", LIGHTP), ("NivoTime platform", "#EEF0FA"), ("AI / ML layer", LIGHTG)]
for i, (n, c) in enumerate(lanes):
    y = 42 - i * 12; ax.add_patch(Rectangle((0, y), 100, 11.5, fc=c, ec="white")); t(ax, 1, y + 5.75, n.replace(" account manager", "\naccount manager").replace(" platform", "\nplatform"), 6, INK, fontweight="bold", va="center")
steps = [(0, 26, "x"), (1, 26, "Request data\n& quotes"), (0, 39, "Upload census\n& claims"), (2, 39, "Validate &\nmap data"),
         (3, 52, "Forecast renewal\n+ benchmark"), (1, 52, "Upload 5\ninsurer quotes"), (3, 65, "Extract &\nnormalise quotes"),
         (1, 65, "Review low-\nconfidence fields"), (3, 78, "Simulate plan\nchanges"), (1, 78, "Choose scenario,\nbuild pack"), (0, 91, "Decide & approve\n(decision log)")]
# lane index mapping: 0 HR,1 broker,2 platform,3 AI  -> y centres
yc = {0: 47.75, 1: 35.75, 2: 23.75, 3: 11.75}
steps[0] = (2, 26, "T-90: renewal\nalert raised")
pos = []
for ln, x, s_ in steps:
    rbox(ax, x - 5.7, yc[ln] - 4, 11.4, 8, fc="white", ec=P, r=0.8); t(ax, x, yc[ln], s_, 5.0, INK, ha="center", va="center"); pos.append((x, yc[ln]))
order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for a, b in zip(order[:-1], order[1:]):
    (x1, y1), (x2, y2) = pos[a], pos[b]
    ax.add_patch(FancyArrowPatch((x1 + (5.7 if x2 > x1 else 0), y1 - (0 if x2 > x1 else (4 if y2 < y1 else -4))),
                                 (x2 - (5.7 if x2 > x1 else 0), y2 + (0 if x2 > x1 else (4 if y2 < y1 else -4))),
                                 arrowstyle="-|>", mutation_scale=8, color=MUTED, lw=0.9, connectionstyle="arc3,rad=0"))
t(ax, 0, 56, "Core user journey: renewal preparation (target: renewal pack in hours, not weeks)", 8.5, INK, fontweight="bold")
fig.savefig(OUT + "d2_renewal_flow.png"); plt.close(fig)

# ---------- D3 quote extraction pipeline ----------
fig, ax = plt.subplots(figsize=(7.0, 2.3)); ax.set_xlim(0, 100); ax.set_ylim(0, 30); ax.axis("off")
st = [("Upload", "PDF / Excel /\nemail attachment"), ("OCR", "Text + table\nlayout"), ("LLM extraction", "Fill fixed schema\n(24 fields)"),
      ("Validate", "Rules + confidence\nscore per field"), ("Human review", "Only fields with\nconfidence < 0.85"), ("Normalise", "Units, limits,\nterm codes"), ("Compare", "Grid + flags +\nvalue score")]
for i, (a, b) in enumerate(st):
    x = 1 + i * 14.1; rbox(ax, x, 13, 12.5, 7, fc=P if i != 4 else C2, ec=P if i != 4 else C2)
    t(ax, x + 6.25, 16.5, a, 6.2, "white", ha="center", va="center", fontweight="bold"); t(ax, x + 6.25, 10.5, b, 5.2, INK2, ha="center", va="top", linespacing=1.3)
    if i < 6: ax.add_patch(FancyArrowPatch((x + 12.6, 16.5), (x + 14.0, 16.5), arrowstyle="-|>", mutation_scale=8, color=G, lw=1.3))
t(ax, 1, 27, "Quote document AI pipeline (Module 2)", 8.5, INK, fontweight="bold")
fig.savefig(OUT + "d3_quote_pipeline.png"); plt.close(fig)

# ---------- D4 zero-login flow ----------
fig, ax = plt.subplots(figsize=(7.0, 2.4)); ax.set_xlim(0, 100); ax.set_ylim(0, 32); ax.axis("off")
st = ["Event\n(renewal, new hire,\nunused benefit)", "Rule engine\n(who, when,\nfrequency cap)", "Channel\n(WhatsApp, email,\npush)", "Secure deep link\n(signed, 72-h expiry)",
      "Sensitive?\nYes → OTP login\nNo → direct action", "Action done\n(logged)", "HR sees\naggregated\nengagement"]
for i, s_ in enumerate(st):
    x = 1 + i * 14.1; rbox(ax, x, 8, 12.5, 14, fc=LIGHTG if i != 4 else "#FBEBD9", ec=G if i != 4 else C2)
    t(ax, x + 6.25, 15, s_, 5.4, INK, ha="center", va="center", linespacing=1.3)
    if i < 6: ax.add_patch(FancyArrowPatch((x + 12.6, 15), (x + 14.0, 15), arrowstyle="-|>", mutation_scale=8, color=P, lw=1.3))
t(ax, 1, 29, "Zero-login engagement flow (Module 4)", 8.5, INK, fontweight="bold")
fig.savefig(OUT + "d4_zerologin_flow.png"); plt.close(fig)

# ---------- D5 ER model ----------
fig, ax = plt.subplots(figsize=(7.0, 4.2)); ax.set_xlim(0, 100); ax.set_ylim(0, 60); ax.axis("off")
ent = {"Broker": (2, 44, ["broker_id", "name, licence_no", "white_label_theme"]),
       "EmployerAccount": (27, 44, ["account_id, broker_id", "industry, employees", "city, renewal_date"]),
       "Policy": (52, 44, ["policy_id, account_id", "insurer_id, tpa_id", "start, end, premium"]),
       "PlanDesign": (77, 44, ["policy_id", "sum_insured, family_def", "co-pay, room_rent, limits"]),
       "Member": (27, 24, ["member_id, account_id", "relation, age_band", "consent_flags"]),
       "Claim": (52, 24, ["claim_id, member_id", "amount, LOS, diagnosis_grp", "status, tat_minutes"]),
       "Quote / QuoteTerm": (77, 24, ["quote_id, policy_id", "field, value, confidence", "reviewed_by"]),
       "Vendor / SLAEvent": (2, 24, ["vendor_id, type", "sla_type, minutes", "ticket_id, status"]),
       "BenchmarkCohort": (2, 4, ["cohort_id, filters", "n_companies (≥10)", "percentiles"]),
       "Nudge": (27, 4, ["nudge_id, member_id", "event, channel", "sent, actioned"]),
       "ModelRun": (52, 4, ["run_id, model, version", "inputs_hash, output", "reviewer, override"]),
       "AuditLog": (77, 4, ["event_id, user_id", "action, object", "timestamp"])}
for n, (x, y, f) in ent.items():
    rbox(ax, x, y, 21, 12.5, fc="white", ec=P, r=0.6); ax.add_patch(Rectangle((x, y + 9), 21, 3.5, fc=P))
    t(ax, x + 10.5, y + 10.75, n, 6, "white", ha="center", va="center", fontweight="bold")
    for i, fl in enumerate(f): t(ax, x + 1, y + 7 - i * 2.4, fl, 5.1, INK2, va="center")
links = [((23, 50), (27, 50)), ((48, 50), (52, 50)), ((73, 50), (77, 50)), ((37, 44), (37, 36.5)), ((48, 30), (52, 30)), ((73, 30), (77, 30)),
         ((62, 44), (62, 36.5)), ((12, 36.5), (52, 44)), ((37, 24), (37, 16.5))]
for (a, b) in links: ax.plot([a[0], b[0]], [a[1], b[1]], color=MUTED, lw=0.8)
t(ax, 0, 59, "Core data model (entity relationship, simplified)", 8.5, INK, fontweight="bold")
fig.savefig(OUT + "d5_datamodel.png"); plt.close(fig)

# ---------- D6 prototype sprint plan ----------
fig, ax = plt.subplots(figsize=(6.6, 3.0))
tasks = [("S0  Design system, clickable Figma flows", 0, 2, P), ("S1  Synthetic data + data model", 1, 2, C1),
         ("S2  Benchmarking Cockpit + peer engine", 2, 2, C1), ("S3  Quote Desk (upload, extract, compare)", 4, 2, C1),
         ("S4  AI Simulation Lab + forecast model", 5, 2, C1), ("S5  Portfolio home, vendor/TPA, nudges", 6, 2, C1),
         ("S6  GTM Command Centre + business simulator", 7, 2, C2), ("S7  Hardening, security, pilot demo", 9, 1, C3)]
for i, (n, s_, d, c) in enumerate(tasks[::-1]):
    ax.barh(i, d, left=s_, color=c, height=0.55); ax.text(-0.1, i, n, ha="right", va="center", fontsize=7, color=INK)
ax.set_yticks([]); ax.set_xlim(0, 10); ax.set_xticks(range(0, 11, 2)); ax.set_xticklabels([f"Wk {k * 4}" for k in range(6)], fontsize=7)
for s in ["top", "right", "left"]: ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRID); ax.tick_params(length=0)
ax.set_title("Prototype build plan (two-week sprints, 20 weeks)", loc="left", fontsize=9, fontweight="bold", color=INK)
fig.savefig(OUT + "d6_sprints.png"); plt.close(fig)
print("figs done")
