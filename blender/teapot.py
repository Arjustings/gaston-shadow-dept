import os;ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","game")+"/"  # repo layout: game/assets
import bpy, bmesh, math
from mathutils import Vector
OUT=ROOT+""
bpy.ops.wm.read_factory_settings(use_empty=True)
def hexc(h):
    c=[int(h[i:i+2],16)/255 for i in (1,3,5)]
    return tuple((x/12.92 if x<=0.04045 else ((x+0.055)/1.055)**2.4) for x in c)+(1,)
def mat(name,h,mottle=0.10,emit=False):
    m=bpy.data.materials.new(name); m.use_nodes=True; nt=m.node_tree; m["hexcol"]=h
    b=next(n for n in nt.nodes if n.type=="BSDF_PRINCIPLED")
    b.inputs["Roughness"].default_value=0.95
    if emit:
        b.inputs["Base Color"].default_value=hexc(h); return m
    noise=nt.nodes.new("ShaderNodeTexNoise"); noise.inputs["Scale"].default_value=5; noise.inputs["Detail"].default_value=6
    ramp=nt.nodes.new("ShaderNodeValToRGB")
    c=hexc(h); ramp.color_ramp.elements[0].position=0.35; ramp.color_ramp.elements[1].position=0.7
    ramp.color_ramp.elements[0].color=tuple(x*(1-mottle*2) for x in c[:3])+(1,)
    ramp.color_ramp.elements[1].color=tuple(min(1,x*(1+mottle)) for x in c[:3])+(1,)
    nt.links.new(noise.outputs["Fac"],ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"],b.inputs["Base Color"])
    return m

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
RED=mat("Vermilion","#E8432A"); GOLD=mat("Mustard","#DBA42C"); CREAM=mat("Paper","#F3E8D2",0.05); INK=mat("Ink","#16130F",0,True)
INK.use_backface_culling=True
parts=[]
def add(o,m):
    o.data.materials.append(m); parts.append(o)
    for p in o.data.polygons: p.use_smooth=True
    return o
def sphere(r,loc,scale,m,seg=48):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r,location=loc,segments=seg,ring_count=seg//2); o=bpy.context.object; o.scale=scale
    bpy.ops.object.transform_apply(scale=True); return add(o,m)
# body: squat and chunky
sphere(1,(0,0,0.95),(1.2,1.2,0.92),RED)
# foot
bpy.ops.mesh.primitive_cylinder_add(radius=0.72,depth=0.22,location=(0,0,0.11),vertices=48); add(bpy.context.object,GOLD)
# collar + lid + knob
bpy.ops.mesh.primitive_torus_add(major_radius=0.62,minor_radius=0.09,location=(0,0,1.72),major_segments=48,minor_segments=16); add(bpy.context.object,GOLD)
sphere(1,(0,0,1.74),(0.6,0.6,0.26),CREAM)
sphere(0.2,(0,0,2.1),(1,1,1),RED,32)
# spout: tapered bezier tube
cu=bpy.data.curves.new("spout","CURVE"); cu.dimensions="3D"; cu.bevel_depth=1; cu.bevel_resolution=8; cu.resolution_u=24; cu.use_fill_caps=True
sp=cu.splines.new("BEZIER"); sp.bezier_points.add(3)
for p,(co,r) in zip(sp.bezier_points,[((0.8,0,0.55),0.3),((1.55,0,0.85),0.2),((1.85,0,1.5),0.13),((2.2,0,1.95),0.15)]):
    p.co=co; p.radius=r; p.handle_left_type=p.handle_right_type="AUTO"
so=bpy.data.objects.new("spout",cu); bpy.context.scene.collection.objects.link(so)
bpy.context.view_layer.objects.active=so; so.select_set(True); bpy.ops.object.convert(target="MESH"); add(bpy.context.object,RED); bpy.ops.object.select_all(action="DESELECT")
# handle: fat ring half-buried in the body
bpy.ops.mesh.primitive_torus_add(major_radius=0.6,minor_radius=0.14,location=(-1.2,0,1.0),rotation=(math.pi/2,0,0),major_segments=48,minor_segments=16); add(bpy.context.object,GOLD)
# polka dots on the belly (A8 clown costume)
import random; random.seed(4)
dots=[]
for i in range(10):
    a=i*(2*math.pi/10)+0.314
    if abs(math.cos(a))>0.8: continue
    z=0.95+(0.32 if i%2 else -0.18)
    n=Vector((math.cos(a)*1.2, math.sin(a)*1.2, (z-0.95)/0.92*1.0)).normalized()
    # point on ellipsoid surface
    t=1/math.sqrt((n.x/1.2)**2+(n.y/1.2)**2+(n.z/0.92)**2)
    p=Vector((0,0,0.95))+n*t
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2,location=p,segments=24,ring_count=12); d=bpy.context.object
    nn=Vector((n.x/1.44,n.y/1.44,n.z/0.8464)).normalized()
    d.rotation_euler=nn.to_track_quat("Z","Y").to_euler(); d.scale=(1,1,0.05); bpy.ops.object.transform_apply(rotation=True,scale=True); add(d,CREAM); parts.pop(); dots.append(d)
bpy.ops.object.select_all(action="DESELECT")
for o in parts: o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]; bpy.ops.object.join(); pot=bpy.context.object; pot.name="Teapot"
# ink outline: inverted hull
bpy.ops.object.duplicate(); ol=bpy.context.object; ol.name="Teapot_outline"; ol.data.materials.clear(); ol.data.materials.append(INK)
bm=bmesh.new(); bm.from_mesh(ol.data)
from mathutils import noise as mn
for v in bm.verts: v.co+=v.normal*(0.03+0.022*mn.noise(v.co*1.7))
bmesh.ops.reverse_faces(bm,faces=bm.faces); bm.to_mesh(ol.data); bm.free(); ol.parent=pot
for d in dots: d.parent=pot
# stage: paper sweep, lamp, camera
bpy.ops.mesh.primitive_plane_add(size=60,location=(0,0,0)); fl=bpy.context.object; fl.data.materials.append(mat("Floor","#F3E8D2",0.03))
w=bpy.data.worlds.new("W"); bpy.context.scene.world=w; w.use_nodes=True; w.node_tree.nodes["Background"].inputs[0].default_value=hexc("#F3E8D2"); w.node_tree.nodes["Background"].inputs[1].default_value=0.45
bpy.ops.object.light_add(type="AREA",location=(-3.5,-4,5)); k=bpy.context.object; k.data.energy=450; k.data.size=3; k.data.color=(1,0.86,0.66); k.rotation_euler=(math.radians(50),0,math.radians(-40))
bpy.ops.object.camera_add(location=(3.2,-8.4,2.6)); cam=bpy.context.object; bpy.context.scene.camera=cam
con=cam.constraints.new("TRACK_TO"); e=bpy.data.objects.new("aim",None); e.location=(0.25,0,1.0); bpy.context.scene.collection.objects.link(e); con.target=e; cam.data.lens=70
sc=bpy.context.scene
for eng in ("BLENDER_EEVEE","BLENDER_EEVEE_NEXT"):
    try: sc.render.engine=eng; break
    except TypeError: pass
sc.view_settings.view_transform="Standard"; sc.render.resolution_x=1200; sc.render.resolution_y=1000
sc.render.filepath=OUT+"assets/teapot-v1.png"; bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT+"blender/teapot.blend")
fl.hide_set(True); bpy.ops.object.select_all(action="DESELECT"); pot.select_set(True); ol.select_set(True); [d.select_set(True) for d in dots]
export_glb(OUT+"assets/teapot-v1.glb")
print("DONE",sc.render.engine)
