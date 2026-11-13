import os;ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","game")+"/"  # repo layout: game/assets
import bpy, numpy as np
D=ROOT+"assets/ui/"
for n,pts in (("poster",[(.5,.5),(.5,.3),(.5,.8)]),("review",[(.5,.6),(.21,.35),(.5,.12)]),("btn-red",[(.5,.5)]),("btn-cream",[(.5,.5)]),("speech",[(.5,.5)]),("marquee",[(.5,.6)])):
    im=bpy.data.images.load(D+n+".png");w,h=im.size;px=np.array(im.pixels[:],dtype=np.float32).reshape(h,w,4)[::-1]
    print("P",n,[tuple(px[int(y*h),int(x*w)].round(2)) for x,y in pts])
