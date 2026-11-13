# Apps, PWAs, mobile and 3D

16 lessons. Most-repeated first.

- Headless three.js checks need `--use-angle=d3d11 --ignore-gpu-blocklist` or WebGL falls back to slow software GL; never run two browser jobs at once on a loaded machine (runs crash with TargetClosed / start-button timeouts). For any game/audio app, test WebKit: Web Audio calls before `AudioContext` exists threw inside the frame loop and froze the whole game (every on-screen button "did nothing"). Guard sound methods when `!ctx`, wrap the per-frame step in try/finally so the loop always reschedules, and let mute toggle a preference even before audio starts.
- "Too 2D" meant two things: flat chrome (4 px radius, hairlines, no elevation) AND a flat canvas scene. Fix both: tokens (radius 18/26, layered warm shadows, surface-2 tiles, radial glow, pill controls, floating nav) plus canvas depth cues (perspective side panes, receding floor band, depth haze over the far layer, floor shadows offset by z, rim, pane edges, glass streak, vignette).
- "similar to Jeda or Sansa" means a walkable 3D space with avatars (three.js, tap/WASD to walk, sit at things), not a 2D floor plan with the same social rules. Before building anything "like X" from the user's own repos, open X's README and code first and match its interaction model; Jeda's vendor/three.module.min.js (r160) can be reused directly.
- IOS web audio: `navigator.audioSession.type = "playback"` (Safari 16.4+) so the silent switch does not mute; resume the AudioContext on visibilitychange/pageshow/pointerdown because iOS leaves it "interrupted" after calls.
- Nongkrong: label collision in 3D must use view depth (camera space z), not distance to camera, or labels near the screen edge are sized wrong and overlap on phones.
- (founder-studio v2) Coplanar three.js path planes over a disc shaded as dark slabs; paint paths into one CanvasTexture on the ground instead.
- Nongkrong: when a web app gains a new ES module, add it to the service worker precache and bump the cache name, or the offline load breaks.
- When a 3D hit mesh (basket) occludes the objects inside it, drag starts must accept the container hit as well as the item hit.
- Never put backdrop-filter on overlays above an animated canvas (it re-blurs every frame); solid rgba pills instead.
- Canvas thumbnails drawn in a requestAnimationFrame right after opening a sheet can run before layout: clientWidth/Height are 0, the canvas falls back to the 300x150 default buffer and the art comes out oversized and clipped. Wait until clientWidth and clientHeight are non-zero (retry a few frames) before sizing the buffer.
- Widgets that cannot run WebGL (Android RemoteViews, WPF) play pre-rendered frames of the same model; index desktop frames by fold (not time) so speed-ups still work; dedupe identical Android poses (16 flips -> 9 drawables).
- Cat.svg must stay flat (no gradients): the WPF desktop widget and the Android frame generator both parse it. Regenerate the widget frames and bump versionCode on every cat change so CI re-releases the APK.
- An offscreen preview page needs `canvas{width:100%;height:100%}`: renderer.setSize(w, h, false) does not set CSS size, so at DPR 2 the canvas overflows the stage and element screenshots come out cropped.
- Fit irregular canvas art (fan tails, long fins) by drawing once on a scratch canvas, reading the alpha bounds with getImageData and scaling to fit; fixed length ratios clip outliers.
- Tooling: Playwright's bundled Chromium can be missing for the installed version ("Executable doesn't exist ... chromium_headless_shell-1223" while only 1187 is cached); launch with a fallback to `channel="msedge"`, then `"chrome"`, instead of installing browsers.
- Three.js raycasts hit invisible LineSegments/helpers: filter raycast targets to visible meshes or drags grab the wrong object.
