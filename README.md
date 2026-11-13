# Gaston Grandiose's Shadow Dept.

A comic 3D shadow-puppet puzzle set in a Paris circus, 1899. The monkeys shredded every puppet, so ringmaster Gaston Grandiose needs you: spin and arrange odd objects (a teapot, a baguette, a fork...) in front of the lamp until their shadow becomes the creature on the poster. Ten scenes, a cranky critic who reviews every show, and a crowd armed with tomatoes.

- **Play (free, no login):** https://amorphous-shadow-sculpt-lab.base44.app
- **Trailer:** https://youtu.be/sh2qEZULHWc
- Entry for the Base44 x Nitro Web Game Contest (2026), hosted on Base44.

Made by Arjun Haridas. Everything in this repository was written, modelled or art-directed by me for this game, except the third-party items listed under Credits.

## How it works

- **Real shadows, not drawings.** The stage is a three.js scene. A spotlight with shadow maps sits behind the props and throws their real shadow onto a paper screen. What you line up from the lamp's point of view is exactly the shadow the audience sees.
- **Scoring.** A camera at the lamp renders the props as a mask, which is compared with the scene's solution mask (overlap, centred, with a small tolerance). The overlap becomes "the house believes N%", the star rating and the crowd's reaction.
- **Ten scenes** are data in `game/stage/levels.js`: props, scale, the solved pose of each prop, Gaston's lines and the critic's reviews.
- **Sound.** The calliope waltz is synthesised live with the Web Audio API (`audio.js`). Sound effects are Pixabay clips (see Credits).

## Repository layout

| Path | What it is |
|---|---|
| `game/stage/index.html` | The whole game: three.js stage, controls, scoring, UI, story, reviews |
| `game/stage/levels.js` | The ten scenes |
| `game/stage/audio.js` | Music synth + sound-effect player |
| `game/stage/viewer.html` | Debug viewer for the 3D props |
| `game/assets/` | Runtime assets: 62 props (`.glb`), screen frame, textures, UI art, character animations, story frames, sound effects |
| `blender/` | Python scripts that build every 3D prop and the screen frame in Blender, headless (`blender -b --python scene12.py`). `proplib.py` is the shared kit (palette, shapes, ink outline, GLB export) |
| `blender/greenkey.py`, `checkerkey.py`, `cutout.py`, `split*.py`, `measure.py` | Image tools used to key, cut out and measure the 2D art |
| `tools/base44/` | Packaging for Base44 (`build.py` compresses the props with meshopt and bundles the game) |
| `tools/trailer/` | Trailer pipeline: scripted gameplay recorder, caption cards, ffmpeg edit |

## Running locally

```
cd game
python3 -m http.server 8821
# open http://localhost:8821/stage/index.html
```
Debug hooks: `?lvl=N` jumps to a scene, `?shot=sol` shows the solved shadow.

## How the assets were made

- **3D props (62) and the screen frame:** modelled procedurally with the Blender Python scripts in `blender/` (one script per batch of scenes), exported to GLB.
- **2D art** (Gaston, Madame Aigre the critic, crowd, tent backdrop, UI panels, buttons, icons, logo, story frames): generated with ChatGPT image generation to my art direction, then keyed, cut out and cleaned with the scripts in `blender/`.
- **Trailer story clips:** Google Flow (Veo 3.1 Lite) animating my story frames. Gameplay in the trailer is the real game, recorded with `tools/trailer/record.mjs`.
- **Code:** written for this game with an AI coding assistant (Claude) under my direction.

## Credits

- [three.js](https://threejs.org) (MIT), loaded from jsDelivr.
- Sound effects: Pixabay, under the Pixabay Content License (no attribution required). Full list in `game/assets/sfx/CREDITS.md`.
- Trailer music: "Circus Theme", Pixabay Content License.
- Fonts: Rye, Abhaya Libre, League Gothic (Google Fonts, SIL Open Font License).

## Licence

Code (`game/stage/*.js`, `game/stage/*.html`, `blender/*.py`, `tools/`) is released under the MIT licence (see `LICENSE`). The game's art, characters, 3D models and story (`game/assets/`, apart from the Pixabay sound effects) are © 2026 Arjun Haridas, all rights reserved.
