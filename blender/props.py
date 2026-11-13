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
# ---------- FORK (brass, chunky, three tines) ----------
R=[(0.14,0),(0.09,1.5),(0.12,1.75),(0.46,2.05),(0.46,3.0),(0.32,3.06),(0.3,2.32),(0.2,2.2),(0.1,2.32),(0.08,3.1)]
pts=[(-x,y) for x,y in R]+[(x,y) for x,y in reversed(R)]
fork=[flat(pts,GOLD,0.06,0.05)]
finish(fork,"Fork",0.028,3.4)
# ---------- BAGUETTE (long neck) ----------
bag=[tube([((0,0,0.3),0.3),((0.08,0,1.0),0.42),((0.16,0,2.0),0.45),((0.08,0,3.0),0.42),((0,0,3.7),0.3)],BREAD), sph(0.3,(0,0,0.3),(1,1,1.1),BREAD,24), sph(0.3,(0,0,3.7),(1,1,1.1),BREAD,24)]
for i in range(5):
    z=0.8+i*0.6
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1,location=(0.12,-0.36,z),rotation=(0,math.radians(-38),0),segments=16,ring_count=8); o=C.object; o.scale=(0.26,0.1,0.07); bag.append(smooth(o,CREAM))
finish(bag,"Baguette",0.03,5.6)
# ---------- FAN (open, striped, spiky edge) ----------
fan=[]; N=9; a0,a1=math.radians(18),math.radians(162); ri,ro=0.55,1.9
for i in range(N):
    b0=a0+(a1-a0)*i/N; b1=a0+(a1-a0)*(i+1)/N; bm_=(b0+b1)/2
    P=lambda r,a:(r*math.cos(a),r*math.sin(a))
    seg=flat([P(ri,b0),P(ro,b0),P(ro+0.22,bm_),P(ro,b1),P(ri,b1)],RED if i%2==0 else CREAM,0.03,0.025); fan.append(seg)
for i in range(N+1):
    b=a0+(a1-a0)*i/N; d=(math.cos(b),math.sin(b)); n=(-d[1]*0.035,d[0]*0.035)
    fan.append(flat([(n[0],n[1]),(d[0]*0.62+n[0],d[1]*0.62+n[1]),(d[0]*0.62-n[0],d[1]*0.62-n[1]),(-n[0],-n[1])],GOLD,0.05,0.02))
fan.append(sph(0.13,(0,0,0),(1,1.2,1),GOLD,24))
f=finish(fan,"Fan",0.026,8.6); f.location.z=0.2
# ---------- LAMP (set piece, petrol) ----------
lamp=[cyl(0.55,0.14,(0,0,0.07),DEEP), cyl(0.07,1.5,(0,0,0.85),DEEP), cyl(0.42,1.0,(0,0,1.75),PETROL,(0,math.pi/2,0)),
      cyl(0.42,0.5,(0.72,0,1.75),GOLD,(0,math.pi/2,0),0.72), cyl(0.3,0.12,(-0.54,0,1.75),DEEP,(0,math.pi/2,0)),
      cyl(0.1,0.3,(0,0,2.3),DEEP), cyl(0.2,0.06,(0,0,2.46),DEEP), sph(0.4,(0.74,0,1.75),(0.25,1,1),GLOW,24)]
finish(lamp,"Lamp",0.03,-3.6)
# ---------- bring in the teapot ----------
with bpy.data.libraries.load(OUT+"blender/teapot.blend") as (src,dst): dst.objects=[n for n in src.objects if n.startswith("Teapot") or n.startswith("Sphere")]
for o in dst.objects:
    if o: C.scene.collection.objects.link(o)
# ---------- stage + render ----------
bpy.ops.mesh.primitive_plane_add(size=80); C.object.data.materials.append(mat("Floor","#F3E8D2",0.03))
w=bpy.data.worlds.new("W"); C.scene.world=w; w.use_nodes=True; bg=w.node_tree.nodes["Background"]; bg.inputs[0].default_value=hexc("#F3E8D2"); bg.inputs[1].default_value=0.45
bpy.ops.object.light_add(type="AREA",location=(-2,-6,7)); k=C.object; k.data.energy=1400; k.data.size=5; k.data.color=(1,0.86,0.66); k.rotation_euler=(math.radians(45),0,math.radians(-25))
bpy.ops.object.camera_add(location=(2.6,-34,5)); cam=C.object; C.scene.camera=cam; cam.data.lens=80
e=bpy.data.objects.new("aim",None); e.location=(2.6,0,1.5); C.scene.collection.objects.link(e); cam.constraints.new("TRACK_TO").target=e
sc=C.scene
for eng in ("BLENDER_EEVEE","BLENDER_EEVEE_NEXT"):
    try: sc.render.engine=eng; break
    except TypeError: pass
sc.view_settings.view_transform="Standard"; sc.render.resolution_x=2000; sc.render.resolution_y=760
sc.render.filepath=OUT+"assets/props-lineup.png"; bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT+"blender/props.blend"); print("DONE")
