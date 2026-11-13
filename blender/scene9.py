import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from proplib import *
from proplib import _act
ORANGE=mat("Orange","#EE7B2B")
# ============ SCENE 9 : LE DRAGON ============
# ---- GARDEN SHEARS (jaws) ----
sh=[]
for sg,yy in ((1,-.045),(-1,.045)):
    a=math.radians(13)*sg; d=(math.cos(a),math.sin(a)); nrm=(-d[1]*sg,d[0]*sg)
    P=[(-.12*d[0],-.12*d[1]),(-.1*d[0]+.2*nrm[0],-.1*d[1]+.2*nrm[1]),(.5*d[0]+.19*nrm[0],.5*d[1]+.19*nrm[1]),(1.35*d[0],1.35*d[1])]
    sh.append(flat(P,STEEL,.02,.02,y=yy))
    h=(-math.cos(a*1.6),sg*math.sin(a*1.6)*-1)
    sh.append(tube([((0,yy,0),.07),((h[0]*.45,yy,h[1]*.45-sg*.04),.07),((h[0]*1.0,yy,h[1]*1.0-sg*.12),.085)],WOOD))
    sh.append(tube([((h[0]*.55,yy,h[1]*.55-sg*.055),.095),((h[0]*1.0,yy,h[1]*1.0-sg*.12),.1)],RED,res=4)); sh.append(sph(.1,(h[0]*1.02,yy,h[1]*1.02-sg*.125),(1,1,1),RED,12))
    sh.append(tube([((h[0]*.08,yy,h[1]*.08),.075),((h[0]*.3,yy,h[1]*.3-sg*.02),.075)],GOLD,res=3))
sh.append(cyl(.09,.2,(.02,0,0),GOLD,rot=(math.pi/2,0,0),bev=.03)); sh.append(cyl(.045,.26,(.02,0,0),BLACK,rot=(math.pi/2,0,0),bev=.01))
finish(sh,"Shears",0.024)
# ---- ACCORDION (body) ----
ac=[]
for sx in (-1,1):
    ac.append(box((.42,.84,1.5),(sx*1.0,0,0),RED,bev=.08)); ac.append(box((.06,.88,1.54),(sx*.8,0,0),GOLD,bev=.02))
    for i in range(3):
        for j in range(4): ac.append(dot(.05,(sx*1.0+(i-1)*.11,-.425,-.36+j*.24),GOLD,th=.4))
    ac.append(box((.3,.03,.12),(sx*1.0,-.43,.6),CREAM,bev=.01))
for i in range(11):
    x=-.7+i*.14; big=i%2==0
    ac.append(box((.15,.78 if big else .62,1.42 if big else 1.24),(x,0,0),CREAM if big else DRED,bev=.03))
for sx in (-1,1):
    for sz in (-1,1):
        for sy in (-1,1): ac.append(box((1.36,.07,.07),(0,sy*.37,sz*.69),RED,bev=.02)) if sx==1 else None
ac.append(box((.1,.6,1.2),(-1.24,0,0),CREAM,bev=.02))                                           # piano keys on the left end
for j in range(9): ac.append(box((.03,.62,.012),(-1.29,0,-.52+j*.13),BLACK,bev=0))
for j in range(6): ac.append(box((.05,.3,.07),(-1.3,.12,-.42+j*.17+(.06 if j>2 else 0)),BLACK,bev=.01))
for i in range(3):                                                                              # buttons on the right end
    for j in range(6): ac.append(dot(.045,(1.215,(i-1)*.2,-.45+j*.18),CREAM,(1,0,0),.5))
ac.append(tube([((-1.0,0,.76),.05),((-.5,0,1.0),.05),((.5,0,1.0),.05),((1.0,0,.76),.05)],DWOOD)); 
for sx in (-1,1): ac.append(cyl(.07,.06,(sx*1.0,0,.77),GOLD,bev=.02))
backfill(ac); finish(ac,"Accordion")
# ---- UMBRELLA, OPEN (wing) ----
um=[]; NG=8; RR=1.3; HH=.7; ZR=1.55
for kk in range(NG):
    def fn(u,v,kk=kk):
        th=2*math.pi*(kk+u)/NG; a=v*math.pi/2*.98; bil=math.sin(math.pi*u)
        r=RR*math.sin(a)*(1+.035*bil*v); z=ZR+HH*math.cos(a)+.1*bil*v*v
        return (r*math.cos(th),r*math.sin(th),z)
    um.append(surf(fn,10,12,RED if kk%2==0 else CREAM,thick=.04))
for kk in range(NG):
    th=2*math.pi*kk/NG; um.append(tube([((RR*math.sin(v*math.pi/2*.98)*math.cos(th),RR*math.sin(v*math.pi/2*.98)*math.sin(th),ZR+HH*math.cos(v*math.pi/2*.98)+.015),.02) for v in (0,.25,.5,.75,1)],GOLD,res=4))
    um.append(sph(.05,(RR*math.cos(th),RR*math.sin(th),ZR+.01),(1,1,1),GOLD,10))
    um.append(tube([((0,0,1.75),.014),((RR*.55*math.cos(th),RR*.55*math.sin(th),ZR+HH*.62),.014)],STEEL,res=2))     # stretchers underneath
um.append(tube([((0,0,.45),.04),((0,0,2.3),.04)],STEEL,res=2)); um.append(lathe([(.04,2.22),(.08,2.25),(.03,2.5),(0.001,2.52)],GOLD,24)); um.append(cyl(.07,.1,(0,0,1.75),GOLD,bev=.02))
um.append(tube([((0,0,.5),.06),((0,0,.22),.06),((.1,0,.04),.06),((.27,0,.02),.06),((.37,0,.16),.06),((.36,0,.28),.055)],DWOOD)); um.append(cyl(.065,.08,(0,0,.5),GOLD,bev=.02))
for o_ in um: rot(o_,(0,math.radians(18),0),(0,0,1.2))
finish(um,"Umbrella",0.024)
# ---- KITE (wing) ----
T,Rt,Bm,Lf,Cn=(0,1.1),(.75,.35),(0,-.95),(-.75,.35),(0,.35)
ki=[flat([T,Rt,Cn],PETROL,.02,.015),flat([Rt,Bm,Cn],CREAM,.02,.015),flat([Bm,Lf,Cn],PETROL,.02,.015),flat([Lf,T,Cn],CREAM,.02,.015)]
ki.append(tube([((0,.045,1.12),.03),((0,.045,-.97),.03)],WOOD,res=2)); ki.append(tube([((-.77,.045,.35),.03),((.77,.045,.35),.03)],WOOD,res=2)); ki.append(sph(.05,(0,.06,.35),(1,1,1),GOLD,10))
ki.append(tube([((x,0,z),.03) for x,z in (T,Rt,Bm,Lf,T)],GOLD,res=2))
for p_ in (Rt,Lf): ki.append(sph(.06,(p_[0],0,p_[1]),(1,1,1),RED,10))
ki.append(dot(.13,(0,-.04,.35),RED,th=.2)); ki.append(dot(.13,(0,.04,.35),RED,(0,1,0),.2))
TL=[(0,-.95),(.1,-1.2),(-.08,-1.45),(.12,-1.7),(-.02,-1.95)]
ki.append(tube([((x,0,z),.018) for x,z in TL],DWOOD,res=6))
for x,z in TL[1:4]:
    for sx in (-1,1): ki.append(flat([(x,z),(x+sx*.2,z+.1),(x+sx*.2,z-.1)],RED,.02,.02))
    ki.append(sph(.04,(x,0,z),(1,1,1),GOLD,10))
finish(ki,"Kite",0.024)
# ---- HAND SAW (back spikes) ----
P=[(-.25,.42),(1.9,.22),(1.97,.12),(1.93,.0)]
n_=20
for i in range(n_): x=1.9-2.15*i/n_; P+= [(x-.05,-.1),(x-2.15/n_,0)]
sa=[flat(P,STEEL,.014,.012)]
sa.append(flat(chaikin([(-.42,.52),(-.1,.5),(-.08,-.08),(-.4,-.22)],1),WOOD,.07,.03))
sa.append(tube([((-.3,0,.5),.085),((-.72,0,.6),.085),((-.95,0,.3),.085),((-.88,0,-.2),.085),((-.5,0,-.3),.085),((-.3,0,-.15),.085)],WOOD))
for x,z in ((-.22,.36),(-.22,.04),(-.3,.2)): sa.append(dot(.045,(x,-.11,z),GOLD,th=.4))
sa.append(flat([(-.12,.5),(-.02,.49),(0,-.06),(-.1,-.09)],RED,.075,.02))
backfill(sa); finish(sa,"Saw",0.022)
# ---- RAKE (claw) ----
ra=[lathe([(0.001,0),(.055,.02),(.055,2.2),(0.001,2.2)],WOOD,24), lathe([(.05,.04),(.07,.05),(.07,.6),(.05,.61)],RED,24), lathe([(.05,2.05),(.075,2.07),(.06,2.4),(.03,2.42)],STEEL,24)]
ra.append(tube([((-.6,0,2.42),.045),((.6,0,2.42),.045)],STEEL,res=2))
for i in range(9):
    x=-.56+i*.14; ra.append(tube([((x,0,2.42),.032),((x,-.02,2.62),.03),((x,-.1,2.78),.014)],STEEL,res=4))
for sx in (-1,1): ra.append(tube([((0,0,2.2),.022),((sx*.3,0,2.3),.022),((sx*.5,0,2.42),.022)],STEEL,res=3))
finish(ra,"Rake",0.022)
# ---- GARDEN HAND FORK (claw) ----
hf=[lathe([(0.001,0),(.09,.02),(.13,.18),(.11,.42),(.08,.6),(0.001,.6)],WOOD,32)]
for z in (.12,.3): hf.append(torus(.125 if z>.2 else .115,.014,(0,0,z),DWOOD))
hf.append(lathe([(.075,.56),(.095,.57),(.075,.74),(.05,.75)],GOLD,32)); hf.append(tube([((0,0,.72),.045),((0,0,.9),.05)],STEEL,res=2))
hf.append(tube([((0,0,.88),.045),((0,-.03,1.15),.04),((0,-.1,1.38),.012)],STEEL,res=4))
for sx in (-1,1): hf.append(tube([((0,0,.88),.045),((sx*.17,0,.96),.042),((sx*.2,-.03,1.16),.038),((sx*.19,-.1,1.36),.012)],STEEL,res=5))
finish(hf,"HandFork",0.022)
# ---- CROISSANT (horns) ----
cr=[]; NS=7
for i in range(NS):                                       # fat rolled segments, biggest in the middle, tips curling in
    t=-1+2*i/(NS-1); ph=math.pi/2+t*math.radians(84); Rc=.6; s_=.37*(1-.55*abs(t)**1.3)
    o_=sph(1,(0,0,0),(s_*1.0,s_*.95,s_*1.05),BREAD,28); rot(o_,(0,-(ph-math.pi/2),0)); move(o_,(Rc*math.cos(ph),0,Rc*math.sin(ph)+.16*abs(t)**2)); cr.append(o_)
    if i<NS-1:                                            # toasted seam between rolls
        t2=t+1/(NS-1); ph2=math.pi/2+t2*math.radians(84); s2=.37*(1-.55*abs(t2)**1.3)
        r_=torus(s2*.86,.028,(0,0,0),WOOD); r_.scale=(1,.95,1); rot(r_,(0,math.pi/2-(ph2-math.pi/2),0)); move(r_,(Rc*math.cos(ph2),0,Rc*math.sin(ph2)+.16*abs(t2)**2)); cr.append(r_)
finish(cr,"Croissant")
# ---- GARDEN HOSE (tail) ----
PTS=[(-1.5,0,0),(-1.2,0,0),(-.8,0,.22),(-.4,-.1,.0),(0,-.12,.25),(.24,-.06,.62),(0,.02,.88),(-.24,.08,.62),(0,.12,.25),(.4,.1,.02),(.8,0,.22),(1.15,0,.1),(1.4,0,.1)]
ho=[tube([(p,.09) for p in PTS],GREEN)]
ho.append(cyl(.11,.14,(-1.5,0,0),GOLD,rot=(0,math.pi/2,0),bev=.03)); ho.append(cyl(.12,.05,(-1.42,0,0),RED,rot=(0,math.pi/2,0),bev=.02))
ho.append(cyl(.11,.12,(1.42,0,.1),RED,rot=(0,math.pi/2,0),bev=.03)); ho.append(cyl(.105,.34,(1.63,0,.1),GOLD,rot=(0,-math.pi/2,0),r2=.055,bev=0)); ho.append(torus(.1,.022,(1.5,0,.1),GOLD,rot=(0,math.pi/2,0)))
ho.append(cyl(.03,.14,(1.55,0,.22),GOLD,bev=0)); ho.append(sph(.05,(1.55,0,.3),(1.6,1,.7),RED,10))
finish(ho,"Hose",0.024)
# ---- FEATHER DUSTER (fire) ----
fd=[lathe([(0.001,0),(.07,.02),(.085,.25),(.06,.7),(.07,.9),(0.001,.9)],WOOD,32), lathe([(.07,.1),(.095,.11),(.092,.34),(.075,.35)],RED,32), lathe([(.06,.84),(.085,.85),(.17,1.06),(.15,1.08)],GOLD,32), sph(.07,(0,0,-.01),(1,1,.7),GOLD,12)]
def feather(rad,z,tilt,ang,m_,sc=(.055,.17,.44)):
    o_=sph(1,(0,0,0),sc,m_,16); rot(o_,(0,tilt,0)); move(o_,(rad,0,z)); rot(o_,(0,0,ang)); return o_
for i in range(10): fd.append(feather(.3,1.38,.52,i*math.pi/5,RED if i%2==0 else ORANGE))
for i in range(8): fd.append(feather(.17,1.55,.28,i*math.pi/4+.3,ORANGE if i%2==0 else GOLD,(.05,.15,.42)))
for i in range(4): fd.append(feather(.05,1.72,.08,i*math.pi/2+.6,GOLD,(.045,.12,.36)))
finish(fd,"FeatherDuster")
lineup(OUT+"assets/lineup-s9.png",OUT+"blender/scene9.blend",res=(3000,900))
