import json
# ---------- Assumptions (all illustrative, labelled in report) ----------
prem_per_life = 61435e7/27.51e7          # Rs, group health premium / group lives FY25 [5]
broker_comm = 0.075                        # A3 broker brokerage share of premium
broker_rev_per_life = prem_per_life*broker_comm
broker_base = 1.8e5                        # A4a broker workspace subscription / yr
per_account = 5000                         # A4b per active employer account / yr (AI renewal + quote pack)
per_life_b = 10                            # A4c per engaged employee life / yr (zero-login layer)
fee_direct = 60                            # A5 Rs per life per year (Rs 5 PEPM)
accounts_mature = 25
impl_broker = 3.0e5; impl_direct = 0.75e5  # A6
advisory_price = 0.75e5                    # A7 renewal advisory pack
lives_per_broker_mature = 25*700           # A8 25 employer accounts x 700 lives
ramp = {1:0.3, 2:0.7, 3:1.0}               # A9 share of mature lives in yr1/2/3 of a broker's life
direct_lives = 700
scen = {
 'Downside': {'brokers_new':[1,2,3], 'direct_new':[3,5,6], 'adv_rate':0.2},
 'Base':     {'brokers_new':[3,5,7], 'direct_new':[4,6,8], 'adv_rate':0.3},
 'Upside':   {'brokers_new':[4,8,12],'direct_new':[5,9,12],'adv_rate':0.4},
}
cost = {  # INCREMENTAL Rs/yr: new hires + reallocated team share, cloud+AI APIs, sales & marketing, security/compliance
 'people':[36e5,48e5,60e5], 'cloud_ai':[6e5,9e5,14e5], 'sm':[12e5,16e5,20e5], 'sec':[8e5,4e5,5e5]}
res={}
for s,p in scen.items():
    cohorts=[]; rows=[]; dcum=0
    for y in range(3):
        cohorts.append(p['brokers_new'][y])
        lives_b = sum(n*lives_per_broker_mature*ramp[y-i+1] for i,n in enumerate(cohorts))
        dcum += p['direct_new'][y]
        lives_d = dcum*direct_lives
        bro_eq = lives_b/lives_per_broker_mature   # broker-equivalents at maturity
        active_brokers = sum(cohorts)
        rec = active_brokers*broker_base*(1 if y>0 else 0.5) + bro_eq*accounts_mature*per_account + lives_b*per_life_b + lives_d*fee_direct
        impl = p['brokers_new'][y]*impl_broker + p['direct_new'][y]*impl_direct
        adv = round(dcum*p['adv_rate'] + sum(cohorts)*25*0.05)*advisory_price  # direct clients + 5% of broker accounts buy a pack
        rev = rec+impl+adv
        c = sum(cost[k][y] for k in cost)
        rows.append(dict(year=y+1, brokers=sum(cohorts), direct=dcum, lives=int(lives_b+lives_d),
             recurring=rec, implementation=impl, advisory=adv, revenue=rev, cost=c, ebitda=rev-c))
    res[s]=rows
# unit economics (base): broker
cac_broker = 0.6*sum(cost['sm'])/sum(scen['Base']['brokers_new'])  # 60% of S&M attributed to broker path
arr_broker = broker_base + accounts_mature*per_account + lives_per_broker_mature*per_life_b
gm = 0.70
life_yrs = 5
ltv = arr_broker*gm*life_yrs
out = dict(prem_per_life=prem_per_life, broker_rev_per_life=broker_rev_per_life, fee_share=0,
           res=res, cac_broker=cac_broker, arr_broker=arr_broker, ltv=ltv, ltv_cac=ltv/cac_broker,
           payback_months=cac_broker/(arr_broker*gm/12))
# customer ROI
acc=40; lives=acc*700; fee=broker_base+acc*per_account+lives*per_life_b
hours_saved = acc*30*0.5; hr_val=700
roi = dict(fee=fee, time_value=hours_saved*hr_val, hours=hours_saved,
      retained=2*700*prem_per_life*broker_comm, won=3*700*prem_per_life*broker_comm)
roi['total']=roi['time_value']+roi['retained']+roi['won']
emp_prem = 700*prem_per_life; emp_fee = 700*fee_direct
out['roi']=roi; out['employer']=dict(premium=emp_prem, fee=emp_fee, breakeven_pct=emp_fee/emp_prem)
# market pool
pool_all = 0
out['pool_all']=pool_all
json.dump(out, open('/home/claude/nivotime/final/model.json','w'), indent=1, default=float)
def cr(x): return f"{x/1e7:.2f} cr"
def lk(x): return f"{x/1e5:.1f} L"
print('prem/life', round(prem_per_life), 'broker rev/life', round(broker_rev_per_life))
for s,rows in res.items():
    print(s)
    for r in rows: print(' Y%d brokers %d direct %d lives %d rev %s (rec %s impl %s adv %s) cost %s ebitda %s'%(r['year'],r['brokers'],r['direct'],r['lives'],lk(r['revenue']),lk(r['recurring']),lk(r['implementation']),lk(r['advisory']),lk(r['cost']),lk(r['ebitda'])))
print('CAC broker',lk(cac_broker),'ARR broker',lk(arr_broker),'LTV',lk(ltv),'LTV/CAC',round(ltv/cac_broker,1),'payback m',round(out['payback_months'],1))
print('ROI', {k:lk(v) if k!='hours' else v for k,v in roi.items()})
print('employer', lk(emp_prem), lk(emp_fee), round(emp_fee/emp_prem*100,2),'%')
print('pool all group lives', cr(pool_all))
