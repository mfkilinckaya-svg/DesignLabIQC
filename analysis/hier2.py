import math, json, itertools, pandas as pd

def gser(x):
    t=.5;r=2.;n=r
    for _ in range(200):
        t+=1;n*=x/t;r+=n
        if abs(n)<abs(r)*1e-16:break
    return r*math.exp(-x+.5*math.log(x)-.5723649429247001)
def gcf(x):
    n=x+.5;a=1/1e-300;i=1/n;o=i
    for s in range(1,301):
        l=-s*(s-.5);n+=2;i=l*i+n
        if abs(i)<1e-300:i=1e-300
        a=n+l/a
        if abs(a)<1e-300:a=1e-300
        i=1/i;u=i*a;o*=u
        if abs(u-1)<1e-16:break
    return o*math.exp(-x+.5*math.log(x)-.5723649429247001)
def erfc_(e):
    if e<0:return 2-erfc_(-e)
    t=e*e;return 1-gser(t) if t<1.5 else gcf(t)
Phic=lambda e:.5*erfc_(e/math.sqrt(2))
cdf=lambda e:1-Phic(e) if e>=0 else Phic(-e)
ins=lambda k,d:cdf(k-d)-cdf(-k-d)
pf=lambda k,n,d=0.:1-ins(k,d)**n

CV={'Leukocytes':(2.38,1.89,1.75),'Erythrocytes':(1.08,0.77,0.73),'Hemoglobin':(1.04,0.70,0.65),
'Hematocrit':(1.60,1.13,1.11),'MCV':(1.07,0.83,0.81),'MCH':(1.05,0.88,0.75),'MCHC':(1.41,1.13,1.04),
'RDW-CV':(0.94,0.72,0.65),'Platelets':(4.24,2.47,1.56),'Platelets fluorescent':(2.29,3.49,1.94),
'MPV':(2.42,1.63,1.25),'Neutrophils abs.':(3.40,2.74,2.49),'Lymphocytes abs.':(3.51,2.74,2.14),
'Monocytes abs.':(8.16,7.43,5.71),'Eosinophils abs.':(6.71,6.71,6.92),'Basophils abs.':(4.48,3.42,3.04),
'Reticulocytes':(3.51,3.43,4.76),'Reticulocyte hemoglobin':(1.10,1.15,1.45)}
N={'Leukocytes':(2,3,2),'Erythrocytes':(2,3,2),'Hemoglobin':(2,3,2),'Hematocrit':(2,3,2),
'MCV':(2,3,2),'MCH':(2,3,2),'MCHC':(2,3,2),'RDW-CV':(2,3,2),'Platelets':(2,3,2),
'Platelets fluorescent':(2,3,2),'MPV':(2,2,2),'Neutrophils abs.':(2,3,2),'Lymphocytes abs.':(2,3,2),
'Monocytes abs.':(2,3,2),'Eosinophils abs.':(2,3,2),'Basophils abs.':(2,3,2),
'Reticulocytes':(2,3,2),'Reticulocyte hemoglobin':(2,3,2)}
PED={'Leukocytes':90,'Hemoglobin':90,'Erythrocytes':90,'MCV':70,'Platelets':90,
'Platelets fluorescent':90,'Reticulocytes':70,'Neutrophils abs.':70}
EFLM={'Leukocytes':(11.1,16.9),'Erythrocytes':(2.6,7),'Hemoglobin':(2.7,6.1),'Hematocrit':(2.8,5.5),
'MCV':(0.8,4),'MCH':(0.8,4.7),'MCHC':(1,1.4),'RDW-CV':(1.7,4.9),'Platelets':(7.3,18.6),
'Platelets fluorescent':(7.3,18.6),'MPV':(2.3,7.1),'Neutrophils abs.':(12.5,25.9),
'Lymphocytes abs.':(10.5,22.8),'Monocytes abs.':(14,23),'Eosinophils abs.':(15.1,67.4),
'Basophils abs.':(12.6,28.6),'Reticulocytes':(9.7,27.1),'Reticulocyte hemoglobin':(1.7,3.4)}
WEST={'Leukocytes':(11.4,21.3),'Erythrocytes':(3.2,6.3),'Hemoglobin':(2.85,6.8),'Hematocrit':(2.7,6.41),
'MCV':(1.4,4.85),'MCH':(1.4,5.2),'MCHC':(1.06,1.2),'RDW-CV':(3.5,5.7),'Platelets':(9.1,21.9),
'Platelets fluorescent':(9.1,21.9),'MPV':(4.3,8.1),'Neutrophils abs.':(17.1,32.8),
'Lymphocytes abs.':(10.2,35.3),'Monocytes abs.':(17.8,49.8),'Eosinophils abs.':(21,76.4),
'Basophils abs.':(28,54.8),'Reticulocytes':(11,29)}
NOK={'MCV':10.,'MCH':10.,'MCHC':10.,'Leukocytes':10.,'RDW-CV':10.,'Reticulocyte hemoglobin':10.,'Platelets':20.}
CLIA={'Erythrocytes':4.,'Hematocrit':4.,'Hemoglobin':4.,'Leukocytes':10.,'Platelets':25.}
RILI={'Leukocytes':6.5,'Erythrocytes':4.,'Hemoglobin':4.,'Hematocrit':5.}
T=lambda c,g,ka,kb:1.65*ka*c+kb*math.sqrt(c*c+g*g)
TIER={'optimal':(.25,.125),'desirable':(.50,.25),'minimum':(.75,.375)}
GRID=[round(1.5+0.1*i,1) for i in range(46)]
BUDGET=0.015

def sources(a):
    s={}
    if a in EFLM:
        for t,(ka,kb) in TIER.items(): s[f'BV EFLM ({t})']=T(*EFLM[a],ka,kb)
    if a in WEST:
        for t,(ka,kb) in TIER.items(): s[f'BV Ricos ({t})']=T(*WEST[a],ka,kb)
    for d,n in ((NOK,'Noklus'),(CLIA,'CLIA 2025'),(RILI,'Rili-BAEK')):
        if a in d: s[n]=d[a]
    return s

INCUMBENT={}
import csv as _csv
for _r in _csv.DictReader(open('current_rules.csv')):
    INCUMBENT.setdefault(_r['analyte'],[]).append(float(_r['k']))

def min_change(a, tea, req):
    """Closest rule set to the one in use that keeps the budget and meets detection."""
    inc=INCUMBENT[a]
    rows=[]
    for cv,n in zip(CV[a],N[a]):
        cs=tea/cv-1.65
        rows.append([(k,pf(k,n),pf(k,n,cs) if cs>0 else 0.) for k in GRID])
    best=None
    for combo in itertools.product(*rows):
        cp=1.
        for k,p,d in combo:
            cp*=1-p
            if 1-cp>BUDGET+1e-12: break
        else:
            cd=1.
            for k,p,d in combo: cd*=1-d
            P,D=1-cp,1-cd
            if req is not None and D*100<req-1e-9: continue
            ks=[c[0] for c in combo]
            cost=sum(abs(k-i) for k,i in zip(ks,inc))
            if best is None or cost<best[0]-1e-12: best=(cost,D,P,ks)
    return best

def best_rules(a, tea, want):
    """Lowest combined Pfr among rules that reach `want` detection and stay in budget.
    Falls back to the highest attainable detection when `want` cannot be reached."""
    rows=[]
    for cv,n in zip(CV[a],N[a]):
        cs=tea/cv-1.65
        rows.append([(k,pf(k,n),pf(k,n,cs) if cs>0 else 0.) for k in GRID])
    feasible=None; fallback=None
    for combo in itertools.product(*rows):
        cp=1.
        for k,p,d in combo:
            cp*=1-p
            if 1-cp>BUDGET+1e-12: break
        else:
            cd=1.
            for k,p,d in combo: cd*=1-d
            P,D=1-cp,1-cd
            if fallback is None or D>fallback[0]: fallback=(D,P,[c[0] for c in combo])
            if D*100>=want-1e-9 and (feasible is None or P<feasible[1]):
                feasible=(D,P,[c[0] for c in combo])
    return feasible, fallback

res=[]
for a in CV:
    req=PED.get(a)
    cand=sorted(sources(a).items(), key=lambda kv: kv[1])
    chosen=None
    for name,tea in cand:
        # floor: the source must be reachable at a sigma of at least three
        if tea/max(CV[a]) < 3.0: continue
        b=min_change(a,tea,req)
        if b is not None:
            _,D,P,ks=b; chosen=(name,tea,D,P,ks); break
    if chosen is None:
        name,tea=cand[-1]
        b=min_change(a,tea,None)
        _,D,P,ks=b
        chosen=(name,tea,D,P,ks)
    name,tea,D,P,ks=chosen
    res.append(dict(analyte=a,source=name,tea=round(tea,2),K=ks,n=list(N[a]),
                    pfr=round(P*100,2),ped=round(D*100,1),req=req,
                    sigma=round(tea/max(CV[a]),2)))
    print(f"{a:24s} {name:24s} TEa {tea:6.2f}  K {ks}  Pfr {P*100:5.2f}%  Ped {D*100:5.1f}%  req {req if req else '-'}")
json.dump(res,open('final_assignment.json','w'),indent=1)
