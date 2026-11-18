#!/bin/bash
# Joins the main-film segments, puts the cold open in front, adds the mixed audio and the Everyday Insides logo badge.
set -e; cd "$(dirname "$0")"
for f in out/seg1/seg_*.mp4; do echo "file '$PWD/$f'"; done > out/segs.txt
ffmpeg -v error -y -f concat -safe 0 -i out/segs.txt -c copy out/main_video.mp4
TOT=$(python3 -c "import json;print(json.load(open('timings.json'))['total'])")
ffmpeg -v error -y -i ../mars3d/out/mars-cold-open-3d-final-1080p.mp4 -i out/main_video.mp4 -i out/audio_mix.wav -loop 1 -i assets/logo_overlay.png -filter_complex \
 "[0:v]setsar=1,fps=30,format=yuv420p[v0];[1:v]setsar=1,fps=30,format=yuv420p,trim=0:$TOT,setpts=PTS-STARTPTS[v1];[0:a]aresample=48000[a0];[2:a]loudnorm=I=-14.5:TP=-2.5:LRA=11,alimiter=limit=0.78,aresample=48000,atrim=0:$TOT[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[vc][a];[3:v]format=rgba[lg];[vc][lg]overlay=1747:913:shortest=1:format=auto,format=yuv420p[v]" \
 -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 18 -profile:v high -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 256k out/mars-full-1080p.mp4
ls -la out/mars-full-1080p.mp4; ffprobe -v error -show_entries format=duration -of csv=p=0 out/mars-full-1080p.mp4
