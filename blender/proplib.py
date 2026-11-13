import os;ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","game")+"/"  # repo layout: game/assets
"""Shared prop-building kit for Gaston Grandiose's Shadow Dept.
Props are modelled in game units, upright in the XZ plane (camera looks along +Y), so the game uses scale 1.
Style: chunky shapes, limited cirque palette, painted decoration, wobbly broken ink outline (inverted hull)."""
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
# ---- palette (brand guideline + a few supporting tones) ----
RED=mat("Vermilion","#E8432A"); GOLD=mat("Mustard","#DBA42C"); CREAM=mat("Paper","#F3E8D2",0.05); INK=mat("Ink","#16130F",0,True); INK.use_backface_culling=True
BREAD=mat("Bread","#E0A552",0.12); PETROL=mat("Petrol","#23788A"); DEEP=mat("DeepPetrol","#103F4B")
GREEN=mat("Green","#4F8F4A"); DGREEN=mat("DarkGreen","#1F4D33"); BOTTLE=mat("Bottle","#2B5A3C",0.14)
ROSE=mat("Rose","#EFA59C",0.07); DROSE=mat("DeepRose","#C8635C"); WOOD=mat("Wood","#C9894A",0.14); DWOOD=mat("DarkWood","#7A4A22",0.14)
STEEL=mat("Steel","#D5CEC0",0.05); BLACK=mat("SoftBlack","#2A2420",0.06); DRED=mat("DeepRed","#A82A1A")
def smooth(o,m):
    o.data.materials.append(m)
    for p in o.data.polygons: p.use_smooth=True
    return o
def _act(o):
    bpy.ops.object.select_all(action="DESELECT"); o.select_set(True); C.view_layer.objects.active=o
def flat(pts,m,ex=0.07,bev=0.04,y=0):
    """Extruded 2D outline (x,z points). Front face sits at y-(ex+bev)."""
    cu=bpy.data.curves.new("f","CURVE"); cu.dimensions="2D"; cu.fill_mode="BOTH"; cu.extrude=ex; cu.bevel_depth=bev; cu.bevel_resolution=3
    sp=cu.splines.new("POLY"); sp.points.add(len(pts)-1)
    for p,(x,z) in zip(sp.points,pts): p.co=(x,z,0,1)
    sp.use_cyclic_u=True
    o=bpy.data.objects.new("f",cu); C.scene.collection.objects.link(o); _act(o); bpy.ops.object.convert(target="MESH")
    o=C.object; o.rotation_euler=(math.pi/2,0,0); o.location.y=y; bpy.ops.object.transform_apply(location=True,rotation=True); return smooth(o,m)
def tube(pts,m,res=24):
    """Tapered bezier tube: pts = [((x,y,z),radius),...]"""
    cu=bpy.data.curves.new("t","CURVE"); cu.dimensions="3D"; cu.bevel_depth=1; cu.bevel_resolution=8; cu.resolution_u=res; cu.use_fill_caps=True
    sp=cu.splines.new("BEZIER"); sp.bezier_points.add(len(pts)-1)
    for p,(co,r) in zip(sp.bezier_points,pts): p.co=co; p.radius=r; p.handle_left_type=p.handle_right_type="AUTO"
    o=bpy.data.objects.new("t",cu); C.scene.collection.objects.link(o); _act(o); bpy.ops.object.convert(target="MESH"); return smooth(C.object,m)
def sph(r,loc,scale,m,seg=32,rot=(0,0,0)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r,location=loc,segments=seg,ring_count=seg//2,rotation=rot); o=C.object; o.scale=scale; bpy.ops.object.transform_apply(scale=True,rotation=True); return smooth(o,m)
def cyl(r,d,loc,m,rot=(0,0,0),r2=None,v=40,bev=0.04):
    if r2 is None: bpy.ops.mesh.primitive_cylinder_add(radius=r,depth=d,location=loc,rotation=rot,vertices=v)
    else: bpy.ops.mesh.primitive_cone_add(radius1=r,radius2=r2,depth=d,location=loc,rotation=rot,vertices=v)
    o=C.object; bpy.ops.object.transform_apply(rotation=True)
    if bev: bv=o.modifiers.new("b","BEVEL"); bv.width=min(bev,d/4,r/3); bv.segments=3; bpy.ops.object.modifier_apply(modifier="b")
    return smooth(o,m)
def box(size,loc,m,rot=(0,0,0),bev=0.03):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc,rotation=rot); o=C.object; o.scale=size; bpy.ops.object.transform_apply(scale=True,rotation=True)
    if bev: bv=o.modifiers.new("b","BEVEL"); bv.width=min(bev,min(size)/3); bv.segments=3; bpy.ops.object.modifier_apply(modifier="b")
    return smooth(o,m)
def torus(R,r,loc,m,rot=(0,0,0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R,minor_radius=r,location=loc,rotation=rot,major_segments=48,minor_segments=14); o=C.object; bpy.ops.object.transform_apply(rotation=True); return smooth(o,m)
def lathe(prof,m,seg=48,scale=(1,1,1),loc=(0,0,0)):
    """Revolve (r,z) profile around Z."""
    bm=bmesh.new(); rings=[]
    for i in range(seg):
        a=2*math.pi*i/seg; rings.append([bm.verts.new((r*math.cos(a),r*math.sin(a),z)) for r,z in prof])
    for i in range(seg):
        A,B=rings[i],rings[(i+1)%seg]
        for j in range(len(prof)-1): bm.faces.new((A[j],B[j],B[j+1],A[j+1]))
    bmesh.ops.remove_doubles(bm,verts=bm.verts,dist=0.0008)
    me=bpy.data.meshes.new("l"); bm.to_mesh(me); bm.free(); o=bpy.data.objects.new("l",me); C.scene.collection.objects.link(o)
    o.scale=scale; o.location=loc; _act(o); bpy.ops.object.transform_apply(location=True,scale=True); return smooth(o,m)
def dot(r,loc,m,n=(0,-1,0),th=0.06):
    """Painted spot: a flattened disc lying on a surface with normal n."""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r,location=loc,segments=20,ring_count=10); o=C.object
    o.rotation_euler=Vector(n).normalized().to_track_quat("Z","Y").to_euler(); o.scale=(1,1,th); bpy.ops.object.transform_apply(rotation=True,scale=True); return smooth(o,m)
def rot(o,e,pivot=(0,0,0)):
    """Rotate object by euler e around pivot and apply."""
    from mathutils import Euler, Matrix
    M=Matrix.Translation(pivot)@Euler(e).to_matrix().to_4x4()@Matrix.Translation(-Vector(pivot)); o.matrix_world=M@o.matrix_world
    _act(o); bpy.ops.object.transform_apply(location=True,rotation=True,scale=True); return o
def move(o,d):
    o.location=Vector(o.location)+Vector(d); _act(o); bpy.ops.object.transform_apply(location=True); return o
DONE=[]
def finish(parts,name,th=0.03):
    bpy.ops.object.select_all(action="DESELECT")
    for o in parts: o.select_set(True)
    C.view_layer.objects.active=parts[0]; bpy.ops.object.join(); o=C.object; o.name=name
    bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    ol=o.copy(); ol.data=o.data.copy(); ol.name=name+"_outline"; C.scene.collection.objects.link(ol); ol.data.materials.clear(); ol.data.materials.append(INK)
    bm=bmesh.new(); bm.from_mesh(ol.data)
    bmesh.ops.remove_doubles(bm,verts=bm.verts,dist=0.0005); bm.normal_update()
    for v in bm.verts: v.co+=v.normal*(th+th*0.7*mn.noise(v.co*1.7))
    bmesh.ops.reverse_faces(bm,faces=bm.faces); bm.to_mesh(ol.data); bm.free(); ol.parent=o
    bpy.ops.object.select_all(action="DESELECT"); o.select_set(True); ol.select_set(True)
    export_glb(OUT+"assets/"+name.lower()+".glb"); DONE.append(o); return o
def lineup(path,blend,gap=0.9,res=(2200,900)):
    """Stand the finished props in a row on the floor and render a beauty shot."""
    x=0; hmax=0
    for o in DONE:
        bb=[o.matrix_world@Vector(c) for c in o.bound_box]; x0=min(v.x for v in bb); x1=max(v.x for v in bb); z0=min(v.z for v in bb); z1=max(v.z for v in bb)
        o.location.x+=x-x0; o.location.z-=z0; x+=x1-x0+gap; hmax=max(hmax,z1-z0)
    W=x-gap; cx=W/2
    bpy.ops.mesh.primitive_plane_add(size=200,location=(cx,0,0)); C.object.data.materials.append(mat("Floor","#F3E8D2",0.03))
    w=bpy.data.worlds.new("W"); C.scene.world=w; w.use_nodes=True; bg=w.node_tree.nodes["Background"]; bg.inputs[0].default_value=hexc("#F3E8D2"); bg.inputs[1].default_value=0.45
    k_=W/12
    bpy.ops.object.light_add(type="AREA",location=(cx-2*k_,-6*k_,7*k_)); k=C.object; k.data.energy=1400*k_*k_; k.data.size=5*k_; k.data.color=(1,0.86,0.66); k.rotation_euler=(math.radians(45),0,math.radians(-25))
    asp=res[0]/res[1]; d=max((W/2+0.8)*80/18, (hmax/2+0.8)*80/18*asp)
    bpy.ops.object.camera_add(location=(cx+d*0.07,-d,hmax/2+d*0.1)); cam=C.object; C.scene.camera=cam; cam.data.lens=80; cam.data.clip_end=1000
    e=bpy.data.objects.new("aim",None); e.location=(cx,0,hmax/2); C.scene.collection.objects.link(e); cam.constraints.new("TRACK_TO").target=e
    sc=C.scene
    for eng in ("BLENDER_EEVEE","BLENDER_EEVEE_NEXT"):
        try: sc.render.engine=eng; break
        except TypeError: pass
    sc.view_settings.view_transform="Standard"; sc.render.resolution_x,sc.render.resolution_y=res
    sc.render.filepath=path; bpy.ops.render.render(write_still=True)
    bpy.ops.wm.save_as_mainfile(filepath=blend); print("DONE")
def surf(fn,nu,nv,m,thick=0,closed_u=False):
    """Mesh from fn(u,v)->xyz on a grid (u,v in 0..1); optional solidify thickness."""
    bm=bmesh.new(); V=[[bm.verts.new(fn(i/nu,j/nv)) for j in range(nv+1)] for i in range(nu if closed_u else nu+1)]
    n=len(V)
    for i in range(nu):
        for j in range(nv): bm.faces.new((V[i][j],V[(i+1)%n][j],V[(i+1)%n][j+1],V[i][j+1]))
    me=bpy.data.meshes.new("s"); bm.to_mesh(me); bm.free(); o=bpy.data.objects.new("s",me); C.scene.collection.objects.link(o)
    if thick:
        _act(o); sd=o.modifiers.new("s","SOLIDIFY"); sd.thickness=thick; sd.offset=0; bpy.ops.object.modifier_apply(modifier="s")
    return smooth(o,m)
def ribbon(pts,w,m,flatten=.3):
    """Flat satin ribbon along (x,y,z) points."""
    o=tube([((x,y/flatten,z),w) for x,y,z in pts],m); o.scale.y=flatten; _act(o); bpy.ops.object.transform_apply(scale=True); return o
def chaikin(pts,n=2):
    """Round off a closed polygon by corner cutting."""
    for _ in range(n):
        q=[]
        for i in range(len(pts)):
            a=pts[i]; b=pts[(i+1)%len(pts)]
            q.append((a[0]*.75+b[0]*.25,a[1]*.75+b[1]*.25)); q.append((a[0]*.25+b[0]*.75,a[1]*.25+b[1]*.75))
        pts=q
    return pts
def backfill(parts):
    """Copy every front-only painted detail (all verts at y<0) onto the back, so the prop is finished from both sides."""
    add=[]
    for o in parts:
        ys=[(o.matrix_world@v.co).y for v in o.data.vertices]
        if max(ys)<0.03:
            c=o.copy(); c.data=o.data.copy(); C.scene.collection.objects.link(c); c.scale.y=-1; _act(c); bpy.ops.object.transform_apply(scale=True)
            add.append(c)   # applying a negative scale already flips the normals back
    parts.extend(add); return parts
