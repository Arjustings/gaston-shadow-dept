import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from proplib import *
from proplib import _act
LPETROL=mat("LightPetrol","#3F9DB0")
# ============ SCENE 4 : PINOCCHIO ============
# ---- BALL OF WOOL (head) : wound bands of strand, loose tail ----
y=[sph(1.0,(0,0,0),(1,1,1),DEEP,32)]; R=1.06
G=(((0,0,0),PETROL,(-.63,-.42,-.21,0,.21,.42,.63)),((1.3,0,.6),LPETROL,(-.3,-.1,.1,.3)),((.5,1.2,0),PETROL,(-.3,-.1,.1,.3)),((-.8,.4,1.2),LPETROL,(-.2,0,.2)),((.25,-.7,.2),PETROL,(-.1,.1)))
for gi,(e,mt,ds) in enumerate(G):
    rr=R+gi*.055
    for d in ds:
        t=torus(math.sqrt(rr*rr-d*d),.11,(0,0,d),mt); rot(t,e); y.append(t)
y.append(tube([((.75,-.6,-.6),.1),((1.1,-.5,-.95),.1),((1.5,-.3,-.9),.1),((1.75,-.2,-1.1),.095),((1.7,-.1,-1.35),.09),((1.45,0,-1.38),.08)],LPETROL))
finish(y,"YarnBall")
# ---- FUNNEL (hat) : tin, red band, loop handle; stands spout-up ----
f=[lathe([(0.001,.02),(.78,.02),(.8,.06),(.17,.98),(.13,1.08),(.1,1.72),(.075,1.74),(0.001,1.74)],STEEL)]
f.append(torus(.8,.06,(0,0,.04),GOLD)); f.append(lathe([(.6,.3),(.63,.31),(.475,.555),(.45,.55)],RED))
f.append(lathe([(.17,.96),(.2,.99),(.16,1.1),(.13,1.08)],GOLD))
f.append(torus(.2,.045,(.62,0,.55),STEEL,rot=(math.pi/2,0,0))); 
finish(f,"Funnel")
# ---- PAINTBRUSH (nose) : red handle, brass ferrule, loaded tip ----
b=[lathe([(0.001,0),(.07,.02),(.105,.3),(.135,.95),(.12,1.3),(.001,1.32)],RED)]
b.append(lathe([(.075,.06),(.09,.07),(.108,.2),(.095,.21)],CREAM))
b.append(lathe([(.115,1.26),(.135,1.28),(.15,1.62),(.13,1.64)],GOLD))
for z in (1.36,1.52): b.append(torus(.145,.022,(0,0,z),GOLD))
b.append(lathe([(0.001,1.6),(.15,1.62),(.2,1.85),(.18,2.08),(.1,2.3),(.001,2.38)],CREAM,48,(1,.6,1)))
b.append(lathe([(.185,2.0),(.19,2.08),(.11,2.3),(.001,2.4)],PETROL,48,(1.04,.66,1)))
b.append(sph(.07,(.12,-.08,1.96),(1,1,1.6),PETROL,12))
finish(b,"Paintbrush")
# ---- QUILL (hat feather) : curved plume, brass nib ----
N=36;Lp=[];Rp=[]
for i in range(N+1):
    t=i/N; cx=.3*math.sin(math.pi*t*.85); z=.55+2.0*t
    w=.42*math.sin(math.pi*(t**.7))**.8
    wl=w*(.5 if abs(t-.4)<.022 else 1); wr=w*.78*(.45 if abs(t-.64)<.022 or abs(t-.27)<.022 else 1)
    Lp.append((cx-wl,z)); Rp.append((cx+wr,z))
q=[flat(Lp+Rp[::-1],PETROL,.025,.02)]
q.append(tube([((0,0,.12),.05),((0.01,-.04,.55),.05),((.15,-.045,1.3),.04),((.3,-.045,2.0),.028),((.22,-.04,2.5),.012)],CREAM))
for i in range(5):                                      # barb strokes
    t=.25+i*.13; cx=.3*math.sin(math.pi*t*.85); z=.55+2.0*t
    q.append(tube([((cx,-.05,z),.014),((cx-.2,-.05,z+.16),.012)],LPETROL)); q.append(tube([((cx,-.05,z),.014),((cx+.16,-.05,z+.15),.012)],LPETROL))
q.append(lathe([(.05,.1),(.065,.12),(.065,.3),(.05,.32)],GOLD))
q.append(flat([(0,-.18),(.055,.02),(.05,.13),(-.05,.13),(-.055,.02)],GOLD,.02,.015))
backfill(q); finish(q,"Quill",0.024)
# ---- RUFF COLLAR : pleated cream ring, red piping ----
NP=18
def rf(u,v):
    th=2*math.pi*u; r=.5+.82*v; z=.17*(.25+.75*v)*math.sin(NP*th)-.08*v*v
    return (r*math.cos(th),r*math.sin(th),z)
r_=[surf(rf,NP*12,6,CREAM,thick=.06,closed_u=True)]
r_.append(tube([(rf(i/(NP*8),1),.04) for i in range(NP*8+1)],RED,res=4))
r_.append(torus(.5,.1,(0,0,.03),GOLD)); r_.append(lathe([(0.001,-.05),(.48,-.05),(.48,.0),(0.001,0)],DEEP))
for o_ in r_: rot(o_,(math.radians(-32),0,0))
finish(r_,"Ruff",0.022)
# ============ SCENE 5 : LA MONTGOLFIERE ============
# ---- PAPER LANTERN (balloon) : ribbed red globe ----
prof=[(0.001,-1.33)]
for i in range(1,48):
    t=i/48; a=math.pi*(t-.5); rr=1.5*math.cos(a)**.85+.022*math.cos(i*math.pi*2/3); prof.append((max(.3,rr),1.33*math.sin(a)))
prof.append((0.001,1.33))
l=[lathe(prof,RED,64)]
def band(z0,z1,m_):
    P=[]
    for i in range(9):
        z=z0+(z1-z0)*i/8; a=math.asin(max(-1,min(1,z/1.33))); P.append((1.5*math.cos(a)**.85+.035,z))
    return lathe([(P[0][0]-.05,P[0][1])]+P+[(P[-1][0]-.05,P[-1][1])],m_,64)
l.append(band(-.32,.32,CREAM))
for z in (-.42,.42): l.append(band(z-.035,z+.035,GOLD))
for k in range(8):
    a=k*math.pi/4; d=flat([(0,.2),(.16,0),(0,-.2),(-.16,0)],RED,.02,.015,y=-1.545); rot(d,(0,0,a)); l.append(d)
for z,sg in ((1.36,1),(-1.36,-1)):
    l.append(cyl(.4,.16,(0,0,z),BLACK,bev=.04)); l.append(torus(.4,.035,(0,0,z+sg*.07),GOLD))
l.append(torus(.16,.035,(0,0,1.58),GOLD,rot=(math.pi/2,0,0)))
l.append(cyl(.035,.16,(0,0,-1.5),GOLD,bev=0)); l.append(lathe([(0.001,-1.56),(.09,-1.6),(.12,-1.9),(.001,-1.92)],GOLD,24))
finish(l,"Lantern")
# ---- PICNIC BASKET : wicker hamper, hoop handle, gingham cloth ----
k=[lathe([(0.001,0),(.62,0),(.7,.06),(.84,.86),(.8,.92),(0.001,.95)],BREAD,64,(1,.72,1))]
for i in range(6):
    z=.1+i*.135; rr=.71+.145*(z-.06)/.8
    k.append(lathe([(rr-.01,z-.05),(rr+.035,z-.02),(rr+.035,z+.02),(rr-.01,z+.05)],WOOD if i%2==0 else BREAD,64,(1,.72,1)))
for i in range(14):
    a=i*2*math.pi/14+.2; x0,y0=.72*math.cos(a),.72*.72*math.sin(a); x1,y1=.87*math.cos(a),.87*.72*math.sin(a)
    k.append(tube([((x0,y0,.05),.035),((x1,y1,.88),.035)],DWOOD,res=4))
k.append(lathe([(.8,.86),(.9,.9),(.9,.98),(.8,1.0)],WOOD,64,(1,.72,1)))
k.append(lathe([(.82,.96),(.6,1.07),(0.001,1.1)],BREAD,64,(1,.72,1))); k.append(box((.09,1.26,.07),(0,0,1.1),DWOOD))
k.append(tube([((-.84,0,.95),.065),((-.72,0,1.5),.065),((0,0,1.85),.065),((.72,0,1.5),.065),((.84,0,.95),.065)],WOOD))
c=flat([(-.42,.98),(.3,.98),(.36,.9),(.1,.5),(-.02,.42),(-.2,.62),(-.46,.86)],RED,.03,.025,y=-.67); k.append(c)
for x,z in ((-.25,.86),(-.02,.86),(.2,.86),(-.14,.7),(.08,.68),(-.02,.54)): k.append(dot(.045,(x,-.73,z),CREAM,th=.3))
backfill(k); finish(k,"Basket")
# ---- DRUMSTICK (ropes, used twice) ----
d=[lathe([(0.001,0),(.07,.02),(.078,1.5),(.048,1.9),(.042,1.96),(.085,2.03),(.08,2.12),(.001,2.16)],WOOD,32)]
d.append(lathe([(.074,.14),(.092,.16),(.094,.56),(.076,.58)],RED,32))
for z in (.14,.58): d.append(torus(.09,.02,(0,0,z),GOLD))
finish(d,"Drumstick",0.024)
# ---- PENNANT : striped flag on a short staff ----
p=[tube([((0,0,0),.045),((0,0,1.5),.045)],WOOD,res=2), sph(.09,(0,0,1.56),(1,1,1),GOLD,16)]
ft=lambda x:1.42-.29*x; fb=lambda x:.72+.29*x
p.append(flat([(.03,1.42),(1.2,1.07),(.03,.72)],RED,.03,.025))
for x0,x1 in ((.25,.45),(.65,.82)): p.append(flat([(x0,ft(x0)-.02),(x1,ft(x1)-.02),(x1,fb(x1)+.02),(x0,fb(x0)+.02)],CREAM,.04,.02))
p.append(dot(.07,(.12,-.06,1.07),GOLD,th=.3))
finish(p,"Pennant",0.024)
lineup(OUT+"assets/lineup-s45.png",OUT+"blender/scene45.blend",res=(2600,900))
