#!/bin/sh
# Renders the 4K whiteboard video in resumable chunks, then joins them: sh scripts/wb_render.sh
B=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell
TOTAL=$(node -e "const n=require('./src/wb/narration.json');console.log(Math.ceil(n.total*24)+96)")
CH=1200; mkdir -p out/wb; i=0; : > out/wb/list.txt
while [ $((i*CH)) -lt $TOTAL ]; do
  a=$((i*CH)); b=$((a+CH-1)); [ $b -ge $TOTAL ] && b=$((TOTAL-1)); f=out/wb/part_$(printf %02d $i).mp4
  if [ ! -f $f ]; then
    npx remotion render UpscWbMonsoon $f.tmp.mp4 --frames=$a-$b --image-format=jpeg --jpeg-quality=95 --concurrency=4 --browser-executable=$B --crf=18 > out/wb/log_$i.txt 2>&1 && mv $f.tmp.mp4 $f
  fi
  echo "file 'part_$(printf %02d $i).mp4'" >> out/wb/list.txt; i=$((i+1))
done
ffmpeg -v error -y -f concat -safe 0 -i out/wb/list.txt -c copy out/upsc_monsoon_whiteboard_4k.mp4 && echo done > out/wb/DONE
