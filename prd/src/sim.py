"""Synthetic simulation of the NivoTime AI/ML layer (prototype evidence, NOT real client data)."""
import numpy as np, pandas as pd, json
from sklearn.ensemble import GradientBoostingRegressor, IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, precision_score, recall_score

rng = np.random.default_rng(42)
N = 600
ind = rng.choice(["IT services", "Manufacturing", "BFSI", "Pharma", "Retail", "Prof. services"], N, p=[.28, .22, .16, .12, .12, .10])
age_base = {"IT services": 30, "Manufacturing": 37, "BFSI": 34, "Pharma": 35, "Retail": 31, "Prof. services": 33}
avg_age = np.array([age_base[i] for i in ind]) + rng.normal(0, 2.5, N)
emp = np.clip(np.exp(rng.normal(np.log(650), 0.6, N)), 250, 2000).astype(int)
family = rng.choice(["E", "E+S+2C", "E+S+2C+P"], N, p=[.15, .50, .35])
si = rng.choice([300000, 500000, 1000000], N, p=[.35, .45, .20])
copay_par = np.where(family == "E+S+2C+P", rng.choice([0, 10, 20], N, p=[.45, .35, .20]), 0)
room = rng.choice(["1%", "2%", "No cap"], N, p=[.45, .30, .25])
tier = rng.choice(["Metro", "Tier 2"], N, p=[.7, .3])

fam_f = {"E": 0.55, "E+S+2C": 1.0, "E+S+2C+P": 1.45}
si_f = {300000: 0.85, 500000: 1.0, 1000000: 1.22}
room_f = {"1%": 0.94, "2%": 1.0, "No cap": 1.07}
age_f = np.exp((avg_age - 33) * 0.035)
f_fam = np.array([fam_f[f] for f in family]); f_si = np.array([si_f[s] for s in si]); f_room = np.array([room_f[r] for r in room])
f_cop = 1 - copay_par / 100 * 0.55 * (family == "E+S+2C+P")
f_tier = np.where(tier == "Metro", 1.05, 0.92)
prem = 2105 * age_f * f_fam * f_si * f_room * f_cop * f_tier * np.exp(rng.normal(0, 0.08, N))
# claims ratio: parents cover w/o co-pay and no cap push it up; small groups more volatile
icr = (0.78 + 0.10 * (family == "E+S+2C+P") * (copay_par == 0) + 0.04 * (room == "No cap") + 0.004 * (avg_age - 33)
       + rng.normal(0, 0.12, N) * np.sqrt(650 / emp))
icr = np.clip(icr, 0.35, 1.6)
engagement = np.clip(rng.normal(0.44, 0.12, N), 0.1, 0.9)
trend = 0.12
cred = np.minimum(1, emp / 1000) ** 0.5
renewal = (trend + cred * 0.55 * (icr - 0.80) + 0.02 * (family == 'E+S+2C+P') + 0.015 * (room == 'No cap')
           + 0.004 * (avg_age - 33) + 0.01 * (tier == 'Metro') + rng.normal(0, 0.02, N))  # next-year loading
df = pd.DataFrame(dict(industry=ind, employees=emp, avg_age=avg_age.round(1), family=family, sum_insured=si,
                       copay_parents=copay_par, room_rent=room, city=tier, premium_per_life=prem.round(0),
                       claims_ratio=icr.round(3), engagement=engagement.round(3), renewal_loading=renewal.round(4)))
df.to_csv("/home/claude/nivotime/prd/synthetic_employer_groups.csv", index=False)

# ---- Model 2: renewal cost forecast ----
X = pd.get_dummies(df.drop(columns=["renewal_loading", "engagement", "premium_per_life"]), drop_first=False).astype(float)
y = df["renewal_loading"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=7)
gbm = GradientBoostingRegressor(n_estimators=300, max_depth=3, learning_rate=0.05, random_state=7).fit(Xtr, ytr)
pred = gbm.predict(Xte)
mae = mean_absolute_error(yte, pred) * 100
mae_naive = mean_absolute_error(yte, np.full(len(yte), trend)) * 100
within5 = float(np.mean(np.abs(yte - pred) <= 0.05) * 100)
pi = permutation_importance(gbm, Xte, yte, n_repeats=10, random_state=7)
imp = pd.Series(pi.importances_mean, index=X.columns)
groups = {"Claims ratio (ICR)": ["claims_ratio"], "Family definition": [c for c in X if c.startswith("family")],
          "Average age": ["avg_age"], "Room-rent cap": [c for c in X if c.startswith("room")],
          "Parents' co-pay": ["copay_parents"], "Group size": ["employees"], "Industry": [c for c in X if c.startswith("industry")],
          "Sum insured": ["sum_insured"], "City tier": [c for c in X if c.startswith("city")]}
gimp = {k: float(imp[v].sum()) for k, v in groups.items()}
tot = sum(max(v, 0) for v in gimp.values())
gimp = {k: round(max(v, 0) / tot * 100, 1) for k, v in sorted(gimp.items(), key=lambda x: -x[1])}

# ---- Model 1: peer matching (k-NN) for a sample client ----
feat = pd.get_dummies(df[["industry", "employees", "avg_age", "family", "sum_insured", "city"]], drop_first=False).astype(float)
Z = StandardScaler().fit_transform(feat)
client = int(df[(df.industry == "IT services") & (df.family == "E+S+2C+P") & (df.copay_parents == 0)].index[0])
nn = NearestNeighbors(n_neighbors=43).fit(Z)
_, idx = nn.kneighbors(Z[[client]])
peers = df.iloc[idx[0][1:]]
c = df.iloc[client]
pct = lambda col: round(float((peers[col] < c[col]).mean() * 100))
peer_view = dict(client=c.to_dict(), n_peers=len(peers), prem_pct=pct("premium_per_life"), icr_client=round(float(c.claims_ratio) * 100),
                 icr_peer_median=round(float(peers.claims_ratio.median()) * 100), eng_client=round(float(c.engagement) * 100),
                 eng_peer_median=round(float(peers.engagement.median()) * 100),
                 pred_renewal=round(float(gbm.predict(X.iloc[[client]])[0]) * 100, 1))

# ---- Model 3: plan-design simulator (log-linear rating relativities) ----
Xr = pd.get_dummies(df[["avg_age", "family", "sum_insured", "copay_parents", "room_rent", "city"]].assign(
    sum_insured=df.sum_insured.astype(str)), drop_first=True).astype(float)
Xr["copay_parents"] = df.copay_parents * (df.family == "E+S+2C+P")
lr = LinearRegression().fit(Xr, np.log(df.premium_per_life))
coef = dict(zip(Xr.columns, lr.coef_))
sim = {
    "10% co-pay on parents": round((np.exp(coef["copay_parents"] * 10) - 1) * 100, 1),
    "20% co-pay on parents": round((np.exp(coef["copay_parents"] * 20) - 1) * 100, 1),
    "Room-rent cap 1% (from no cap)": round((np.exp(-coef.get("room_rent_No cap", 0) + coef.get("room_rent_2%", 0) * 0) - 1) * 100, 1),
    "Sum insured ₹5L → ₹10L": round((np.exp(coef.get("sum_insured_1000000", 0) - coef.get("sum_insured_500000", 0)) - 1) * 100, 1),
    "Drop parents' cover": round((np.exp(coef.get("family_E+S+2C", 0) - coef.get("family_E+S+2C+P", 0)) - 1) * 100, 1),
}
r2 = lr.score(Xr, np.log(df.premium_per_life))

# ---- Model 5: claims anomaly detection ----
M = 5000
amt = np.exp(rng.normal(np.log(45000), 0.7, M)); los = np.clip(rng.poisson(3, M), 1, 20).astype(float)
age = rng.integers(1, 80, M).astype(float)
lab = np.zeros(M, int); k = int(M * 0.02); an = rng.choice(M, k, replace=False)
amt[an] *= rng.uniform(3, 6, k); los[an] = np.clip(los[an] * rng.uniform(0.2, 0.5, k), 1, 20); lab[an] = 1
C = np.c_[np.log(amt), los, np.log(amt / los)]
iso = IsolationForest(contamination=0.02, random_state=7).fit(C)
flag = (iso.predict(C) == -1).astype(int)
iso2 = IsolationForest(contamination=0.05, random_state=7).fit(C)
cpd = amt / los
hyb = ((iso2.predict(C) == -1) & (cpd > np.percentile(cpd, 95))).astype(int)
anom = dict(claims=M, injected=k, flagged=int(flag.sum()), precision=round(precision_score(lab, flag) * 100),
            recall=round(recall_score(lab, flag) * 100), hyb_flagged=int(hyb.sum()),
            hyb_precision=round(precision_score(lab, hyb) * 100), hyb_recall=round(recall_score(lab, hyb) * 100))

out = dict(n_groups=N, mean_premium=round(float(df.premium_per_life.mean())), mean_icr=round(float(df.claims_ratio.mean()) * 100, 1),
           forecast=dict(mae_pp=round(mae, 2), naive_mae_pp=round(mae_naive, 2), within_5pp=round(within5, 1), test_n=len(yte),
                         improvement=round((1 - mae / mae_naive) * 100)),
           drivers=gimp, peer=peer_view, simulator=sim, sim_r2=round(r2, 3), anomaly=anom,
           industry_counts=df.industry.value_counts().to_dict())
json.dump(out, open("/home/claude/nivotime/prd/sim.json", "w"), indent=1, default=str)
print(json.dumps(out, indent=1, default=str)[:2500])
