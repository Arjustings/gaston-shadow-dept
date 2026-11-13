import os;ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","game")+"/"  # repo layout: game/assets
import bpy, bmesh, math
from mathutils import Vector, noise as mn
OUT=ROOT+""
bpy.ops.wm.read_factory_settings(use_empty=True)
C=bpy.context
def hexc(h):
    c=[int(h[i:i+2],16)/255 for i in (1,3,5)]
    return tuple((x/12.92 if x<=0.04045 else ((x+0.055)/1.055)**2.4) for x in c)+(1,)
def mat(name,h,mottle=0.10,plain=False,emit=0):
    m=bpy.data.materials.new(name); m.use_nodes=True; nt=m.node_tree; m["hexcol"]=h
    b=next(n for n in nt.nodes if n.type=="BSDF_PRINCIPLED"); b.inputs["Roughness"].default_value=0.9
    if emit:
        b.inputs["Emission Color"].default_value=hexc(h); b.inputs["Emission Strength"].default_value=emit
    if plain: b.inputs["Base Color"].default_value=hexc(h); return m
    no=nt.nodes.new("ShaderNodeTexNoise"); no.inputs["Scale"].default_value=5; no.inputs["Detail"].default_value=6
    r=nt.nodes.new("ShaderNodeValToRGB"); c=hexc(h); e=r.color_ramp.elements; e[0].position=.35; e[1].position=.7
    e[0].color=tuple(x*(1-mottle*2) for x in c[:3])+(1,); e[1].color=tuple(min(1,x*(1+mottle)) for x in c[:3])+(1,)
    nt.links.new(no.outputs["Fac"],r.inputs["Fac"]); nt.links.new(r.outputs["Color"],b.inputs["Base Color"]); return m
def export_glb(path):
    saved=[]
    for m in bpy.data.materials:
        if not m.use_nodes or "hexcol" not in m: continue
        nt=m.node_tree; b=next((n for n in nt.nodes if n.type=="BSDF_PRINCIPLED"),None); inp=b.inputs["Base Color"]
        for l in list(inp.links): saved.append((nt,l.from_socket,inp)); nt.links.remove(l)
        inp.default_value=hexc(m["hexcol"])
    bpy.ops.export_scene.gltf(filepath=path,use_selection=True,export_apply=True)
    for nt,a,b in saved: nt.links.new(a,b)
RED=mat("Vermilion","#C8341F"); DEEP=mat("DeepRed","#8E1E14"); GOLD=mat("Mustard","#DBA42C"); CREAM=mat("Paper","#F3E8D2",.05)
INK=mat("Ink","#16130F",0,True); INK.use_backface_culling=True; BULB=mat("BulbA","#FFE2A0",0,True,emit=3.0); BULB2=mat("BulbB","#FFE2A0",0,True,emit=3.0); bi=[0]
parts=[]
def keep(o,m):
    o.data.materials.append(m)
    for p in o.data.polygons: p.use_smooth=True
    parts.append(o); return o
def box(sx,sy,sz,loc,m,bev=.08):
    bpy.ops.mesh.primitive_cube_add(location=loc); o=C.object; o.scale=(sx/2,sy/2,sz/2); bpy.ops.object.transform_apply(scale=True)
    b=o.modifiers.new("b","BEVEL"); b.width=bev; b.segments=4; bpy.ops.object.modifier_apply(modifier="b"); return keep(o,m)
def tube(pts,r,m,closed=True):
    cu=bpy.data.curves.new("t","CURVE"); cu.dimensions="3D"; cu.bevel_depth=r; cu.bevel_resolution=4
    sp=cu.splines.new("POLY"); sp.points.add(len(pts)-1)
    for p,co in zip(sp.points,pts): p.co=(*co,1)
    sp.use_cyclic_u=closed
    o=bpy.data.objects.new("t",cu); C.scene.collection.objects.link(o); bpy.ops.object.select_all(action="DESELECT"); o.select_set(True); C.view_layer.objects.active=o
    bpy.ops.object.convert(target="MESH"); return keep(C.object,m)
def sph(r,loc,scale,m,seg=24):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r,location=loc,segments=seg,ring_count=seg//2); o=C.object; o.scale=scale; bpy.ops.object.transform_apply(scale=True); return keep(o,m)
def cyl(r,d,loc,m,rot=(math.pi/2,0,0),v=32):
    bpy.ops.mesh.primitive_cylinder_add(radius=r,depth=d,location=loc,rotation=rot,vertices=v); o=C.object; bpy.ops.object.transform_apply(rotation=True)
    b=o.modifiers.new("b","BEVEL"); b.width=min(.05,d/4); b.segments=3; bpy.ops.object.modifier_apply(modifier="b"); return keep(o,m)
W,H,BW,D=14.0,8.0,.95,.6       # opening, bar width, depth (Y)
hx,hz=W/2,H/2; ox,oz=hx+BW,hz+BW
# rails
box(2*ox,D,BW,(0,0,hz+BW/2),RED); box(2*ox,D,BW*1.15,(0,0,-hz-BW*1.15/2+.0),RED)
box(BW,D,2*hz,( -hx-BW/2,0,0),RED); box(BW,D,2*hz,(hx+BW/2,0,0),RED)
# raised deep-red panel strip on each face of the rails (painted inset look)
for y in (D/2+.01,-D/2-.01):
    box(2*ox-.5,.04,BW-.3,(0,y,hz+BW/2),DEEP,.02); box(2*ox-.5,.04,BW*1.15-.3,(0,y,-hz-BW*1.15/2),DEEP,.02)
    box(BW-.3,.04,2*hz-.4,(-hx-BW/2,y,0),DEEP,.02); box(BW-.3,.04,2*hz-.4,(hx+BW/2,y,0),DEEP,.02)
# gold beading: inner edge + outer edge, both faces
for y in (D/2+.02,-D/2-.02):
    tube([(-hx,y,-hz),(hx,y,-hz),(hx,y,hz),(-hx,y,hz)],.11,GOLD)
    tube([(-hx-.42,y+(.02 if y>0 else -.02),-hz-.5),(hx+.42,y+(.02 if y>0 else -.02),-hz-.5),(hx+.42,y+(.02 if y>0 else -.02),hz+.42),(-hx-.42,y+(.02 if y>0 else -.02),hz+.42)],.035,CREAM)
    tube([(-ox,y,-oz-.14),(ox,y,-oz-.14),(ox,y,oz),(-ox,y,oz)],.09,GOLD)
# corner rosettes
for sx in (-1,1):
    for sz in (-1,1):
        x,z=sx*(hx+BW/2),sz*(hz+BW/2)-(0.05 if sz<0 else 0)
        cyl(.66,D+.2,(x,0,z),GOLD); sph(.34,(x,D/2+.12,z),(1,.6,1),RED,16); sph(.34,(x,-D/2-.12,z),(1,.6,1),RED,16)
# crest: half disc with gold rim and star medallion
bm=bmesh.new(); R=2.3; n=40
verts=[bm.verts.new((R*math.cos(math.pi*i/n),0,R*math.sin(math.pi*i/n))) for i in range(n+1)]
f=bm.faces.new(verts); ext=bmesh.ops.extrude_face_region(bm,geom=[f]); 
for v in [e for e in ext["geom"] if isinstance(e,bmesh.types.BMVert)]: v.co.y+=D-.1
bmesh.ops.translate(bm,verts=bm.verts,vec=(0,-(D-.1)/2,hz+BW-.05))
me=bpy.data.meshes.new("crest"); bm.to_mesh(me); bm.free(); o=bpy.data.objects.new("crest",me); C.scene.collection.objects.link(o)
bpy.ops.object.select_all(action="DESELECT"); o.select_set(True); C.view_layer.objects.active=o
b=o.modifiers.new("b","BEVEL"); b.width=.06; b.segments=3; bpy.ops.object.modifier_apply(modifier="b"); keep(o,RED)
for y in (D/2-.02,-D/2+.02):
    tube([(R*math.cos(math.pi*i/n),y,hz+BW-.05+R*math.sin(math.pi*i/n)) for i in range(n+1)],.08,GOLD,closed=False)
    cyl(.82,.08,(0,y,hz+BW+1.05),CREAM)
    star=[];
    for i in range(10):
        a=math.pi/2+i*math.pi/5; rr=.62 if i%2==0 else .27; star.append((rr*math.cos(a),y+(.05 if y>0 else -.05),hz+BW+1.05+rr*math.sin(a)))
    bm=bmesh.new(); vs=[bm.verts.new(p) for p in star]; bm.faces.new(vs); me=bpy.data.meshes.new("star"); bm.to_mesh(me); bm.free()
    so=bpy.data.objects.new("star",me); C.scene.collection.objects.link(so); bpy.ops.object.select_all(action="DESELECT"); so.select_set(True); C.view_layer.objects.active=so
    s=so.modifiers.new("s","SOLIDIFY"); s.thickness=.08; bpy.ops.object.modifier_apply(modifier="s"); keep(so,GOLD)
for i in range(1,8):
    a=math.pi*i/8; sph(.2,(R*1.04*math.cos(a),0,hz+BW-.05+R*1.04*math.sin(a)),(1,1.6,1),GOLD,16)
for sx in (-1,1):
    bpy.ops.mesh.primitive_torus_add(major_radius=.55,minor_radius=.14,location=(sx*(R+.55),0,hz+BW+.35),rotation=(math.pi/2,0,0),major_segments=32,minor_segments=10); keep(C.object,GOLD)
    sph(.24,(sx*(R+1.1),0,hz+BW+.1),(1,1.5,1),GOLD,16)
cyl(.06,.7,(0,0,hz+BW+R+.3),GOLD,rot=(0,0,0)); sph(.18,(0,0,hz+BW+R+.72),(1,1,1),GOLD)
# marquee bulbs along top rail, both faces
k=-hx+.7
while k<=hx-.6:
    for y in (D/2+.12,-D/2-.12):
        if abs(k)>R+1.4: sph(.17,(k,y,hz+BW/2),(1,1,1),BULB if bi[0]%2==0 else BULB2,16)
        sph(.17,(k,y,-hz-BW*1.15/2),(1,1,1),BULB2 if bi[0]%2==0 else BULB,16)
    bi[0]+=1
    k+=1.0
# feet: gilded ball feet on red plinths
for sx in (-1,1):
    x=sx*(hx+BW/2); zb=-hz-BW*1.15
    box(1.6,2.4,.26,(x,0,-5+.13),DEEP,.08)
    for yy in (-.75,.75): sph(.3,(x,yy,-5+.26+.24),(1,1,.8),GOLD,16)
    box(.8,1.8,abs(zb-(-5+.26)),(x,0,(zb+(-5+.26))/2),RED,.08)
# join + ink outline
bpy.ops.object.select_all(action="DESELECT")
for o in parts: o.select_set(True)
C.view_layer.objects.active=parts[0]; bpy.ops.object.join(); fr=C.object; fr.name="Screen"
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
ol=fr.copy(); ol.data=fr.data.copy(); ol.name="Screen_outline"; C.scene.collection.objects.link(ol); ol.data.materials.clear(); ol.data.materials.append(INK)
bm=bmesh.new(); bm.from_mesh(ol.data); bmesh.ops.remove_doubles(bm,verts=bm.verts,dist=.0005); bm.normal_update()
for v in bm.verts: v.co+=v.normal*(.05+.03*mn.noise(v.co*1.3))
bmesh.ops.reverse_faces(bm,faces=bm.faces); bm.to_mesh(ol.data); bm.free(); ol.parent=fr
bpy.ops.object.select_all(action="DESELECT"); fr.select_set(True); ol.select_set(True)
export_glb(OUT+"assets/screen.glb")
# preview render: paper + frame, front and back
bpy.ops.mesh.primitive_plane_add(size=1,location=(0,0,0),rotation=(math.pi/2,0,0)); p=C.object; p.scale=(W,H,1); p.data.materials.append(mat("PaperP","#F3E8D2",.04))
bpy.ops.mesh.primitive_plane_add(size=60,location=(0,0,-5)); C.object.data.materials.append(mat("Floor","#6a3d22",.06))
w=bpy.data.worlds.new("W"); C.scene.world=w; w.use_nodes=True; w.node_tree.nodes["Background"].inputs[0].default_value=hexc("#2a1610"); w.node_tree.nodes["Background"].inputs[1].default_value=.6
bpy.ops.object.light_add(type="AREA",location=(-6,-12,10)); L=C.object; L.data.energy=5000; L.data.size=8; L.data.color=(1,.88,.7); L.rotation_euler=(math.radians(50),0,math.radians(-25))
bpy.ops.object.light_add(type="AREA",location=(8,12,8)); L2=C.object; L2.data.energy=2500; L2.data.size=8; L2.rotation_euler=(math.radians(-55),0,math.radians(150))
sc=C.scene
for eng in ("BLENDER_EEVEE","BLENDER_EEVEE_NEXT"):
    try: sc.render.engine=eng; break
    except TypeError: pass
sc.view_settings.view_transform="Standard"; sc.render.resolution_x=1600; sc.render.resolution_y=1100
bpy.ops.object.light_add(type="AREA",location=(-4,14,9)); L3=C.object; L3.data.energy=4500; L3.data.size=8; L3.rotation_euler=(math.radians(-50),0,math.radians(195))
for nm,loc in (("front",(10,-30,5)),("back",(-10,30,4))):
    bpy.ops.object.camera_add(location=loc); cam=C.object; sc.camera=cam; cam.data.lens=50
    e=bpy.data.objects.new("aim",None); e.location=(0,0,0.9); C.scene.collection.objects.link(e); cam.constraints.new("TRACK_TO").target=e
    sc.render.filepath=OUT+"assets/screen-"+nm+".png"; bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT+"blender/screen.blend"); print("DONE")
