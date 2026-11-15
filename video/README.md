# 3D video project (Three.js + Remotion)

- `npm install` – install deps
- `npm run studio` – live preview editor
- `npm run render` – render `out/video.mp4`

Edit `src/Main.tsx`: 3D scene (`@remotion/three`), captions (`@remotion/captions`).
Audio: put files in `public/` and use `<Audio src={staticFile("x.mp3")} />`.
Animate with `useCurrentFrame()`, not timers.
