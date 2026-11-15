# Moss and the Silver Trail — AI animation prompt pack

Oakenvale Tales · Pilot · 9:16 vertical · about 74 seconds (paced to Lily's narration)

This pack recreates the *method* behind AI "animated feature film" shorts (like the two reference
videos): design the characters as still images first, make a start frame for every shot, then
animate each start frame with an image-to-video model. Everything here is your own story and your
own characters, so the finished film is original.

---

## 1. The workflow (same as the reference videos)

| Step | Tool (any of these) | What you make |
|---|---|---|
| 1. Character sheets | Midjourney, Nano Banana Pro, Ideogram | One clean reference image per character (Moss, Juniper, Pebble) |
| 2. Start frames | Same image tool, with the character sheets attached as references | One still image per shot (8 images) |
| 3. Animate | Seedance 2 (Higgsfield, Dreamina, vidIQ), Kling 2.x, Hailuo/MiniMax | One clip per shot from its start frame + the motion prompt |
| 4. Assemble | Send the clips back to me | I add Lily's narration, captions, music, sound effects and the moral card |

**Golden rules for consistency**
- Always attach the three character sheets as references (Midjourney: `--cref` / Omni Reference; Nano Banana: add the images; Kling: "Elements"; Seedance: reference images / "ingredients").
- Paste the **style line** at the start of every image prompt, unchanged.
- Generate 3–4 versions of each shot and keep the best. Reuse the same seed when a tool offers one.
- Ask for **no text, no subtitles, no logos**: captions and titles are added in the edit.
- Settings: **9:16, 1080p (or 720p), 24 or 30 fps**.

---

## 2. Style line (paste at the start of every image prompt)

> Stylized 3D animated feature-film look, warm cinematic lighting, soft subsurface-scattered fur and skin, big expressive glossy eyes, gentle rounded character design, richly detailed miniature woodland world, autumn colours, shallow depth of field, soft bokeh, 9:16 vertical composition, no text.

---

## 3. Character sheets (make these first)

Each prompt: style line + the text below + *"full body, front three-quarter view, standing on a plain soft cream background, character turnaround reference sheet, front, side and back views"*.

**Moss the snail (he)**
> A small pale green snail with big round dark glossy eyes and a gentle, calm smile, two short soft eye-stalks, a mossy green swirled shell with tiny tufts of real moss, and a tiny glowing mushroom lantern with a warm orange cap tucked on top of his shell. He leaves a faint shimmering silver trail. Cosy, kind, unhurried.

**Juniper the squirrel (she)**
> A russet red squirrel with a huge fluffy curled tail, cream belly and muzzle, bright cheeky eyes and a confident grin, wearing a tiny mustard yellow knitted scarf. Quick, playful and a little boastful, but warm hearted.

**Pebble the rabbit (he)**
> A round, soft grey rabbit with one floppy left ear and one upright right ear (pink inside), a white muzzle and cotton tail, sweet slightly worried eyes, and a small blue satchel worn across his body on a strap. Bouncy and a bit of a worrier.

**Places (optional extra references)**
- *Oakenvale village:* "A tiny woodland village of giant oak trees and red-capped toadstool houses with round glowing windows and little wooden doors, a winding mossy dirt path, golden hour."
- *Harvest Lantern Fair:* "On a rolling hill (Fernwhistle Hill), a little fair with striped tents and dozens of glowing paper lanterns strung between poles, warm orange and gold light, dusk."
- *The lantern gate:* "A rustic wooden arched gate strung with glowing paper lanterns, at the foot of the hill, leading into the fair."

---

## 4. Shot list (start frame + motion prompt)

Durations are matched to the narration. Generate a little longer than the slot; I trim in the edit.

### Shot 1 · 0:00–0:07 · generate 8 s · *"In Oakenvale, the Harvest Lantern Fair was glowing on the far side of Fernwhistle Hill."*
- **Start frame:** Wide establishing view down a winding mossy path through a tiny village of oak trees and red toadstool houses with glowing round windows; far away on a hill, a fair glows with dozens of paper lanterns. Golden hour, warm haze, falling leaves.
- **Motion prompt:** Slow, smooth cinematic push-in down the village path toward the distant glowing hill fair. Leaves drift gently through warm sunbeams, lantern lights twinkle on the hill, chimney-like wisps rise from a toadstool house. Calm, magical, no characters.

### Shot 2 · 0:07–0:17 · generate 10–11 s · *"'Last one there is a slowpoke!' laughed Juniper the squirrel, and off she zipped. Pebble the rabbit hopped after her. Hop, hop… gone!"*
- **Start frame:** On the village path, Juniper the squirrel stands grinning cheekily at camera with hands on hips, Pebble the rabbit beside her, Moss the snail smiling just behind them. Medium shot, golden hour.
- **Motion prompt:** Juniper laughs and points ahead teasingly, then spins around and dashes off along the path in a blur, her fluffy tail bouncing, kicking up a small puff of dust. Pebble blinks, then hops after her in three big bouncy hops and disappears down the path. Moss stays where he is, smiling calmly. Playful, energetic, comedic timing.

### Shot 3 · 0:17–0:26 · generate 9–10 s · *"Little Moss the snail just smiled, and kept to the path. Slow and steady, one silvery inch at a time."*
- **Start frame:** Low close-up of Moss the snail on the mossy path, gentle smile, tiny mushroom lantern glowing on his shell, warm golden backlight, soft bokeh village behind.
- **Motion prompt:** Moss smiles softly, blinks slowly, and glides forward along the path, his body gently stretching and contracting. Behind him a thin trail shimmers silver with tiny sparkles catching the light. Camera tracks slowly alongside him at ground level. Peaceful and content.

### Shot 4 · 0:26–0:37 · generate 11–12 s · *"But as the sun slipped down, a thick fog came rolling in. Juniper stopped. Pebble stopped. Every tree looked the same."*
- **Start frame:** A hillside among many identical oak trees at sunset, orange sky; Juniper and Pebble have just run into a small clearing.
- **Motion prompt:** The sun sinks behind the hill and the sky shifts from orange to dusky blue as thick grey fog rolls in between the trees. Juniper skids to a stop, then Pebble stops beside her. They look left, then right, then at each other, confused; every tree looks exactly the same. Slow push-in, the mood turning quiet and a little uneasy.

### Shot 5 · 0:37–0:40 · generate 4–5 s · *"'Which way is the Fair?' Pebble whispered."*
- **Start frame:** Close-up of Pebble the rabbit in soft blue fog, ears drooping, big worried eyes; Juniper's paw entering frame.
- **Motion prompt:** Pebble's floppy ear droops lower, his eyes glisten, and he whispers a small question. Juniper gently takes his paw to comfort him. Very slow push-in, soft and tender.

### Shot 6 · 0:40–0:48 · generate 8 s · *"Then, through the fog, something shimmered. A thin silver line, glowing in the moonlight. 'It's Moss's trail!'"*
- **Start frame:** Night in the foggy wood, blue moonlight. Juniper and Pebble stand close together looking down at the misty ground.
- **Motion prompt:** A thin line on the ground begins to glow silver and shimmer, revealing itself through the fog and stretching away into the distance like a path of starlight. Its soft light rises onto the friends' faces as they gasp in wonder; Juniper's face lights up and she points excitedly. Magical sparkles, hopeful mood.

### Shot 7 · 0:48–0:58 · generate 10–11 s · *"They followed it, step by step, until the fog melted away, and there was Moss, waiting at the gate of the Fair."*
- **Start frame:** Juniper and Pebble walking side by side along the glowing silver trail into the fog, seen from behind.
- **Motion prompt:** The two friends walk carefully along the glowing silver trail. The fog melts away around them, revealing a wooden arched gate strung with glowing paper lanterns at the foot of the hill. Waiting right at the gate is Moss the snail, his little mushroom lantern twinkling, smiling at them. Camera follows behind, then rises gently to reveal the gate and the glowing fair beyond.

### Shot 8 · 0:58–1:14 · generate 15 s · *"'You're not slow, Moss,' said Juniper. 'You're the one who lit the way.'"* then the moral.
- **Start frame:** At the lantern-lit gate at night, Juniper, cheeks pink, stands in front of Moss; Pebble beside them; the fair glowing behind.
- **Motion prompt:** Juniper, cheeks blushing pink, smiles shyly and says something kind to Moss, then gives him a big warm hug while Pebble hops happily. Then all three friends turn and walk together through the lantern-lit gate into the fair as autumn leaves fall like confetti. Camera slowly pulls back into a wide shot and holds on the glowing fair. Warm, joyful, heart-warming ending.
- *(The moral card "Slow is not small. Every gift can light someone's way." and the Oakenvale Tales logo are added in the edit over the final wide shot.)*

---

## 5. Sending the clips back

Name them `shot1.mp4` … `shot8.mp4` (any length close to the target is fine) and either:
- upload them to this chat, or
- put them in `video/public/moss/clips/` in the repository.

I then render the final film with Lily's narration, word-by-word captions, the music-box score,
sound effects, the opening title and the moral card. Shots that are a little short or long are
gently sped up or slowed down (up to 20%) or hold on their last frame, so timing always matches
the narration.

**Tip:** these video models often add their own sound. The edit mutes the clips and uses our
soundtrack, so the narration stays clear.
