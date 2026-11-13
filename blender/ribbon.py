import os;ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","game")+"/"  # repo layout: game/assets
import bpy, numpy as np
im=bpy.data.images.load(ROOT+"assets/ui/review.png");w,h=im.size
px=np.array(im.pixels[:],dtype=np.float32).reshape(h,w,4)[::-1];r,g,b=px[...,0],px[...,1],px[...,2]
cream=(r>.88)&(g>.68)&(b>.38)&(b<.8)
y0,y1=int(h*.04),int(h*.24)
for fx in (.24,.3,.4,.5,.6,.7,.76):
    x=int(w*fx);col=cream[y0:y1,x];best=(0,0);run=0;start=0
    for i,v in enumerate(col):
        if v: 
            if run==0: start=i
            run+=1
            if run>best[0]: best=(run,start)
        else: run=0
    L,S=best;print("COL %.2f top %.4f bot %.4f mid %.4f"%(fx,(y0+S)/h,(y0+S+L)/h,(y0+S+L/2)/h))
