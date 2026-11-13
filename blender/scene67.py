import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from proplib import *
from proplib import _act
VARN=mat("Varnish","#C8642A",0.14)
def spline(K,z):
    for (z0,w0),(z1,w1) in zip(K,K[1:]):
        if z0<=z<=z1: t=(z-z0)/(z1-z0); t=t*t*(3-2*t); return w0+(w1-w0)*t
    return 0
def edot(r,c,abc,x,z,m,th=.25):
    """Spot on the front (-Y) of an ellipsoid centred c with radii abc, at world x,z."""
    a,b,cc=abc; u=(x-c[0])/a; w=(z-c[2])/cc; y=-b*math.sqrt(max(0,1-u*u-w*w))
    return dot(r,(x,c[1]+y,z),m,(u/a,y/(b*b),w/cc),th)
# ============ SCENE 6 : LE VOILIER ============
# ---- VIOLIN (hull) ----
K=[(0,0),(.04,.3),(.2,.57),(.45,.63),(.75,.56),(.95,.4),(1.05,.35),(1.15,.4),(1.3,.48),(1.55,.5),(1.8,.42),(1.95,.2),(2.0,0)]
ZZ=[2.0*i/80 for i in range(81)]
v=[flat([(spline(K,z),z) for z in ZZ]+[(-spline(K,z),z) for z in reversed(ZZ)][1:-1],VARN,.12,.1)]
FY=-.22
for sx in (-1,1):                                         # f-holes
    v.append(tube([((sx*.27,FY,.8),.012),((sx*.2,FY-.01,.9),.035),((sx*.25,FY-.01,1.1),.035),((sx*.18,FY,1.2),.012)],BLACK))
    v.append(sph(.045,(sx*.28,FY,.78),(1,.5,1),BLACK,12)); v.append(sph(.045,(sx*.17,FY,1.22),(1,.5,1),BLACK,12))
v.append(flat([(-.1,.06),(.1,.06),(.16,.6),(-.16,.6)],BLACK,.03,.03,y=FY-.02))          # tailpiece
v.append(sph(.2,(-.36,FY,.22),(1,.3,.75),BLACK,20))                                    # chinrest
v.append(flat([(-.2,.86),(-.16,1.0),(.16,1.0),(.2,.86)],CREAM,.03,.02,y=FY-.04))       # bridge
v.append(box((.15,.14,1.05),(0,-.02,2.45),VARN,bev=.04))                               # neck
v.append(flat([(-.1,1.25),(.1,1.25),(.07,2.9),(-.07,2.9)],BLACK,.03,.03,y=FY-.03))     # fingerboard
for i in range(4): x=(i-1.5)*.045; v.append(tube([((x*1.6,FY-.09,.5),.012),((x*1.5,FY-.11,.93),.012),((x,FY-.09,2.92),.012)],CREAM,res=2))   # strings
v.append(box((.2,.2,.42),(0,0,3.1),VARN,bev=.05))                                      # pegbox
for i,(sx,z) in enumerate(((-1,3.0),(1,3.08),(-1,3.16),(1,3.24))):
    v.append(cyl(.03,.2,(sx*.18,0,z),BLACK,rot=(0,math.pi/2,0),bev=0)); v.append(sph(.07,(sx*.3,0,z),(.6,1,1.3),BLACK,12))
v.append(tube([((0,0,3.3),.09),((.0,0,3.48),.09),((.12,0,3.58),.08),((.22,0,3.48),.07),((.15,0,3.38),.06),((.1,0,3.44),.045)],VARN))   # scroll
finish(v,"Violin")
# ---- BROOM (mast) ----
b=[tube([((0,0,1.25),.075),((.05,0,2.0),.07),((-.04,0,2.9),.068),((.06,0,3.7),.065),((0,0,4.4),.06)],DWOOD)]
b.append(sph(.075,(0,0,4.42),(1,1,1),DWOOD,12)); b.append(sph(.05,(.07,-.03,3.05),(1,1,1.4),DWOOD,10))
b.append(lathe([(.1,1.5),(.17,1.42),(.24,1.2),(.46,.5),(.56,.08),(.5,0),(0.001,0)],BREAD,48,(1,.62,1)))
NSTR=22
for i in range(NSTR):                                     # straws all the way round the bundle
    ph=2*math.pi*i/NSTR+.1; cx,cy=math.cos(ph),.62*math.sin(ph); jz=-.05-.07*((i*7)%3)/2
    b.append(tube([((.19*cx,.19*cy,1.32),.03),((.36*cx,.36*cy,.78),.036),((.55*cx,.55*cy,.2),.036),((.6*cx,.6*cy,jz),.016)],WOOD if i%2 else BREAD,res=4))
for i in range(9):                                        # ragged inner tufts
    ph=2*math.pi*i/9; b.append(tube([((.3*math.cos(ph),.18*math.sin(ph),.3),.05),((.36*math.cos(ph),.22*math.sin(ph),-.1-.05*(i%3)),.012)],BREAD,res=3))
for z,rr in ((1.36,.2),(1.24,.245)): b.append(lathe([(rr-.02,z-.045),(rr+.03,z-.025),(rr+.03,z+.025),(rr-.02,z+.045)],RED,48,(1,.66,1)))
b.append(lathe([(.215,1.27),(.25,1.285),(.25,1.315),(.215,1.33)],GOLD,48,(1,.66,1)))
finish(b,"Broom")
# ---- BLOOMERS (mainsail) ----
HIP=((0,0,1.32),(1.02,.36,.6)); LEG=lambda sx:((sx*.52,0,.78),(.56,.33,.62))
bl=[sph(1,HIP[0],HIP[1],CREAM,40)]
for sx in (-1,1):
    c,abc=LEG(sx); bl.append(sph(1,c,abc,CREAM,40))
    bl.append(lathe([(.26,.2),(.33,.22),(.33,.34),(.26,.36)],RED,32,(1,.8,1),(sx*.52,0,0)))                 # knee band
    def fr(u,v,sx=sx):
        th=2*math.pi*u; r=.3+.2*v+.035*v*math.sin(12*th); return (sx*.52+r*math.cos(th),.8*r*math.sin(th),.24-.26*v)
    bl.append(surf(fr,96,3,CREAM,thick=.05,closed_u=True))                                                    # frill
    for sy in (-1,1): bl.append(sph(.09,(sx*.52+sy*.1,-.29,.28),(1,.5,.7),RED,12,rot=(0,sy*.5,0)))
    bl.append(sph(.045,(sx*.52,-.31,.28),(1,1,1),GOLD,10))
    for x,z in ((.3,.62),(.62,.9),(.42,1.02),(.74,.6)): bl.append(edot(.075,c,abc,sx*x,z,RED))
for x,z in ((0,1.2),(-.35,1.45),(.35,1.45),(-.7,1.3),(.7,1.3),(0,1.62),(-.22,.98),(.22,.98)): bl.append(edot(.075,HIP[0],HIP[1],x,z,RED))
bl.append(lathe([(.7,1.72),(.76,1.75),(.76,1.92),(.7,1.95),(0.001,1.95)],CREAM,48,(1,.42,1)))                 # waistband
for i in range(9): x=(i-4)*.17; bl.append(tube([((x,-.325*math.sqrt(1-(x/.78)**2),1.74),.016),((x,-.325*math.sqrt(1-(x/.78)**2),1.93),.016)],DROSE,res=2))
for sx in (-1,1):
    bl.append(sph(.1,(sx*.1,-.33,1.83),(1,.5,.65),RED,12,rot=(0,sx*.5,0))); bl.append(tube([((0,-.34,1.82),.025),((sx*.08,-.36,1.6),.025),((sx*.14,-.37,1.46),.02)],RED,res=4))
bl.append(sph(.05,(0,-.36,1.83),(1,1,1),GOLD,10))
backfill(bl); finish(bl,"Bloomers")
# ---- COAT HANGER (jib) ----
h=[]
for sx in (-1,1):
    h.append(tube([((0,0,.78),.075),((sx*.5,0,.62),.07),((sx*1.0,0,.26),.06)],WOOD)); h.append(sph(.075,(sx*1.02,0,.24),(1,1,1),WOOD,12))
h.append(tube([((-1.0,0,.24),.045),((1.0,0,.24),.045)],WOOD,res=2))
h.append(cyl(.09,.14,(0,0,.82),GOLD,bev=.03))
h.append(tube([((0,0,.86),.035),((0,0,1.05),.035),((.17,0,1.26),.035),((.05,0,1.46),.035),((-.15,0,1.4),.035),((-.2,0,1.28),.03)],STEEL))
finish(h,"Hanger",0.024)
# ---- SOCK (flag) : striped, darned heel and toe ----
s=[tube([((0,0,1.32),.25),((0,0,.6),.25),((.04,0,.36),.26),((.3,0,.24),.25),((.72,0,.24),.23)],CREAM)]
for z in (.62,.84,1.06): s.append(lathe([(.23,z-.06),(.265,z-.05),(.265,z+.05),(.23,z+.06)],RED,32))
s.append(lathe([(.23,1.2),(.285,1.22),(.285,1.36),(.23,1.38),(0.001,1.38)],GOLD,32))
s.append(sph(.25,(.76,0,.24),(1,1,.96),RED,24)); s.append(sph(.27,(-.02,0,.3),(1,.98,1),RED,24))
for o_ in s: o_.scale.y=.7; _act(o_); bpy.ops.object.transform_apply(scale=True)
finish(s,"Sock")
# ---- CORKSCREW (anchor) ----
c=[lathe([(0.001,-.5),(.09,-.48),(.13,-.3),(.15,0),(.13,.3),(.09,.48),(0.001,.5)],WOOD,32)]; rot(c[0],(0,math.pi/2,0)); move(c[0],(0,0,1.05))
for sx in (-1,1): c.append(torus(.125,.022,(sx*.3,0,1.05),GOLD,rot=(0,math.pi/2,0)))
c.append(cyl(.075,.12,(0,0,.9),GOLD,bev=.02)); c.append(tube([((0,0,.9),.04),((0,0,.62),.04)],STEEL,res=2))
H=[]
for i in range(41):
    t=i/40; a=t*4.5*2*math.pi; r=.11*min(1,t*8)*(1-.25*t); H.append(((r*math.cos(a),r*math.sin(a),.62-.62*t),.036*(1-.6*t**3)))
c.append(tube(H,STEEL,res=6))
finish(c,"Corkscrew",0.022)
# ============ SCENE 7 : L'ELEPHANT ============
# ---- BASS DRUM (body) : faces the lamp ----
d=[cyl(1.4,1.1,(0,0,0),RED,rot=(math.pi/2,0,0),v=64)]
for sy in (-1,1):
    d.append(cyl(1.34,.06,(0,sy*.56,0),CREAM,rot=(math.pi/2,0,0),v=64,bev=.02)); d.append(torus(1.42,.09,(0,sy*.52,0),GOLD,rot=(math.pi/2,0,0)))
P=[]
for i in range(10): a=math.pi/2+i*math.pi/5; rr=.78 if i%2==0 else .32; P.append((rr*math.cos(a),rr*math.sin(a)))
d.append(flat(P,RED,.02,.02,y=-.6)); d.append(torus(1.06,.03,(0,-.59,0),RED,rot=(math.pi/2,0,0)))
for i in range(10):
    a=i*math.pi/5+.3; d.append(box((.12,.2,.2),(1.45*math.cos(a),-.5,1.45*math.sin(a)),BLACK,rot=(0,-a,0),bev=.03))
    a2=a+math.pi/10; d.append(tube([((1.44*math.cos(a),-.44,1.44*math.sin(a)),.025),((1.46*math.cos(a2),0,1.46*math.sin(a2)),.025),((1.44*math.cos(a+math.pi/5),.44,1.44*math.sin(a+math.pi/5)),.025)],CREAM,res=3))
backfill(d); finish(d,"BassDrum")
# ---- TRUMPET (trunk) ----
t=[tube([((-1.3,0,.2),.045),((-.2,0,.2),.05),((.45,0,.2),.065),((.9,0,.2),.13),((1.18,0,.2),.27),((1.32,0,.2),.45)],GOLD)]
t.append(torus(.45,.04,(1.32,0,.2),GOLD,rot=(0,math.pi/2,0))); t.append(cyl(.4,.03,(1.325,0,.2),DWOOD,rot=(0,math.pi/2,0),bev=0))
t.append(tube([((-.3,0,.2),.045),((-.85,0,.2),.045),((-1.0,0,.02),.045),((-.85,0,-.16),.045),((.3,0,-.16),.045),((.46,0,.02),.045),((.36,0,.17),.045)],GOLD))
for i,x in enumerate((-.42,-.2,.02)):
    t.append(cyl(.075,.62,(x,0,.06),GOLD,bev=.02)); t.append(cyl(.085,.07,(x,0,-.25),DWOOD,bev=.02))
    t.append(cyl(.025,.14,(x,0,.43),STEEL,bev=0)); t.append(cyl(.06,.05,(x,0,.5),RED,bev=.02)); t.append(torus(.08,.018,(x,0,.3),RED))
t.append(cyl(.1,.16,(-1.38,0,.2),GOLD,rot=(0,math.pi/2,0),r2=.045,bev=0)); t.append(torus(.1,.02,(-1.46,0,.2),GOLD,rot=(0,math.pi/2,0)))
t.append(tube([((-.62,0,.2),.02),((-.62,0,-.16),.02)],GOLD,res=2)); t.append(torus(.07,.02,(.62,0,.2),RED,rot=(0,math.pi/2,0)))
finish(t,"Trumpet",0.026)
# ---- TAMBOURINE (ear) : faces the lamp ----
tm=[cyl(.75,.3,(0,0,0),WOOD,rot=(math.pi/2,0,0),v=64,bev=.03), cyl(.69,.06,(0,-.14,0),CREAM,rot=(math.pi/2,0,0),v=64,bev=.02), cyl(.69,.06,(0,.14,0),DWOOD,rot=(math.pi/2,0,0),v=64,bev=.02)]
tm.append(torus(.5,.03,(0,-.17,0),RED,rot=(math.pi/2,0,0)))
P=[]
for i in range(10): a=math.pi/2+i*math.pi/5; rr=.3 if i%2==0 else .13; P.append((rr*math.cos(a),rr*math.sin(a)))
tm.append(flat(P,RED,.015,.015,y=-.175))
for i in range(6):
    a=i*math.pi/3+.52
    for sy in (-.07,.07): tm.append(cyl(.14,.035,(.8*math.cos(a),sy,.8*math.sin(a)),GOLD,rot=(math.pi/2,0,0),bev=.012))
    tm.append(box((.3,.2,.06),(.73*math.cos(a),0,.73*math.sin(a)),BLACK,rot=(0,math.pi/2-a,0),bev=.01))
finish(tm,"Tambourine",0.026)
# ---- JUGGLING CLUB (leg) ----
j=[lathe([(0.001,0),(.11,.02),(.12,.11),(.07,.19),(.055,.35),(.06,1.1),(.1,1.35),(.2,1.65),(.265,1.95),(.25,2.15),(.15,2.34),(.001,2.4)],CREAM,40)]
j.append(lathe([(.058,.22),(.078,.23),(.082,1.08),(.064,1.1)],RED,40)); j.append(lathe([(0.001,-.01),(.115,.01),(.125,.11),(.075,.19),(0.001,.19)],GOLD,40))
for z,r_ in ((1.12,.068),(1.4,.118),(2.14,.26)): j.append(lathe([(r_-.02,z-.03),(r_+.012,z-.02),(r_+.012,z+.02),(r_-.02,z+.03)],GOLD,40))
j.append(lathe([(.2,1.62),(.215,1.63),(.282,1.95),(.27,2.08),(.255,2.08)],RED,40))
for k_ in range(6):
    a=k_*math.pi/3; dd=flat([(0,.13),(.09,0),(0,-.13),(-.09,0)],CREAM,.015,.012,y=-.28); move(dd,(0,0,1.9)); rot(dd,(0,0,a)); j.append(dd)
j.append(lathe([(.155,2.32),(.16,2.34),(.001,2.42)],RED,40))
finish(j,"JugglingClub")
# ---- MILK BOTTLE (leg) ----
mb=[lathe([(0.001,0),(.36,0),(.4,.05),(.4,.8),(.34,1.0),(.21,1.2),(.18,1.36),(.23,1.39),(.23,1.45),(0.001,1.46)],CREAM,48)]
mb.append(lathe([(.4,.3),(.418,.32),(.418,.68),(.4,.7)],PETROL,48))
for z in (.34,.66): mb.append(lathe([(.415,z-.02),(.425,z-.012),(.425,z+.012),(.415,z+.02)],GOLD,48))
mb.append(dot(.11,(0,-.42,.5),CREAM,th=.2)); mb.append(dot(.05,(-.16,-.39,.56),CREAM,(-.35,-1,0),th=.25)); mb.append(dot(.04,(.15,-.39,.44),CREAM,(.35,-1,0),th=.25))
mb.append(lathe([(.19,1.3),(.25,1.33),(.26,1.44),(.2,1.5),(0.001,1.51)],RED,48))
mb.append(lathe([(.34,.99),(.35,1.0),(.33,1.04),(.32,1.03)],STEEL,48))
backfill(mb); finish(mb,"MilkBottle")
# ---- BOOT (leg) ----
bo=[flat(chaikin([(-.5,.16),(-.54,.9),(-.5,1.62),(.16,1.62),(.2,1.1),(.3,.84),(.62,.74),(.92,.62),(1.06,.4),(1.04,.16)],3),DWOOD,.2,.17)]
bo.append(flat(chaikin([(-.6,0),(-.6,.2),(1.08,.2),(1.12,.1),(1.06,0),(.24,0),(.16,.1),(-.2,.1),(-.26,0)],1),BLACK,.34,.04))
bo.append(flat(chaikin([(-.6,1.4),(-.64,1.76),(-.5,1.86),(.2,1.86),(.3,1.76),(.26,1.4)],2),BREAD,.24,.15))
BODY=chaikin([(-.5,.16),(-.54,.9),(-.5,1.62),(.16,1.62),(.2,1.1),(.3,.84),(.62,.74),(.92,.62),(1.06,.4),(1.04,.16)],3)
TOE=[(x,z) for x,z in BODY if x>.66]; TOE.sort(key=lambda q:math.atan2(q[1]-.4,q[0]-.7))
TOE=[(.66+(x-.66)*1.035+.004,.42+(z-.42)*1.05) for x,z in TOE]
bo.append(flat(TOE,WOOD,.215,.18))                                                    # toe cap wraps the whole toe
bo.append(tube([((.665,-.4,.2),.02),((.665,-.42,.45),.022),((.665,-.36,.74),.02)],BLACK,res=3)); bo.append(tube([((.665,.4,.2),.02),((.665,.42,.45),.022),((.665,.36,.74),.02)],BLACK,res=3))
bo.append(flat([(-.56,.86),(.22,.98),(.24,1.14),(-.56,1.02)],BLACK,.36,.04))
bo.append(box((.26,.06,.3),(-.12,-.42,1.0),GOLD,rot=(0,-.16,0),bev=.02)); bo.append(box((.14,.07,.18),(-.12,-.43,1.0),BLACK,rot=(0,-.16,0),bev=.01))
for i in range(4): bo.append(tube([((-.42+i*.18,-.4,1.5),.02),((-.42+i*.18,-.4,1.72),.02)],DWOOD,res=2))
bo.append(tube([((-.6,0,1.84),.035),((-.74,0,2.0),.035),((-.62,0,2.12),.035),((-.5,0,1.88),.035)],BREAD,res=6))
backfill(bo); finish(bo,"Boot")
# ---- PEPPER MILL (leg) ----
pm=[lathe([(0.001,0),(.3,0),(.32,.06),(.27,.2),(.2,.5),(.24,.8),(.31,.95),(.31,1.02),(.2,1.08),(.17,1.15),(.25,1.3),(.25,1.42),(.13,1.52),(.001,1.55)],DWOOD,48)]
for z,r_ in ((.06,.325),(.985,.315),(1.36,.255)): pm.append(lathe([(r_-.02,z-.035),(r_+.012,z-.022),(r_+.012,z+.022),(r_-.02,z+.035)],GOLD,48))
pm.append(lathe([(.2,1.07),(.215,1.08),(.185,1.15),(.17,1.15)],CREAM,48)); pm.append(sph(.09,(0,0,1.6),(1,1,1),GOLD,16)); pm.append(cyl(.03,.08,(0,0,1.54),GOLD,bev=0))
pm.append(lathe([(.215,.42),(.225,.44),(.24,.6),(.228,.62)],RED,48))
finish(pm,"PepperMill")
lineup(OUT+"assets/lineup-s67.png",OUT+"blender/scene67.blend",res=(3000,900))
