# thebasemesh-openusd

An **OpenUSD** (`.usda`, ASCII) copy of the CC0 base-mesh library from
[thebasemesh.com](https://www.thebasemesh.com/) — 100% free, public-domain 3D base meshes at real-world
scale with basic UVs.

## What this is

thebasemesh.com distributes each model as a ZIP of `.fbx` / `.glb` / `.obj`. This repo converts the **FBX**
source to **OpenUSD ASCII** (`.usda`) so they drop straight into USD pipelines (Omniverse, usdview,
Pixar OpenUSD, Godot, Blender). FBX is chosen over OBJ (identical quad topology) because it also carries
custom split normals / smoothing / material metadata; the `.glb` is the triangulated derivative and is
**not** used (it would destroy the n-gon topology).

- **`models/*.usda`** — one ASCII USD file per model (Z-up, meters, materials + UVs + normals).
- **N-gon / quad topology is preserved** — the converter does **not** triangulate, so the original
  quad-dominant base-mesh topology (and any n-gons) survives the round-trip.
- **`models-manifest.txt`** — the source download URLs on thebasemesh.com.

## Coverage

This first pass covers **60 models** (thebasemesh.com's statically-served first page). The full library is
~1,254 models loaded via the site's dynamic (Wix) pagination; extending to the full set is a mechanical
follow-up (paginate → download → convert with the same pipeline).

## How it was made

Each FBX is converted with **Blender** (headless), preserving topology:

```
blender --background --factory-startup --python fbx_to_usda_batch.py -- <fbx_dir> <usda_dir>
```

`bpy.ops.import_scene.fbx` → `bpy.ops.wm.usd_export` with materials/UVs/normals, no triangulation.

## License

Source models are **CC0 1.0** (public domain) from thebasemesh.com. This USD conversion is released the same
way — **CC0 1.0 Universal**, see [LICENSE](LICENSE). Credit to thebasemesh.com is appreciated but not
required.
