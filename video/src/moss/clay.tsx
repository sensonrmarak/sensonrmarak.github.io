import * as THREE from "three";
import { rand } from "./util";

/** Thumbprint-style bump texture shared by every clay surface. */
let _bump: THREE.CanvasTexture | null = null;
export const clayBump = () => {
  if (_bump) return _bump;
  const c = document.createElement("canvas");
  c.width = c.height = 256;
  const g = c.getContext("2d")!;
  g.fillStyle = "#808080";
  g.fillRect(0, 0, 256, 256);
  for (let i = 0; i < 70; i++) {
    const x = rand(i) * 256, y = rand(i + 99) * 256, r = 20 + rand(i + 7) * 22;
    for (let k = 0; k < 5; k++) {
      g.strokeStyle = `rgba(${k % 2 ? 255 : 0},${k % 2 ? 255 : 0},${k % 2 ? 255 : 0},0.07)`;
      g.lineWidth = 2;
      g.beginPath();
      g.ellipse(x, y, r - k * 3.5, (r - k * 3.5) * 0.7, rand(i + 3) * 3, 0, Math.PI * 1.6);
      g.stroke();
    }
  }
  for (let i = 0; i < 1600; i++) {
    const v = Math.floor(100 + rand(i + 500) * 60);
    g.fillStyle = `rgba(${v},${v},${v},0.25)`;
    g.fillRect(rand(i + 900) * 256, rand(i + 1300) * 256, 2, 2);
  }
  _bump = new THREE.CanvasTexture(c);
  _bump.wrapS = _bump.wrapT = THREE.RepeatWrapping;
  _bump.repeat.set(2, 2);
  return _bump;
};

/** Soft round sprite used for fog puffs and glows. */
let _soft: THREE.CanvasTexture | null = null;
export const softTex = () => {
  if (_soft) return _soft;
  const c = document.createElement("canvas");
  c.width = c.height = 128;
  const g = c.getContext("2d")!;
  const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64);
  gr.addColorStop(0, "rgba(255,255,255,1)");
  gr.addColorStop(0.4, "rgba(255,255,255,0.55)");
  gr.addColorStop(1, "rgba(255,255,255,0)");
  g.fillStyle = gr;
  g.fillRect(0, 0, 128, 128);
  _soft = new THREE.CanvasTexture(c);
  return _soft;
};

export const Clay = ({ color, rough = 0.88, bump = 1 }: { color: string; rough?: number; bump?: number }) => (
  <meshStandardMaterial color={color} roughness={rough} metalness={0} bumpMap={clayBump()} bumpScale={bump} />
);

export const Glow = ({ color, intensity = 1.5, opacity = 1 }: { color: string; intensity?: number; opacity?: number }) => (
  <meshStandardMaterial color={color} emissive={color} emissiveIntensity={intensity} roughness={0.6}
    transparent={opacity < 1} opacity={opacity} />
);

export const Eye = ({ r = 0.06 }: { r?: number }) => (
  <group>
    <mesh><sphereGeometry args={[r, 20, 16]} /><meshStandardMaterial color="#17110d" roughness={0.12} /></mesh>
    <mesh position={[r * 0.35, r * 0.4, r * 0.75]}><sphereGeometry args={[r * 0.28, 10, 8]} /><meshBasicMaterial color="#ffffff" /></mesh>
    <mesh position={[-r * 0.3, -r * 0.35, r * 0.85]}><sphereGeometry args={[r * 0.12, 8, 6]} /><meshBasicMaterial color="#ffffff" /></mesh>
  </group>
);
