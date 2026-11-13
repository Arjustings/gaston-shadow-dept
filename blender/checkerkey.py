import bpy, numpy as np, sys, os
from collections import deque
src,dst=sys.argv[sys.argv.index("--")+1:]
for fn in sorted(os.listdir(src)):
    im=bpy.data.images.load(os.path.join(src,fn)); w,h=im.size
    px=np.array(im.pixels[:],dtype=np.float32).reshape(h,w,4); rgb=px[...,:3]
    mn,mx=rgb.min(-1),rgb.max(-1)
    cand=(mn>0.80)&((mx-mn)<0.07)|(px[...,3]<0.5)
    er=cand.copy()
    for dy in (-1,0,1):
        for dx in (-1,0,1): er&=np.roll(np.roll(cand,dy,0),dx,1)
    seen=np.zeros((h,w),bool);q=deque()
    for x in range(w):
        for y in (0,h-1):
            if er[y,x]: seen[y,x]=True;q.append((y,x))
    for y in range(h):
        for x in (0,w-1):
            if er[y,x] and not seen[y,x]: seen[y,x]=True;q.append((y,x))
    while q:
        y,x=q.popleft()
        for ny,nx in ((y+1,x),(y-1,x),(y,x+1),(y,x-1)):
            if 0<=ny<h and 0<=nx<w and er[ny,nx] and not seen[ny,nx]: seen[ny,nx]=True;q.append((ny,nx))
    bg=seen.copy()
    for _ in range(2):
        g=bg.copy()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)): g|=np.roll(np.roll(bg,dy,0),dx,1)
        bg=(g&cand)|bg
    # enclosed checkerboard pockets (e.g. between head and raised arm): two-tone neutral components
    rest=cand&~bg;lab=np.zeros((h,w),np.int32);nid=0
    for y0,x0 in zip(*np.where(rest)):
        if lab[y0,x0]: continue
        nid+=1;q=deque([(y0,x0)]);lab[y0,x0]=nid;pts=[(y0,x0)]
        while q:
            y,x=q.popleft()
            for ny,nx in ((y+1,x),(y-1,x),(y,x+1),(y,x-1)):
                if 0<=ny<h and 0<=nx<w and rest[ny,nx] and not lab[ny,nx]: lab[ny,nx]=nid;q.append((ny,nx));pts.append((ny,nx))
        if len(pts)<20:
            ys,xs=np.array(pts).T;y0,y1,x0,x1=max(ys.min()-3,0),min(ys.max()+4,h),max(xs.min()-3,0),min(xs.max()+4,w)
            win=bg[y0:y1,x0:x1];comp=(lab[y0:y1,x0:x1]==nid)
            if win[~comp].mean()>.45: bg[ys,xs]=True
            continue
        ys,xs=np.array(pts).T;v=mn[ys,xs]
        if v.mean()>.86: bg[ys,xs]=True
    px[...,3]=np.where(bg,0,1)
    o=bpy.data.images.new("o",w,h,alpha=True);o.pixels=px.ravel();o.filepath_raw=os.path.join(dst,fn);o.file_format="PNG";o.save();bpy.data.images.remove(o);bpy.data.images.remove(im)
print("DONE",len(os.listdir(dst)))
