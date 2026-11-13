import os;ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","game")+"/"  # repo layout: game/assets
import bpy, numpy as np
D=ROOT+"assets/ui/"
im=bpy.data.images.load(D+"icons.png");w,h=im.size;px=np.array(im.pixels[:],dtype=np.float32).reshape(h,w,4)
cols=(px[...,3]>.1).sum(0);mid=[x for x in range(int(w*.3),int(w*.6)) if cols[x]<3]
cut=mid[len(mid)//2]
for name,part in (("icon-spin",px[:,:cut]),("icon-turn",px[:,cut:])):
    xs=np.where((part[...,3]>.05).any(0))[0];ys=np.where((part[...,3]>.05).any(1))[0];part=part[ys.min():ys.max()+1,xs.min():xs.max()+1]
    o=bpy.data.images.new(name,part.shape[1],part.shape[0],alpha=True);o.pixels=part.ravel();o.filepath_raw=D+name+".png";o.file_format="PNG";o.save();print("SPLIT",name,part.shape[1],part.shape[0])
