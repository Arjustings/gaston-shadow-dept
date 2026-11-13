import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from proplib import *
from proplib import _act
# ============ SCENE 8 : LE MOULIN ============
# ---- MILK CHURN (tower) ----
m=[lathe([(0.001,0),(.74,0),(.78,.06),(.78,1.85),(.7,2.1),(.46,2.4),(.42,2.6),(.57,2.84),(.57,2.92),(0.001,2.92)],STEEL,64)]
for z,r_ in ((.1,.79),(1.82,.79)): m.append(lathe([(r_-.02,z-.06),(r_+.03,z-.04),(r_+.03,z+.04),(r_-.02,z+.06)],GOLD,64))
m.append(lathe([(.78,.7),(.8,.72),(.8,1.22),(.78,1.24)],RED,64))
for k in range(10):
    a=k*math.pi/5; m.append(dot(.09,(.81*math.cos(a),.81*math.sin(a),.97),CREAM,(math.cos(a),math.sin(a),0),.2))
m.append(lathe([(.4,2.56),(.44,2.58),(.44,2.64),(.4,2.66)],GOLD,64)); m.append(torus(.57,.04,(0,0,2.88),GOLD))
m.append(lathe([(.5,2.9),(.52,2.98),(.24,3.06),(0.001,3.08)],STEEL,64)); m.append(cyl(.06,.1,(0,0,3.12),GOLD,bev=.02)); m.append(sph(.1,(0,0,3.22),(1,1,.8),RED,16))
for sx in (-1,1): m.append(torus(.2,.05,(sx*.74,0,2.12),DEEP,rot=(math.pi/2,0,0))); m.append(sph(.07,(sx*.66,0,2.3),(1,1,1),GOLD,12))
finish(m,"MilkChurn")
# ---- COLANDER (cap) ----
c=[lathe([(.34,.2),(.62,.3),(.85,.6),(.93,.95),(.96,1.0),(.9,1.0),(.8,.62),(.56,.36),(0.001,.3),(0.001,.2)],CREAM,64)]
c.append(lathe([(.3,0),(.38,0),(.36,.22),(.3,.22)],RED,64)); c.append(torus(.94,.045,(0,0,1.0),RED))
def cpt(a,z):
    r=.62+(z-.3)*.77 if z<.6 else .85+(z-.6)*.23
    return (r*math.cos(a),r*math.sin(a),z),(math.cos(a),math.sin(a),-.45)
for k in range(8):
    a0=k*math.pi/4
    for da,z in ((0,.74),(-.11,.66),(.11,.66),(0,.58),(-.11,.82),(.11,.82)):
        p,n=cpt(a0+da,z); c.append(dot(.038,(p[0]*1.012,p[1]*1.012,p[2]),DEEP,n,.3))
    p,n=cpt(a0+math.pi/8,.45); c.append(dot(.034,(p[0]*1.012,p[1]*1.012,p[2]),DEEP,n,.3))
for k in range(10): a=k*math.pi/5; c.append(dot(.04,(.4*math.cos(a),.4*math.sin(a),.335),DEEP,(0,0,1),.3))
c.append(dot(.045,(0,0,.305),DEEP,(0,0,1),.3))
for sx in (-1,1): c.append(tube([((sx*.92,-.22,.96),.045),((sx*1.14,-.16,.93),.045),((sx*1.2,0,.92),.045),((sx*1.14,.16,.93),.045),((sx*.92,.22,.96),.045)],RED))
finish(c,"Colander")
# ---- ALARM CLOCK (hub) ----
k=[cyl(.5,.36,(0,0,0),RED,rot=(math.pi/2,0,0),v=64,bev=.06)]
k.append(cyl(.43,.04,(0,-.185,0),CREAM,rot=(math.pi/2,0,0),v=64,bev=.01)); k.append(torus(.45,.04,(0,-.18,0),GOLD,rot=(math.pi/2,0,0)))
for i in range(12):
    a=i*math.pi/6; k.append(dot(.035 if i%3 else .05,(.35*math.sin(a),-.207,.35*math.cos(a)),BLACK,th=.3))
k.append(tube([((0,-.22,0),.03),((.13,-.22,.16),.022)],BLACK,res=2)); k.append(tube([((0,-.225,0),.024),((-.2,-.225,.22),.016)],BLACK,res=2)); k.append(dot(.05,(0,-.225,0),GOLD,th=.5))
k.append(cyl(.42,.04,(0,.185,0),CREAM,rot=(math.pi/2,0,0),v=64,bev=.01))                               # back plate with winding keys
for x,z in ((-.17,.08),(.17,.08)):
    k.append(cyl(.03,.1,(x,.24,z),GOLD,rot=(math.pi/2,0,0),bev=0)); k.append(box((.16,.03,.1),(x,.3,z),GOLD,bev=.012))
k.append(cyl(.05,.05,(0,.21,-.2),GOLD,rot=(math.pi/2,0,0),bev=.01))
for i in range(5): k.append(dot(.025,(-.08+i*.04,.207,-.02-.0*i),BLACK,(0,1,0),.3))
for sx in (-1,1):
    b_=sph(.21,(sx*.3,0,.56),(1,1,.75),GOLD,24); rot(b_,(0,sx*.45,0),(sx*.3,0,.56)); k.append(b_)
    k.append(tube([((sx*.2,0,.42),.03),((sx*.28,0,.52),.03)],STEEL,res=2)); k.append(sph(.045,(sx*.36,0,.74),(1,1,1),STEEL,10))
    k.append(tube([((sx*.3,0,-.38),.05),((sx*.42,0,-.58),.035)],GOLD,res=2)); k.append(sph(.05,(sx*.43,0,-.6),(1,1,1),GOLD,10))
k.append(tube([((0,0,.48),.022),((0,0,.66),.022)],STEEL,res=2)); k.append(sph(.06,(0,0,.68),(1.4,1,1),STEEL,10))
k.append(tube([((-.3,0,.7),.03),((-.16,0,.88),.03),((.16,0,.88),.03),((.3,0,.7),.03)],GOLD))
finish(k,"AlarmClock",0.026)
# ---- TENNIS RACKET (sail) ----
t=[]; CZ=2.0; A,B=.52,.7
t.append(tube([((A*math.sin(a),0,CZ+B*math.cos(a)),.06) for a in [i*math.pi/12 for i in range(25)]],WOOD))
for i in range(-3,4):
    x=i*.13; h=B*math.sqrt(max(0,1-(x/A)**2)); t.append(tube([((x,0,CZ-h),.013),((x,0,CZ+h),.013)],CREAM,res=2))
for i in range(-4,5):
    z=i*.14; w=A*math.sqrt(max(0,1-(z/B)**2)); t.append(tube([((-w,0,CZ+z),.013),((w,0,CZ+z),.013)],CREAM,res=2))
for sx in (-1,1): t.append(tube([((sx*.3,0,CZ-.58),.05),((sx*.14,0,1.12),.05),((sx*.05,0,.95),.05)],WOOD))
t.append(lathe([(0.001,0),(.1,.02),(.105,.12),(.085,.16),(.08,.9),(.1,.96),(.1,1.04),(.06,1.1),(0.001,1.1)],DWOOD,32))
t.append(lathe([(.082,.18),(.1,.19),(.098,.86),(.08,.87)],RED,32))
for z in (.3,.44,.58,.72): t.append(torus(.1,.012,(0,0,z),DRED,rot=(.25,0,0)))
for z in (1.0,1.2): t.append(lathe([(.1,z-.04),(.115,z-.03),(.115,z+.03),(.1,z+.04)],CREAM,32,(1,.7,1)))
t.append(lathe([(0.001,-.02),(.11,0),(.11,.1),(0.001,.1)],GOLD,32))
finish(t,"TennisRacket",0.024)
# ---- CARPET BEATER (sail) : knotted rattan ----
cb=[]; R=.045
for ph in (0,math.pi):                                    # twisted double shaft
    cb.append(tube([((.05*math.cos(ph+z*5),.05*math.sin(ph+z*5),z),R) for z in [i*.08 for i in range(23)]],BREAD if ph==0 else WOOD,res=4))
HZ=2.35
def loop(cx,cz,rx,rz,ph,m_,n=24,yo=.03):
    return tube([((cx+rx*math.cos(ph+2*math.pi*i/n),yo*math.sin(3*2*math.pi*i/n),cz+rz*math.sin(ph+2*math.pi*i/n)),R) for i in range(n+1)],m_,res=4)
cb.append(loop(0,HZ,.62,.62,-math.pi/2,WOOD)); cb.append(loop(0,HZ+.02,.5,.5,-math.pi/2,BREAD,yo=-.03))
for a in (math.pi/2,math.pi/2+2.094,math.pi/2-2.094):
    cb.append(loop(.24*math.cos(a),HZ+.24*math.sin(a),.3,.3,0,BREAD if a==math.pi/2 else WOOD))
cb.append(loop(0,HZ,.16,.16,0,BREAD,yo=-.03))
for sx in (-1,1): cb.append(tube([((sx*.04,0,1.72),R),((sx*.2,0,1.82),R),((sx*.36,0,1.84),R)],WOOD,res=4))
cb.append(lathe([(.09,1.6),(.12,1.62),(.12,1.78),(.09,1.8)],RED,24)); cb.append(lathe([(.09,.02),(.12,.04),(.12,.5),(.09,.52)],RED,24)); cb.append(lathe([(0.001,-.03),(.11,-.01),(.11,.05),(0.001,.05)],GOLD,24))
finish(cb,"CarpetBeater",0.022)
# ---- FLY SWATTER (sail) ----
f=[lathe([(0.001,0),(.08,.02),(.1,.3),(.085,.6),(.05,.66),(0.001,.66)],RED,32)]
f.append(lathe([(.075,.08),(.095,.09),(.105,.3),(.09,.3)],CREAM,32)); f.append(lathe([(.045,.62),(.065,.63),(.065,.7),(.045,.71)],GOLD,32))
for ph in (0,math.pi): f.append(tube([((.03*math.cos(ph+z*9),.03*math.sin(ph+z*9),z),.024) for z in [.66+i*.06 for i in range(16)]],STEEL,res=4))
PW,PH,PZ=.4,.48,2.0
pad=chaikin([(-PW,PZ-PH),(PW,PZ-PH),(PW,PZ+PH),(-PW,PZ+PH)],2)
f.append(flat(pad,PETROL,.02,.03)); f.append(tube([((x,0,z),.035) for x,z in pad]+[((pad[0][0],0,pad[0][1]),.035)],DEEP,res=3))
for i in range(5):
    for j in range(6): f.append(dot(.04,(-.26+i*.13,-.052,PZ-.33+j*.132),DEEP,th=.3))
f.append(flat([(-.1,1.5),(.1,1.5),(.16,1.62),(-.16,1.62)],DEEP,.03,.03))
backfill(f); finish(f,"FlySwatter",0.024)
# ---- BUTTERFLY NET (sail) ----
n=[lathe([(0.001,0),(.05,.01),(.05,1.9),(0.001,1.9)],WOOD,24)]
n.append(lathe([(.045,.05),(.062,.06),(.062,.5),(.045,.51)],RED,24)); n.append(lathe([(.045,1.76),(.065,1.77),(.065,1.92),(.045,1.93)],GOLD,24))
bag=[lathe([(.5,0),(.46,-.3),(.34,-.7),(.16,-1.05),(0.001,-1.2)],CREAM,48), torus(.5,.04,(0,0,0),GOLD)]
for z,r_ in ((-.3,.465),(-.6,.385),(-.88,.255)): bag.append(lathe([(r_,z-.015),(r_+.012,z),(r_,z+.015)],PETROL,48))
for kk in range(10):
    a=kk*math.pi/5; bag.append(tube([((.5*math.cos(a),.5*math.sin(a),0),.012),((.4*math.cos(a),.4*math.sin(a),-.55),.012),((.2*math.cos(a),.2*math.sin(a),-1.0),.012),((0,0,-1.2),.01)],PETROL,res=3))
from mathutils import Euler
E_=Euler((math.radians(-25),math.radians(-100),0)); rim=min((E_.to_matrix()@Vector((.5*math.cos(a),.5*math.sin(a),0)) for a in [i*.1 for i in range(63)]),key=lambda v:v.z)
for o_ in bag: rot(o_,tuple(E_)); move(o_,(-rim.x,-rim.y,1.93-rim.z))      # hoop rim sits on the pole tip
n.append(sph(.07,(0,0,1.93),(1,1,1),GOLD,12))
n+=bag
finish(n,"ButterflyNet",0.022)
# ---- GLOVE (weathervane) : pointing white glove ----
g=[sph(1,(0,0,0),(.36,.23,.33),CREAM,32)]
g.append(tube([((.2,0,.14),.11),((.6,0,.17),.105),((.95,0,.18),.095)],CREAM)); g.append(sph(.095,(.96,0,.18),(1.15,1,1),CREAM,16))
for z in (.0,-.14,-.26): g.append(sph(.125,(.32,0,z),(1.1,1.3,.72),CREAM,16))
g.append(tube([((-.08,0,.2),.11),((0,0,.42),.1),((.14,0,.56),.09)],CREAM)); g.append(sph(.09,(.15,0,.57),(1,1,1),CREAM,16))
g.append(cyl(.31,.24,(-.42,0,0),CREAM,rot=(0,math.pi/2,0),r2=.26,bev=.04)); g.append(torus(.3,.05,(-.3,0,0),RED,rot=(0,math.pi/2,0))); g.append(cyl(.25,.02,(-.545,0,0),DEEP,rot=(0,math.pi/2,0),bev=0))
for z in (-.1,.02,.14): g.append(tube([((-.16,-.2,z),.016),((.06,-.215,z),.02)],BLACK,res=2))      # darts on the back of the hand
g.append(dot(.045,(-.3,.3,0),GOLD,(0,1,0),.5)); g.append(tube([((-.1,.2,-.12),.014),((.1,.21,-.02),.016),((.18,.19,.12),.012)],DROSE,res=3))   # palm side: button + crease
finish(g,"Glove",0.026)
lineup(OUT+"assets/lineup-s8.png",OUT+"blender/scene8.blend",res=(2600,900))
