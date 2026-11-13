import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from proplib import *
from proplib import _act
ORANGE=mat("Orange","#EE7B2B"); BULB=mat("BulbGlass","#FFE7A0",0.05)
# ============ SCENE 10 : GASTON LE GRAND ============
# ---- TOP HAT ----
th=[lathe([(0.001,.06),(.5,.06),(.9,.02),(1.03,.1),(1.02,.17),(.9,.11),(.53,.14),(.5,.55),(.56,1.42),(.61,1.52),(0.001,1.54)],BLACK,64)]
th.append(lathe([(.525,.15),(.545,.17),(.535,.44),(.512,.45)],RED,64)); th.append(lathe([(.6,1.5),(.625,1.52),(.6,1.55)],GOLD,64)); th.append(torus(1.025,.03,(0,0,.135),GOLD))
th.append(box((.26,.05,.26),(0,-.545,.3),GOLD,bev=.02)); th.append(box((.14,.06,.14),(0,-.55,.3),RED,bev=.01))
tk=flat([(-.12,0),(.12,0),(.12,.42),(-.12,.42)],CREAM,.012,.01); rot(tk,(0,.3,0)); move(tk,(.56,-.1,.3)); th.append(tk); th.append(dot(.04,(.6,-.115,.56),RED,th=.3))
backfill(th); finish(th,"TopHat")
# ---- GLOBE (head) ----
GZ=1.6; GR=.8
gl=[sph(GR,(0,0,GZ),(1,1,1),PETROL,48), torus(GR+.004,.014,(0,0,GZ),CREAM)]
LANDS=[(-5,28,.3),(15,-8,.24),(75,38,.3),(95,12,.2),(150,-22,.26),(-120,34,.3),(-98,-10,.24),(-55,52,.17),(125,50,.2),(-170,-40,.18),(200,25,.2),(40,62,.16)]
import random; random.seed(7)
for i,(lo,la,r_) in enumerate(LANDS):                    # ragged continents: clusters of overlapping patches
    mt=GREEN if i%4==1 else BREAD
    for j in range(7):
        lo2=math.radians(lo+random.uniform(-1,1)*r_*38); la2=math.radians(la+random.uniform(-1,1)*r_*38); rr=r_*random.uniform(.38,.7)
        n_=(math.cos(la2)*math.sin(lo2),-math.cos(la2)*math.cos(lo2),math.sin(la2))
        gl.append(dot(rr,(n_[0]*GR*.992,n_[1]*GR*.992,GZ+n_[2]*GR*.992),mt,n_,.14))
for la in (-50,-25,25,50):                               # latitude lines
    la2=math.radians(la); gl.append(torus(GR*math.cos(la2)+.003,.009,(0,0,GZ+GR*math.sin(la2)),CREAM))
for o_ in gl: rot(o_,(0,math.radians(20),0),(0,0,GZ))
ax=Vector((math.sin(math.radians(20)),0,math.cos(math.radians(20))))
gl.append(tube([((-.93*math.cos(a)*math.cos(math.radians(20))+.93*math.sin(a)*ax.x,0,GZ+.93*math.cos(a)*math.sin(math.radians(20))+.93*math.sin(a)*ax.z),.035) for a in [math.radians(-90+180*i/12) for i in range(13)]],GOLD))
for sg in (-1,1): gl.append(sph(.06,(sg*.93*ax.x,0,GZ+sg*.93*ax.z),(1,1,1),GOLD,12)); gl.append(tube([((sg*.8*ax.x,0,GZ+sg*.8*ax.z),.025),((sg*.93*ax.x,0,GZ+sg*.93*ax.z),.025)],GOLD,res=2))
gl.append(lathe([(0.001,0),(.5,0),(.52,.06),(.42,.14),(.16,.2),(.1,.3),(.13,.42),(.08,.5),(.08,.66),(.12,.7),(0.001,.72)],DWOOD,48))
for z,r_ in ((.07,.52),(.42,.135)): gl.append(lathe([(r_-.02,z-.03),(r_+.012,z-.02),(r_+.012,z+.02),(r_-.02,z+.03)],GOLD,48))
finish(gl,"Globe")
# ---- BICYCLE HANDLEBARS (moustache) ----
hb=[]; PATH=[(0,0),(.35,.03),(.68,.13),(.93,.03),(1.05,-.2),(.95,-.4),(.72,-.42)]
for sx in (-1,1):
    hb.append(tube([((sx*x,-.06*min(1,x),z),.055) for x,z in PATH],STEEL))
    hb.append(tube([((sx*1.03,-.06,-.27),.08),((sx*.95,-.06,-.4),.08),((sx*.72,-.06,-.42),.08)],CREAM,res=6)); hb.append(sph(.085,(sx*.7,-.06,-.42),(1,1,1),RED,12))
    for q in ((1.04,-.24),(.84,-.425)): hb.append(torus(.082,.016,(sx*q[0],-.06,q[1]),RED,rot=(0,math.pi/2 if q[0]<1 else .5*sx,0)))
hb.append(cyl(.09,.2,(0,0,0),GOLD,rot=(0,math.pi/2,0),bev=.03)); hb.append(tube([((0,0,0),.06),((0,.2,-.06),.06),((0,.3,-.25),.06),((0,.3,-.55),.06)],STEEL)); hb.append(cyl(.075,.1,(0,.3,-.56),GOLD,bev=.02))
hb.append(sph(.12,(.4,-.03,.14),(1,1,.7),GOLD,20)); hb.append(cyl(.03,.06,(.4,-.03,.07),STEEL,bev=0)); hb.append(sph(.035,(.4,-.03,.24),(1,1,1),RED,10)); hb.append(tube([((.5,-.03,.12),.014),((.56,-.03,.2),.014)],STEEL,res=2)); hb.append(sph(.03,(.57,-.03,.21),(1,1,1),RED,8))
finish(hb,"Handlebars",0.024)
# ---- LIGHT BULB (nose) ----
BP=[(0.001,1.02)]+[(.4*math.sin(a),.62+.4*math.cos(a)) for a in [math.radians(8+i*8) for i in range(15)]]+[(.3,.36),(.23,.24),(.19,.16),(.17,.1),(0.001,.1)]
lb=[lathe(BP,BULB,64)]
lb.append(lathe([(.17,.14),(.19,.12),(.19,-.14),(.13,-.22),(0.001,-.22)],GOLD,32))
for z in (.06,-.02,-.1): lb.append(torus(.19,.022,(0,0,z),GOLD,rot=(.12,0,0)))
lb.append(lathe([(0.001,-.3),(.06,-.28),(.09,-.22),(0.001,-.2)],BLACK,24))
F=[(-.08,.2),(-.1,.5),(-.16,.62),(-.08,.7),(-.04,.58),(0,.72),(.04,.58),(.08,.7),(.16,.62),(.1,.5),(.08,.2)]
def yb(x,z):
    P=[(1.02,0.001),(.98,.2),(.8,.36),(.6,.4),(.36,.33),(.18,.2)]
    for (z0,r0),(z1,r1) in zip(P,P[1:]):
        if z1<=z<=z0: r=r0+(r1-r0)*(z0-z)/(z0-z1); return -math.sqrt(max(0,r*r-x*x))
    return -.2
lb.append(tube([((x,yb(x,z)-.012,z),.02) for x,z in F],ORANGE,res=6)); lb.append(dot(.06,(-.17,yb(-.17,.74)+.012,.74),CREAM,(-.42,-.85,.3),.1))
backfill(lb); finish(lb,"LightBulb")
# ---- WINE BARREL (belly) ----
BH=2.2; br=lambda z:.72+.23*math.sin(math.pi*z/BH)
wb=[lathe([(0.001,.08),(br(0)-.04,.08),(br(0)-.04,0),(br(0),0)]+[(br(BH*i/16),BH*i/16) for i in range(1,17)]+[(br(BH)-.04,BH),(br(BH)-.04,BH-.08),(0.001,BH-.08)],WOOD,64)]
for kk in range(16):
    a=kk*math.pi/8+.1; wb.append(tube([(((br(z)+.004)*math.cos(a),(br(z)+.004)*math.sin(a),z),.014) for z in [BH*i/8 for i in range(9)]],DWOOD,res=3))
for z in (.16,.62,1.58,2.04): wb.append(lathe([(br(z-.07)+.012,z-.07),(br(z)+.035,z-.05),(br(z)+.035,z+.05),(br(z+.07)+.012,z+.07)],DEEP,64))
for z in (.16,2.04):
    for kk in range(8): a=kk*math.pi/4; wb.append(dot(.03,((br(z)+.04)*math.cos(a),(br(z)+.04)*math.sin(a),z),GOLD,(math.cos(a),math.sin(a),0),.5))
for kk in range(5): x=(kk-2)*.26; wb.append(box((.012,1.3*math.sqrt(max(.05,1-(x/.72)**2)),.012),(x,0,BH-.075),DWOOD,bev=0))
wb.append(cyl(.1,.1,(0,-br(1.1)-.02,1.1),DWOOD,rot=(math.pi/2,0,0),bev=.02))                                         # bung, front
wb.append(cyl(.05,.3,(0,-br(.4)-.1,.4),GOLD,rot=(math.pi/2,0,0),bev=.01)); wb.append(tube([((0,-br(.4)-.24,.4),.045),((0,-br(.4)-.3,.36),.045),((0,-br(.4)-.3,.26),.04)],GOLD,res=4)); wb.append(box((.2,.05,.05),(0,-br(.4)-.18,.5),RED,bev=.02)); wb.append(cyl(.02,.1,(0,-br(.4)-.18,.46),GOLD,bev=0))
star=[]
for i in range(10): a=math.pi/2+i*math.pi/5; rr=.2 if i%2==0 else .085; star.append((rr*math.cos(a),1.1+rr*math.sin(a)))
st=flat(star,RED,.015,.012,y=br(1.1)+.012); wb.append(st)                                                             # painted star, back
finish(wb,"Barrel")
# ---- MEGAPHONE ----
mg=[lathe([(0.001,.12),(.075,.12),(.52,1.6),(.5,1.64),(.44,1.6),(0.001,1.6)],RED,48)]
cone=lambda z:.075+.445*(z-.12)/1.48
for z0,z1 in ((.55,.75),(1.1,1.3)): mg.append(lathe([(cone(z0),z0),(cone(z0)+.016,z0+.01),(cone(z1)+.016,z1-.01),(cone(z1),z1)],CREAM,48))
mg.append(torus(.51,.04,(0,0,1.62),GOLD)); mg.append(lathe([(0.001,1.5),(.45,1.5),(.47,1.61),(0.001,1.61)],DEEP,48))
mg.append(lathe([(0.001,-.06),(.11,-.06),(.12,0),(.07,.06),(.075,.16),(0.001,.16)],GOLD,32)); mg.append(torus(.115,.02,(0,0,-.04),GOLD))
mg.append(tube([((cone(.5),0,.5),.035),((cone(.5)+.22,0,.62),.035),((cone(1.0)+.22,0,.95),.035),((cone(1.05),0,1.05),.035)],BLACK)); 
for z in (.5,1.05): mg.append(sph(.05,(cone(z),0,z),(1,1,1),GOLD,10))
for o_ in mg: rot(o_,(0,math.radians(72),0))
finish(mg,"Megaphone")
# ---- WALKING CANE ----
wc=[lathe([(0.001,0),(.04,.01),(.055,.3),(.065,2.55),(0.001,2.55)],BLACK,24)]
wc.append(lathe([(0.001,-.03),(.045,-.02),(.058,.26),(.04,.27)],GOLD,24)); wc.append(lathe([(.06,2.4),(.085,2.42),(.08,2.6),(.05,2.62)],GOLD,24)); wc.append(sph(.17,(0,0,2.76),(1,1,.95),GOLD,24))
wc.append(torus(.08,.02,(0,0,2.5),RED)); wc.append(dot(.05,(-.07,-.13,2.82),CREAM,(-.4,-.8,.4),.2))
wc.append(tube([((.064*math.cos(t*14),.064*math.sin(t*14),.4+t*1.95),.016) for t in [i/60 for i in range(61)]],RED,res=3))
finish(wc,"Cane",0.022)
# ---- BOWLING PIN (leg) ----
bp=[lathe([(0.001,0),(.2,0),(.27,.1),(.34,.55),(.31,.9),(.16,1.3),(.125,1.46),(.17,1.66),(.145,1.82),(.001,1.9)],CREAM,48)]
for z in (1.27,1.4): 
    r_=.17 if z<1.3 else .135; bp.append(lathe([(r_,z-.035),(r_+.02,z-.025),(r_+.012,z+.025),(r_-.008,z+.035)],RED,48))
bp.append(lathe([(.2,0),(.215,.0),(.285,.1),(.27,.1)],BLACK,48))
cw=flat([(-.12,.5),(-.14,.68),(-.07,.6),(0,.72),(.07,.6),(.14,.68),(.12,.5)],GOLD,.012,.01,y=-.345); bp.append(cw)
backfill(bp); finish(bp,"BowlingPin")
# ---- ROLLING PIN (leg) ----
rp=[lathe([(0.001,.5),(.2,.5),(.225,.56),(.225,1.64),(.2,1.7),(0.001,1.7)],WOOD,48)]
for z0,sg in ((.5,-1),(1.7,1)):
    rp.append(lathe([(0.001,z0),(.07,z0),(.05,z0+sg*.1),(.08,z0+sg*.3),(.085,z0+sg*.42),(.04,z0+sg*.5),(0.001,z0+sg*.5)][::(1 if sg>0 else -1)],RED,32))
    rp.append(torus(.07,.022,(0,0,z0+sg*.03),GOLD))
rp.append(lathe([(.225,.9),(.24,.91),(.24,1.29),(.225,1.3)],CREAM,48))
for kk in range(8): a=kk*math.pi/4; rp.append(dot(.06,(.243*math.cos(a),.243*math.sin(a),1.1),RED,(math.cos(a),math.sin(a),0),.3))
for z in (.9,1.3): rp.append(torus(.235,.016,(0,0,z),GOLD))
finish(rp,"RollingPin")
# ---- SCRUB BRUSH (epaulette) ----
sb=[box((1.4,.56,.3),(0,0,.7),WOOD,bev=.13), box((1.42,.58,.06),(0,0,.66),RED,bev=.02)]
sb.append(box((1.26,.46,.1),(0,0,.52),DWOOD,bev=.03))
for i in range(11):
    for j in range(4):
        x=-.58+i*.116; y=-.18+j*.12; o_=cyl(.07,.5,(x,y,.27),CREAM if (i+j)%2 else BREAD,r2=.045,v=10,bev=0); rot(o_,(-y*.9,x*.32,0),(x,y,.5)); sb.append(o_)
sb.append(torus(.08,.025,(.74,0,.72),GOLD,rot=(math.pi/2,0,0))); sb.append(tube([((-.4,0,.86),.025),((.4,0,.86),.025)],DWOOD,res=2))
finish(sb,"ScrubBrush",0.022)
lineup(OUT+"assets/lineup-s10.png",OUT+"blender/scene10.blend",res=(3000,900))
