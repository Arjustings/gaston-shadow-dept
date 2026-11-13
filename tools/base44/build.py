#!/usr/bin/env python3
"""Pack the game into one bundle for Base44: base44/game.zip + base44/models.zip

  python3 base44/build.py [path/to/gltf-transform]

The zip holds index.html, levels.js, audio.js and assets/** (only what the game loads).
GLBs are meshopt-compressed, big PNG textures become WebP. The Base44 page (loader.jsx)
downloads the zip, turns every file into a blob URL and runs index.html in a full-screen frame.
"""
import glob, os, re, shutil, subprocess, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, 'dist')
GT = sys.argv[1] if len(sys.argv) > 1 else shutil.which('gltf-transform')

shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(os.path.join(OUT, 'assets'))

html = open(os.path.join(ROOT, 'stage/index.html'), encoding='utf-8').read()
levels = open(os.path.join(ROOT, 'stage/levels.js'), encoding='utf-8').read()
audio = open(os.path.join(ROOT, 'stage/audio.js'), encoding='utf-8').read()

# ---- which assets does the game load? ----
files = set(re.findall(r'\.\./assets/([\w\-./]+\.(?:png|webp|gif|glb|mp3|jpg))', html))
ids = set(re.findall(r"P\('([\w-]+)'", levels)) | set(re.findall(r"file: *'([\w-]+)'", levels)) | set(re.findall(r"id: *'([\w-]+)'", levels))
for i in ids:
    if os.path.exists(os.path.join(ROOT, 'assets', i + '.glb')): files.add(i + '.glb')
for pat in ['crowd-cheer.gif', 'crowd-bored.gif', 'loyal-*-react.webp', 'ui/splat[123].webp', 'ui/tomato.webp',
            'icons/*.webp', 'story/[1-5].webp', 'sfx/*.mp3', 'lamp.glb', 'screen.glb', 'wood.png', 'tent-blur.png', 'paper.png']:
    for f in glob.glob(os.path.join(ROOT, 'assets', pat)): files.add(os.path.relpath(f, os.path.join(ROOT, 'assets')))

TO_WEBP = {'paper.png': 82, 'wood.png': 82, 'tent-blur.png': 86}
for f in sorted(files):
    src = os.path.join(ROOT, 'assets', f)
    if not os.path.exists(src): print('MISSING', f); continue
    dst = os.path.join(OUT, 'assets', f)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if f.endswith('.glb') and GT:
        subprocess.run([GT, 'meshopt', src, dst], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif f in TO_WEBP:
        subprocess.run(['cwebp', '-quiet', '-q', str(TO_WEBP[f]), src, '-o', dst[:-4] + '.webp'], check=True)
    else:
        shutil.copy(src, dst)

# ---- patch the page so it runs from blob URLs inside the Base44 frame ----
for f in TO_WEBP: html = html.replace(f, f[:-4] + '.webp')

SHIM = r'''<script>
/* Base44 bundle: window.__F maps bundle paths to blob URLs (set by the loader page). */
(()=>{const F=window.__F;window.__R=u=>{if(!F||typeof u!=='string')return u;const m=u.match(/assets\/[^?#)]+|levels\.js|audio\.js/);return(m&&F[m[0]])||u};
if(!F)return;const R=window.__R,d=Object.getOwnPropertyDescriptor(HTMLImageElement.prototype,'src');
Object.defineProperty(HTMLImageElement.prototype,'src',{configurable:true,enumerable:true,get(){return d.get.call(this)},set(v){d.set.call(this,R(v))}});
const f=window.fetch.bind(window);window.fetch=(u,o)=>f(R(u),o)})();
</script>
'''
def sub1(s, a, b):
    assert s.count(a) == 1, (s.count(a), a)
    return s.replace(a, b)

html = sub1(html, '<meta charset="utf-8">', '<meta charset="utf-8">\n' + SHIM)
html = sub1(html, "import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';",
            "import {GLTFLoader as GLTFLoader0} from 'three/addons/loaders/GLTFLoader.js';\n"
            "import {MeshoptDecoder} from 'three/addons/libs/meshopt_decoder.module.js';\n"
            "THREE.DefaultLoadingManager.setURLModifier(window.__R);\n"
            "class GLTFLoader extends GLTFLoader0{constructor(m){super(m);this.setMeshoptDecoder(MeshoptDecoder)}}")
html = sub1(html, "await import('./levels.js?v='+Date.now())", "await import(window.__F?window.__R('levels.js'):'./levels.js')")
html = sub1(html, "background-image:url(../assets/story/${f}.webp)", "background-image:url(${window.__R('../assets/story/'+f+'.webp')})")
html = sub1(html, "location.href=location.pathname", "location.reload()")
html = html.replace('../assets/', 'assets/')
audio = audio.replace('../assets/', 'assets/')

open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(html)
open(os.path.join(OUT, 'levels.js'), 'w', encoding='utf-8').write(levels)
open(os.path.join(OUT, 'audio.js'), 'w', encoding='utf-8').write(audio)

# two zips (each under 10 MB): models.zip = the 3D props, game.zip = everything else
tot = 0
for zn, pick in (('game.zip', lambda f: not f.endswith('.glb')), ('models.zip', lambda f: f.endswith('.glb'))):
    zp = os.path.join(HERE, zn)
    if os.path.exists(zp): os.remove(zp)
    n = 0
    with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for d, _, fs in os.walk(OUT):
            for f in sorted(fs):
                if f.startswith('.') or not pick(f): continue
                p = os.path.join(d, f); z.write(p, os.path.relpath(p, OUT)); n += 1
    tot += os.path.getsize(zp)
    print(f'{zn}: {n} files, {os.path.getsize(zp)/1e6:.1f} MB')
print(f'total {tot/1e6:.1f} MB')
