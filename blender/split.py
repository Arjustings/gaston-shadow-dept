import os;ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","game")+"/"  # repo layout: game/assets
import bpy, numpy as np
D=ROOT+"assets/ui/"
im=bpy.data.images.load(D+"buttons.png"); w,h=im.size
px=np.array(im.pixels[:],dtype=np.float32).reshape(h,w,4)
rows=(px[...,3]>0.1).sum(1); mid=h//2; gap=[y for y in range(int(h*.3),int(h*.7)) if rows[y]<5]
cut=gap[len(gap)//2] if gap else mid
for name,part in (("btn-cream",px[:cut]),("btn-red",px[cut:])):   # blender rows are bottom-up
    ys=np.where((part[...,3]>0.05).any(1))[0]; part=part[ys.min():ys.max()+1]
    o=bpy.data.images.new(name,part.shape[1],part.shape[0],alpha=True);o.pixels=part.ravel();o.filepath_raw=D+name+".png";o.file_format="PNG";o.save();print("SPLIT",name,part.shape[1],part.shape[0])
