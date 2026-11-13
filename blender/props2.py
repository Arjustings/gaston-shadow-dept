import os;ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","game")+"/"  # repo layout: game/assets
import bpy, bmesh, math
from mathutils import Vector, noise as mn
OUT=ROOT+""
bpy.ops.wm.read_factory_settings(use_empty=True)
C=bpy.context
def hexc(h):
    c=[int(h[i:i+2],16)/255 for i in (1,3,5)]
    return tuple((x/12.92 if x<=0.04045 else ((x+0.055)/1.055)**2.4) for x in c)+(1,)
def mat(name,h,mottle=0.10,plain=False):
    m=bpy.data.materials.new(name); m.use_nodes=True; nt=m.node_tree; m["hexcol"]=h
    b=next(n for n in nt.nodes if n.type=="BSDF_PRINCIPLED"); b.inputs["Roughness"].default_value=0.95
    if plain: b.inputs["Base Color"].default_value=hexc(h); return m
    no=nt.nodes.new("ShaderNodeTexNoise"); no.inputs["Scale"].default_value=5; no.inputs["Detail"].default_value=6
    r=nt.nodes.new("ShaderNodeValToRGB"); c=hexc(h); e=r.color_ramp.elements; e[0].position=0.35; e[1].position=0.7
    e[0].color=tuple(x*(1-mottle*2) for x in c[:3])+(1,); e[1].color=tuple(min(1,x*(1+mottle)) for x in c[:3])+(1,)
    nt.links.new(no.outputs["Fac"],r.inputs["Fac"]); nt.links.new(r.outputs["Color"],b.inputs["Base Color"]); return m

def export_glb(path):
    saved=[]
    for m in bpy.data.materials:
        if not m.use_nodes: continue
        nt=m.node_tree; b=next((n for n in nt.nodes if n.type=="BSDF_PRINCIPLED"),None)
        if not b or "hexcol" not in m: continue
        inp=b.inputs["Base Color"]
        for l in list(inp.links): saved.append((nt,l.from_socket,inp)); nt.links.remove(l)
        inp.default_value=hexc(m["hexcol"])
    bpy.ops.export_scene.gltf(filepath=path,use_selection=True,export_apply=True)
    for nt,a,b in saved: nt.links.new(a,b)
RED=mat("Vermilion","#E8432A"); GOLD=mat("Mustard","#DBA42C"); CREAM=mat("Paper","#F3E8D2",0.05); INK=mat("Ink","#16130F",0,True); INK.use_backface_culling=True
BREAD=mat("Bread","#E0A552",0.12); PETROL=mat("Petrol","#23788A"); DEEP=mat("DeepPetrol","#103F4B"); GLOW=mat("LampGlow","#FFD582",0,True)
def smooth(o,m):
    o.data.materials.append(m)
    for p in o.data.polygons: p.use_smooth=True
    return o
def flat(pts,m,ex=0.07,bev=0.04):
    cu=bpy.data.curves.new("f","CURVE"); cu.dimensions="2D"; cu.fill_mode="BOTH"; cu.extrude=ex; cu.bevel_depth=bev; cu.bevel_resolution=3
    sp=cu.splines.new("POLY"); sp.points.add(len(pts)-1)
    for p,(x,y) in zip(sp.points,pts): p.co=(x,y,0,1)
    sp.use_cyclic_u=True
    o=bpy.data.objects.new("f",cu); C.scene.collection.objects.link(o)
    bpy.ops.object.select_all(action="DESELECT"); o.select_set(True); C.view_layer.objects.active=o; bpy.ops.object.convert(target="MESH")
    o=C.object; o.rotation_euler=(math.pi/2,0,0); bpy.ops.object.transform_apply(rotation=True); return smooth(o,m)
def tube(pts,m):
    cu=bpy.data.curves.new("t","CURVE"); cu.dimensions="3D"; cu.bevel_depth=1; cu.bevel_resolution=8; cu.resolution_u=24; cu.use_fill_caps=True
    sp=cu.splines.new("BEZIER"); sp.bezier_points.add(len(pts)-1)
    for p,(co,r) in zip(sp.bezier_points,pts): p.co=co; p.radius=r; p.handle_left_type=p.handle_right_type="AUTO"
    o=bpy.data.objects.new("t",cu); C.scene.collection.objects.link(o)
    bpy.ops.object.select_all(action="DESELECT"); o.select_set(True); C.view_layer.objects.active=o; bpy.ops.object.convert(target="MESH"); return smooth(C.object,m)
def sph(r,loc,scale,m,seg=32):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r,location=loc,segments=seg,ring_count=seg//2); o=C.object; o.scale=scale; bpy.ops.object.transform_apply(scale=True); return smooth(o,m)
def cyl(r,d,loc,m,rot=(0,0,0),r2=None,v=40):
    if r2 is None: bpy.ops.mesh.primitive_cylinder_add(radius=r,depth=d,location=loc,rotation=rot,vertices=v)
    else: bpy.ops.mesh.primitive_cone_add(radius1=r,radius2=r2,depth=d,location=loc,rotation=rot,vertices=v)
    o=C.object; bpy.ops.object.transform_apply(rotation=True)
    bv=o.modifiers.new("b","BEVEL"); bv.width=min(0.04,d/4); bv.segments=3; bpy.ops.object.modifier_apply(modifier="b"); return smooth(o,m)
def finish(parts,name,th=0.03,x=0):
    bpy.ops.object.select_all(action="DESELECT")
    for o in parts: o.select_set(True)
    C.view_layer.objects.active=parts[0]; bpy.ops.object.join(); o=C.object; o.name=name
    bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    ol=o.copy(); ol.data=o.data.copy(); ol.name=name+"_outline"; C.scene.collection.objects.link(ol); ol.data.materials.clear(); ol.data.materials.append(INK)
    bm=bmesh.new(); bm.from_mesh(ol.data)
    bmesh.ops.remove_doubles(bm,verts=bm.verts,dist=0.0005)
    bm.normal_update()
    for v in bm.verts: v.co+=v.normal*(th+th*0.7*mn.noise(v.co*1.7))
    bmesh.ops.reverse_faces(bm,faces=bm.faces); bm.to_mesh(ol.data); bm.free(); ol.parent=o
    bpy.ops.object.select_all(action="DESELECT"); o.select_set(True); ol.select_set(True)
    export_glb(OUT+"assets/"+name.lower()+".glb")
    o.location.x=x; return o

GREEN=mat("Leaf","#6E8B3D"); ORANGE=mat("Carrot","#E8742A"); STEEL=mat("Steel","#E6DCC8",0.04); BLACK=mat("HatBlack","#2A2420",0.06); FLAME=mat("Flame","#FFC24A",0,True)
X=[0]
def place(o,name):  # finish + lay out in a row for the lineup render
    f=finish(o,name,0.028,X[0]); X[0]+=3.2; return f
def lathe(prof,m,seg=48):   # prof: list of (r,z) revolved around Z
    bm=bmesh.new(); rings=[]
    for i in range(seg):
        a=2*math.pi*i/seg; rings.append([bm.verts.new((r*math.cos(a),r*math.sin(a),z)) for r,z in prof])
    for i in range(seg):
        A,B=rings[i],rings[(i+1)%seg]
        for j in range(len(prof)-1): bm.faces.new((A[j],B[j],B[j+1],A[j+1]))
    me=bpy.data.meshes.new("l"); bm.to_mesh(me); bm.free(); o=bpy.data.objects.new("l",me); C.scene.collection.objects.link(o)
    bpy.ops.object.select_all(action="DESELECT"); o.select_set(True); C.view_layer.objects.active=o; return smooth(o,m)
# PEAR
pear=[lathe([(0.001,-1.0),(.45,-.95),(.72,-.7),(.78,-.35),(.62,.05),(.42,.4),(.34,.7),(.26,.92),(.001,1.0)],GOLD), cyl(.05,.35,(.03,0,1.12),BLACK)]
lf=flat([(0,0),(.22,.12),(.4,.05),(.22,-.05)],GREEN,.03,.02); lf.location=(.06,0,1.15); pear.append(lf)
place(pear,"Pear")
# APPLE
apple=[lathe([(0.001,-.62),(.4,-.66),(.68,-.45),(.76,0),(.66,.42),(.32,.6),(.12,.52),(0.001,.48)],RED), cyl(.045,.3,(0,0,.64),BLACK)]
lf=flat([(0,0),(.28,.16),(.48,.06),(.26,-.06)],GREEN,.03,.02); lf.location=(.05,0,.68); apple.append(lf)
place(apple,"Apple")
# SPOON (brass, like the fork)
sp=[flat([(math.cos(a)*.42,1.6+math.sin(a)*.62) for a in [i*math.pi*2/36 for i in range(36)]],GOLD,.06,.05),
    flat([(-.11,-1.4),(.11,-1.4),(.07,1.0),(-.07,1.0)],GOLD,.06,.05)]
place(sp,"Spoon")
# FEATHER (broad curved plume, notched vane, gold quill)
N=30;L=[];R=[]
for i in range(N+1):
    t=i/N; cx=.28*math.sin(math.pi*t*.85); z=-1.2+3.0*t
    w=.62*math.sin(math.pi*(t**.75))
    wl=w*(.55 if abs(t-.42)<.025 else 1); wr=w*.8*(.5 if abs(t-.66)<.025 or abs(t-.3)<.025 else 1)
    L.append((cx-wl,z)); R.append((cx+wr,z))
fe=[flat(L+R[::-1],CREAM,.03,.02)]
q=tube([((0,0,-1.9),.05),((0.02,-.04,-1.2),.045),((.14,-.04,0),.035),((.28,-.04,1.0),.025),((.2,-.04,1.75),.012)],GOLD); fe.append(q)
place(fe,"Feather")
# SCISSORS (open V)
sc=[]
for sgn in (-1,1):
    bl=flat([(0,0),(.16,.1),(.1,2.0),(0,2.1),(-.04,.15)],STEEL,.05,.03); bl.rotation_euler=(0,sgn*.42,0); sc.append(bl)
    bpy.ops.mesh.primitive_torus_add(major_radius=.36,minor_radius=.09,location=(-sgn*.55,0,-.85),rotation=(math.pi/2,0,0),major_segments=32,minor_segments=10); sc.append(smooth(C.object,RED))
    arm=tube([((0,0,0),.07),((-sgn*.35,0,-.5),.07)],RED); sc.append(arm)
sc.append(cyl(.1,.2,(0,0,0),GOLD,rot=(math.pi/2,0,0)))
place(sc,"Scissors")
# BANANA
ba=[tube([((-1.2,0,.55),.08),((-.7,0,-.05),.28),((0,0,-.3),.33),((.75,0,-.05),.28),((1.2,0,.55),.09)],GOLD), cyl(.09,.3,(-1.3,0,.72),BLACK,rot=(0,.6,0))]
place(ba,"Banana")
# UMBRELLA (furled, J-hook handle at top)
um=[lathe([(0.001,-1.75),(.08,-1.55),(.36,-.9),(.46,-.2),(.42,.4),(.2,.85),(.07,1.0),(0.001,1.02)],RED)]
for k in range(6):
    ang=k*math.pi/3; um.append(tube([((math.cos(ang)*.09,math.sin(ang)*.09,-1.5),.022),((math.cos(ang)*.45,math.sin(ang)*.45,-.2),.026),((math.cos(ang)*.08,math.sin(ang)*.08,.95),.02)],DEEP))
um.append(cyl(.47,.14,(0,0,-.35),CREAM)); um.append(sph(.07,(.47,0,-.35),(1,1,1),GOLD,12))
um.append(cyl(.035,.45,(0,0,-1.95),GOLD)); um.append(sph(.06,(0,0,-2.18),(1,1,1),GOLD,12))
um.append(tube([((0,0,.9),.07),((0,0,1.5),.07),((.15,0,1.85),.07),((.5,0,1.9),.07),((.72,0,1.6),.07),((.7,0,1.35),.07)],GOLD))
place(um,"Umbrella")
# CARROT (lathe, wide at the leafy top, tapering to a point below)
ca=[lathe([(0.001,-1.1),(.07,-.8),(.15,-.3),(.24,.3),(.32,.85),(.3,1.02),(0.001,1.06)],ORANGE)]
for z in (-.55,-.05,.45): ca.append(lathe([(.0,z-.03),(.03+.14*(z+1.1)/1.6*1.6*.6,z),(.0,z+.03)],DEEP if 'DEEP' in globals() else ORANGE,24))
for a_ in (-.45,0,.45): lf=flat([(0,0),(.14,.45),(0,1.0),(-.14,.45)],GREEN,.04,.02); lf.rotation_euler=(0,a_,0); lf.location=(0,0,1.0); ca.append(lf)
place(ca,"Carrot")
# CANDLE (in brass dish)
cn=[cyl(.26,1.7,(0,0,0),CREAM), cyl(.55,.12,(0,0,-.9),GOLD), sph(.12,(0,0,-.84),(1,1,.6),GOLD,16), cyl(.02,.18,(0,0,.92),BLACK)]
cn.append(sph(.12,(0,0,1.12),(1,1,1.8),FLAME,16)); cn.append(sph(.06,(.22,0,.6),(1,1,2),CREAM,12))
place(cn,"Candle")
# CROISSANT (tapered crescent of rolled layers)
cr=[]
segs=[(-1.35,.16),(-1.0,.26),(-.55,.36),(0,.42),(.55,.36),(1.0,.26),(1.35,.16)]
for x,r in segs:
    z=.55*(1-(x/1.4)**2)-.35; s_=sph(r*1.35,(x,0,z),(1.15,.85,.85),BREAD,24); s_.rotation_euler=(0,-x*.55,0); cr.append(s_)
place(cr,"Croissant")
# COMB
cb=[flat([(-1.3,0),(1.3,0),(1.3,.32),(-1.3,.32)],GOLD,.05,.04)]
for k in range(17): cb.append(flat([(-1.22+k*.152,0),(-1.15+k*.152,0),(-1.15+k*.152,-.55),(-1.22+k*.152,-.55)],GOLD,.05,.0))
place(cb,"Comb")
# TOP HAT
th=[cyl(.62,1.4,(0,0,.25),BLACK,r2=.66), cyl(1.05,.1,(0,0,-.47),BLACK), cyl(.635,.26,(0,0,-.25),RED)]
place(th,"TopHat")
# lineup render
bpy.ops.mesh.primitive_plane_add(size=120,location=(16,0,-1.3)); C.object.data.materials.append(mat("Floor","#F3E8D2",0.03))
w=bpy.data.worlds.new("W"); C.scene.world=w; w.use_nodes=True; w.node_tree.nodes["Background"].inputs[0].default_value=hexc("#F3E8D2"); w.node_tree.nodes["Background"].inputs[1].default_value=0.45
bpy.ops.object.light_add(type="AREA",location=(14,-8,9)); k=C.object; k.data.energy=6000; k.data.size=12; k.data.color=(1,.86,.66); k.rotation_euler=(math.radians(40),0,0)
bpy.ops.object.camera_add(location=(17.6,-58,2.5)); cam=C.object; C.scene.camera=cam; cam.data.lens=55
e=bpy.data.objects.new("aim",None); e.location=(17.6,0,0); C.scene.collection.objects.link(e); cam.constraints.new("TRACK_TO").target=e
sc_=C.scene
for eng in ("BLENDER_EEVEE","BLENDER_EEVEE_NEXT"):
    try: sc_.render.engine=eng; break
    except TypeError: pass
sc_.view_settings.view_transform="Standard"; sc_.render.resolution_x=2600; sc_.render.resolution_y=600
sc_.render.filepath=OUT+"assets/props2-lineup.png"; bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT+"blender/props2.blend"); print("DONE")
