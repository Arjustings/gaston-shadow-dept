import os;ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","game")+"/"  # repo layout: game/assets
import bpy, numpy as np
D=ROOT+"assets/ui/"
def load(n):
    im=bpy.data.images.load(D+n+".png");w,h=im.size;px=np.array(im.pixels[:],dtype=np.float32).reshape(h,w,4)[::-1];return px,w,h  # top-down
def bbox(m):
    ys,xs=np.where(m);return xs.min(),ys.min(),xs.max(),ys.max()
# --- poster inner paper: cream, low saturation, central region
px,w,h=load("poster");r,g,b=px[...,0],px[...,1],px[...,2]
cream=(r>.9)&(g>.7)&(g<.94)&(b>.38)&(b<.74)&(px[...,3]>.9)
# take rows/cols where cream dominates
rows=cream.mean(1);cols=cream.mean(0)
yr=np.where(rows>.4)[0];xr=np.where(cols>.4)[0]
print("POSTER",w,h,"paper x %.3f-%.3f y %.3f-%.3f"%(xr.min()/w,xr.max()/w,yr.min()/h,yr.max()/h))
# --- review: star outlines are gold; find in band y .2-.5
px,w,h=load("review");r,g,b=px[...,0],px[...,1],px[...,2]
gold=(r>.55)&(g>.2)&(g<.7)&(b<.2)&(b<g*.45)
band=gold.copy();band[:int(h*.2)]=False;band[int(h*.5):]=False
cols=band.sum(0);xs=np.where(cols>2)[0]
# split clusters
groups=[];start=xs[0];prev=xs[0]
for x in xs[1:]:
    if x-prev>8: groups.append((start,prev));start=x
    prev=x
groups.append((start,prev))
groups=[g_ for g_ in groups if g_[1]-g_[0]>w*.08]
for g0,g1 in groups:
    sub=band[:,g0:g1+1];ys=np.where(sub.any(1))[0]
    print("STAR x %.3f-%.3f (c %.3f) y %.3f-%.3f (c %.3f)"%(g0/w,g1/w,(g0+g1)/2/w,ys.min()/h,ys.max()/h,(ys.min()+ys.max())/2/h))
# masthead banner: cream region in top 20%
cream=(r>.9)&(g>.7)&(g<.94)&(b>.38)&(b<.74)
top=cream.copy();top[int(h*.22):]=False;top[:int(h*.03)]=False
rows=top.sum(1);yb=np.where(rows>w*.35)[0]
print("BANNER y %.3f-%.3f"%(yb.min()/h,yb.max()/h) if len(yb) else "no banner")
# body paper below stars
body=cream.copy();body[:int(h*.45)]=False
rows=body.mean(1);yb=np.where(rows>.6)[0];cols=body[int(h*.5):int(h*.85)].mean(0);xb=np.where(cols>.6)[0]
print("BODY x %.3f-%.3f y %.3f-%.3f"%(xb.min()/w,xb.max()/w,yb.min()/h,yb.max()/h))
# --- buttons: face bbox
for n,cond in (("btn-red",lambda r,g,b:(r>.55)&(g<.32)&(b<.25)),("btn-cream",lambda r,g,b:(r>.9)&(g>.7)&(g<.94)&(b>.38)&(b<.74))):
    px,w,h=load(n);m=cond(px[...,0],px[...,1],px[...,2])&(px[...,3]>.9)
    rows=m.mean(1);cols=m.mean(0);yr=np.where(rows>.3)[0];xr=np.where(cols>.3)[0]
    print(n.upper(),w,h,"face x %.3f-%.3f y %.3f-%.3f centre %.3f,%.3f"%(xr.min()/w,xr.max()/w,yr.min()/h,yr.max()/h,(xr.min()+xr.max())/2/w,(yr.min()+yr.max())/2/h))
# marquee red panel
px,w,h=load("marquee");m=(px[...,0]>.5)&(px[...,1]<.3)&(px[...,2]<.25)
rows=m.mean(1);cols=m.mean(0);yr=np.where(rows>.5)[0];xr=np.where(cols>.4)[0]
print("MARQUEE",w,h,"panel x %.3f-%.3f y %.3f-%.3f"%(xr.min()/w,xr.max()/w,yr.min()/h,yr.max()/h))
# speech inner
px,w,h=load("speech");r,g,b=px[...,0],px[...,1],px[...,2];m=(r>.9)&(g>.7)&(g<.94)&(b>.38)&(b<.74)
rows=m.mean(1);cols=m.mean(0);yr=np.where(rows>.5)[0];xr=np.where(cols>.5)[0]
print("SPEECH",w,h,"paper x %.3f-%.3f y %.3f-%.3f"%(xr.min()/w,xr.max()/w,yr.min()/h,yr.max()/h))
