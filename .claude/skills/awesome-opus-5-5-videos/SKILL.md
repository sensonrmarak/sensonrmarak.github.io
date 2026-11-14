---
name: awesome-opus-5-5-videos
description: Reference library of 703 real prompts behind viral videos made with Claude Opus 5.5 (motion showreels, product promos, explainers, kinetic type, 3D, data viz). Use when the user wants a video "like the ones people make with Opus 5.5", needs prompt ideas or a proven starting prompt, or asks what techniques/styles work for code-made video.
---

# Awesome Opus 5.5 videos

A local copy of [yihui-dev/awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos) (see `LICENSE`).

## Files

- `data/videos.json`: a list of 703 entries with `slug`, `author`, `post_url`, `category`, `tech_tags`, `prompt`, `prompt_partial`, `skillry_url`, `added`, `has_remake`.
- `prompts/<slug>.md`: one Markdown file per video with the full prompt and links to the original post and a live remake.

## How to use

1. Search instead of reading everything. Filter `data/videos.json` by `category` or `tech_tags`, or grep `prompts/` for a keyword (for example `showreel`, `kinetic`, `three.js`, `product`).
2. Pick 2–3 close matches, read their prompt files, and note what made them work: length, structure, named chapters, duration, palette, stack.
3. Write a new prompt for the user's own topic, borrowing structure, never copying a creator's brand or content. Credit the source entries in your reply.
4. Build the video with the tools in this project (HyperFrames, Remotion, three.js, the motion skills).

`prompt_partial: true` means only part of the original prompt was published.
