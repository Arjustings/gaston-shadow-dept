import os;ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","game")+"/"  # repo layout: game/assets
import bpy, numpy as np, sys
from collections import deque
A=ROOT+"assets/"
def cut(name,tol=0.085,r=2):
    im=bpy.data.images.load(A+name+".png"); w,h=im.size
    px=np.array(im.pixels[:],dtype=np.float32).reshape(h,w,4)
    rgb=px[...,:3]
    # background colour = median of a border ring
    ring=np.concatenate([rgb[:12].reshape(-1,3),rgb[-12:].reshape(-1,3),rgb[:,:12].reshape(-1,3),rgb[:,-12:].reshape(-1,3)])
    bg=np.median(ring,axis=0)
    # local background estimate would be better, but the sheets are flat: distance to bg colour
    d=np.sqrt(((rgb-bg)**2).sum(-1))
    cand=d<tol
    # erode candidates so the fill cannot squeeze through gaps in the broken outline
    er=cand.copy()
    for dy in range(-r,r+1):
        for dx in range(-r,r+1):
            er&=np.roll(np.roll(cand,dy,0),dx,1)
    seen=np.zeros((h,w),bool); q=deque()
    for x in range(w):
        for y in (0,h-1):
            if er[y,x] and not seen[y,x]: seen[y,x]=True; q.append((y,x))
    for y in range(h):
        for x in (0,w-1):
            if er[y,x] and not seen[y,x]: seen[y,x]=True; q.append((y,x))
    while q:
        y,x=q.popleft()
        for ny,nx in ((y+1,x),(y-1,x),(y,x+1),(y,x-1)):
            if 0<=ny<h and 0<=nx<w and er[ny,nx] and not seen[ny,nx]: seen[ny,nx]=True; q.append((ny,nx))
    # grow back by the erosion radius (+1), only over candidate pixels
    bgm=seen.copy()
    for _ in range(r+1):
        g=bgm.copy()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)): g|=np.roll(np.roll(bgm,dy,0),dx,1)
        bgm=g&cand|bgm
    a=(~bgm).astype(np.float32)
    # soften edge 1px
    s=a.copy()
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)): s+=np.roll(np.roll(a,dy,0),dx,1)
    a=np.minimum(a,s/5*1.25).clip(0,1)
    px[...,3]=a
    out=bpy.data.images.new(name+"-cut",w,h,alpha=True); out.pixels=px.ravel(); out.filepath_raw=A+name+"-cut.png"; out.file_format="PNG"; out.save()
    print("CUT",name,w,h,"bg",bg.round(3),"kept %.1f%%"%(a.mean()*100))
for n in sys.argv[sys.argv.index("--")+1:]: cut(n)
