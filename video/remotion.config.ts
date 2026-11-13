import { Config } from "@remotion/cli/config";
Config.setEntryPoint("src/index.ts");
Config.setChromiumOpenGlRenderer("swangle"); // needed for WebGL/Three.js when rendering
