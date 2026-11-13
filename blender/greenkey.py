import os;ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","game")+"/"  # repo layout: game/assets
import bpy, numpy as np, sys
D=ROOT+"assets/ui/"
for n in sys.argv[sys.argv.index("--")+1:]:
    im=bpy.data.images.load(D+n+"-green.png"); w,h=im.size
    px=np.array(im.pixels[:],dtype=np.float32).reshape(h,w,4)
    r,g,b=px[...,0],px[...,1],px[...,2]
    # greenness: how much g exceeds the larger of r,b
    gx=g-np.maximum(r,b)
    a=1-np.clip((gx-0.10)/0.18,0,1)
    # despill: clamp green to max(r,b) where it leaks
    spill=np.clip(gx,0,None)*(a>0)
    px[...,1]=np.where(a<1,np.minimum(g,np.maximum(r,b)+0.02),g)
    px[...,3]=a
    # crop to content
    ys,xs=np.where(a>0.05); y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
    px=px[y0:y1,x0:x1]; hh,ww=px.shape[:2]
    out=bpy.data.images.new(n,ww,hh,alpha=True); out.pixels=px.ravel(); out.filepath_raw=D+n+".png"; out.file_format="PNG"; out.save()
    print("KEY",n,ww,hh)
