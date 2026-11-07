"""Builds Oakenvale_Moss_AI_Animation.ipynb (run: python3 colab/build_notebook.py)."""
import json, os

cells = []


def md(text):
    cells.append({"cell_type": "markdown", "metadata": {}, "source": text.strip("\n").splitlines(keepends=True)})


def code(text):
    cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
                  "source": text.strip("\n").splitlines(keepends=True)})


md("""
# 🌰 Oakenvale Tales — *Moss and the Silver Trail* (free AI animation)

This notebook makes the 8 shots of the pilot with **free, open-source AI models** on Google's free GPU. No paid credits.

| Step | Model | What it makes |
|---|---|---|
| 1 | SDXL | Character reference images for Moss, Juniper and Pebble |
| 2 | SDXL + IP-Adapter | A start frame for each shot, using the characters as references |
| 3 | LTX-Video (image-to-video) | The animated clips, chained so longer shots stay continuous |

**How to run**
1. `Runtime → Change runtime type → T4 GPU` (Colab) or `Settings → Accelerator → GPU T4` (Kaggle).
2. `Runtime → Run all`. Everything is saved to **Google Drive → MyDrive/Oakenvale**, so if Colab disconnects, just run all again and it continues where it stopped.
3. When it finishes, download **`Oakenvale/clips`** (shot1.mp4 … shot8.mp4) and send them back to Claude for the final edit (narration, captions, music, moral card).

**Better characters for free (optional):** make the character images or start frames in the free **Gemini app (Nano Banana)** using the prompt pack, and upload them to `MyDrive/Oakenvale/refs/moss_custom.png`, `juniper_custom.png`, `pebble_custom.png`, or `MyDrive/Oakenvale/frames/shot3_1_custom.png` etc. The notebook uses your images instead of generating its own.

⏱️ Expect roughly 2–3 hours of GPU time in total. Colab's free tier has daily limits, so it may take two sessions. Kaggle's free tier (30 GPU hours a week, more memory) also works.
""")

code(r'''
#@title 1. Setup: GPU check, storage folder, libraries
import os, sys, subprocess, shutil, gc, json, time
IN_COLAB = "google.colab" in sys.modules
IN_KAGGLE = os.path.exists("/kaggle/working")
if IN_COLAB:
    from google.colab import drive
    drive.mount("/content/drive")
    ROOT = "/content/drive/MyDrive/Oakenvale"
elif IN_KAGGLE:
    ROOT = "/kaggle/working/Oakenvale"
else:
    ROOT = os.path.abspath("Oakenvale")
for d in ("refs", "frames", "segs", "clips"):
    os.makedirs(os.path.join(ROOT, d), exist_ok=True)
print("Saving everything to", ROOT)
gpu = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
                     capture_output=True, text=True).stdout.strip()
print("GPU:", gpu or "NONE! Switch the runtime to a GPU (Runtime > Change runtime type > T4 GPU), then run again.")
''')

code(r'''
#@title 2. Install the free AI libraries (about 1 minute)
!pip -q install -U diffusers transformers accelerate sentencepiece "imageio[ffmpeg]" ftfy
''')

code(r'''
#@title 3. Story, characters and settings (edit prompts here if you like)

# ---- quality / speed settings ----
W, H = 480, 832          # video size (9:16). 576x1024 looks sharper but is slower.
FPS = 24
NUM_FRAMES = 121         # frames per segment (must be 8*k+1). 121 = about 5 seconds.
VIDEO_STEPS = 40         # LTX-Video steps (30 = faster, 50 = a little better)
IMAGE_STEPS = 30         # SDXL steps
N_CAND = 3               # how many candidate images to make for each character / start frame
SEED = 2024
IP_SCALE_ONE = 0.6       # how strongly a start frame copies the character reference (one character)
IP_SCALE_MANY = 0.4      # same, when several characters are in the frame
SDXL_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
LTX_MODEL = "Lightricks/LTX-Video"

# ---- look ----
STYLE_IMG = ("3d animated feature film still, cute stylized characters, soft warm cinematic lighting, "
             "subsurface scattering, big expressive glossy eyes, miniature woodland world, depth of field, highly detailed")
NEG_IMG = "photo, realistic, live action, text, watermark, logo, blurry, deformed, extra limbs, ugly, low quality, frame, border"
STYLE_VID = ("Stylized 3D animated feature film, soft warm cinematic lighting, cute expressive characters with big glossy eyes, "
             "smooth natural character animation, rich detailed miniature woodland world, shallow depth of field.")
NEG_VID = ("worst quality, inconsistent motion, blurry, jittery, distorted, deformed face, morphing, extra limbs, "
           "text, subtitles, watermark, logo, live action, realistic photo")

# ---- characters (keep identical everywhere) ----
CHARACTERS = {
    "moss": "a small pale green snail with big round dark glossy eyes, a gentle smile, a mossy green swirled shell "
            "with a tiny glowing orange mushroom lantern on top",
    "juniper": "a russet red squirrel with a huge fluffy curled tail, cream belly, bright cheeky eyes, "
               "wearing a tiny mustard yellow knitted scarf",
    "pebble": "a round soft grey rabbit with one floppy ear and one upright ear, white muzzle, sweet worried eyes, "
              "a small blue satchel worn across his body",
}
M, J, P = CHARACTERS["moss"], CHARACTERS["juniper"], CHARACTERS["pebble"]

# ---- shots: each segment is ~5 s. A segment with "frame" starts from a new start image;
#      a segment without "frame" continues from the last frame of the previous segment. ----
SHOTS = [
    {"n": 1, "segments": [
        {"chars": [], "frame": "wide view down a winding mossy dirt path through a tiny woodland village of giant oak trees and red "
                               "toadstool houses with glowing round windows, a distant hill with a fair glowing with paper lanterns, golden hour, falling leaves",
         "motion": "A slow, smooth cinematic push-in down a winding mossy path through a tiny woodland village of giant oak trees and red "
                   "toadstool houses with glowing windows. Far away on a hill a fair glows with dozens of paper lanterns. Autumn leaves "
                   "drift through warm golden sunbeams and the lanterns twinkle. Calm and magical, no characters."}]},
    {"n": 2, "segments": [
        {"chars": ["juniper", "pebble", "moss"],
         "frame": f"{J} grinning cheekily with hands on hips on a mossy village path, next to {P}, and {M} smiling behind them, golden hour",
         "motion": f"{J} laughs, points ahead teasingly, then spins around and dashes away down the mossy path in a blur, her huge fluffy "
                   "tail bouncing, kicking up a small puff of dust. Her friends watch her go. Playful, energetic, comedic."},
        {"motion": f"{P} blinks in surprise, then hops after her in three big bouncy hops and disappears down the path, while {M} stays "
                   "behind smiling calmly. The camera holds steady. Playful and bouncy."}]},
    {"n": 3, "segments": [
        {"chars": ["moss"], "frame": f"low close-up of {M} on a mossy path, warm golden backlight, soft bokeh village behind",
         "motion": f"Close-up of {M}. He smiles softly, blinks slowly and glides forward along the mossy path, his body gently stretching. "
                   "Behind him a thin trail shimmers silver with tiny sparkles catching the golden light. The camera tracks slowly at ground level."},
        {"motion": f"{M} keeps gliding slowly and contentedly along the path, slow and steady, his little mushroom lantern glowing warmly. "
                   "The shimmering silver trail stretches behind him. Peaceful, gentle, golden light."}]},
    {"n": 4, "segments": [
        {"chars": ["juniper", "pebble"],
         "frame": f"{J} and {P} running into a small clearing between many identical oak trees on a hillside, orange sunset sky",
         "motion": f"The sun sinks behind the hill and the sky turns from orange to dusky blue as thick grey fog starts rolling in between "
                   f"the trees. {J} skids to a stop, then {P} stops beside her. The mood turns quiet."},
        {"motion": "Thick grey fog swirls between the identical trees. The squirrel and the rabbit look left, then right, then at each other, "
                   "confused and a little worried. Every tree looks the same. Slow push-in, dim blue dusk light."}]},
    {"n": 5, "segments": [
        {"chars": ["pebble", "juniper"],
         "frame": f"close-up of {P} in soft blue fog at dusk, ears drooping, big worried eyes, a red squirrel paw beside him",
         "motion": f"Close-up of {P} in soft blue fog. His floppy ear droops lower, his eyes glisten, and he whispers a small worried "
                   "question. A red squirrel's paw gently takes his paw to comfort him. Very slow push-in, tender."}]},
    {"n": 6, "segments": [
        {"chars": ["juniper", "pebble"],
         "frame": f"night in a foggy wood under blue moonlight, {J} and {P} standing close together looking down at the misty ground",
         "motion": "Night in a foggy wood under blue moonlight. A thin line on the ground begins to glow silver and shimmer, revealing "
                   "itself through the fog and stretching away into the distance like a path of starlight, with magical sparkles."},
        {"motion": f"The silver light rises onto the friends' faces. {J} gasps in wonder, her face lights up with joy and she points at the "
                   f"glowing trail excitedly while {P} smiles with relief. Hopeful, magical."}]},
    {"n": 7, "segments": [
        {"chars": ["juniper", "pebble"],
         "frame": f"{J} and {P} seen from behind walking side by side along a glowing silver trail into misty fog at night",
         "motion": f"Seen from behind, {J} and {P} walk carefully side by side along a glowing silver trail. The fog slowly melts away "
                   "around them under the moonlight. The camera follows behind them."},
        {"chars": ["moss", "juniper", "pebble"],
         "frame": f"{M} waiting and smiling in front of a rustic wooden arched gate strung with glowing paper lanterns at night, "
                  "a glowing fair on the hill behind",
         "motion": f"{M} waits at a wooden arched gate strung with glowing paper lanterns, his little mushroom lantern twinkling. "
                   "He smiles warmly as his friends arrive. The camera rises gently to reveal the glowing lantern fair on the hill behind."}]},
    {"n": 8, "segments": [
        {"chars": ["juniper", "moss", "pebble"],
         "frame": f"{J} with pink blushing cheeks standing in front of {M} at a lantern-lit wooden gate at night, {P} beside them",
         "motion": f"{J}, cheeks blushing pink, smiles shyly and says something kind to {M}, then gives him a big warm hug. "
                   f"{P} hops happily beside them. Warm lantern light."},
        {"motion": "All three friends turn and walk together through the lantern-lit gate into the fair as autumn leaves fall like "
                   "confetti. Warm, joyful."},
        {"motion": "The camera slowly pulls back into a wide shot of the glowing lantern fair on the hill at night, paper lanterns "
                   "twinkling, leaves drifting down. A peaceful, heart-warming ending."}]},
]
n_seg = sum(len(s["segments"]) for s in SHOTS)
print(f"{len(SHOTS)} shots, {n_seg} video segments of ~{NUM_FRAMES / FPS:.1f}s each")
''')

code(r'''
#@title 4. Helpers
import torch
from PIL import Image, ImageOps
from IPython.display import display

def free():
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

def p(*parts):
    return os.path.join(ROOT, *parts)

def show(paths, titles=None, size=256):
    imgs = [Image.open(x) for x in paths if os.path.exists(x)]
    if not imgs:
        return
    thumbs = [ImageOps.contain(im.convert("RGB"), (size, size)) for im in imgs]
    sheet = Image.new("RGB", (size * len(thumbs), size), "white")
    for i, t in enumerate(thumbs):
        sheet.paste(t, (i * size + (size - t.width) // 2, (size - t.height) // 2))
    if titles:
        print("   ".join(titles))
    display(sheet)

def fit(img):
    return ImageOps.fit(img.convert("RGB"), (W, H), Image.LANCZOS)
''')

code(r'''
#@title 5. Character reference images (SDXL)
from diffusers import StableDiffusionXLPipeline, AutoencoderKL
from transformers import CLIPVisionModelWithProjection

def load_sdxl():
    enc = CLIPVisionModelWithProjection.from_pretrained("h94/IP-Adapter", subfolder="models/image_encoder", torch_dtype=torch.float16)
    vae = AutoencoderKL.from_pretrained("madebyollin/sdxl-vae-fp16-fix", torch_dtype=torch.float16)
    kw = dict(vae=vae, image_encoder=enc, torch_dtype=torch.float16, use_safetensors=True)
    try:
        pipe = StableDiffusionXLPipeline.from_pretrained(SDXL_MODEL, variant="fp16", **kw)
    except Exception:
        pipe = StableDiffusionXLPipeline.from_pretrained(SDXL_MODEL, **kw)
    pipe.load_ip_adapter("h94/IP-Adapter", subfolder="sdxl_models", weight_name="ip-adapter-plus_sdxl_vit-h.safetensors")
    pipe.to("cuda")
    pipe.enable_vae_tiling()
    return pipe

BLANK = Image.new("RGB", (224, 224), "white")
sdxl = load_sdxl()
sdxl.set_ip_adapter_scale(0.0)
for name, desc in CHARACTERS.items():
    if os.path.exists(p("refs", f"{name}_custom.png")):
        print(name, ": using your uploaded image")
        continue
    for c in range(N_CAND):
        out = p("refs", f"{name}_{c}.png")
        if os.path.exists(out):
            continue
        t = time.time()
        img = sdxl(prompt=f"{desc}, full body character design, standing, front three-quarter view, plain soft cream background, centered, {STYLE_IMG}",
                   negative_prompt=NEG_IMG, width=1024, height=1024, num_inference_steps=IMAGE_STEPS, guidance_scale=6.0,
                   ip_adapter_image=[[BLANK]], generator=torch.Generator("cuda").manual_seed(SEED + c)).images[0]
        img.save(out)
        print(f"{name} candidate {c}: {time.time() - t:.0f}s")
    show([p("refs", f"{name}_{c}.png") for c in range(N_CAND)], [f"{name} {c}" for c in range(N_CAND)])
''')

code(r'''
#@title 6. Pick the best character images (change the numbers, then run this cell again)
CHAR_PICK = {"moss": 0, "juniper": 0, "pebble": 0}
for name, c in CHAR_PICK.items():
    custom = p("refs", f"{name}_custom.png")
    shutil.copy(custom if os.path.exists(custom) else p("refs", f"{name}_{c}.png"), p("refs", f"{name}.png"))
show([p("refs", f"{n}.png") for n in CHARACTERS], list(CHARACTERS))
''')

code(r'''
#@title 7. Start frames for every shot (SDXL + IP-Adapter with the character images)
refs = {n: Image.open(p("refs", f"{n}.png")).convert("RGB") for n in CHARACTERS}
for shot in SHOTS:
    for k, seg in enumerate(shot["segments"], 1):
        if "frame" not in seg:
            continue
        tag = f"shot{shot['n']}_{k}"
        if os.path.exists(p("frames", f"{tag}_custom.png")):
            print(tag, ": using your uploaded image")
            continue
        chars = seg.get("chars", [])
        sdxl.set_ip_adapter_scale(0.0 if not chars else IP_SCALE_ONE if len(chars) == 1 else IP_SCALE_MANY)
        ref_imgs = [refs[n] for n in chars] or [BLANK]
        for c in range(N_CAND):
            out = p("frames", f"{tag}_cand{c}.png")
            if os.path.exists(out):
                continue
            t = time.time()
            img = sdxl(prompt=f"{seg['frame']}, {STYLE_IMG}", negative_prompt=NEG_IMG, width=768, height=1344,
                       num_inference_steps=IMAGE_STEPS, guidance_scale=6.0, ip_adapter_image=[ref_imgs],
                       generator=torch.Generator("cuda").manual_seed(SEED + 10 * shot["n"] + k * 100 + c)).images[0]
            img.save(out)
            print(f"{tag} candidate {c}: {time.time() - t:.0f}s")
        show([p("frames", f"{tag}_cand{c}.png") for c in range(N_CAND)], [f"{tag} #{c}" for c in range(N_CAND)], 200)
del sdxl
free()
''')

code(r'''
#@title 8. Pick the best start frames (e.g. FRAME_PICK = {"shot3_1": 2}), then run this cell again
FRAME_PICK = {}
chosen = []
for shot in SHOTS:
    for k, seg in enumerate(shot["segments"], 1):
        if "frame" not in seg:
            continue
        tag = f"shot{shot['n']}_{k}"
        custom = p("frames", f"{tag}_custom.png")
        src = custom if os.path.exists(custom) else p("frames", f"{tag}_cand{FRAME_PICK.get(tag, 0)}.png")
        fit(Image.open(src)).save(p("frames", f"{tag}.png"))
        chosen.append(tag)
show([p("frames", f"{t}.png") for t in chosen], chosen, 160)
''')

code(r'''
#@title 9. Animate every shot with LTX-Video (the long step; safe to re-run, finished segments are kept)
from diffusers import LTXImageToVideoPipeline
from diffusers.utils import export_to_video
import imageio, numpy as np

LTX_DTYPE = torch.bfloat16   # if you get errors or black videos, change to torch.float16

# 9a. Encode all prompts first with the big text encoder, then unload it (saves memory on free GPUs)
todo = [(s, k, seg) for s in SHOTS for k, seg in enumerate(s["segments"], 1)
        if not os.path.exists(p("segs", f"shot{s['n']}_{k}.mp4"))]
EMB = {}
if todo:
    enc = LTXImageToVideoPipeline.from_pretrained(LTX_MODEL, transformer=None, vae=None, torch_dtype=LTX_DTYPE)
    enc.text_encoder.to("cuda")
    with torch.no_grad():
        for s, k, seg in todo:
            pe, pm, ne, nm = enc.encode_prompt(prompt=f"{seg['motion']} {STYLE_VID}", negative_prompt=NEG_VID,
                                               do_classifier_free_guidance=True, max_sequence_length=256, device="cuda")
            EMB[(s["n"], k)] = [x.to("cpu") for x in (pe, pm, ne, nm)]
    del enc
    free()
    print(f"Encoded {len(EMB)} prompts")

# 9b. Generate the segments
if todo:
    ltx = LTXImageToVideoPipeline.from_pretrained(LTX_MODEL, text_encoder=None, tokenizer=None, torch_dtype=LTX_DTYPE)
    ltx.to("cuda")
    ltx.vae.enable_tiling()
for shot in SHOTS:
    for k, seg in enumerate(shot["segments"], 1):
        tag = f"shot{shot['n']}_{k}"
        vid, last = p("segs", f"{tag}.mp4"), p("segs", f"{tag}_last.png")
        if os.path.exists(vid):
            continue
        start = p("frames", f"{tag}.png") if "frame" in seg else p("segs", f"shot{shot['n']}_{k - 1}_last.png")
        image = fit(Image.open(start))
        pe, pm, ne, nm = [x.to("cuda") for x in EMB[(shot["n"], k)]]
        t = time.time()
        frames = ltx(image=image, prompt_embeds=pe, prompt_attention_mask=pm, negative_prompt_embeds=ne,
                     negative_prompt_attention_mask=nm, width=W, height=H, num_frames=NUM_FRAMES,
                     num_inference_steps=VIDEO_STEPS, guidance_scale=3.0,
                     generator=torch.Generator("cuda").manual_seed(SEED + shot["n"] * 10 + k)).frames[0]
        if np.asarray(frames[len(frames) // 2]).mean() < 3:
            print("⚠️ This segment came out black: set LTX_DTYPE = torch.float16 (or bfloat16) and run this cell again.")
        export_to_video(frames, vid, fps=FPS)
        frames[-1].save(last)
        print(f"{tag}: {time.time() - t:.0f}s")
        free()

# 9c. Join the segments of each shot into clips/shotN.mp4
for shot in SHOTS:
    out = p("clips", f"shot{shot['n']}.mp4")
    writer = imageio.get_writer(out, fps=FPS, codec="libx264", quality=8, macro_block_size=16)
    for k, seg in enumerate(shot["segments"], 1):
        reader = imageio.get_reader(p("segs", f"shot{shot['n']}_{k}.mp4"))
        for i, fr in enumerate(reader):
            if k > 1 and i == 0 and "frame" not in seg:
                continue  # skip the repeated frame where a segment continues the previous one
            writer.append_data(fr)
        reader.close()
    writer.close()
    print("saved", out)
''')

code(r'''
#@title 10. Download the clips (send these 8 files back to Claude for the final edit)
shutil.make_archive(p("oakenvale_moss_clips"), "zip", p("clips"))
print("Zip:", p("oakenvale_moss_clips.zip"))
if IN_COLAB:
    from google.colab import files
    files.download(p("oakenvale_moss_clips.zip"))
''')

nb = {"cells": cells, "metadata": {"accelerator": "GPU", "colab": {"provenance": [], "gpuType": "T4"},
                                   "kernelspec": {"display_name": "Python 3", "name": "python3"},
                                   "language_info": {"name": "python"}},
      "nbformat": 4, "nbformat_minor": 0}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Oakenvale_Moss_AI_Animation.ipynb")
json.dump(nb, open(out, "w"), indent=1)
print("wrote", out, len(cells), "cells")
