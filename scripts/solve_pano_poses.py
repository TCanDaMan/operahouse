import numpy as np, sys
from scipy.optimize import least_squares
D=np.pi/180
OBS = [
 ('P1','val',  1.7, 46.3), ('P1','apex', 1.7, 60.0), ('P1','lip', 1.7, -4.1),
 ('P1','pilL',-39.5,None), ('P1','pilR', 40.7,None), ('P1','scrL',-17.6,41.5), ('P1','scrR', 23.7,42.0),
 ('P3','val', -3.6, -0.5), ('P3','apex',-3.6, 10.4), ('P3','lip', -3.6,-19.9),
 ('P3','pilL',-17.8,None), ('P3','pilR', 13.0,None), ('P3','scrL', -9.4,-2.8), ('P3','scrR',  2.9,-2.75), ('P3','chan',-12.3,24.8),
 ('P4','val', -0.2,-11.8), ('P4','apex',-0.2, -1.2), ('P4','pilL',-14.2,None), ('P4','pilR', 14.4,None),
 ('P4','scrL', -5.1,-13.8), ('P4','scrR', 7.0,-13.7), ('P4','chan', 8.2, 3.7),
 ('P5','val',  5.0,-18.9), ('P5','scrL', 0.9,-20.0), ('P5','scrR', 9.4,-19.9), ('P5','pilL',-4.8,None), ('P5','pilR',14.8,None),
 ('P2','val',  2.8,  8.6), ('P2','lip',  2.8,-14.3), ('P2','pilL',-15.5,None), ('P2','pilR', 21.8,None),
 ('P2','scrL', -4.3, 6.1), ('P2','scrR',10.3, 6.2), ('P2','chan', 2.1, 44.9),
 ('Q1','chan',11.1,4.1), ('Q1','apex',2.5,-4.0), ('Q1','val',2.5,-12.4), ('Q1','pilL',-11.9,None), ('Q1','pilR',17.8,None),
 ('Q2','chan',-6.2,23.9), ('Q2','apex',1.6,10.4), ('Q2','val',1.6,-2.2), ('Q2','pilL',-12.2,None), ('Q2','pilR',19.3,None), ('Q2','lip',1.6,-19.6),
 ('Q4','apex',1.9,19.7), ('Q4','val',1.9,8.3), ('Q4','lip',1.9,-12.4), ('Q4','pilL',-15.8,None), ('Q4','pilR',20.5,None),
]
PANOS=['P1','P2','P3','P4','P5','Q1','Q2','Q4']
SIG={'P1':0.4,'P2':0.4,'P3':0.4,'P4':0.4,'P5':0.4,'Q1':0.6,'Q2':0.6,'Q4':0.6}
PITCH_SIG=float(sys.argv[1]) if len(sys.argv)>1 else 1.0
def unpack(p):
    cams={n:p[5*i:5*i+5] for i,n in enumerate(PANOS)}; k=5*len(PANOS)
    return cams, p[k], p[k+1:k+4], p[k+4:k+7], p[k+7:k+10]
def feat(name,apex_y,scrL,scrR,chan):
    return {'val':np.array([0,35.0,0]),'apex':np.array([0,apex_y,0]),'lip':np.array([0,3.5,-4.33]),'scrL':scrL,'scrR':scrR,'chan':chan}[name]
def project(cam,X):
    cx,cy,cz,h,pt=cam; d=X-np.array([cx,cy,cz]); ch,sh=np.cos(h*D),np.sin(h*D)
    dx=d[0]*ch-(-d[2])*sh; dzf=d[0]*sh+(-d[2])*ch; dy=d[1]; cp,sp=np.cos(pt*D),np.sin(pt*D)
    fwd=dzf*cp+dy*sp; up=-dzf*sp+dy*cp
    return np.arctan2(dx,fwd)/D, np.arctan2(up,np.hypot(dx,fwd))/D
def resid(p):
    cams,apex_y,scrL,scrR,chan=unpack(p); r=[]
    for pn,f,az,el in OBS:
        cam=cams[pn]; s=SIG[pn]
        if f in ('pilL','pilR'):
            X=np.array([-26.0 if f=='pilL' else 26.0, cam[1], 0.0]); a,_=project(cam,X); r.append((a-az)/s)
        else:
            X=feat(f,apex_y,scrL,scrR,chan); a,e=project(cam,X); r.append((a-az)/s); r.append((e-el)/s)
    for pn in PANOS: r.append(cams[pn][4]/PITCH_SIG)
    return np.array(r)
init={'P1':[0,5.3,28,0,0],'P2':[0,20,70,0,0],'P3':[0,30,88,0,0],'P4':[0,45,100,0,0],'P5':[0,65,150,0,0],'Q1':[0,45,100,0,0],'Q2':[0,30,88,0,0],'Q4':[0,20,70,0,0]}
p0=[]; [p0.extend(init[n]) for n in PANOS]; p0+=[45.0,-8,28,-2,8,28,-2, 0,50,50]
sol=least_squares(resid,p0,method='lm',max_nfev=50000)
cams,apex_y,scrL,scrR,chan=unpack(sol.x); r=resid(sol.x)
print(f'pitch prior sigma {PITCH_SIG} deg; rms residual (weighted) {np.sqrt(np.mean(r**2)):.2f}; max |resid| {np.max(np.abs(r[:-len(PANOS)]))*0.4:.2f} deg (P sigma units)')
for n in PANOS:
    cx,cy,cz,h,pt=cams[n]; print(f"{n}: x={cx:6.1f}  cam_height={cy:6.1f} ft  dist_from_curtain={cz:6.1f} ft  heading={h:6.1f}  pitch={pt:5.2f}")
print('apex',round(apex_y,1),' chandelier tip',np.round(chan,1),' screen width',round(np.linalg.norm(scrR-scrL),1),'screen ht',round(scrL[1],1))
# covariance-based 1-sigma on heights
J=sol.jac; cov=np.linalg.pinv(J.T@J); sd=np.sqrt(np.diag(cov))
print('1-sigma cam height:', {n: round(sd[5*i+1],1) for i,n in enumerate(PANOS)})
print('1-sigma dist:', {n: round(sd[5*i+2],1) for i,n in enumerate(PANOS)})
