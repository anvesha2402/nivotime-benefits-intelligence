"""
NivoTime Benefits Intelligence Suite — interactive prototype
==============================================================
A Streamlit prototype of the Benchmarking Cockpit / Simulation Lab / AI layer
proposed in the Live Company Project report and specified in the PRD
(prd/src/prd_part1.md–prd_part4.md).

IMPORTANT: every number here is computed live from a SYNTHETIC dataset,
calibrated to published aggregate statistics (IRDAI mean premium/life,
typical claims ratios) — not real NivoTime or client data, which was not
available for this project. Treat this as proof the mechanics work, not
proof of real-world accuracy. See prd/src/prd_part4.md, Appendix A.
"""

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import GradientBoostingRegressor, IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, precision_score, recall_score

st.set_page_config(
    page_title="NivoTime Benefits Intelligence Suite",
    page_icon="\U0001F4CA",
    layout="wide",
)

PURPLE = "#5553B5"
ORANGE = "#E08A2E"
GREEN = "#3F8A3A"
PINK = "#A7479A"
BRAND_PURPLE = "#3B3A73"
BRAND_GREEN = "#87B549"

# ----------------------------------------------------------------------
# 1. Synthetic data + model training (cached — computed once per session)
# ----------------------------------------------------------------------


@st.cache_data(show_spinner="Generating synthetic employer-group data...")
def generate_data(n: int = 600, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    ind = rng.choice(
        ["IT services", "Manufacturing", "BFSI", "Pharma", "Retail", "Prof. services"],
        n, p=[.28, .22, .16, .12, .12, .10],
    )
    age_base = {"IT services": 30, "Manufacturing": 37, "BFSI": 34, "Pharma": 35, "Retail": 31, "Prof. services": 33}
    avg_age = np.array([age_base[i] for i in ind]) + rng.normal(0, 2.5, n)
    emp = np.clip(np.exp(rng.normal(np.log(650), 0.6, n)), 250, 2000).astype(int)
    family = rng.choice(["E", "E+S+2C", "E+S+2C+P"], n, p=[.15, .50, .35])
    si = rng.choice([300000, 500000, 1000000], n, p=[.35, .45, .20])
    copay_par = np.where(family == "E+S+2C+P", rng.choice([0, 10, 20], n, p=[.45, .35, .20]), 0)
    room = rng.choice(["1%", "2%", "No cap"], n, p=[.45, .30, .25])
    tier = rng.choice(["Metro", "Tier 2"], n, p=[.7, .3])

    fam_f = {"E": 0.55, "E+S+2C": 1.0, "E+S+2C+P": 1.45}
    si_f = {300000: 0.85, 500000: 1.0, 1000000: 1.22}
    room_f = {"1%": 0.94, "2%": 1.0, "No cap": 1.07}
    age_f = np.exp((avg_age - 33) * 0.035)
    f_fam = np.array([fam_f[f] for f in family])
    f_si = np.array([si_f[s] for s in si])
    f_room = np.array([room_f[r] for r in room])
    f_cop = 1 - copay_par / 100 * 0.55 * (family == "E+S+2C+P")
    f_tier = np.where(tier == "Metro", 1.05, 0.92)
    prem = 2105 * age_f * f_fam * f_si * f_room * f_cop * f_tier * np.exp(rng.normal(0, 0.08, n))

    icr = (0.78 + 0.10 * (family == "E+S+2C+P") * (copay_par == 0) + 0.04 * (room == "No cap")
           + 0.004 * (avg_age - 33) + rng.normal(0, 0.12, n) * np.sqrt(650 / emp))
    icr = np.clip(icr, 0.35, 1.6)
    engagement = np.clip(rng.normal(0.44, 0.12, n), 0.1, 0.9)
    trend = 0.12
    cred = np.minimum(1, emp / 1000) ** 0.5
    renewal = (trend + cred * 0.55 * (icr - 0.80) + 0.02 * (family == "E+S+2C+P") + 0.015 * (room == "No cap")
               + 0.004 * (avg_age - 33) + 0.01 * (tier == "Metro") + rng.normal(0, 0.02, n))

    return pd.DataFrame(dict(
        industry=ind, employees=emp, avg_age=avg_age.round(1), family=family, sum_insured=si,
        copay_parents=copay_par, room_rent=room, city=tier, premium_per_life=prem.round(0),
        claims_ratio=icr.round(3), engagement=engagement.round(3), renewal_loading=renewal.round(4),
    ))


@st.cache_resource(show_spinner="Training the AI/ML layer...")
def train_models(df: pd.DataFrame):
    # Renewal forecast (Gradient Boosting)
    X = pd.get_dummies(df.drop(columns=["renewal_loading", "engagement", "premium_per_life"]), drop_first=False).astype(float)
    y = df["renewal_loading"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=7)
    gbm = GradientBoostingRegressor(n_estimators=300, max_depth=3, learning_rate=0.05, random_state=7).fit(Xtr, ytr)
    pred = gbm.predict(Xte)
    mae = mean_absolute_error(yte, pred) * 100
    mae_naive = mean_absolute_error(yte, np.full(len(yte), 0.12)) * 100
    within5 = float(np.mean(np.abs(yte - pred) <= 0.05) * 100)

    pi = permutation_importance(gbm, Xte, yte, n_repeats=10, random_state=7)
    imp = pd.Series(pi.importances_mean, index=X.columns)
    groups = {
        "Claims ratio (ICR)": ["claims_ratio"], "Family definition": [c for c in X if c.startswith("family")],
        "Average age": ["avg_age"], "Room-rent cap": [c for c in X if c.startswith("room")],
        "Parents' co-pay": ["copay_parents"], "Group size": ["employees"],
        "Industry": [c for c in X if c.startswith("industry")], "Sum insured": ["sum_insured"],
        "City tier": [c for c in X if c.startswith("city")],
    }
    gimp = {k: float(imp[v].sum()) for k, v in groups.items()}
    tot = sum(max(v, 0) for v in gimp.values())
    gimp = {k: round(max(v, 0) / tot * 100, 1) for k, v in sorted(gimp.items(), key=lambda x: -x[1])}

    # Peer matching (k-NN) — fit once, reused per client at query time
    feat = pd.get_dummies(df[["industry", "employees", "avg_age", "family", "sum_insured", "city"]], drop_first=False).astype(float)
    scaler = StandardScaler().fit(feat)
    Z = scaler.transform(feat)
    nn = NearestNeighbors(n_neighbors=43).fit(Z)

    # Plan-design simulator (log-linear)
    Xr = pd.get_dummies(df[["avg_age", "family", "sum_insured", "copay_parents", "room_rent", "city"]].assign(
        sum_insured=df.sum_insured.astype(str)), drop_first=True).astype(float)
    Xr["copay_parents"] = df.copay_parents * (df.family == "E+S+2C+P")
    lr = LinearRegression().fit(Xr, np.log(df.premium_per_life))
    r2 = lr.score(Xr, np.log(df.premium_per_life))
    coef = dict(zip(Xr.columns, lr.coef_))

    # Claims anomaly detection
    rng = np.random.default_rng(7)
    m = 5000
    amt = np.exp(rng.normal(np.log(45000), 0.7, m))
    los = np.clip(rng.poisson(3, m), 1, 20).astype(float)
    lab = np.zeros(m, int)
    k = int(m * 0.02)
    an = rng.choice(m, k, replace=False)
    amt[an] *= rng.uniform(3, 6, k)
    los[an] = np.clip(los[an] * rng.uniform(0.2, 0.5, k), 1, 20)
    lab[an] = 1
    C = np.c_[np.log(amt), los, np.log(amt / los)]
    iso = IsolationForest(contamination=0.02, random_state=7).fit(C)
    flag = (iso.predict(C) == -1).astype(int)
    iso2 = IsolationForest(contamination=0.05, random_state=7).fit(C)
    cpd = amt / los
    hyb = ((iso2.predict(C) == -1) & (cpd > np.percentile(cpd, 95))).astype(int)
    anomaly = dict(
        claims=m, injected=k, precision=round(precision_score(lab, flag) * 100),
        recall=round(recall_score(lab, flag) * 100), hyb_precision=round(precision_score(lab, hyb) * 100),
        hyb_recall=round(recall_score(lab, hyb) * 100),
        sample=pd.DataFrame({"claim_amount": amt, "length_of_stay": los, "flagged_hybrid": hyb.astype(bool)})
                .sort_values("claim_amount", ascending=False).head(8).round(0),
    )

    return dict(X=X, gbm=gbm, mae=mae, mae_naive=mae_naive, within5=within5, drivers=gimp,
                scaler=scaler, feat_cols=feat.columns, nn=nn, lr=lr, r2=r2, coef=coef, anomaly=anomaly)


df = generate_data()
M = train_models(df)

# ----------------------------------------------------------------------
# 2. Sidebar filters
# ----------------------------------------------------------------------

st.sidebar.markdown("### NivoTime")
st.sidebar.caption("Benefits Intelligence Suite — prototype")
st.sidebar.divider()
st.sidebar.markdown("**Benchmarking filters**")

f_industry = st.sidebar.multiselect("Industry", sorted(df.industry.unique()), default=list(df.industry.unique()))
f_size = st.sidebar.slider("Company size (employees)", int(df.employees.min()), int(df.employees.max()),
                            (int(df.employees.min()), int(df.employees.max())))
f_family = st.sidebar.multiselect("Family cover", sorted(df.family.unique()), default=list(df.family.unique()))
f_si = st.sidebar.multiselect("Sum insured", sorted(df.sum_insured.unique()),
                               default=list(df.sum_insured.unique()),
                               format_func=lambda x: f"₹{x/100000:.0f}L")
f_copay = st.sidebar.select_slider("Parents' co-pay filter", options=["Any", "0%", "10%", "20%"], value="Any")

mask = (
    df.industry.isin(f_industry) & df.employees.between(*f_size)
    & df.family.isin(f_family) & df.sum_insured.isin(f_si)
)
if f_copay != "Any":
    mask &= df.copay_parents == int(f_copay.strip("%"))
fdf = df[mask]

st.sidebar.divider()
st.sidebar.caption(
    "All figures are computed live from a synthetic dataset calibrated to published "
    "industry aggregates — not real client data. Proof of mechanics, not of "
    "real-world accuracy. See the PRD, Appendix A."
)

# ----------------------------------------------------------------------
# 3. Header + KPI row
# ----------------------------------------------------------------------

st.title("Benefits Intelligence Suite")
st.caption(
    "Interactive prototype of the AI-powered benchmarking, quote and simulation layer "
    "proposed for NivoTime's broker-facing platform — built from the Live Company "
    "Project report and its PRD."
)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Groups matching filter", f"{len(fdf):,}", help=f"out of {len(df)} total")
k2.metric("Mean premium / life", f"₹{fdf.premium_per_life.mean():,.0f}" if len(fdf) else "—")
k3.metric("Mean claims ratio", f"{fdf.claims_ratio.mean()*100:,.0f}%" if len(fdf) else "—")
k4.metric("Mean forecast renewal loading", f"{fdf.renewal_loading.mean()*100:,.1f}%" if len(fdf) else "—")

tab1, tab2, tab3, tab4 = st.tabs([
    "\U0001F4CA Benchmarking Cockpit", "\U0001F52C Simulation Lab",
    "\U0001F4C8 Renewal Forecast Model", "\U0001F6A9 Claims Anomaly Detection",
])

# ----------------------------------------------------------------------
# Tab 1 — Benchmarking Cockpit
# ----------------------------------------------------------------------
with tab1:
    if len(fdf) < 10:
        st.warning("Fewer than 10 groups match this filter — the platform would refuse to show a "
                   "benchmark here to protect individual-company privacy (report/PRD privacy-by-design rule).")
    else:
        c1, c2 = st.columns(2)
        with c1:
            fig = px.histogram(fdf, x="premium_per_life", nbins=30, color_discrete_sequence=[PURPLE],
                                title="Premium per life — distribution of the filtered peer set")
            fig.update_layout(bargap=0.05, xaxis_title="Premium per life (₹)", yaxis_title="Employer groups")
            st.plotly_chart(fig, width='stretch')
        with c2:
            fig = px.histogram(fdf, x="claims_ratio", nbins=30, color_discrete_sequence=[ORANGE],
                                title="Claims ratio — distribution of the filtered peer set")
            fig.update_layout(bargap=0.05, xaxis_title="Claims ratio", yaxis_title="Employer groups",
                               xaxis_tickformat=".0%")
            st.plotly_chart(fig, width='stretch')

        st.markdown("##### Benchmark a specific client against this peer set")
        idx = st.selectbox(
            "Pick a client from the filtered set", fdf.index,
            format_func=lambda i: f"{df.loc[i,'industry']} · {df.loc[i,'employees']} lives · "
                                   f"{df.loc[i,'family']} · ₹{df.loc[i,'premium_per_life']:,.0f}/life",
        )
        client = df.loc[idx]
        peers = fdf.drop(index=idx)
        pct = lambda col: round(float((peers[col] < client[col]).mean() * 100)) if len(peers) else None

        cc1, cc2, cc3 = st.columns(3)
        cc1.metric("Premium percentile vs peers", f"{pct('premium_per_life')}th" if len(peers) else "—")
        cc2.metric("Claims ratio (client vs peer median)",
                   f"{client.claims_ratio*100:.0f}%", f"peer median {peers.claims_ratio.median()*100:.0f}%" if len(peers) else "")
        cc3.metric("Employee engagement (client vs peer median)",
                   f"{client.engagement*100:.0f}%", f"peer median {peers.engagement.median()*100:.0f}%" if len(peers) else "")

        Xc = pd.get_dummies(pd.DataFrame([client]).drop(columns=["renewal_loading", "engagement", "premium_per_life"]),
                             drop_first=False).astype(float).reindex(columns=M["X"].columns, fill_value=0)
        forecast = float(M["gbm"].predict(Xc)[0]) * 100
        st.info(f"**AI renewal forecast for this client: {forecast:+.1f}%** next-year premium change "
                f"(model MAE {M['mae']:.1f} pts on held-out synthetic data — see the Renewal Forecast Model tab).")

# ----------------------------------------------------------------------
# Tab 2 — Simulation Lab
# ----------------------------------------------------------------------
with tab2:
    st.markdown("##### Plan-design simulator")
    st.caption("Move the controls to see the estimated % change in premium per life, from a log-linear "
               f"rating model fitted on the full synthetic book (R² = {M['r2']:.2f}).")

    s1, s2, s3 = st.columns(3)
    with s1:
        copay_choice = st.select_slider("Parents' co-pay", options=[0, 10, 20], value=0, format_func=lambda x: f"{x}%")
    with s2:
        room_choice = st.select_slider("Room-rent cap", options=["No cap", "2%", "1%"], value="No cap")
    with s3:
        si_choice = st.select_slider("Sum insured", options=[300000, 500000, 1000000], value=500000,
                                      format_func=lambda x: f"₹{x/100000:.0f}L")
    drop_parents = st.checkbox("Drop parents' cover entirely")

    coef = M["coef"]
    log_impact = 0.0
    if not drop_parents:
        log_impact += coef.get("copay_parents", 0) * copay_choice
    else:
        log_impact += coef.get("family_E+S+2C", 0) - coef.get("family_E+S+2C+P", 0)
    if room_choice == "1%":
        log_impact += -coef.get("room_rent_No cap", 0)
    elif room_choice == "2%":
        log_impact += coef.get("room_rent_2%", 0) - coef.get("room_rent_No cap", 0)
    if si_choice == 1000000:
        log_impact += coef.get("sum_insured_1000000", 0) - coef.get("sum_insured_500000", 0)
    elif si_choice == 300000:
        log_impact += -coef.get("sum_insured_500000", 0)

    pct_impact = (np.exp(log_impact) - 1) * 100
    st.metric("Estimated premium impact vs. the current plan", f"{pct_impact:+.1f}%")

    fig = go.Figure(go.Waterfall(
        orientation="v", measure=["relative"], x=["Selected changes"], y=[pct_impact],
        text=[f"{pct_impact:+.1f}%"], textposition="outside",
        connector={"line": {"color": "#999"}},
        decreasing={"marker": {"color": GREEN}}, increasing={"marker": {"color": ORANGE}},
    ))
    fig.update_layout(title="Premium impact of the simulated plan change", yaxis_title="% change in premium",
                       showlegend=False, height=350)
    st.plotly_chart(fig, width='stretch')

# ----------------------------------------------------------------------
# Tab 3 — Renewal Forecast Model
# ----------------------------------------------------------------------
with tab3:
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("##### Model accuracy (held-out synthetic test set)")
        st.metric("Forecast mean absolute error", f"{M['mae']:.2f} pts",
                   f"{M['mae'] - M['mae_naive']:+.2f} pts vs. naive baseline ({M['mae_naive']:.2f} pts)",
                   delta_color="inverse")
        st.metric("Forecasts within ±5 pts of actual", f"{M['within5']:.0f}%")
        st.caption(f"Improvement over the naive baseline (always predict the {12}% market trend): "
                   f"{round((1 - M['mae']/M['mae_naive'])*100)}%.")
    with c2:
        drivers = pd.Series(M["drivers"]).sort_values()
        fig = px.bar(drivers, orientation="h", color_discrete_sequence=[PURPLE],
                     title="What drives the renewal forecast — permutation importance")
        fig.update_layout(xaxis_title="Relative importance (%)", yaxis_title="", showlegend=False)
        st.plotly_chart(fig, width='stretch')
    st.info("Gradient Boosting Regressor, trained on the synthetic book. Before any client-facing accuracy "
            "claim, the report and PRD both call for back-testing on real pilot renewals (≤ 5-point MAE "
            "target, report KPI 13.4).")

# ----------------------------------------------------------------------
# Tab 4 — Claims Anomaly Detection
# ----------------------------------------------------------------------
with tab4:
    an = M["anomaly"]
    st.markdown("##### Isolation Forest alone vs. Isolation Forest + a cost-per-day rule")
    c1, c2, c3 = st.columns(3)
    c1.metric("Synthetic claims tested", f"{an['claims']:,}")
    c2.metric("Isolation Forest alone", f"{an['precision']}% precision / {an['recall']}% recall")
    c3.metric("Hybrid (+ cost-per-day rule)", f"{an['hyb_precision']}% precision / {an['hyb_recall']}% recall",
              f"{an['hyb_precision']-an['precision']:+d} / {an['hyb_recall']-an['recall']:+d} pts")

    fig = go.Figure()
    fig.add_bar(name="Precision", x=["Isolation Forest alone", "Hybrid (+ rule)"],
                y=[an["precision"], an["hyb_precision"]], marker_color=PURPLE)
    fig.add_bar(name="Recall", x=["Isolation Forest alone", "Hybrid (+ rule)"],
                y=[an["recall"], an["hyb_recall"]], marker_color=ORANGE)
    fig.update_layout(barmode="group", title="Precision / recall, pure model vs. hybrid rule", yaxis_title="%")
    st.plotly_chart(fig, width='stretch')

    st.markdown("##### Highest-value flagged claims (sample)")
    st.dataframe(an["sample"], width='stretch', hide_index=True)
    st.warning("Even the hybrid approach is a **screening** tool, not an auto-decline. Every flagged claim "
               "still goes to human review before any action — the AI-governance principle carried "
               "through both documents (report Sec. 12.4, PRD AI-G1–G5).")

st.divider()
st.caption(
    "Source: NivoTime Live Company Project report and PRD (this repository, report/ and prd/). "
    "All data synthetic — see prd/src/prd_part4.md, Appendix A for the generation spec."
)
