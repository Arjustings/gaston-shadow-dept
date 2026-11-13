#!/usr/bin/env python3
"""Cut the 16:9 trailer for Gaston Grandiose's Shadow Dept.  ->  trailer/out/trailer.mp4

Story (Google Flow clips, Veo 3.1 Lite) + sped-up real gameplay (trailer/record.mjs) + caption cards
(trailer/cards) + Pixabay music and game SFX.  Edit the SHOTS / SFX tables and rerun.
Timing model for a gameplay clip with n props: build = 5.4 .. 5.4+1.05n, Ready R = 6.1+1.05n,
shadow full from the audience ~R+4, Gazette card ~R+5.5, stars lit ~R+7.
"""
import os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
G, F, C = (os.path.join(HERE, d) for d in ('gameplay', 'flow-out', 'cards'))
ASSETS = os.path.join(os.path.dirname(HERE), 'assets')
OUT = os.path.join(HERE, 'out'); os.makedirs(OUT, exist_ok=True)
FPS, W, H = 30, 1920, 1080

N = dict(rabbit=3, eiffel=4, sea=4, fail=5, ship=6, elephant=7, dragon=10, gaston=10)
R = {k: 6.1 + 1.05 * n for k, n in N.items()}
B = {k: (5.4, 5.4 + 1.05 * n) for k, n in N.items()}

# (source, in, out, speed, card or None, kind)   kind: g = gameplay, f = flow clip, s = still
SHOTS = [
    # hook: junk on rods, then the lamp turns it into a sea monster
    ('sea',      B['sea'][0], B['sea'][1], 4.0, None, 'g'),
    ('sea',      R['sea'] + .2, R['sea'] + 4.4, 1.25, None, 'g'),
    # the story
    ('s1', 0.4, 3.9, 1, 'c1', 'f'),
    ('s2', 0.0, 3.6, 1, 'c2', 'f'),
    ('s3', 0.0, 4.0, 1, 'c3', 'f'),
    ('s4', 0.2, 3.6, 1, 'c4', 'f'),
    ('s5', 0.0, 3.6, 1, 'c5', 'f'),
    # gameplay montage
    ('rabbit',   B['rabbit'][0], B['rabbit'][1], 3.0, 'g1', 'g'),
    ('eiffel',   B['eiffel'][0], B['eiffel'][1], 3.0, 'g1', 'g'),
    ('elephant', B['elephant'][0], B['elephant'][1], 4.0, 'g1', 'g'),
    ('dragon',   B['dragon'][0], B['dragon'][1], 5.0, None, 'g'),
    ('dragon',   R['dragon'] + .2, R['dragon'] + 4.4, 1.35, 'g2', 'g'),
    ('ship',     R['ship'] + 4.2, R['ship'] + 8.0, 1.2, 'g3', 'g'),
    ('fail',     R['fail'] + 3.6, R['fail'] + 8.8, 1.0, 'g4', 'g'),
    ('gaston',   R['gaston'] + 4.6, R['gaston'] + 7.6, 1.0, None, 'g'),
    ('elephant', R['elephant'] + 6.0, R['elephant'] + 9.8, 1.0, 'g5', 'g'),
    # payoff + end card
    ('s6still',  0, 3.6, 1, 'f1', 's'),
    ('end',      0, 6.0, 1, None, 'e'),
]

def src(name, kind):
    if kind == 'g': return os.path.join(G, name + '.mp4')
    if kind == 'f': return os.path.join(F, name + '.mp4')
    if kind == 's': return os.path.join(HERE, 'flow-in', 's6.jpg')
    return os.path.join(C, 'end.png')

inputs, chains, t, cuts = [], [], 0.0, []
for i, (name, a, b, sp, card, kind) in enumerate(SHOTS):
    d = (b - a) / sp
    if kind in 'se':
        inputs += ['-loop', '1', '-t', f'{d:.3f}', '-i', src(name, kind)]
        z = 'zoompan=z=\'1+0.06*on/{n}\':x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':d={n}:s={W}x{H}:fps={f}'.format(n=int(d * FPS), W=W, H=H, f=FPS)
        pre = f'scale={W*2}:{H*2},{z}' if kind == 's' else f'scale={W*2}:{H*2},' + z.replace('0.06', '0.035')
        chains.append(f'[{len(inputs)//6 if False else i}:v]{pre},trim=duration={d:.3f},setpts=PTS-STARTPTS,format=yuv420p[v{i}]')
    else:
        inputs += ['-i', src(name, kind)]
        chains.append(f'[{i}:v]trim={a:.3f}:{b:.3f},setpts=(PTS-STARTPTS)/{sp},fps={FPS},scale={W}:{H}:flags=lanczos,setsar=1,format=yuv420p[v{i}]')
    cuts.append((t, t + d, card, name))
    t += d
TOTAL = t

# join, then lay cards on top (a card spanning several shots stays up continuously)
chains.append(''.join(f'[v{i}]' for i in range(len(SHOTS))) + f'concat=n={len(SHOTS)}:v=1:a=0[base]')
spans = {}
for a, b, card, _ in cuts:
    if card:
        s = spans.setdefault(card, [a, b]); s[0] = min(s[0], a); s[1] = max(s[1], b)
cur, k = 'base', len(SHOTS)
for card, (a, b) in spans.items():
    inputs += ['-loop', '1', '-t', f'{TOTAL:.3f}', '-i', os.path.join(C, card + '.png')]
    fi, fo = a + .12, b - .25
    chains.append(f'[{k}:v]format=rgba,fade=t=in:st={fi:.3f}:d=0.2:alpha=1,fade=t=out:st={fo:.3f}:d=0.2:alpha=1[c{k}]')
    chains.append(f'[{cur}][c{k}]overlay=0:0:enable=\'between(t,{a:.3f},{b:.3f})\'[o{k}]')
    cur, k = f'o{k}', k + 1
chains.append(f'[{cur}]fade=t=in:st=0:d=0.25,fade=t=out:st={TOTAL-.6:.3f}:d=0.6,format=yuv420p[vout]')

# audio: music bed + SFX on the beats
def at(shot_idx, off=0.0): return cuts[shot_idx][0] + off
SFX = [  # (file, time, gain dB)
    ('whoosh', at(0), -6), ('drumroll', at(0, .2), -4), ('lamp', at(1, .05), -2), ('crash', at(1, 1.1), -4), ('screams', at(1, 1.6), -6),
    ('whoosh', at(2), -10), ('laughbig', at(2, .6), -10),
    ('whoosh', at(3), -8),
    ('whoosh', at(4), -10), ('hmm', at(4, 1.6), -10),
    ('lamp', at(5, .2), -8),
    ('whoosh', at(7), -8), ('tick', at(7, .3), -6), ('whoosh', at(8), -8), ('tick', at(8, .3), -6), ('whoosh', at(9), -8), ('whoosh', at(10), -8),
    ('lamp', at(11, .05), -4), ('crash', at(11, 1.0), -5), ('screams', at(11, 1.5), -8),
    ('cheer', at(12), -6),
    ('boo', at(13), -4), ('splat', at(13, 1.4), -2), ('splat', at(13, 2.1), -3), ('splat', at(13, 2.9), -2),
    ('applause', at(14), -5), ('laugh', at(14, .5), -8),
    ('ding', at(15, 1.2), -4), ('ding', at(15, 1.6), -5), ('ding', at(15, 2.0), -4),
    ('applause', at(16), -7), ('crash', at(17, .1), -6), ('cheer', at(17, .2), -12),
]
music = os.path.join(HERE, 'music', 'm3.mp3')
ai = k
inputs += ['-i', music]
chains.append(f'[{ai}:a]atrim=0:{TOTAL:.3f},asetpts=PTS-STARTPTS,volume=-7dB,afade=t=in:st=0:d=0.4,afade=t=out:st={TOTAL-2.5:.3f}:d=2.5[mus]')
mix = ['[mus]']
for j, (f, tt, g) in enumerate(SFX):
    inputs += ['-i', os.path.join(ASSETS, 'sfx', f + '.mp3')]
    ms = int(tt * 1000)
    chains.append(f'[{ai+1+j}:a]volume={g}dB,adelay={ms}|{ms},apad[s{j}]')
    mix.append(f'[s{j}]')
chains.append(''.join(mix) + f'amix=inputs={len(mix)}:normalize=0:duration=first,atrim=0:{TOTAL:.3f},loudnorm=I=-16:TP=-1.5:LRA=11,volume=-1.4dB[aout]')

out = os.path.join(OUT, 'trailer.mp4')
cmd = ['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', ';\n'.join(chains), '-map', '[vout]', '-map', '[aout]',
       '-r', str(FPS), '-c:v', 'libx264', '-crf', '17', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-color_range', 'tv', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart', out]
open(os.path.join(OUT, 'filter.txt'), 'w').write(';\n'.join(chains))
r = subprocess.run(cmd); assert r.returncode == 0, "ffmpeg failed (see filter.txt)"
for a, b, card, name in cuts: print(f'{a:6.2f}-{b:6.2f}  {name:9s} {card or ""}')
print(f'TOTAL {TOTAL:.2f}s -> {out}')
