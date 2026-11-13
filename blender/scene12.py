import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from proplib import *
from proplib import _act
# ============ SCENE 1 : LE LAPIN ============
# ---- WATERMELON (head) : striped, curly stem ----
LGREEN=mat("LightGreen","#93C25B",0.08); LROSE=mat("LightRose","#F7CFC6",0.05)
def surf(fn,nu,nv,m):
    """Mesh from fn(u,v)->xyz on a nu x nv grid (u,v in 0..1)."""
    bm=bmesh.new(); V=[[bm.verts.new(fn(i/nu,j/nv)) for j in range(nv+1)] for i in range(nu+1)]
    for i in range(nu):
        for j in range(nv): bm.faces.new((V[i][j],V[i+1][j],V[i+1][j+1],V[i][j+1]))
    me=bpy.data.meshes.new("s"); bm.to_mesh(me); bm.free(); o=bpy.data.objects.new("s",me); C.scene.collection.objects.link(o); return smooth(o,m)
RM=1.1; ZS=1.0
m=[sph(RM,(0,0,0),(1,1,ZS),GREEN,64)]
NS=11
for k in range(NS):                                      # narrow dark zigzag stripes converging on the stem (Pinterest ref)
    c=2*math.pi*k/NS+.2
    def fn(u,v,c=c,k=k):
        lat=math.radians(-86+172*u)
        w=.105*(1+.25*math.sin(lat*9+k*2.1))
        lon=c+w*(2*v-1)+.075*math.sin(lat*11+k*1.3)
        R=RM*1.012
        return (R*math.cos(lat)*math.cos(lon),R*math.cos(lat)*math.sin(lon),R*math.sin(lat)*ZS)
    m.append(surf(fn,96,4,DGREEN))
m.append(cyl(.16,.1,(0,0,RM*ZS-.01),DGREEN,r2=.1,bev=.02))
m.append(tube([((0,0,.98),.07),((.05,0,1.18),.06),((.2,0,1.3),.05),((.34,0,1.22),.04),((.33,0,1.08),.035),((.24,0,1.1),.03)],DWOOD))
lf=flat([(0,0),(.1,.16),(.3,.24),(.46,.12),(.3,.02),(.12,-.04)],GREEN,.03,.025); rot(lf,(0,.5,0)); move(lf,(-.06,0,1.02)); m.append(lf)
for o_ in m: rot(o_,(-.38,.22,0))
finish(m,"Melon")
# ---- BALLET SLIPPER (ears, used twice) : rose satin, cream lining, ribbon bow ----
def hw(z):                                              # half-width seen from above: narrow heel (-1.15) to broad blunt toe (1.15)
    K=[(-1.15,0),(-1.11,.14),(-1.0,.23),(-.7,.29),(-.3,.32),(.1,.37),(.5,.43),(.8,.45),(.98,.41),(1.08,.31),(1.14,.16),(1.15,0)]
    for (z0,w0),(z1,w1) in zip(K,K[1:]):
        if z0<=z<=z1: t=(z-z0)/(z1-z0); t=t*t*(3-2*t); return w0+(w1-w0)*t
    return 0
ZZ=[-1.15+2.3*i/60 for i in range(61)]
out=[(hw(z),z) for z in ZZ]+[(-hw(z),z) for z in reversed(ZZ)][1:-1]
s=[flat(out,ROSE,.08,.17)]                                # puffy satin body
FY=-.25
TAN=mat("Suede","#E9CFA6",0.08)
ZO=[-1.06+1.36*i/40 for i in range(41)]                   # wide U-shaped opening, thin satin border, pale lining
def ow(z):
    e=.3-z
    return max(0,(hw(z)-.065))*min(1,e/.34)**.45 if e>0 else 0
U=[(ow(z),z) for z in ZO]+[(-ow(z),z) for z in reversed(ZO)]
s.append(flat(U,LROSE,.03,.02,y=FY+.02))
s.append(flat([(x*.62,-.42+(z+.42)*.78) for x,z in U],TAN,.03,.015,y=FY+.0))                    # suede insole
s.append(tube([((x*.5,FY-.035,.27-(.27-z)*.25),.022) for x,z in U[30:52]],DROSE))               # shadow line under the vamp
s.append(tube([((x,FY-.03,z),.035) for x,z in U[::3]]+[((U[0][0],FY-.03,U[0][1]),.035)],DROSE)) # binding
def ribbon(pts,w=.07,m_=ROSE):                            # flat satin ribbon along a path
    o=tube([((x,y*3.3,z),w) for x,y,z in pts],m_); o.scale.y=.3; _act(o); bpy.ops.object.transform_apply(scale=True); return o
RY=FY-.02
for sx in (-1,1): s.append(sph(.075,(sx*.07,FY-.05,.33),(1,.5,.6),DROSE,16,rot=(0,sx*.5,0)))   # drawstring bow
s.append(tube([((-.3,FY+.02,.84),.018),((-.16,FY-.01,.97),.026),((0,FY-.02,1.01),.028),((.16,FY-.01,.97),.026),((.3,FY+.02,.84),.018)],DROSE))         # toe platform seam
for sx in (-1,1):                                         # ribbons from the sides, tied in a bow behind the heel
    s.append(ribbon([(sx*.3,RY+.12,-.35),(sx*.4,RY+.12,-.8),(sx*.22,RY+.12,-1.12),(0,RY+.12,-1.28)],.07))
    s.append(ribbon([(0,RY+.1,-1.28),(sx*.3,RY+.1,-1.14),(sx*.56,RY+.1,-1.3),(sx*.46,RY+.1,-1.54),(sx*.15,RY+.1,-1.42),(0,RY+.1,-1.3)],.075))
s.append(ribbon([(0,RY+.1,-1.3),(-.12,RY+.1,-1.6),(-.36,RY+.1,-1.86)],.07)); s.append(ribbon([(0,RY+.1,-1.3),(.14,RY+.1,-1.62),(.12,RY+.1,-1.98)],.07))
s.append(sph(.1,(0,FY+.03,-1.29),(1,.6,1),DROSE,16))
s.append(flat([(x*.76,z*.9-.02) for x,z in out],TAN,.03,.025,y=.245))   # leather sole on the underside
s.append(flat([(x*.5,-.62+(z+.62)*.3) for x,z in out],BREAD,.03,.02,y=.275))
finish(s,"Slipper")
# ============ SCENE 2 : LA TOUR EIFFEL ============
# ---- STEPLADDER (legs) : wooden A-frame, red treads ----
L=[]; H=4.1; B=1.25; ang=math.atan2(B,H); LEN=math.hypot(B,H)
for sx in (-1,1):
    for y in (-.5,.5):
        L.append(box((.2,.13,LEN),(sx*B/2,y,H/2),WOOD,rot=(0,-sx*ang,0)))
        L.append(box((.3,.2,.14),(sx*(B+.02),y,.07),DEEP))
for t in (.18,.38,.58,.78):
    L.append(box((.5,1.0,.1),(-B*(1-t)+.12,0,H*t),RED))
for t in (.3,.66):
    L.append(box((.1,1.0,.16),(B*(1-t),0,H*t),WOOD,rot=(0,ang,0)))
for y in (-.59,.59):
    L.append(box((B*2*(1-.42)+.1,.05,.09),(0,y,H*.42),PETROL)); L.append(cyl(.07,.06,(0,y,H*.42),GOLD,rot=(math.pi/2,0,0),bev=0))
L.append(box((.86,1.26,.2),(0,0,H+.06),RED,bev=.05))
L.append(dot(.16,(-.12,-.2,H+.165),CREAM,(0,0,1),.12)); L.append(dot(.07,(.16,-.42,H+.165),CREAM,(0,0,1),.15)); L.append(sph(.06,(.02,-.64,H-.02),(1,.6,1.8),CREAM,12))
finish(L,"Stepladder")
# ---- WINE BOTTLE (tower) ----
b=[lathe([(0.001,0),(.4,0),(.44,.06),(.44,1.35),(.4,1.55),(.21,1.92),(.15,2.06),(.15,2.4),(0.001,2.42)],BOTTLE)]
b.append(lathe([(.44,.42),(.462,.44),(.462,1.14),(.44,1.16)],CREAM))
for z in (.5,1.08): b.append(lathe([(.46,z-.03),(.47,z-.02),(.47,z+.02),(.46,z+.03)],GOLD))
d=flat([(0,.2),(.14,0),(0,-.2),(-.14,0)],RED,.02,.015,y=-.465); move(d,(0,0,.79)); b.append(d)
b.append(dot(.045,(0,-.49,.79),CREAM))
b.append(lathe([(.15,1.98),(.178,2.0),(.178,2.4),(.2,2.42),(.2,2.52),(.17,2.56),(0.001,2.57)],GOLD))
b.append(lathe([(.18,2.12),(.19,2.13),(.19,2.19),(.18,2.2)],RED))
backfill(b); finish(b,"WineBottle")
# ---- HATPIN (antenna) : long steel pin, red pearl ----
h=[tube([((0,0,0),.012),((0,0,.3),.045),((0,0,1.75),.05)],STEEL)]
h.append(sph(.08,(0,0,1.7),(1,1,1),GOLD,16)); h.append(cyl(.12,.09,(0,0,1.8),GOLD,bev=.03))
h.append(sph(.23,(0,0,2.04),(1,1,1),RED,32)); h.append(dot(.07,(-.09,-.19,2.12),CREAM,(-.4,-.85,.35),.2))
h.append(sph(.075,(0,0,2.3),(1,1,1.2),GOLD,16))
finish(h,"Hatpin",0.024)
# ---- BOW TIE (first-floor deck) : red with cream spots ----
bt=[]; W=[(.08,.12),(.4,.3),(.72,.44),(.8,.36),(.83,0),(.8,-.36),(.72,-.44),(.4,-.3),(.08,-.12)]
bt.append(flat(W,RED,.1,.09)); bt.append(flat([(-x,z) for x,z in reversed(W)],RED,.1,.09))
for x,z,r in ((.36,.08,.07),(.62,-.16,.075),(.6,.2,.06),(.3,-.1,.05),(.72,.02,.045)):
    for sx in (-1,1): bt.append(dot(r,(sx*x,-.19,z),CREAM))
bt.append(box((.28,.34,.36),(0,-.02,0),DRED,bev=.11))
for sx in (-1,1): bt.append(box((.03,.3,.3),(sx*.17,-.02,0),GOLD,bev=.01))
backfill(bt); finish(bt,"BowTie")
lineup(OUT+"assets/lineup-s12.png",OUT+"blender/scene12.blend")
