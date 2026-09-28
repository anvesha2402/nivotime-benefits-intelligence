import json, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch, Circle
import numpy as np

P = "#3B3A73"   # brand purple (diagrams)
G = "#87B549"   # brand green (diagrams)
# validated categorical palette for data series
C1, C2, C3, C4 = "#5553B5", "#E08A2E", "#3F8A3A", "#A7479A"
INK, INK2, MUTED, GRID, SURF = "#1F2130", "#4A4D5E", "#8A8FA3", "#E4E6EC", "#FFFFFF"
LIGHTP, LIGHTG = "#ECEBF7", "#EEF6E4"

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": GRID,
    "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2, "axes.titleweight": "bold",
    "axes.titlesize": 11, "axes.titlecolor": INK, "figure.dpi": 200, "savefig.bbox": "tight",
    "savefig.pad_inches": 0.12})
OUT = "/home/claude/nivotime/final/fig/"
M = json.load(open("/home/claude/nivotime/final/model.json"))

def clean(ax, grid_y=True):
    for s in ["top", "right", "left"]: ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    if grid_y:
        ax.yaxis.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
    ax.tick_params(length=0)

def box(ax, x, y, w, h, text, fc, ec=None, tc=INK, fs=8, bold=False, r=0.02):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                 fc=fc, ec=ec or fc, lw=1))
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fs, color=tc,
            fontweight="bold" if bold else "normal", wrap=True)

def arrow(ax, x1, y1, x2, y2, c=MUTED, lw=1.2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=9, color=c, lw=lw))

# ---------- F1 group health premium ----------
fig, ax = plt.subplots(figsize=(6.4, 2.9))
yrs = ["FY24", "FY25", "FY26"]; vals = [55020, 60809, 68641]
b = ax.bar(yrs, vals, width=0.5, color=C1)
for i, v in enumerate(vals):
    ax.text(i, v + 1200, f"₹{v:,} cr", ha="center", color=INK, fontsize=9, fontweight="bold")
ax.text(1, 30000, "+10.5%", ha="center", color="white", fontsize=9)
ax.text(2, 30000, "+12.9%", ha="center", color="white", fontsize=9)
ax.set_ylim(0, 80000); ax.set_yticks([0, 20000, 40000, 60000, 80000])
ax.set_yticklabels(["0", "20k", "40k", "60k", "80k"])
ax.set_title("Group health insurance premium in India (₹ crore)", loc="left")
clean(ax)
ax.text(0, -0.2, "Source: CareEdge Ratings (Apr 2026), industry premium data. Group business ≈ half of all health premium.",
        transform=ax.transAxes, fontsize=7, color=MUTED)
fig.savefig(OUT + "f1_market.png"); plt.close(fig)

# ---------- F2 strategic group map ----------
fig, ax = plt.subplots(figsize=(6.4, 4.2))
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
ax.axvline(5, color=GRID, lw=1); ax.axhline(5, color=GRID, lw=1)
pts = [("Bharatsure", 2.2, 7.4, C1), ("Turtlefin", 2.0, 3.2, C1), ("NivoTime\n(today)", 3.4, 6.2, C2),
       ("Plum", 8.3, 8.4, C4), ("Pazcare", 7.4, 7.6, C4), ("Loop Health", 8.6, 6.8, C4),
       ("Onsurity", 7.6, 3.0, C4), ("Nova Benefits", 6.6, 4.0, C4),
       ("Prudent\n(BenchmarkPro, in-house)", 6.2, 8.9, C3), ("Aon / Marsh\n(proprietary)", 9.1, 9.3, C3)]
for n, x, y, c in pts:
    ax.scatter(x, y, s=90, color=c, edgecolor="white", linewidth=1.5, zorder=3)
    ax.text(x + 0.22, y, n, va="center", fontsize=7.5, color=INK)
ax.annotate("", xy=(2.9, 8.8), xytext=(3.35, 6.55), arrowprops=dict(arrowstyle="-|>", color=C2, lw=1.4, ls="--"))
ax.text(1.1, 9.3, "Target: AI benefits intelligence\nfor mid-size brokers", fontsize=7.5, color=C2, fontweight="bold")
ax.set_xticks([]); ax.set_yticks([])
ax.set_xlabel("Sells technology to intermediaries  ←→  Is itself the intermediary / broker", fontsize=8)
ax.set_ylabel("Narrow module  ←→  Full benefits + intelligence stack", fontsize=8)
for s in ax.spines.values(): s.set_color(GRID)
ax.set_title("Strategic group map: where NivoTime can win", loc="left")
handles = [plt.Line2D([], [], marker="o", ls="", color=c, label=l, markersize=7) for c, l in
           [(C1, "Tech vendors to intermediaries"), (C4, "Tech-enabled brokers/agents"), (C3, "Large brokers (build own)"), (C2, "NivoTime")]]
ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.2), ncol=4, fontsize=7, frameon=False)
fig.savefig(OUT + "f2_groupmap.png"); plt.close(fig)

# ---------- F3 platform architecture ----------
fig, ax = plt.subplots(figsize=(6.6, 5.0)); ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
ax.text(0, 9.7, "NivoTime Benefits Intelligence Suite — proposed architecture", fontsize=11, fontweight="bold", color=INK)
# users
users = ["Broker workspace\n(white-label)", "HR / CFO\ndashboard", "Employee\n(zero-login)", "Vendor / TPA\nportal"]
for i, u in enumerate(users):
    box(ax, 0.1 + i*2.5, 8.2, 2.25, 1.0, u, P, tc="white", fs=7.5, bold=True)
# modules
mods = ["Benchmarking\nCockpit", "Quote &\nRenewal Desk", "Vendor / TPA\nManagement", "Engagement\nEngine", "Advisory &\nConsulting"]
for i, m in enumerate(mods):
    box(ax, 0.1 + i*2.0, 6.55, 1.8, 1.1, m, LIGHTP, ec=P, fs=7.2, bold=True)
ax.text(4.1, 7.78, "MODULES", fontsize=6.5, color=MUTED, fontweight="bold")
# AI layer
box(ax, 0.1, 4.75, 9.8, 1.25, "", LIGHTG, ec=G)
ax.text(0.25, 5.8, "AI / ML LAYER", fontsize=6.5, color="#4F7A22", fontweight="bold")
ai = ["Peer-group\nmatching (k-NN)", "Renewal cost\nforecast (GBM)", "Plan-design\nsimulator", "Quote document\nAI (OCR + LLM)", "Claims anomaly\ndetection", "Policy Q&A\nassistant (RAG)"]
for i, a in enumerate(ai):
    box(ax, 0.25 + i*1.6, 4.88, 1.5, 0.82, a, "white", ec=G, fs=6.4)
# data layer
box(ax, 0.1, 3.05, 9.8, 1.2, "", "#F4F5F8", ec=GRID)
ax.text(0.25, 4.02, "DATA LAYER  (consent-tagged, anonymised benchmark pool, min. cohort size 10)", fontsize=6.5, color=INK2, fontweight="bold")
dl = ["Employer &\nemployee master", "Policy & plan\ndesign data", "Claims &\nutilisation", "Quotes &\nrenewal history", "Vendor SLAs\n& tickets"]
for i, d in enumerate(dl):
    box(ax, 0.25 + i*1.93, 3.15, 1.8, 0.75, d, "white", ec=GRID, fs=6.4)
# integrations
ints = ["Insurers", "TPAs", "HRMS / payroll", "Wellness\nvendors", "Bima Sugam\n(future)"]
for i, t in enumerate(ints):
    box(ax, 0.1 + i*1.98, 1.6, 1.8, 0.8, t, "white", ec=P, fs=6.8)
ax.text(0.1, 2.55, "INTEGRATIONS (API-first)", fontsize=6.5, color=MUTED, fontweight="bold")
box(ax, 0.1, 0.2, 9.8, 0.9, "Security & governance: role-based access · audit trail · encryption\nDPDP consent & retention · human review of every AI output",
    P, tc="white", fs=7)
for x in [1.2, 3.7, 6.2, 8.7]: arrow(ax, x, 8.2, x, 7.7, c=P)
arrow(ax, 5, 6.55, 5, 6.02, c=G); arrow(ax, 5, 4.75, 5, 4.27, c=MUTED); arrow(ax, 5, 2.42, 5, 3.03, c=MUTED)
fig.savefig(OUT + "f3_architecture.png"); plt.close(fig)

# ---------- F4 dashboard mockup: Benchmarking Cockpit ----------
fig = plt.figure(figsize=(7.0, 4.6)); fig.patch.set_facecolor("#F4F5F8")
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(0, 66); ax.axis("off")
ax.add_patch(Rectangle((0, 60), 100, 6, fc=P))
ax.text(2, 63, "NivoTime  |  Benefits Benchmarking Cockpit", color="white", fontsize=9, fontweight="bold", va="center")
ax.text(98, 63, "Client: Acme Tech Pvt Ltd (sample)  ·  Renewal in 74 days", color="white", fontsize=6.5, va="center", ha="right")
filters = [("Industry", "IT services"), ("Company size", "500–1,000"), ("Family cover", "E+S+2C"),
           ("Sum insured", "₹5 lakh"), ("Co-pay", "0%"), ("Peer set", "42 companies")]
for i, (k, v) in enumerate(filters):
    x = 2 + i*16.2
    ax.add_patch(FancyBboxPatch((x, 52.5), 15, 5.5, boxstyle="round,pad=0,rounding_size=0.8", fc="white", ec=GRID))
    ax.text(x + 1, 56.3, k, fontsize=5.5, color=MUTED); ax.text(x + 1, 53.9, v + "  ▾", fontsize=7, color=INK, fontweight="bold")
kpis = [("Premium / life", "₹2,410", "58th pct"), ("Claims ratio (ICR)", "92%", "Peer median 81%"),
        ("Expected renewal load", "+14.2%", "Range 11–17%"), ("Employee engagement", "38%", "Peer median 46%")]
for i, (k, v, s) in enumerate(kpis):
    x = 2 + i*24.3
    ax.add_patch(FancyBboxPatch((x, 40.5), 23, 10.5, boxstyle="round,pad=0,rounding_size=0.8", fc="white", ec=GRID))
    ax.text(x + 1.5, 48.5, k, fontsize=6, color=MUTED); ax.text(x + 1.5, 44.6, v, fontsize=12, color=INK, fontweight="bold")
    ax.text(x + 1.5, 42.0, s, fontsize=6, color=C2 if i in (1, 2, 3) else INK2)
# chart panel: benchmark percentile bars
ax.add_patch(FancyBboxPatch((2, 3), 56, 36, boxstyle="round,pad=0,rounding_size=0.8", fc="white", ec=GRID))
ax.text(4, 36.3, "Where you sit vs. peers (percentile)", fontsize=7, color=INK, fontweight="bold")
items = [("Sum insured", 45), ("Parental cover", 30), ("Maternity limit", 62), ("Room-rent cap", 71), ("OPD / wellness", 22), ("Premium per life", 58)]
for i, (n, p) in enumerate(items):
    y = 31 - i*4.6
    ax.text(4, y, n, fontsize=6.3, color=INK2, va="center")
    ax.add_patch(Rectangle((19, y - 0.9), 34, 1.8, fc="#EEF0F4", ec="none"))
    ax.add_patch(Rectangle((19, y - 0.9), 34*p/100, 1.8, fc=C1, ec="none"))
    ax.plot([19 + 17, 19 + 17], [y - 1.4, y + 1.4], color=INK2, lw=0.8)
    ax.text(54.2, y, f"{p}", fontsize=6.3, va="center", color=INK, fontweight="bold")
ax.text(36, 4.5, "│ peer median", fontsize=5.5, color=MUTED)
# AI insight panel
ax.add_patch(FancyBboxPatch((60, 3), 38, 36, boxstyle="round,pad=0,rounding_size=0.8", fc=LIGHTG, ec=G))
ax.text(62, 36.3, "AI renewal insights", fontsize=7.5, color="#3E6A18", fontweight="bold")
ins = ["1. Claims ratio is 11 pts above peers; 64% of\n    claim value from parents' cover.",
       "2. Scenario: 10% co-pay on parents only →\n    est. premium −6.8% (±2%), 3% of lives affected.",
       "3. OPD/wellness is in the bottom quartile —\n    low-cost add-on could lift engagement.",
       "4. 3 of 5 quotes exclude modern treatments;\n    flagged in Quote Workspace."]
for i, t in enumerate(ins):
    ax.text(62, 31.5 - i*7.2, t, fontsize=6.1, color=INK, va="top", linespacing=1.35)
ax.text(62, 4.6, "Model outputs are estimates; broker reviews before sharing.", fontsize=5.2, color=INK2, style="italic")
fig.savefig(OUT + "f4_cockpit.png", facecolor=fig.get_facecolor()); plt.close(fig)

# ---------- F5 quote comparison mockup ----------
fig = plt.figure(figsize=(7.0, 3.9)); fig.patch.set_facecolor("#F4F5F8")
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(0, 56); ax.axis("off")
ax.add_patch(Rectangle((0, 50), 100, 6, fc=P))
ax.text(2, 53, "NivoTime  |  Quote & Renewal Workspace", color="white", fontsize=9, fontweight="bold", va="center")
ax.text(98, 53, "5 quotes uploaded (PDF/Excel) · auto-extracted · 2 fields need review", color="white", fontsize=6.5, va="center", ha="right")
cols = ["Term", "Expiring", "Insurer A", "Insurer B", "Insurer C", "Insurer D"]
rows = [["Premium (₹ lakh)", "38.2", "42.9", "41.1", "44.6", "40.3"],
        ["Sum insured", "₹5L", "₹5L", "₹5L", "₹5L", "₹5L"],
        ["Room-rent cap", "1%", "No cap", "1%", "No cap", "2%"],
        ["Parents co-pay", "0%", "10%", "0%", "0%", "20%"],
        ["Maternity limit", "₹75k", "₹75k", "₹50k", "₹1L", "₹75k"],
        ["Modern treatments", "Covered", "Covered", "Sub-limit", "Covered", "Excluded"],
        ["Waiting period (PED)", "Waived", "Waived", "Waived", "Waived", "Waived"],
        ["AI value score", "—", "82", "71", "88", "64"]]
colx = [2, 26, 40, 54, 68, 82]; w = 13.5
for j, c in enumerate(cols):
    ax.text(colx[j] + (0 if j == 0 else w/2), 46.5, c, fontsize=6.8, fontweight="bold", color=INK, ha="left" if j == 0 else "center")
flag = {(3, 2): C2, (3, 5): C2, (4, 3): C2, (5, 3): C2, (5, 5): C2, (2, 2): C3, (2, 4): C3, (4, 4): C3}
for i, r in enumerate(rows):
    y = 42 - i*4.7
    ax.add_patch(Rectangle((1, y - 2.1), 95, 4.2, fc="white" if i % 2 == 0 else "#FAFAFC", ec="none"))
    for j, v in enumerate(r):
        c = flag.get((i, j + 0))
        if c and j > 0:
            ax.add_patch(FancyBboxPatch((colx[j] + 1, y - 1.6), w - 2, 3.2, boxstyle="round,pad=0,rounding_size=0.6", fc="none", ec=c, lw=1.1))
        ax.text(colx[j] + (0 if j == 0 else w/2), y, v, fontsize=6.5, color=INK, ha="left" if j == 0 else "center", va="center",
                fontweight="bold" if i == 7 else "normal")
ax.add_patch(FancyBboxPatch((1, 1.2), 95, 4.2, boxstyle="round,pad=0,rounding_size=0.6", fc=LIGHTG, ec=G))
ax.text(3, 3.3, "Recommendation draft: Insurer C gives the widest cover (premium +16.8% vs expiring); Insurer B is cheapest like-for-like. Orange boxes = worse than expiring; green = better.",
        fontsize=6.2, color=INK, va="center")
fig.savefig(OUT + "f5_quotes.png", facecolor=fig.get_facecolor()); plt.close(fig)

# ---------- F6 GTM data flow ----------
fig, ax = plt.subplots(figsize=(6.8, 2.2)); ax.set_xlim(0, 12); ax.set_ylim(0.6, 4); ax.axis("off")
steps = [("Lead\nsources", "LinkedIn ABM\nfounder network\nbenchmark report"), ("CRM", "HubSpot or Zoho\none record\nper account"),
         ("Marketing\nautomation", "Email sequences\nnurture tracks\nlead scoring"), ("Sales", "Discovery, demo\npilot, proposal"),
         ("Customer\nsuccess", "Onboarding\nusage tracking\nrenewal health"), ("BI\ndashboard", "Power BI / Looker\npipeline, CAC,\nretention")]
for i, (t, d) in enumerate(steps):
    x = 0.05 + i*2.0
    box(ax, x, 2.2, 1.75, 1.1, t, P, tc="white", fs=7.5, bold=True)
    ax.text(x + 0.875, 1.75, d, ha="center", va="top", fontsize=6.3, color=INK2, linespacing=1.3)
    if i < 5: arrow(ax, x + 1.77, 2.75, x + 2.03, 2.75, c=G, lw=1.5)
ax.text(0.05, 3.7, "Recommended go-to-market data flow", fontsize=9.5, fontweight="bold", color=INK)
fig.savefig(OUT + "f6_dataflow.png"); plt.close(fig)

# ---------- F7 broker flywheel ----------
fig, ax = plt.subplots(figsize=(5.6, 5.0)); ax.set_xlim(-5.2, 5.2); ax.set_ylim(-5.0, 5.0); ax.axis("off"); ax.set_aspect("equal")
lab = ["More\nmid-size\nbrokers\nadopt", "More\nemployer\naccounts\nonboard", "Bigger\nanonymised\ndata pool", "Sharper\nbenchmarks\n& AI insight",
       "Stronger\nbroker pitch", "Brokers win\n& retain\naccounts"]
n = len(lab); R = 3.5
for i, l in enumerate(lab):
    a = np.pi/2 - i*2*np.pi/n
    x, y = R*np.cos(a), R*np.sin(a)
    ax.add_patch(Circle((x, y), 1.3, fc=P if i % 2 == 0 else G, ec="white", lw=2))
    ax.text(x, y, l, ha="center", va="center", fontsize=6.6, color="white", fontweight="bold")
    a2 = np.pi/2 - (i + 1)*2*np.pi/n
    am = (a + a2)/2
    ax.annotate("", xy=(R*np.cos(am - 0.18), R*np.sin(am - 0.18)), xytext=(R*np.cos(am + 0.18), R*np.sin(am + 0.18)),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.3, shrinkA=0, shrinkB=0))
ax.text(0, 0.25, "Data network\neffect", ha="center", va="center", fontsize=9, fontweight="bold", color=INK)
ax.text(0, -0.7, "the moat", ha="center", fontsize=7.5, color=MUTED)
fig.savefig(OUT + "f7_flywheel.png"); plt.close(fig)

# ---------- F8 roadmap gantt ----------
fig, ax = plt.subplots(figsize=(6.0, 3.6))
tasks = [("Feature audit, fix login security, CRM set-up", 0, 2, P), ("Named-account list (100 brokers + 150 employers)", 0, 3, P),
         ("Benchmarking Cockpit MVP (public + pilot data)", 2, 3, C1), ("Broker pilots ×2, employer pilots ×3", 3, 4, C2),
         ("Quote document AI + renewal workspace", 4, 4, C1), ("First case study + benchmark report", 6, 2, C2),
         ("Renewal-cost forecast model (needs claims data)", 7, 4, C1), ("Industry playbooks (IT, manufacturing)", 8, 4, C3),
         ("Scale broker channel; Bima Sugam readiness", 9, 3, C2)]
for i, (t, s, d, c) in enumerate(tasks[::-1]):
    ax.barh(i, d, left=s, color=c, height=0.55)
    ax.text(-0.15, i, t, ha="right", va="center", fontsize=7.8, color=INK)
ax.set_yticks([]); ax.set_xlim(0, 12); ax.set_xticks(range(0, 13, 3))
ax.set_xticklabels(["M0", "M3", "M6", "M9", "M12"])
for x in [3, 6]: ax.axvline(x, color=GRID, lw=0.8, ls="--")
ax.text(1.5, len(tasks) - 0.2, "Quick wins", ha="center", fontsize=7, color=MUTED)
ax.text(4.5, len(tasks) - 0.2, "Mid-term", ha="center", fontsize=7, color=MUTED)
ax.text(9, len(tasks) - 0.2, "Long-term", ha="center", fontsize=7, color=MUTED)
clean(ax, grid_y=False); ax.spines["bottom"].set_visible(True)
handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in [P, C1, C2, C3]]
ax.legend(handles, ["Foundation", "Product / AI build", "Commercial", "Expansion"], ncol=4, fontsize=6.8, frameon=False,
          loc="upper center", bbox_to_anchor=(0.3, -0.1))
ax.set_title("12-month roadmap", loc="left", pad=16)
fig.savefig(OUT + "f8_roadmap.png"); plt.close(fig)

# ---------- F9 scenarios ----------
fig, axs = plt.subplots(1, 3, figsize=(6.0, 3.0), sharey=True)
for k, (s, c) in enumerate([("Downside", C4), ("Base", C1), ("Upside", C3)]):
    rows = M["res"][s]; ax = axs[k]
    rev = [r["revenue"]/1e5 for r in rows]; cost = [r["cost"]/1e5 for r in rows]
    x = np.arange(3)
    ax.bar(x - 0.19, rev, 0.36, color=c, label="Revenue")
    ax.bar(x + 0.19, cost, 0.36, color="#C9CCD6", label="Incremental cost")
    for i, r in enumerate(rows):
        e = r["ebitda"]/1e5
        ax.text(i, max(rev[i], cost[i]) + 6, f"{e:+.0f}", ha="center", fontsize=7, color=INK, fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(["Y1", "Y2", "Y3"]); ax.set_title(s, fontsize=9, loc="left")
    clean(ax)
axs[0].set_ylabel("₹ lakh"); axs[0].set_ylim(0, 190)
axs[1].legend(fontsize=6.8, frameon=False, loc="upper left")
fig.suptitle("Illustrative 3-year scenarios (numbers above bars = operating profit, ₹ lakh)", x=0.02, ha="left", fontsize=9.5, fontweight="bold", color=INK)
fig.tight_layout()
fig.savefig(OUT + "f9_scenarios.png"); plt.close(fig)

# ---------- F10 risk heat map ----------
fig, ax = plt.subplots(figsize=(5.6, 3.9))
cmap = [["#F3F4F7", "#F7EEDF", "#F6E1C8"], ["#F7EEDF", "#F6E1C8", "#F2CFAA"], ["#F6E1C8", "#F2CFAA", "#EDB98A"]]
for i in range(3):
    for j in range(3):
        ax.add_patch(Rectangle((j, i), 1, 1, fc=cmap[i][j], ec="white", lw=2))
risks = [("R1 Benchmark cold start", 2.5, 2.55), ("R2 No proof points", 2.5, 2.2), ("R3 Brokers build own", 1.5, 2.55),
         ("R4 Regulatory boundary", 1.5, 1.5), ("R5 Data privacy breach", 0.5, 2.65), ("R6 Team stretched", 2.5, 1.5),
         ("R7 AI error in advice", 1.5, 1.75), ("R8 Bima Sugam delay", 1.5, 0.5)]
for n, x, y in risks:
    ax.scatter(x - 0.38, y, s=26, color=INK, zorder=3)
    ax.text(x - 0.3, y, n, fontsize=6.2, va="center", color=INK)
ax.set_xlim(0, 3); ax.set_ylim(0, 3)
ax.set_xticks([0.5, 1.5, 2.5]); ax.set_xticklabels(["Low", "Medium", "High"]); ax.set_xlabel("Likelihood")
ax.set_yticks([0.5, 1.5, 2.5]); ax.set_yticklabels(["Low", "Medium", "High"]); ax.set_ylabel("Impact")
for s in ax.spines.values(): s.set_visible(False)
ax.tick_params(length=0); ax.set_title("Risk heat map", loc="left")
fig.savefig(OUT + "f10_risk.png"); plt.close(fig)

# ---------- F11 broker funnel ----------
fig, ax = plt.subplots(figsize=(6.4, 3.1)); ax.axis("off"); ax.set_xlim(0, 10.6); ax.set_ylim(0, 6.4)
stg = [("Named mid-size brokers targeted", 100), ("Replied / first meeting", 30), ("Discovery + demo", 18),
       ("Pilot (90 days)", 6), ("Paid contract", 3)]
for i, (n, v) in enumerate(stg):
    w = 9.0*v/100 if v > 10 else 9.0*max(v, 3)/100 + 1.2
    w = [9.0, 6.6, 4.8, 3.0, 2.0][i]
    y = 5.0 - i*1.1
    ax.add_patch(FancyBboxPatch((5 - w/2, y), w, 0.85, boxstyle="round,pad=0,rounding_size=0.08", fc=C1 if i < 4 else C3, ec="white"))
    ax.text(5, y + 0.43, f"{v}", ha="center", va="center", fontsize=9, color="white", fontweight="bold")
    ax.text(5 + w/2 + 0.15, y + 0.43, n, va="center", fontsize=7, color=INK)
ax.text(0, 6.2, "Illustrative Year-1 broker funnel (assumed conversion rates; replace with CRM data)", fontsize=9, fontweight="bold", color=INK)
fig.savefig(OUT + "f11_funnel.png"); plt.close(fig)

# ---------- F12 journey ----------
fig, ax = plt.subplots(figsize=(6.8, 1.6)); ax.set_xlim(0, 12); ax.set_ylim(0.4, 3); ax.axis("off")
st = [("Contract", "Day 0"), ("Data upload\n& mapping", "Days 1–10"), ("White-label\nset-up", "Days 5–15"), ("Train broker\nteam", "Days 10–20"),
      ("First client\nlive", "Day 30"), ("First renewal\non platform", "Day 60–90")]
for i, (t, d) in enumerate(st):
    x = i*2.0
    ax.add_patch(FancyBboxPatch((x + 0.05, 1.1), 1.8, 1.2, boxstyle="round,pad=0,rounding_size=0.1", fc=P if i < 5 else G, ec="white"))
    ax.text(x + 0.95, 1.7, t, ha="center", va="center", fontsize=6.8, color="white", fontweight="bold")
    ax.text(x + 0.95, 0.75, d, ha="center", fontsize=6.5, color=INK2)
    if i < 5: arrow(ax, x + 1.86, 1.7, x + 2.04, 1.7, c=MUTED)
ax.text(0.05, 2.65, "Broker onboarding journey — target: time-to-first-value under 30 days", fontsize=9, fontweight="bold", color=INK)
fig.savefig(OUT + "f12_onboarding.png"); plt.close(fig)
print("done")
