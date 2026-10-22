/* =====================================================================
   10 · Dunia 3D: langit, bukit berundak, 150 goa, macan, kamera
   ===================================================================== */
const canvas = $('#gl');
const WORLD = {
  ok: false, renderer: null, scene: null, camera: null, clock: null,
  skyRig: null, sky: null, stars: null, moon: null, moonGlow: null,
  aurora: null, clouds: null, rainbow: null, fireflies: null,
  terrain: null, caveGroup: null, caveFrame: null, cavePortal: null, caveGlow: null,
  caveCrystal: null, caveStars: null, marker: null, markerLabel: null,
  tiger: null, mom: null, tigerRoot: null, momRoot: null, tigerShadow: null,
  pointLight: null, biome: null, style: null,
  pickable: [],
};
const CAM = {
  mode: 'intro', yaw: 0.18, pitch: 0.1, dist: 5.4, zoom: 1,
  pos: new THREE.Vector3(0, 20, 80), target: new THREE.Vector3(0, 8, 0),
  posGoal: new THREE.Vector3(), targetGoal: new THREE.Vector3(),
  override: null, shake: 0, introT: 0,
};
const LEVELS = BABS.length;
const DY = 3.0;
const R0 = 76;
const RTOP = 11;
const DR = (R0 - RTOP) / (LEVELS - 1);   // tepat selebar satu teras
const FLOOR0 = 2.2;
const PROFILE = 0.78;
const CAVE_H = 2.34;

function floorY(b) { return FLOOR0 + b * DY; }
function outerR(b) {
  const t = clamp(b / (LEVELS - 1), 0, 1);
  return RTOP + (R0 - RTOP) * Math.pow(1 - t, PROFILE);
}
function innerR(b) { return Math.max(RTOP - 1.4, outerR(b) - DR); }
function summitY() { return FLOOR0 + LEVELS * DY; }
function caveAngle(i) { return i * (Math.PI * 2 / 5) + Math.floor(i / 5) * 0.22; }

function cavePose(i) {
  const b = Math.floor(i / 5);
  const th = caveAngle(i);
  // mulut goa tepat di kaki tebing tingkat berikutnya (bukan di tengah teras)
  const r = b < LEVELS - 1 ? outerR(b + 1) : innerR(LEVELS - 1);
  const y = floorY(b);
  const sx = Math.sin(th), cz = Math.cos(th);
  return {
    i, b, th, r, y,
    outward: new THREE.Vector3(sx, 0, cz),
    tangent: new THREE.Vector3(cz, 0, -sx),
    base: new THREE.Vector3(sx * (r + 0.85), y + 0.015, cz * (r + 0.85)),
    stand: new THREE.Vector3(sx * (r + 2.0), y + 0.015, cz * (r + 2.0)),
    mouth: new THREE.Vector3(sx * (r + 0.1), y + 0.9, cz * (r + 0.1)),
    star: new THREE.Vector3(sx * (r + 0.15), y + 3.05, cz * (r + 0.15)),
    camOff: 1,
  };
}

/* ---------- Util tekstur ---------- */
function makeCanvas(size, draw) {
  const c = document.createElement('canvas');
  c.width = size; c.height = size;
  draw(c.getContext('2d'), size);
  return c;
}
function texFromCanvas(c, repeatX, repeatY, srgb) {
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.repeat.set(repeatX || 1, repeatY || 1);
  if (srgb !== false) t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 4;
  t.needsUpdate = true;
  return t;
}
function noiseCanvas(base, amp, blotches) {
  return makeCanvas(256, (ctx, S) => {
    ctx.fillStyle = '#' + base.toString(16).padStart(6, '0');
    ctx.fillRect(0, 0, S, S);
    const img = ctx.getImageData(0, 0, S, S);
    for (let i = 0; i < img.data.length; i += 4) {
      const n = (Math.random() * 2 - 1) * amp;
      img.data[i] = clamp(img.data[i] + n, 0, 255);
      img.data[i + 1] = clamp(img.data[i + 1] + n, 0, 255);
      img.data[i + 2] = clamp(img.data[i + 2] + n, 0, 255);
    }
    ctx.putImageData(img, 0, 0);
    for (let i = 0; i < (blotches || 90); i++) {
      const x = Math.random() * S, y = Math.random() * S;
      const r = 2 + Math.random() * 14;
      const a = 0.04 + Math.random() * 0.10;
      ctx.fillStyle = Math.random() > 0.5 ? 'rgba(0,0,0,' + a + ')' : 'rgba(255,255,255,' + a + ')';
      ctx.beginPath(); ctx.ellipse(x, y, r, r * (0.5 + Math.random()), Math.random() * 3, 0, Math.PI * 2); ctx.fill();
    }
    // goresan batu
    ctx.strokeStyle = 'rgba(0,0,0,.07)';
    ctx.lineWidth = 1;
    for (let i = 0; i < 26; i++) {
      ctx.beginPath();
      const x = Math.random() * S;
      ctx.moveTo(x, Math.random() * S);
      ctx.lineTo(x + (Math.random() * 40 - 20), Math.random() * S);
      ctx.stroke();
    }
  });
}
function radialCanvas(inner, outer, power) {
  return makeCanvas(128, (ctx, S) => {
    const g = ctx.createRadialGradient(S / 2, S / 2, 0, S / 2, S / 2, S / 2);
    g.addColorStop(0, inner);
    g.addColorStop(Math.min(0.7, power || 0.45), outer);
    g.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, S, S);
  });
}
function starCanvas() {
  return makeCanvas(64, (ctx, S) => {
    const g = ctx.createRadialGradient(S / 2, S / 2, 0, S / 2, S / 2, S / 2);
    g.addColorStop(0, 'rgba(255,255,255,1)');
    g.addColorStop(0.25, 'rgba(255,255,255,.9)');
    g.addColorStop(0.55, 'rgba(255,255,255,.25)');
    g.addColorStop(1, 'rgba(255,255,255,0)');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, S, S);
  });
}
function heartCanvas() {
  return makeCanvas(128, (ctx, S) => {
    ctx.clearRect(0, 0, S, S);
    ctx.translate(S / 2, S / 2 + 6);
    ctx.fillStyle = '#ff6b8a';
    ctx.beginPath();
    for (let t = 0; t <= Math.PI * 2; t += 0.02) {
      const x = 16 * Math.pow(Math.sin(t), 3);
      const y = -(13 * Math.cos(t) - 5 * Math.cos(2 * t) - 2 * Math.cos(3 * t) - Math.cos(4 * t));
      if (t === 0) ctx.moveTo(x * 2.4, y * 2.4); else ctx.lineTo(x * 2.4, y * 2.4);
    }
    ctx.fill();
    ctx.globalCompositeOperation = 'source-atop';
    const g = ctx.createLinearGradient(0, -40, 0, 50);
    g.addColorStop(0, 'rgba(255,255,255,.65)');
    g.addColorStop(1, 'rgba(255,255,255,0)');
    ctx.fillStyle = g; ctx.fillRect(-60, -60, 120, 120);
  });
}

/* ---------- Inisialisasi Three ---------- */
function initThree() {
  if (!window.THREE) { $('#stage').classList.add('no-webgl'); return false; }
  try {
    WORLD.renderer = new THREE.WebGLRenderer({
      canvas, antialias: true, alpha: false, powerPreference: 'high-performance',
      preserveDrawingBuffer: false,
    });
  } catch (e) {
    console.warn('WebGL tidak tersedia:', e);
    $('#stage').classList.add('no-webgl');
    return false;
  }
  const r = WORLD.renderer;
  r.setPixelRatio(Math.min(window.devicePixelRatio || 1, isMobile ? 1.7 : 2));
  r.setSize(window.innerWidth, window.innerHeight, false);
  r.outputColorSpace = THREE.SRGBColorSpace;
  r.toneMapping = THREE.ACESFilmicToneMapping;
  r.toneMappingExposure = 1.16;

  WORLD.scene = new THREE.Scene();
  WORLD.camera = new THREE.PerspectiveCamera(46, window.innerWidth / window.innerHeight, 0.08, 1600);
  WORLD.camera.position.set(0, 20, 80);
  WORLD.scene.fog = new THREE.FogExp2(0x0c1424, 0.0052);
  WORLD.clock = new THREE.Clock();

  buildSky();
  buildLights();
  buildGround();
  buildMountain();
  buildCaves();
  buildVegetation();
  buildSummit();
  buildTiger();
  buildMarker();
  applyBiome(state.biome, true);
  applyStyle(state.style, true);

  WORLD.scene.add(WORLD.tigerRoot);
  WORLD.scene.add(WORLD.momRoot);
  placeTigerAt(state.cave, true);

  window.addEventListener('resize', onResize);
  bindCameraControls();
  WORLD.ok = true;
  return true;
}

function onResize() {
  if (!WORLD.renderer) return;
  WORLD.renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, isMobile ? 1.7 : 2));
  WORLD.renderer.setSize(window.innerWidth, window.innerHeight, false);
  WORLD.camera.aspect = window.innerWidth / window.innerHeight;
  WORLD.camera.updateProjectionMatrix();
}

/* ---------- Langit ---------- */
function buildSky() {
  const rig = new THREE.Group();
  WORLD.skyRig = rig;
  WORLD.scene.add(rig);

  const uniforms = {
    topColor: { value: new THREE.Color('#040a18') },
    midColor: { value: new THREE.Color('#141335') },
    botColor: { value: new THREE.Color('#3b2360') },
    sunDir: { value: new THREE.Vector3(0.3, 0.35, -1).normalize() },
    sunColor: { value: new THREE.Color('#c7d2fe') },
    glow: { value: 0.35 },
  };
  WORLD.skyUniforms = uniforms;
  const mat = new THREE.ShaderMaterial({
    uniforms,
    side: THREE.BackSide,
    depthWrite: false,
    fog: false,
    toneMapped: false,
    vertexShader: `
      varying vec3 vDir;
      void main(){
        vDir = normalize(position);
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }`,
    fragmentShader: `
      uniform vec3 topColor, midColor, botColor, sunColor;
      uniform vec3 sunDir;
      uniform float glow;
      varying vec3 vDir;
      void main(){
        vec3 d = normalize(vDir);
        float h = d.y;
        vec3 col = mix(botColor, midColor, smoothstep(-0.10, 0.22, h));
        col = mix(col, topColor, smoothstep(0.14, 0.72, h));
        float s = max(dot(d, normalize(sunDir)), 0.0);
        col += sunColor * pow(s, 320.0) * 2.2;
        col += sunColor * pow(s, 24.0) * 0.22 * glow;
        col += sunColor * pow(s, 5.0) * 0.05 * glow;
        gl_FragColor = vec4(col, 1.0);
      }`,
  });
  const sky = new THREE.Mesh(new THREE.SphereGeometry(900, 32, 20), mat);
  sky.renderOrder = -10;
  rig.add(sky);
  WORLD.sky = sky;

  // Bintang
  const N = 1500;
  const pos = new Float32Array(N * 3);
  const sizes = new Float32Array(N);
  for (let i = 0; i < N; i++) {
    const u = Math.random() * Math.PI * 2;
    const v = Math.acos(clamp(Math.random() * 1.15 - 0.12, -1, 1));
    const rad = 820;
    pos[i * 3] = Math.sin(v) * Math.cos(u) * rad;
    pos[i * 3 + 1] = Math.cos(v) * rad;
    pos[i * 3 + 2] = Math.sin(v) * Math.sin(u) * rad;
    sizes[i] = Math.random() * 2.4 + 0.6;
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  g.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
  const starMat = new THREE.PointsMaterial({
    size: 3.8, map: new THREE.CanvasTexture(starCanvas()), transparent: true, opacity: 0.95,
    depthWrite: false, blending: THREE.AdditiveBlending, sizeAttenuation: false,
    color: 0xdfe9ff, fog: false, toneMapped: false,
  });
  starMat.map.colorSpace = THREE.SRGBColorSpace;
  WORLD.stars = new THREE.Points(g, starMat);
  WORLD.stars.renderOrder = -9;
  rig.add(WORLD.stars);

  // Bulan
  const moonGroup = new THREE.Group();
  const moonMat = new THREE.MeshBasicMaterial({ color: 0xfff4d2, fog: false, toneMapped: false });
  const moon = new THREE.Mesh(new THREE.SphereGeometry(26, 28, 20), moonMat);
  moonGroup.add(moon);
  const glowMat = new THREE.SpriteMaterial({
    map: new THREE.CanvasTexture(radialCanvas('rgba(255,248,220,.95)', 'rgba(255,240,190,.28)', 0.3)),
    transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, depthTest: false,
    opacity: 0.9, fog: false, toneMapped: false,
  });
  glowMat.map.colorSpace = THREE.SRGBColorSpace;
  const glow = new THREE.Sprite(glowMat);
  glow.scale.set(210, 210, 1);
  moonGroup.add(glow);
  moonGroup.position.set(-300, 430, -620);
  WORLD.moon = moonGroup;
  WORLD.moonGlow = glow;
  rig.add(moonGroup);

  // Aurora
  const auroraGroup = new THREE.Group();
  const auroraMat = new THREE.ShaderMaterial({
    transparent: true, depthWrite: false, side: THREE.DoubleSide, blending: THREE.AdditiveBlending,
    uniforms: {
      uTime: { value: 0 },
      c1: { value: new THREE.Color('#22d3ee') },
      c2: { value: new THREE.Color('#a855f7') },
      uOpacity: { value: 0.42 },
    },
    vertexShader: `
      varying vec2 vUv;
      void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }`,
    fragmentShader: `
      uniform float uTime; uniform vec3 c1, c2; uniform float uOpacity;
      varying vec2 vUv;
      void main(){
        vec2 uv = vUv;
        float wave = sin(uv.x * 9.0 + uTime * 0.35) * 0.5 + 0.5;
        float wave2 = sin(uv.x * 4.0 - uTime * 0.22 + 1.7) * 0.5 + 0.5;
        float band = pow(wave * 0.55 + wave2 * 0.45, 2.4);
        float vertical = smoothstep(0.0, 0.45, uv.y) * smoothstep(1.0, 0.55, uv.y);
        float alpha = band * vertical * uOpacity * (0.55 + 0.45 * sin(uTime * 0.5 + uv.x * 5.0));
        vec3 col = mix(c2, c1, clamp(uv.y * 1.2 + wave * 0.3, 0.0, 1.0));
        gl_FragColor = vec4(col, alpha);
      }`,
  });
  for (let k = 0; k < 3; k++) {
    const geo = new THREE.PlaneGeometry(760, 260, 48, 1);
    const m = new THREE.Mesh(geo, auroraMat.clone());
    m.material.uniforms.uTime = auroraMat.uniforms.uTime;
    m.position.set(0, 300 + k * 40, -620 + k * 40);
    m.rotation.z = (k - 1) * 0.06;
    m.material.uniforms.c1.value = new THREE.Color(k === 1 ? '#67e8f9' : '#22d3ee');
    m.material.uniforms.c2.value = new THREE.Color(k === 2 ? '#ec4899' : '#a855f7');
    m.renderOrder = -8;
    auroraGroup.add(m);
  }
  WORLD.aurora = auroraGroup;
  rig.add(auroraGroup);

  // Awan
  const cloudGroup = new THREE.Group();
  const cloudMat = new THREE.MeshStandardMaterial({
    color: 0xffffff, roughness: 1, metalness: 0, transparent: true, opacity: 0.52,
    depthWrite: false, flatShading: true, fog: false,
  });
  WORLD.cloudMat = cloudMat;
  const cloudGeo = new THREE.IcosahedronGeometry(1, 1);
  for (let k = 0; k < 9; k++) {
    const cg = new THREE.Group();
    const parts = 4 + Math.floor(Math.random() * 4);
    for (let p = 0; p < parts; p++) {
      const m = new THREE.Mesh(cloudGeo, cloudMat);
      m.position.set((Math.random() - 0.5) * 60, (Math.random() - 0.5) * 10, (Math.random() - 0.5) * 26);
      m.scale.set(18 + Math.random() * 24, 7 + Math.random() * 6, 12 + Math.random() * 14);
      cg.add(m);
    }
    const ang = (k / 9) * Math.PI * 2;
    cg.position.set(Math.sin(ang) * 420, 250 + Math.random() * 80, Math.cos(ang) * 420);
    cg.rotation.y = ang;
    cloudGroup.add(cg);
  }
  WORLD.clouds = cloudGroup;
  rig.add(cloudGroup);

  // Pelangi
  const rainbowGroup = new THREE.Group();
  const cols = [0xef4444, 0xf97316, 0xeab308, 0x22c55e, 0x3b82f6, 0x8b5cf6];
  cols.forEach((col, k) => {
    const geo = new THREE.TorusGeometry(260 - k * 7, 4.2, 6, 80, Math.PI);
    const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({
      color: col, transparent: true, opacity: 0.42, depthWrite: false, fog: false, toneMapped: false,
    }));
    m.position.set(0, 30, -560);
    rainbowGroup.add(m);
  });
  WORLD.rainbow = rainbowGroup;
  rig.add(rainbowGroup);
}

/* ---------- Cahaya ---------- */
function buildLights() {
  const hemi = new THREE.HemisphereLight(0x9db4ff, 0x16232e, 0.75);
  WORLD.hemi = hemi;
  WORLD.scene.add(hemi);

  const amb = new THREE.AmbientLight(0xd7e4ff, 0.38);
  WORLD.amb = amb;
  WORLD.scene.add(amb);

  const dir = new THREE.DirectionalLight(0xf2f6ff, 1.25);
  dir.position.set(80, 140, 70);
  WORLD.dir = dir;
  WORLD.dir.target.position.set(0, 30, 0);
  WORLD.scene.add(WORLD.dir.target);
  WORLD.scene.add(dir);

  const rim = new THREE.DirectionalLight(0x7dd3fc, 0.55);
  rim.position.set(-90, 60, -80);
  WORLD.rim = rim;
  WORLD.scene.add(rim);

  const point = new THREE.PointLight(0xffd9a0, 26, 18, 1.6);
  point.position.set(0, 8, 60);
  WORLD.pointLight = point;
  WORLD.scene.add(point);

  const hero = new THREE.PointLight(0xffe8c8, 11, 11, 2);
  WORLD.heroLight = hero;
  WORLD.scene.add(hero);
}

/* ---------- Tanah & danau ---------- */
function buildGround() {
  const g = new THREE.Group();
  const disk = new THREE.Mesh(
    new THREE.CircleGeometry(520, 64),
    new THREE.MeshStandardMaterial({ color: 0x16261f, roughness: 1, metalness: 0 })
  );
  disk.rotation.x = -Math.PI / 2;
  disk.position.y = -0.35;
  g.add(disk);

  const water = new THREE.Mesh(
    new THREE.RingGeometry(60.5, 520, 96, 1),
    new THREE.MeshStandardMaterial({
      color: 0x14344a, roughness: 0.18, metalness: 0.35, transparent: true, opacity: 0.72,
      emissive: 0x0a2030, emissiveIntensity: 0.35,
    })
  );
  water.rotation.x = -Math.PI / 2;
  water.position.y = 0.06;
  WORLD.water = water;
  g.add(water);

  // Siluet perbukitan jauh
  const hillMat = new THREE.MeshStandardMaterial({ color: 0x122c2a, roughness: 1, flatShading: true, emissive: 0x0a1a1c, emissiveIntensity: 0.7 });
  WORLD.hillMat = hillMat;
  let seed = 7;
  const rnd = () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
  for (let i = 0; i < 18; i++) {
    const ang = (i / 18) * Math.PI * 2 + rnd() * 0.2;
    const rad = 130 + rnd() * 210;
    const h = 14 + rnd() * 44;
    const rr = 24 + rnd() * 48;
    const hill = new THREE.Mesh(new THREE.ConeGeometry(rr, h, 7, 1), hillMat);
    hill.position.set(Math.sin(ang) * rad, h / 2 - 1.5, Math.cos(ang) * rad);
    hill.rotation.y = rnd() * 3;
    g.add(hill);
  }
  WORLD.terrainBase = g;
  WORLD.scene.add(g);
}

/* ---------- Bukit berundak ---------- */
function disturbWall(geo, radius, level, isFloor) {
  const pos = geo.attributes.position;
  for (let i = 0; i < pos.count; i++) {
    const x = pos.getX(i), y = pos.getY(i), z = pos.getZ(i);
    const a = Math.atan2(x, z);
    const rr = Math.hypot(x, z);
    if (rr < 0.01) continue;
    const wob = 1
      + Math.sin(a * 3 + level * 1.3) * 0.008
      + Math.sin(a * 7 - level * 0.7) * 0.005
      + Math.sin(a * 13 + level * 2.1) * 0.003;
    const along = isFloor ? 1 : 1 + Math.sin(y * 1.7 + a * 2.2) * 0.002;
    const nr = rr * wob * along;
    pos.setXYZ(i, x / rr * nr, y, z / rr * nr);
  }
  pos.needsUpdate = true;
  geo.computeVertexNormals();
}

function buildMountain() {
  const group = new THREE.Group();
  WORLD.terrain = group;
  WORLD.scene.add(group);

  const rockTex = texFromCanvas(noiseCanvas(0xcfc7b8, 30, 220), 4, 1);
  const grassTex = texFromCanvas(noiseCanvas(0xdfe4d0, 20, 140), 9, 9);
  WORLD.rockTex = rockTex;
  WORLD.grassTex = grassTex;

  WORLD.levelCliffMats = [];
  WORLD.levelGrassMats = [];
  WORLD.levelRims = [];

  for (let b = 0; b < LEVELS; b++) {
    const f = b / (LEVELS - 1);
    const y = floorY(b);
    const ro = outerR(b);
    const ri = innerR(b);

    const cliffMat = new THREE.MeshStandardMaterial({
      color: new THREE.Color(0x3a4f63).lerp(new THREE.Color(0x6a7d92), f * 0.5),
      map: rockTex, roughness: 0.95, metalness: 0.02, flatShading: true,
      emissive: 0x1b2a3a, emissiveIntensity: 0.55,
    });
    const grassMat = new THREE.MeshStandardMaterial({
      color: new THREE.Color(0x2a615b).lerp(new THREE.Color(0x4e8a74), f * 0.55),
      map: grassTex, roughness: 0.9, metalness: 0.02,
      emissive: 0x0e2a26, emissiveIntensity: 0.5,
    });
    const rimMat = new THREE.MeshBasicMaterial({
      color: 0x2dd4bf, transparent: true, opacity: 0.38 + f * 0.18, depthWrite: false,
      blending: THREE.AdditiveBlending, toneMapped: false,
    });
    WORLD.levelCliffMats.push(cliffMat);
    WORLD.levelGrassMats.push(grassMat);
    WORLD.levelRims.push(rimMat);

    const wallGeo = new THREE.CylinderGeometry(ro, ro + 0.52, DY + 0.12, 112, 1, true);
    disturbWall(wallGeo, ro, b);
    const wall = new THREE.Mesh(wallGeo, cliffMat);
    wall.position.y = y - DY / 2;
    group.add(wall);

    const floorGeo = new THREE.RingGeometry(ri, ro + 0.02, 96, 1);
    disturbWall(floorGeo, ro, b, true);
    const floor = new THREE.Mesh(floorGeo, grassMat);
    floor.rotation.x = -Math.PI / 2;
    floor.position.y = y;
    group.add(floor);

    const rim = new THREE.Mesh(new THREE.TorusGeometry(ro - 0.02, 0.035, 4, 96), rimMat);
    rim.rotation.x = Math.PI / 2;
    rim.position.y = y + 0.012;
    rim.scale.setScalar(1.004);
    group.add(rim);

    // bongkahan batu agar dinding tidak tampak mulus
    if (b % 1 === 0) {
      for (let k = 0; k < 8; k++) {
        const ang = k * 0.78 + b * 0.37;
        const chunk = new THREE.Mesh(new THREE.IcosahedronGeometry(0.55, 0), cliffMat);
        const sc = 0.6 + ((b * 5 + k * 7) % 6) * 0.26;
        chunk.position.set(
          Math.sin(ang) * (ro - 0.5),
          y - 1.15 - ((k % 3) * 0.5),
          Math.cos(ang) * (ro - 0.5)
        );
        chunk.scale.set(sc, sc * (0.8 + (k % 2) * 0.5), sc);
        chunk.rotation.set(k * 0.7, ang * 2, b * 0.3);
        group.add(chunk);
      }
    }
  }

  // Dinding & puncak
  const sy = summitY();
  const sr = innerR(LEVELS - 1);
  const topMat = new THREE.MeshStandardMaterial({
    color: new THREE.Color(0x6a7d92), map: rockTex, roughness: 0.95, metalness: 0.02, flatShading: true,
    emissive: 0x1b2a3a, emissiveIntensity: 0.55,
  });
  const topWallGeo = new THREE.CylinderGeometry(sr, sr + 0.52, DY + 0.12, 112, 1, true);
  disturbWall(topWallGeo, sr, LEVELS);
  const topWall = new THREE.Mesh(topWallGeo, topMat);
  topWall.position.y = sy - DY / 2;
  group.add(topWall);
  WORLD.topMat = topMat;

  const topDisk = new THREE.Mesh(new THREE.CircleGeometry(sr, 96), WORLD.levelGrassMats[LEVELS - 1]);
  topDisk.rotation.x = -Math.PI / 2;
  topDisk.position.y = sy;
  group.add(topDisk);

  const topRim = new THREE.Mesh(new THREE.TorusGeometry(sr - 0.03, 0.06, 4, 112),
    new THREE.MeshBasicMaterial({ color: 0xfbbf24, transparent: true, opacity: 0.35, depthWrite: false,
      blending: THREE.AdditiveBlending, toneMapped: false }));
  topRim.rotation.x = Math.PI / 2;
  topRim.position.y = sy + 0.02;
  group.add(topRim);
  WORLD.topRim = topRim;

}

/* ---------- Goa ---------- */
function archShape(rw, legH) {
  const s = new THREE.Shape();
  s.moveTo(-rw, 0);
  s.lineTo(-rw, legH);
  s.absarc(0, legH, rw, Math.PI, 0, true);
  s.lineTo(rw, 0);
  s.lineTo(-rw, 0);
  return s;
}
function archFrameShape(rw, legH, t) {
  const s = new THREE.Shape();
  s.moveTo(-rw, 0);
  s.lineTo(-rw, legH);
  s.absarc(0, legH, rw, Math.PI, 0, true);
  s.lineTo(rw, 0);
  s.lineTo(rw - t, 0);
  s.lineTo(rw - t, legH);
  s.absarc(0, legH, rw - t, 0, Math.PI, false);
  s.lineTo(-rw + t, 0);
  s.closePath();
  return s;
}
function roughGeometry(geo, amp) {
  const pos = geo.attributes.position;
  const map = new Map();
  const key = (x, y, z) => (x.toFixed(3) + '|' + y.toFixed(3) + '|' + z.toFixed(3));
  for (let i = 0; i < pos.count; i++) {
    const x = pos.getX(i), y = pos.getY(i), z = pos.getZ(i);
    const k = key(x, y, z);
    let off = map.get(k);
    if (!off) {
      let h = 0;
      for (let c = 0; c < k.length; c++) h = (h * 31 + k.charCodeAt(c)) % 100000;
      const rnd = (n) => { const v = Math.sin(h * 12.9898 + n * 78.233) * 43758.5453; return (v - Math.floor(v)) * 2 - 1; };
      off = [rnd(1) * amp, rnd(2) * amp, rnd(3) * amp];
      map.set(k, off);
    }
    pos.setXYZ(i, x + off[0], y + off[1], z + off[2]);
  }
  pos.needsUpdate = true;
  geo.computeVertexNormals();
  return geo;
}

function buildCaves() {
  const group = new THREE.Group();
  WORLD.caveGroup = group;
  WORLD.scene.add(group);

  const N = N_CAVES;
  const portalGeo = new THREE.ShapeGeometry(archShape(1.5, 1.6), 26);
  const frameGeo = roughGeometry(new THREE.ExtrudeGeometry(archFrameShape(1.92, 1.78, 0.42),
    { depth: 0.32, bevelEnabled: false, curveSegments: 22 }).translate(0, 0, -0.12), 0.06);

  const portalMat = new THREE.MeshBasicMaterial({ color: 0x03060c, fog: false, toneMapped: false });
  const frameMat = new THREE.MeshStandardMaterial({ color: 0x8a8378, roughness: 1.0, metalness: 0.0, flatShading: true,
    emissive: 0x3c352c, emissiveIntensity: 0.6 });
  const crystalMat = new THREE.MeshStandardMaterial({
    color: 0xffffff, emissive: 0xffffff, emissiveIntensity: 0.75, roughness: 0.18, metalness: 0.15, flatShading: true,
  });
  const glowTex = new THREE.CanvasTexture(radialCanvas('rgba(255,255,255,.75)', 'rgba(255,255,255,.18)', 0.4));
  glowTex.colorSpace = THREE.SRGBColorSpace;
  const glowMat = new THREE.MeshBasicMaterial({
    map: glowTex, transparent: true, opacity: 0.34, blending: THREE.AdditiveBlending,
    depthWrite: false, toneMapped: false, fog: false,
  });
  const starMat = new THREE.MeshStandardMaterial({
    color: 0xffffff, emissive: 0xfbbf24, emissiveIntensity: 0.18, roughness: 0.3, metalness: 0.35,
    flatShading: true,
  });

  const portal = new THREE.InstancedMesh(portalGeo, portalMat, N);
  // rongga gelap: bola dengan sisi belakang (BackSide) -> terlihat seperti goa
  const cavityMat = new THREE.MeshBasicMaterial({ color: 0x05070b, side: THREE.BackSide, fog: false, toneMapped: false });
  const cavity = new THREE.InstancedMesh(new THREE.SphereGeometry(1.7, 22, 16), cavityMat, N);
  cavity.frustumCulled = false;
  cavity.renderOrder = 1;
  group.add(cavity);
  // bongkahan batu pembentuk bukit karang di sekeliling mulut goa
  const boulderMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 1.0, metalness: 0.0, flatShading: true });
  const boulders = new THREE.InstancedMesh(new THREE.IcosahedronGeometry(1, 1), boulderMat, N * 5);
  boulders.frustumCulled = false;
  group.add(boulders);
  WORLD.caveBoulderMat = boulderMat;
  // pendaran hangat di dalam mulut goa
  const innerGlow = new THREE.InstancedMesh(
    new THREE.PlaneGeometry(1.5, 1.45),
    new THREE.MeshBasicMaterial({
      map: new THREE.CanvasTexture(radialCanvas('rgba(255,206,132,.95)', 'rgba(255,158,64,.18)', 0.32)),
      transparent: true, opacity: 0.5, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false, fog: false,
    }),
    N
  );
  innerGlow.frustumCulled = false;
  innerGlow.renderOrder = 4;
  group.add(innerGlow);
  WORLD.caveInnerGlow = innerGlow;
  const caveTuftMat = new THREE.MeshStandardMaterial({ color: 0x2a6b58, roughness: 0.95, flatShading: true });
  const caveTuft = new THREE.InstancedMesh(new THREE.ConeGeometry(0.12, 0.42, 4), caveTuftMat, N * 8);
  caveTuft.frustumCulled = false;
  group.add(caveTuft);
  WORLD.caveTuftMat = caveTuftMat;
  const frame = new THREE.InstancedMesh(frameGeo, frameMat, N);
  const glow = new THREE.InstancedMesh(new THREE.PlaneGeometry(4.8, 4.2), glowMat, N);
  const crystal = new THREE.InstancedMesh(new THREE.ConeGeometry(0.17, 0.72, 5), crystalMat, N * 2);
  const stars = new THREE.InstancedMesh(new THREE.OctahedronGeometry(0.17, 0), starMat, N * 3);
  [portal, frame, glow, crystal, stars].forEach(m => {
    m.frustumCulled = false;
    group.add(m);
  });
  portal.renderOrder = 2;
  cavity.renderOrder = 1;
  glow.renderOrder = 3;

  const dummy = new THREE.Object3D();
  const col = new THREE.Color();
  for (let i = 0; i < N; i++) {
    const p = cavePose(i);
    dummy.position.set(p.base.x + p.outward.x * 0.02, p.base.y, p.base.z + p.outward.z * 0.02);
    dummy.rotation.set(0, p.th, 0);
    dummy.scale.set(1, 1, 1);
    dummy.updateMatrix();
    portal.setMatrixAt(i, dummy.matrix);
    frame.setMatrixAt(i, dummy.matrix);

    dummy.position.set(p.base.x + p.outward.x * 0.34, p.base.y + 0.72, p.base.z + p.outward.z * 0.34);
    dummy.rotation.set(0, p.th, 0);
    dummy.scale.set(1, 1, 1);
    dummy.updateMatrix();
    innerGlow.setMatrixAt(i, dummy.matrix);

    // rongga: bola gelap di belakang mulut goa (tertanam di dinding bukit)
    dummy.position.set(p.base.x - p.outward.x * 0.42, p.base.y + 1.02, p.base.z - p.outward.z * 0.42);
    dummy.rotation.set(0, p.th, 0);
    dummy.scale.set(1.12, 1.08, 0.62);
    dummy.updateMatrix();
    cavity.setMatrixAt(i, dummy.matrix);

    // empat bongkahan batu: kiri, kanan, atas-kiri, atas-kanan
    const bpos = [
      [-2.05, 0.36, 0.5, 0.18],
      [2.06, 0.36, 0.5, -0.18],
      [-1.52, 2.36, 0.38, 0.3],
      [1.54, 2.42, 0.4, -0.25],
      [-0.06, 3.02, 0.3, 0.1],
    ];
    bpos.slice(0, 5).forEach((bp, k) => {
      dummy.position.set(
        p.base.x + p.tangent.x * bp[0] + p.outward.x * 0.02,
        p.base.y + bp[1],
        p.base.z + p.tangent.z * bp[0] + p.outward.z * 0.02
      );
      dummy.rotation.set(bp[3], p.th + k * 0.7, bp[0] * 0.12);
      dummy.scale.set(bp[2] * 0.95, bp[2] * 0.82, bp[2] * 0.9);
      dummy.updateMatrix();
      boulders.setMatrixAt(i * 5 + k, dummy.matrix);
    });

    dummy.position.set(p.base.x + p.outward.x * 0.3, p.base.y + 1.62, p.base.z + p.outward.z * 0.3);
    dummy.scale.set(1.12, 1.12, 1);
    dummy.updateMatrix();
    glow.setMatrixAt(i, dummy.matrix);

    for (let k = 0; k < 8; k++) {
      const side = k % 2 ? 1 : -1;
      const tang = side * (1.55 + ((k * 7 + i) % 5) * 0.34);
      const rad = p.r + 0.34 + ((k * 3 + i) % 4) * 0.29;
      dummy.position.set(
        Math.sin(p.th) * rad + p.tangent.x * tang,
        p.base.y + 0.18,
        Math.cos(p.th) * rad + p.tangent.z * tang
      );
      dummy.rotation.set(0, p.th + k, 0);
      dummy.scale.set(1 + (k % 3) * 0.25, 1 + (k % 2) * 0.35, 1 + (k % 3) * 0.25);
      dummy.updateMatrix();
      caveTuft.setMatrixAt(i * 8 + k, dummy.matrix);
    }
    for (let k = 0; k < 2; k++) {
      const side = k === 0 ? -1 : 1;
      dummy.position.set(
        p.base.x + p.tangent.x * side * 2.12 + p.outward.x * 0.24,
        p.base.y + 0.38,
        p.base.z + p.tangent.z * side * 2.12 + p.outward.z * 0.24
      );
      dummy.rotation.set(0, p.th + side * 0.18, side * 0.16);
      dummy.scale.setScalar(1 + (i % 3) * 0.08);
      dummy.updateMatrix();
      crystal.setMatrixAt(i * 2 + k, dummy.matrix);
    }

    for (let k = 0; k < 3; k++) {
      dummy.position.set(
        p.base.x + p.tangent.x * (k - 1) * 0.52 + p.outward.x * 0.2,
        p.base.y + 3.28 + (k === 1 ? 0.16 : 0),
        p.base.z + p.tangent.z * (k - 1) * 0.52 + p.outward.z * 0.2
      );
      dummy.rotation.set(0, p.th, 0);
      dummy.scale.setScalar(0.92);
      dummy.updateMatrix();
      stars.setMatrixAt(i * 3 + k, dummy.matrix);
      stars.setColorAt(i * 3 + k, col.set(0x334155));
    }
  }
  portal.instanceMatrix.needsUpdate = true;
  frame.instanceMatrix.needsUpdate = true;
  cavity.instanceMatrix.needsUpdate = true;
  innerGlow.instanceMatrix.needsUpdate = true;
  boulders.instanceMatrix.needsUpdate = true;
  caveTuft.instanceMatrix.needsUpdate = true;
  glow.instanceMatrix.needsUpdate = true;
  crystal.instanceMatrix.needsUpdate = true;
  stars.instanceMatrix.needsUpdate = true;
  if (stars.instanceColor) stars.instanceColor.needsUpdate = true;

  WORLD.cavePortal = portal;
  WORLD.caveCavity = cavity;
  WORLD.caveBoulders = boulders;
  WORLD.caveFrame = frame;
  WORLD.caveGlow = glow;
  WORLD.caveCrystal = crystal;
  WORLD.caveStars = stars;
  refreshCaveColors();
}

function refreshCaveColors() {
  if (!WORLD.caveFrame) return;
  const b = WORLD.biome || BIOMES[state.biome];
  const frameBase = new THREE.Color(b.caveRock);
  const frameCurrent = new THREE.Color('#d8cdb6');
  const cGold = new THREE.Color('#fbbf24');
  const cDim = new THREE.Color('#2b3646');
  const glowPassed = new THREE.Color(b.glow || '#22d3ee');
  const glowCurrent = new THREE.Color('#fbbf24');
  const glowFuture = new THREE.Color('#334155');
  const crystalBase = new THREE.Color(b.crystal || '#a78bfa');
  const crystalCurrent = new THREE.Color('#fde68a');
  const c = new THREE.Color();
  for (let i = 0; i < N_CAVES; i++) {
    const current = i === state.frontier && !isPassed(i);
    const passed = isPassed(i);
    const future = i > state.frontier;

    WORLD.caveFrame.setColorAt(i, current ? c.copy(frameBase).lerp(frameCurrent, 0.3) : c.copy(frameBase).multiplyScalar(future ? 0.6 : 1));
    WORLD.caveGlow.setColorAt(i, current ? glowCurrent : passed ? glowPassed : glowFuture);
    for (let k = 0; k < 2; k++) {
      WORLD.caveCrystal.setColorAt(i * 2 + k, current ? crystalCurrent : future ? c.copy(crystalBase).multiplyScalar(0.55) : crystalBase);
    }
    const st = state.stars[i] || 0;
    for (let k = 0; k < 3; k++) {
      WORLD.caveStars.setColorAt(i * 3 + k, k < st ? cGold : cDim);
    }
  }
  if (WORLD.caveFrame.instanceColor) WORLD.caveFrame.instanceColor.needsUpdate = true;
  if (WORLD.caveGlow.instanceColor) WORLD.caveGlow.instanceColor.needsUpdate = true;
  if (WORLD.caveCrystal.instanceColor) WORLD.caveCrystal.instanceColor.needsUpdate = true;
  if (WORLD.caveStars.instanceColor) WORLD.caveStars.instanceColor.needsUpdate = true;
}

/* ---------- Tanaman & batu ---------- */
function buildVegetation() {
  const group = new THREE.Group();
  WORLD.decor = group;
  WORLD.scene.add(group);

  const N_TREE_T = 30 * 7 + 70;
  const trunkMat = new THREE.MeshStandardMaterial({ color: 0x4a3728, roughness: 1, flatShading: true });
  const leafMat = new THREE.MeshStandardMaterial({ color: 0x0f5b52, roughness: 0.9, flatShading: true, emissive: 0x082b26, emissiveIntensity: 0.6 });
  const trunk = new THREE.InstancedMesh(new THREE.CylinderGeometry(0.13, 0.2, 1.2, 6), trunkMat, N_TREE_T);
  const leaf1 = new THREE.InstancedMesh(new THREE.ConeGeometry(0.95, 1.9, 7), leafMat, N_TREE_T);
  const leaf2 = new THREE.InstancedMesh(new THREE.ConeGeometry(0.68, 1.5, 7), leafMat, N_TREE_T);
  [trunk, leaf1, leaf2].forEach(m => { m.frustumCulled = false; group.add(m); });
  WORLD.treeTrunk = trunk; WORLD.treeLeaf1 = leaf1; WORLD.treeLeaf2 = leaf2;
  WORLD.trunkMat = trunkMat; WORLD.leafMat = leafMat;

  const d = new THREE.Object3D();
  let n = 0;
  for (let b = 0; b < LEVELS; b++) {
    const y = floorY(b);
    const r = outerR(b) - 0.38;
    for (let k = 0; k < 7; k++) {
      const ang = b * 0.7 + k * 0.92 + 0.5;
      const scale = 0.32 + ((b * 7 + k * 3) % 5) * 0.045;
      const x = Math.sin(ang) * r, z = Math.cos(ang) * r;
      d.position.set(x, y + 0.6 * scale, z);
      d.rotation.set(0, ang + k, 0);
      d.scale.set(scale, scale, scale);
      d.updateMatrix();
      trunk.setMatrixAt(n, d.matrix);
      d.position.y = y + 1.45 * scale;
      d.updateMatrix(); leaf1.setMatrixAt(n, d.matrix);
      d.position.y = y + 2.2 * scale;
      d.scale.set(scale * 0.9, scale * 0.9, scale * 0.9);
      d.updateMatrix(); leaf2.setMatrixAt(n, d.matrix);
      n++;
    }
  }
  // pohon di tanah sekitar bukit
  let seed = 91;
  const rnd = () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
  for (let k = 0; k < 70; k++) {
    const ang = rnd() * Math.PI * 2;
    const rad = 68 + rnd() * 100;
    const scale = 0.9 + rnd() * 1.4;
    const x = Math.sin(ang) * rad, z = Math.cos(ang) * rad;
    d.position.set(x, 0.6 * scale, z);
    d.rotation.set(0, ang, 0);
    d.scale.set(scale, scale, scale);
    d.updateMatrix(); trunk.setMatrixAt(n, d.matrix);
    d.position.y = 1.45 * scale; d.updateMatrix(); leaf1.setMatrixAt(n, d.matrix);
    d.position.y = 2.2 * scale;
    d.scale.set(scale * 0.9, scale * 0.9, scale * 0.9);
    d.updateMatrix(); leaf2.setMatrixAt(n, d.matrix);
    n++;
  }
  [trunk, leaf1, leaf2].forEach(m => { m.instanceMatrix.needsUpdate = true; m.count = n; });

  // semak / rumput di tepi teras
  const tuftMat = new THREE.MeshStandardMaterial({ color: 0x2a6b58, roughness: 0.95, flatShading: true });
  const tuft = new THREE.InstancedMesh(new THREE.ConeGeometry(0.13, 0.42, 4), tuftMat, LEVELS * 22);
  tuft.frustumCulled = false;
  group.add(tuft);
  WORLD.tuft = tuft; WORLD.tuftMat = tuftMat;
  let m = 0;
  for (let b = 0; b < LEVELS; b++) {
    for (let k = 0; k < 22; k++) {
      const ang = k * 0.285 + b * 0.41;
      const rad = outerR(b) - 0.16;
      d.position.set(Math.sin(ang) * rad, floorY(b) + 0.2, Math.cos(ang) * rad);
      d.rotation.set(0, ang, 0);
      d.scale.setScalar(0.7 + ((b + k) % 3) * 0.2);
      d.updateMatrix(); tuft.setMatrixAt(m++, d.matrix);
    }
  }
  tuft.count = m; tuft.instanceMatrix.needsUpdate = true;

  // batu
  const rockMat = new THREE.MeshStandardMaterial({ color: 0x415266, roughness: 0.98, flatShading: true, emissive: 0x18202c, emissiveIntensity: 0.8 });
  const rocks = new THREE.InstancedMesh(new THREE.IcosahedronGeometry(0.55, 0), rockMat, LEVELS * 12 + 30);
  rocks.frustumCulled = false;
  group.add(rocks);
  WORLD.rocks = rocks; WORLD.rockMat = rockMat;
  let rn = 0;
  for (let b = 0; b < LEVELS; b++) {
    for (let k = 0; k < 12; k++) {
      const ang = (b * 1.7 + k * 2.1) % (Math.PI * 2);
      const rad = outerR(b) + ((k % 2) ? 0.1 : -0.7);
      const yy = floorY(b) - 0.5 + (k % 3) * 0.6;
      const s = 0.3 + ((b * 3 + k) % 5) * 0.18;
      d.position.set(Math.sin(ang) * rad, yy, Math.cos(ang) * rad);
      d.rotation.set(k, ang, b);
      d.scale.set(s, s * 0.75, s);
      d.updateMatrix(); rocks.setMatrixAt(rn++, d.matrix);
    }
  }
  rocks.count = rn; rocks.instanceMatrix.needsUpdate = true;

  // kunang-kunang
  const fireN = 260;
  const fp = new Float32Array(fireN * 3);
  for (let i = 0; i < fireN; i++) {
    const ang = Math.random() * Math.PI * 2;
    const rr = 12 + Math.random() * 65;
    fp[i * 3] = Math.sin(ang) * rr;
    fp[i * 3 + 1] = 2 + Math.random() * 70;
    fp[i * 3 + 2] = Math.cos(ang) * rr;
  }
  const fg = new THREE.BufferGeometry();
  fg.setAttribute('position', new THREE.BufferAttribute(fp, 3));
  const fMat = new THREE.PointsMaterial({
    size: 0.38, map: new THREE.CanvasTexture(starCanvas()), color: 0xfff1a8, transparent: true,
    opacity: 0.9, depthWrite: false, blending: THREE.AdditiveBlending, sizeAttenuation: true,
    fog: true, toneMapped: false,
  });
  fMat.map.colorSpace = THREE.SRGBColorSpace;
  WORLD.fireflies = new THREE.Points(fg, fMat);
  group.add(WORLD.fireflies);
}

/* ---------- Puncak & induk ---------- */
function buildSummit() {
  const g = new THREE.Group();
  g.position.y = summitY();
  WORLD.summit = g;
  WORLD.scene.add(g);

  // gerbang cahaya
  const archMat = new THREE.MeshBasicMaterial({
    color: 0xfbbf24, transparent: true, opacity: 0.32, blending: THREE.AdditiveBlending,
    depthWrite: false, toneMapped: false,
  });
  for (let k = 0; k < 3; k++) {
    const torus = new THREE.Mesh(new THREE.TorusGeometry(3.2 + k * 0.34, 0.09, 6, 64, Math.PI), archMat);
    torus.position.set(0, 0.2, 0.5);
    g.add(torus);
  }
  // pilar cahaya
  const beamMat = new THREE.MeshBasicMaterial({
    color: 0xfde68a, transparent: true, opacity: 0.055, side: THREE.DoubleSide, depthWrite: false,
    blending: THREE.AdditiveBlending, toneMapped: false, fog: false,
  });
  const beam = new THREE.Mesh(new THREE.CylinderGeometry(2.1, 4.6, 26, 24, 1, true), beamMat);
  beam.position.y = 12.5;
  g.add(beam);
  WORLD.beam = beam;

  const glowMat = new THREE.SpriteMaterial({
    map: new THREE.CanvasTexture(radialCanvas('rgba(255,220,130,.9)', 'rgba(255,190,80,.16)', 0.35)),
    transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, opacity: 0.85,
    toneMapped: false, fog: false,
  });
  glowMat.map.colorSpace = THREE.SRGBColorSpace;
  const glow = new THREE.Sprite(glowMat);
  glow.scale.set(18, 18, 1);
  glow.position.y = 2.2;
  g.add(glow);

  // hati (disembunyikan sampai akhir)
  const heartMat = new THREE.SpriteMaterial({
    map: new THREE.CanvasTexture(heartCanvas()), transparent: true, depthWrite: false,
    toneMapped: false, opacity: 0.95,
  });
  heartMat.map.colorSpace = THREE.SRGBColorSpace;
  WORLD.hearts = [];
  for (let i = 0; i < 14; i++) {
    const s = new THREE.Sprite(heartMat.clone());
    s.scale.set(1.5, 1.5, 1);
    s.position.set((Math.random() - 0.5) * 6, 1 + Math.random() * 5, (Math.random() - 0.5) * 4);
    s.userData = { v: 0.4 + Math.random() * 0.7, ph: Math.random() * 6 };
    s.visible = false;
    g.add(s);
    WORLD.hearts.push(s);
  }
  WORLD.momRoot = new THREE.Group();
  WORLD.momRoot.position.set(0, 0.02, 1.2);
  WORLD.momRoot.rotation.y = 0;
  WORLD.scene.add(WORLD.momRoot);
}

/* ---------- Macan ---------- */
function stripeTexture(cfg) {
  return texFromCanvas(makeCanvas(512, (ctx, S) => {
    ctx.fillStyle = cfg.fur; ctx.fillRect(0, 0, S, S);
    // gradasi: punggung lebih gelap, perut lebih terang
    const g = ctx.createLinearGradient(0, 0, 0, S);
    g.addColorStop(0, 'rgba(255,255,255,.14)');
    g.addColorStop(0.42, 'rgba(255,255,255,0)');
    g.addColorStop(0.72, 'rgba(0,0,0,.16)');
    g.addColorStop(1, 'rgba(0,0,0,.30)');
    ctx.fillStyle = g; ctx.fillRect(0, 0, S, S);
    // belang vertikal (meridian pada bola) dengan tepi bergelombang
    ctx.fillStyle = cfg.stripe;
    const n = 13;
    for (let i = 0; i < n; i++) {
      const cx = (i + 0.5) * (S / n);
      const w = 7 + (i % 3) * 3;
      const top = S * (0.02 + (i % 2) * 0.03);
      const bot = S * (0.82 + (i % 4) * 0.03);
      ctx.beginPath();
      ctx.moveTo(cx - w / 2, top);
      for (let y = top; y <= bot; y += 12) {
        ctx.lineTo(cx - w / 2 + Math.sin(y * 0.035 + i) * 5, y);
      }
      for (let y = bot; y >= top; y -= 12) {
        ctx.lineTo(cx + w / 2 + Math.sin(y * 0.035 + i) * 5, y);
      }
      ctx.closePath();
      ctx.fill();
    }
    // bintik halus bulu
    for (let i = 0; i < 2200; i++) {
      ctx.fillStyle = 'rgba(0,0,0,' + (0.02 + Math.random() * 0.05) + ')';
      ctx.fillRect(Math.random() * S, Math.random() * S, 1.6, 3.2);
    }
  }), 1, 1);
}

function headTexture(cfg) {
  return texFromCanvas(makeCanvas(512, (ctx, S) => {
    ctx.fillStyle = cfg.fur; ctx.fillRect(0, 0, S, S);
    const g = ctx.createLinearGradient(0, 0, 0, S);
    g.addColorStop(0, 'rgba(255,255,255,.10)');
    g.addColorStop(0.5, 'rgba(0,0,0,0)');
    g.addColorStop(1, 'rgba(0,0,0,.14)');
    ctx.fillStyle = g; ctx.fillRect(0, 0, S, S);
    ctx.fillStyle = cfg.stripe;
    // belang mahkota: garis pendek memancar dari atas
    const n = 9;
    for (let i = 0; i < n; i++) {
      const x = (i + 0.5) * (S / n);
      const len = S * (0.30 + (i % 3) * 0.055);
      const w = 13 + (i % 2) * 4;
      ctx.beginPath();
      ctx.moveTo(x - w, 0);
      ctx.quadraticCurveTo(x + 4, len * 0.62, x - 1, len);
      ctx.quadraticCurveTo(x + 9, len * 0.5, x + w, 0);
      ctx.closePath();
      ctx.fill();
    }
    // garis tengah dahi
    ctx.beginPath();
    ctx.moveTo(S / 2 - 5, 0);
    ctx.quadraticCurveTo(S / 2 + 2, S * 0.26, S / 2 - 2, S * 0.34);
    ctx.quadraticCurveTo(S / 2 + 6, S * 0.24, S / 2 + 5, 0);
    ctx.closePath(); ctx.fill();
    // belang pelipis
    for (let side = 0; side < 2; side++) {
      for (let k = 0; k < 3; k++) {
        const x = side ? S * (0.80 + k * 0.05) : S * (0.05 + k * 0.05);
        ctx.save();
        ctx.translate(x, S * (0.34 + k * 0.07));
        ctx.rotate((side ? -1 : 1) * 0.5);
        ctx.beginPath();
        ctx.ellipse(0, 0, 7, 26, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      }
    }
    for (let i = 0; i < 1600; i++) {
      ctx.fillStyle = 'rgba(0,0,0,' + (0.02 + Math.random() * 0.045) + ')';
      ctx.fillRect(Math.random() * S, Math.random() * S, 1.5, 3);
    }
  }), 1, 1);
}

function buildTigerModel(cfg, mom) {
  const root = new THREE.Group();
  const parts = {};
  const furTex = stripeTexture(cfg);
  const matFur = new THREE.MeshStandardMaterial({ map: furTex, color: 0xffffff, roughness: 0.72, metalness: 0.0 });
  const matPlain = new THREE.MeshStandardMaterial({ color: cfg.fur, roughness: 0.74 });
  const matHead = new THREE.MeshStandardMaterial({ map: headTexture(cfg), color: 0xffffff, roughness: 0.72 });
  const matBelly = new THREE.MeshStandardMaterial({ color: cfg.belly, roughness: 0.86 });
  const matDark = new THREE.MeshStandardMaterial({ color: cfg.stripe, roughness: 0.7 });
  const matPink = new THREE.MeshStandardMaterial({ color: cfg.nose, roughness: 0.45 });
  const matInner = new THREE.MeshStandardMaterial({ color: cfg.inner, roughness: 0.78 });
  const matEye = new THREE.MeshStandardMaterial({
    color: cfg.eye, roughness: 0.18, metalness: 0.05, emissive: cfg.eye, emissiveIntensity: 0.30,
  });
  const matWhite = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.32 });
  const matGold = new THREE.MeshStandardMaterial({ color: 0xfbbf24, roughness: 0.26, metalness: 0.62 });
  const shared = { matFur, matPlain, matHead, matBelly, matDark, matPink, matInner, matEye, matWhite, matGold };

  const add = (geo, mat, x, y, z, sx, sy, sz, parent) => {
    const m = new THREE.Mesh(geo, mat);
    m.position.set(x, y, z);
    if (sx != null) m.scale.set(sx, sy, sz);
    (parent || root).add(m);
    return m;
  };

  /* ---------- badan ---------- */
  const body = new THREE.Group();
  body.position.y = 0.74 * cfg.body;
  root.add(body);
  parts.body = body;
  add(new THREE.SphereGeometry(0.5, 28, 22), matFur, 0, 0, 0, 0.94, 1.04, 0.88, body);
  add(new THREE.SphereGeometry(0.4, 24, 18), matBelly, 0, -0.04, 0.24, 0.86, 0.92, 0.72, body);
  // bulu dada
  add(new THREE.SphereGeometry(0.26, 18, 14), matBelly, 0, 0.26, 0.28, 1.0, 0.86, 0.6, body);

  /* ---------- kepala ---------- */
  const head = new THREE.Group();
  head.position.set(0, 1.42 + (cfg.head - 1) * 0.16, 0.03);
  head.scale.setScalar(cfg.head);
  root.add(head);
  parts.head = head;
  add(new THREE.SphereGeometry(0.54, 40, 30), matHead, 0, 0, 0, 1.12, 0.98, 0.98, head);

  // kuping
  [-1, 1].forEach(side => {
    const ear = new THREE.Group();
    ear.position.set(side * 0.4, 0.4, -0.02);
    ear.rotation.z = -side * 0.26;
    add(new THREE.SphereGeometry(0.205, 18, 14), matPlain, 0, 0, 0, 1, 1.02, 0.45, ear);
    add(new THREE.SphereGeometry(0.132, 14, 12), matInner, 0, -0.012, 0.045, 1, 1, 0.32, ear);
    head.add(ear);
    parts[side < 0 ? 'earL' : 'earR'] = ear;
  });

  // pipi berbulu (ciri harimau)
  [-1, 1].forEach(side => {
    add(new THREE.SphereGeometry(0.23, 18, 14), matBelly, side * 0.36, -0.10, 0.26, 0.95, 0.78, 0.72, head)
      .rotation.z = side * 0.3;
    add(new THREE.SphereGeometry(0.185, 16, 12), matBelly, side * 0.42, -0.06, 0.19, 1.12, 0.55, 0.5, head)
      .rotation.z = side * 0.5;
    const blushMat = new THREE.MeshBasicMaterial({ color: cfg.cheek, transparent: true, opacity: 0.5 });
    add(new THREE.SphereGeometry(0.085, 12, 10), blushMat, side * 0.35, -0.045, 0.455, 1.35, 0.6, 0.3, head);
  });

  // mata besar
  [-1, 1].forEach(side => {
    const eye = new THREE.Group();
    eye.position.set(side * 0.2, 0.075, 0.43);
    add(new THREE.SphereGeometry(0.122, 20, 18), matWhite, 0, 0, 0, 1, 1.1, 0.6, eye);
    add(new THREE.SphereGeometry(0.108, 20, 18), matEye, 0, 0, 0.042, 1, 1.06, 0.5, eye);
    add(new THREE.SphereGeometry(0.07, 14, 12), matDark, 0, 0.004, 0.082, 1, 1.06, 0.5, eye);
    add(new THREE.SphereGeometry(0.029, 10, 10), matWhite, -side * 0.03, 0.04, 0.108, 1, 1, 1, eye);
    add(new THREE.SphereGeometry(0.014, 8, 8), matWhite, side * 0.038, -0.032, 0.108, 1, 1, 1, eye);
    // kelopak atas
    add(new THREE.SphereGeometry(0.139, 18, 8, 0, Math.PI * 2, 0, Math.PI * 0.30), matPlain,
      0, 0.02, 0.004, 1, 1.02, 0.6, eye).rotation.x = 0.16;
    head.add(eye);
    parts[side < 0 ? 'eyeL' : 'eyeR'] = eye;
  });

  // moncong + hidung + mulut
  add(new THREE.SphereGeometry(0.155, 20, 16), matBelly, -0.085, -0.115, 0.415, 1.15, 0.88, 0.72, head);
  add(new THREE.SphereGeometry(0.155, 20, 16), matBelly, 0.085, -0.115, 0.415, 1.15, 0.88, 0.72, head);
  add(new THREE.SphereGeometry(0.072, 16, 12), matPink, 0, -0.035, 0.535, 1.35, 0.95, 0.85, head);
  const mouth = add(new THREE.TorusGeometry(0.062, 0.012, 6, 14, Math.PI), matDark, 0, -0.145, 0.53, 1, 1, 1, head);
  mouth.rotation.z = Math.PI; mouth.rotation.x = -0.08;
  add(new THREE.SphereGeometry(0.022, 8, 8), matPink, 0, -0.175, 0.512, 1.5, 0.75, 0.6, head);

  // kumis halus
  [-1, 1].forEach(side => {
    for (let k = 0; k < 2; k++) {
      const w = add(new THREE.CylinderGeometry(0.0038, 0.0038, 0.26, 3), matWhite,
        side * (0.15 + k * 0.012), -0.09 - k * 0.05, 0.5, 1, 1, 1, head);
      w.rotation.z = side * (Math.PI / 2 - 0.2 + k * 0.22);
      w.rotation.y = -side * 0.28;
    }
  });

  // syal
  if (cfg.scarf) {
    const scarfMat = new THREE.MeshStandardMaterial({ color: cfg.scarf, roughness: 0.55 });
    add(new THREE.TorusGeometry(0.36, 0.075, 10, 26), scarfMat, 0, 1.1, 0.01, 1, 1, 1, root).rotation.x = Math.PI / 2;
    add(new THREE.SphereGeometry(0.085, 10, 8), scarfMat, 0, 1.06, 0.34, 1, 1, 1, root);
    const st1 = add(new THREE.BoxGeometry(0.11, 0.36, 0.04), scarfMat, -0.06, 0.87, 0.36, 1, 1, 1, root);
    st1.rotation.z = 0.2; st1.rotation.x = -0.12;
    const st2 = add(new THREE.BoxGeometry(0.1, 0.29, 0.04), scarfMat, 0.075, 0.9, 0.36, 1, 1, 1, root);
    st2.rotation.z = -0.16;
  }

  // rompi + ransel
  if (cfg.vest) {
    const vestMat = new THREE.MeshStandardMaterial({ color: cfg.vest, roughness: 0.55, side: THREE.DoubleSide });
    const vest = new THREE.Mesh(new THREE.CylinderGeometry(0.47, 0.51, 0.55, 22, 1, true, 0.5, Math.PI * 2 - 1.0), vestMat);
    vest.position.y = 0.8; vest.rotation.y = Math.PI;
    root.add(vest);
    const packMat = new THREE.MeshStandardMaterial({ color: cfg.pack || '#b45309', roughness: 0.55 });
    add(new THREE.BoxGeometry(0.42, 0.38, 0.24), packMat, 0, 0.82, -0.46, 1, 1, 1, root);
    add(new THREE.BoxGeometry(0.24, 0.12, 0.06), packMat, 0, 0.9, -0.59, 1, 1, 1, root);
    add(new THREE.BoxGeometry(0.05, 0.4, 0.05), matDark, -0.26, 0.95, 0.3, 1, 1, 1, root).rotation.z = -0.4;
    add(new THREE.BoxGeometry(0.05, 0.4, 0.05), matDark, 0.26, 0.95, 0.3, 1, 1, 1, root).rotation.z = 0.4;
  }

  // peci emas
  if (cfg.hat) {
    const hatMat = new THREE.MeshStandardMaterial({ color: cfg.hat, roughness: 0.4, metalness: 0.2 });
    add(new THREE.CylinderGeometry(0.235, 0.275, 0.21, 20), hatMat, 0, 0.57, 0.01, 1, 1, 1, head);
    add(new THREE.TorusGeometry(0.275, 0.03, 8, 26), matGold, 0, 0.47, 0.01, 1, 1, 1, head).rotation.x = Math.PI / 2;
    add(new THREE.OctahedronGeometry(0.06, 0), matGold, 0, 0.56, 0.26, 1, 1.25, 0.6, head);
  }

  // mahkota induk
  if (mom) {
    add(new THREE.CylinderGeometry(0.27, 0.22, 0.14, 12), matGold, 0, 0.57, 0, 1, 1, 1, head);
    for (let k = 0; k < 5; k++) {
      const a = (k / 5) * Math.PI * 2;
      add(new THREE.ConeGeometry(0.05, 0.17, 4), matGold, Math.sin(a) * 0.22, 0.69, Math.cos(a) * 0.22, 1, 1, 1, head);
    }
  }

  // lengan
  [-1, 1].forEach(side => {
    const arm = new THREE.Group();
    arm.position.set(side * 0.44, 0.95, 0.06);
    const mesh = new THREE.Mesh(new THREE.CapsuleGeometry(0.12, 0.26, 6, 12), matFur);
    mesh.position.y = -0.21;
    arm.add(mesh);
    const paw = new THREE.Mesh(new THREE.SphereGeometry(0.135, 14, 12), matPlain);
    paw.position.set(0, -0.4, 0.02); paw.scale.set(1, 0.78, 1.05);
    arm.add(paw);
    const beans = new THREE.Mesh(new THREE.SphereGeometry(0.055, 8, 6), matInner);
    beans.position.set(side * 0.015, -0.43, 0.1); beans.scale.set(1.2, 0.3, 0.9);
    arm.add(beans);
    arm.userData.baseZ = side * 0.22;
    arm.rotation.z = arm.userData.baseZ;
    root.add(arm);
    parts[side < 0 ? 'armL' : 'armR'] = arm;
  });

  // kaki
  [-1, 1].forEach(side => {
    const leg = new THREE.Group();
    leg.position.set(side * 0.235, 0.44, 0.02);
    const mesh = new THREE.Mesh(new THREE.CapsuleGeometry(0.145, 0.24, 6, 12), matFur);
    mesh.position.y = -0.16;
    leg.add(mesh);
    const paw = new THREE.Mesh(new THREE.SphereGeometry(0.16, 14, 12), matPlain);
    paw.position.set(0, -0.33, 0.035); paw.scale.set(1, 0.62, 1.2);
    leg.add(paw);
    const pad = new THREE.Mesh(new THREE.SphereGeometry(0.07, 8, 6), matInner);
    pad.position.set(side * 0.018, -0.36, 0.14); pad.scale.set(1.2, 0.3, 0.9);
    leg.add(pad);
    root.add(leg);
    parts[side < 0 ? 'legL' : 'legR'] = leg;
  });

  // ekor
  const tail = new THREE.Group();
  tail.position.set(0, 0.62, -0.42);
  for (let i = 0; i < 6; i++) {
    const r = 0.078 - i * 0.008;
    const m = add(new THREE.SphereGeometry(r, 10, 8), i % 2 ? matDark : matFur,
      0, 0.1 + i * 0.105, -0.05 - i * 0.07, 1, 1, 1, tail);
    m.rotation.x = -0.5;
  }
  add(new THREE.SphereGeometry(0.05, 8, 8), matDark, 0, 0.68, -0.45, 1, 1.3, 1, tail);
  root.add(tail);
  parts.tail = tail;

  // bintang melayang
  const stars = new THREE.Group();
  stars.position.set(0, 2.35, 0);
  for (let i = -1; i <= 1; i++) {
    const s = new THREE.Mesh(new THREE.OctahedronGeometry(0.15, 0), matGold);
    s.position.set(i * 0.42, i === 0 ? 0.16 : 0, 0);
    stars.add(s);
  }
  stars.visible = false;
  root.add(stars);
  parts.stars = stars;

  if (mom) root.scale.setScalar(1.22);
  root.userData.parts = parts;
  root.userData.mats = shared;
  return root;
}

function buildTiger() {
  WORLD.tigerRoot = new THREE.Group();
  WORLD.tigerRoot.position.copy(cavePose(state.cave).stand);
  WORLD.scene.add(WORLD.tigerRoot);

  const shadowTex = new THREE.CanvasTexture(radialCanvas('rgba(0,0,0,.55)', 'rgba(0,0,0,.12)', 0.5));
  const shadow = new THREE.Mesh(
    new THREE.PlaneGeometry(2.0, 2.0),
    new THREE.MeshBasicMaterial({ map: shadowTex, transparent: true, opacity: 0.65, depthWrite: false })
  );
  shadow.rotation.x = -Math.PI / 2;
  shadow.position.y = 0.03;
  WORLD.tigerShadow = shadow;
  WORLD.tigerRoot.add(shadow);

  WORLD.tigerHolder = new THREE.Group();
  WORLD.tigerRoot.add(WORLD.tigerHolder);
  WORLD.momHolder = new THREE.Group();
  WORLD.momRoot.add(WORLD.momHolder);

  WORLD.tiger = buildTigerModel(SKINS[state.style], false);
  WORLD.tiger.scale.setScalar(0.74);
  WORLD.tigerHolder.add(WORLD.tiger);

  WORLD.mom = buildTigerModel(SKINS[state.style], true);
  WORLD.mom.scale.setScalar(0.95);
  WORLD.mom.rotation.y = Math.PI * 0.92;
  WORLD.momHolder.add(WORLD.mom);
  WORLD.momRoot.position.y = summitY() + 0.02;
  WORLD.momRoot.position.z = 1.4;

  // bintang di atas induk
  const halo = new THREE.Mesh(
    new THREE.TorusGeometry(1.7, 0.03, 4, 48),
    new THREE.MeshBasicMaterial({ color: 0xfbbf24, transparent: true, opacity: 0.28, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false })
  );
  halo.rotation.x = Math.PI / 2;
  halo.position.y = 2.9;
  WORLD.momHolder.add(halo);
  WORLD.momHalo = halo;
}

function clearTiger(root) {
  const walk = obj => {
    if (obj.geometry) obj.geometry.dispose();
    if (obj.material) {
      (Array.isArray(obj.material) ? obj.material : [obj.material]).forEach(m => {
        if (m.map && m.map.isTexture) m.map.dispose();
        m.dispose();
      });
    }
    obj.children.slice().forEach(walk);
  };
  walk(root);
  root.clear();
}

function rebuildTigerModels() {
  if (!WORLD.ok) return;
  clearTiger(WORLD.tigerHolder);
  clearTiger(WORLD.momHolder);
  WORLD.tiger = buildTigerModel(SKINS[state.style], false);
  WORLD.tiger.scale.setScalar(0.74);
  WORLD.tigerHolder.add(WORLD.tiger);
  WORLD.mom = buildTigerModel(SKINS[state.style], true);
  WORLD.mom.scale.setScalar(0.95);
  WORLD.mom.rotation.y = Math.PI * 0.92;
  WORLD.momHolder.add(WORLD.mom);
}

/* ---------- Penanda goa aktif ---------- */
function buildMarker() {
  const g = new THREE.Group();
  const gold = new THREE.MeshStandardMaterial({
    color: 0xfbbf24, emissive: 0xf59e0b, emissiveIntensity: 0.6, roughness: 0.28, metalness: 0.45,
  });
  const gem = new THREE.Mesh(new THREE.OctahedronGeometry(0.22, 0), gold);
  gem.name = 'gem';
  g.add(gem);
  const ring = new THREE.Mesh(
    new THREE.TorusGeometry(0.42, 0.035, 6, 28),
    new THREE.MeshBasicMaterial({ color: 0xfde68a, transparent: true, opacity: 0.8, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false })
  );
  ring.rotation.x = Math.PI / 2;
  g.add(ring);
  WORLD.marker = g;
  WORLD.scene.add(g);
  updateMarker();
}
function updateMarker() {
  if (!WORLD.marker) return;
  const p = cavePose(state.cave);
  WORLD.marker.position.set(
    p.base.x + p.outward.x * 0.5,
    p.base.y + 3.42,
    p.base.z + p.outward.z * 0.5
  );
}

/* ---------- Biome ---------- */
function applyBiome(key, initial) {
  const b = BIOMES[key] || BIOMES.starlight;
  WORLD.biome = b;
  const scene = WORLD.scene;
  scene.fog.color.set(b.fog);
  scene.fog.density = b.fogDensity;

  const u = WORLD.skyUniforms;
  if (u) {
    u.topColor.value.set(b.skyTop);
    u.midColor.value.set(b.skyMid);
    u.botColor.value.set(b.skyBot);
    u.sunColor.value.set(b.light);
  }
  if (WORLD.stars) WORLD.stars.material.opacity = b.stars;
  if (WORLD.moon) WORLD.moon.visible = !!b.moon;
  if (WORLD.aurora) WORLD.aurora.visible = !!b.aurora;
  if (WORLD.clouds) WORLD.clouds.visible = !!b.clouds;
  if (WORLD.rainbow) WORLD.rainbow.visible = !!b.rainbow;
  if (WORLD.fireflies) WORLD.fireflies.visible = !!b.fireflies;
  if (WORLD.beam) WORLD.beam.material.color.set(b.moon ? '#fde68a' : '#fff7d6');
  if (WORLD.cloudMat) WORLD.cloudMat.opacity = 0.5 * (b.clouds || 0);
  if (WORLD.hemi) {
    WORLD.hemi.color.set(b.hemiSky);
    WORLD.hemi.groundColor.set(b.hemiGround);
    WORLD.hemi.intensity = b.amb * 0.9;
  }
  if (WORLD.amb) {
    WORLD.amb.color.set(b.light);
    WORLD.amb.intensity = 0.14 + b.amb * 0.30;
  }
  if (WORLD.dir) {
    WORLD.dir.color.set(b.light);
    WORLD.dir.intensity = b.sun;
    if (WORLD.rim) WORLD.rim.intensity = b.sun * 0.34;
  }
  if (WORLD.water) {
    WORLD.water.material.color.set(b.moon ? '#122b40' : b.key === 'sunset' ? '#5a3a4a' : '#2a5a5e');
    WORLD.water.material.emissive.set(b.moon ? '#123a4a' : b.glow);
    WORLD.water.material.emissiveIntensity = b.moon ? 0.22 : 0.1;
  }
  if (WORLD.hillMat) { WORLD.hillMat.color.set(b.cliff2).multiplyScalar(0.5); WORLD.hillMat.emissive.set(b.cliff2).multiplyScalar(0.12); }
  if (WORLD.terrainBase && WORLD.terrainBase.children[0]) {
    WORLD.terrainBase.children[0].material.color.set(b.key === 'starlight' ? '#111b22' : b.cliff2);
  }
  const cBase = new THREE.Color(b.cliff);
  const cTop = new THREE.Color(b.cliff2);
  const gBase = new THREE.Color(b.grass);
  const gTop = new THREE.Color(b.grass2);
  const rimCol = new THREE.Color(b.glow);
  if (WORLD.levelCliffMats) {
    WORLD.levelCliffMats.forEach((m, i) => {
      const f = i / Math.max(1, LEVELS - 1);
      m.color.copy(cBase).lerp(cTop, 0.25 + f * 0.55);
      m.emissive.copy(m.color).multiplyScalar(b.emissive != null ? b.emissive : 0.2);
      m.emissiveIntensity = 1;
    });
  }
  if (WORLD.levelGrassMats) {
    WORLD.levelGrassMats.forEach((m, i) => {
      const f = i / Math.max(1, LEVELS - 1);
      m.color.copy(gBase).lerp(gTop, 0.2 + f * 0.6);
      m.emissive.copy(m.color).multiplyScalar((b.emissive != null ? b.emissive : 0.2) * 0.9);
      m.emissiveIntensity = 1;
    });
  }
  if (WORLD.topMat) { WORLD.topMat.color.copy(cTop); WORLD.topMat.emissive.copy(cTop).multiplyScalar(b.emissive != null ? b.emissive : 0.2); }
  if (WORLD.levelRims) WORLD.levelRims.forEach(m => m.color.copy(rimCol));
  if (WORLD.topRim) WORLD.topRim.material.color.set(b.moon ? '#fbbf24' : b.glow);
  if (WORLD.rimMat) WORLD.rimMat.color.set(b.glow);
  if (WORLD.rockMat) { WORLD.rockMat.color.set(b.rock); WORLD.rockMat.emissive.set(b.rock).multiplyScalar((b.emissive || 0.2) * 0.4); }
  if (WORLD.trunkMat) WORLD.trunkMat.color.set(b.trunk);
  if (WORLD.leafMat) { WORLD.leafMat.color.set(b.tree); WORLD.leafMat.emissive.set(b.tree).multiplyScalar((b.emissive || 0.2) * 0.45); }
  if (WORLD.tuftMat) WORLD.tuftMat.color.set(b.tree2);
  if (WORLD.caveTuftMat) { WORLD.caveTuftMat.color.set(b.tree2); WORLD.caveTuftMat.emissive.set(b.tree2).multiplyScalar((b.emissive || 0.2) * 0.45); }
  if (WORLD.caveCrystal) {
    WORLD.caveCrystal.material.emissive.set(b.crystal);
    WORLD.caveCrystal.material.emissiveIntensity = 0.85;
  }
  if (WORLD.cavePortal) WORLD.cavePortal.material.color.set(b.portal);
  if (WORLD.caveBoulderMat) WORLD.caveBoulderMat.color.set(b.caveRock).multiplyScalar(1.15);
  if (WORLD.caveStars) WORLD.caveStars.material.emissiveIntensity = b.moon ? 0.7 : 0.4;
  if (WORLD.pointLight) { WORLD.pointLight.color.set(b.moon ? '#ffd9a0' : '#fff0c8'); WORLD.pointLight.intensity = b.moon ? 26 : 20; }
  if (WORLD.tigerShadow) WORLD.tigerShadow.material.opacity = 0.55;
  if (WORLD.heroLight) {
    WORLD.heroLight.color.set(b.moon ? '#ffe6c2' : '#fff4dc');
    WORLD.heroLight.intensity = b.moon ? 11.0 : 7.0;
  }
  refreshCaveColors();
  if (!initial) saveState();
}

/* ---------- Gaya macan ---------- */
function applyStyle(key, initial) {
  const s = SKINS[key] || SKINS.sumatera;
  WORLD.style = s;
  state.style = s.key;
  if (!initial) {
    rebuildTigerModels();
    placeTigerAt(state.cave, true);
    saveState();
  }
}

/* ---------- Penempatan & animasi ---------- */
const TIGER_ANIM = { mode: 'idle', t: 0, blink: 0, nextBlink: 3, wave: 0, jump: 0, scale: 1 };
let travelAnim = null;

function snapCamera() {
  if (!WORLD.ok) return;
  const g = followGoal();
  CAM.pos.copy(g.pos);
  CAM.target.copy(g.target);
}
function placeTigerAt(i, instant) {
  const p = cavePose(i);
  WORLD.tigerRoot.position.set(p.stand.x, p.stand.y + 0.02, p.stand.z);
  WORLD.tigerRoot.rotation.y = p.th;
  WORLD.tigerShadow.position.set(0, 0.03, 0);
  if (WORLD.pointLight) {
    WORLD.pointLight.position.set(
      p.base.x + p.outward.x * 1.8,
      p.base.y + 2.3,
      p.base.z + p.outward.z * 1.8
    );
  }
  updateMarker();
  refreshCaveColors();
  if (instant) {
    WORLD.tigerRoot.visible = true;
    WORLD.tigerHolder.scale.setScalar(1);
    WORLD.tigerHolder.visible = true;
  }
}

function updateTigerAnim(dt, time) {
  const t = WORLD.tiger;
  if (!t) return;
  const parts = t.userData.parts;
  const mode = TIGER_ANIM.mode;
  const speed = mode === 'walk' ? 1.0 : mode === 'climb' ? 1.4 : 0.6;

  // napas
  const br = Math.sin(time * 2.1) * 0.018;
  parts.body.scale.y = 1 + br;
  parts.body.scale.x = 1 - br * 0.4;

  // kedip
  TIGER_ANIM.nextBlink -= dt;
  let blink = 1;
  if (TIGER_ANIM.nextBlink <= 0) {
    TIGER_ANIM.nextBlink = 2.6 + Math.random() * 3.6;
    TIGER_ANIM.blink = 0.13;
  }
  if (TIGER_ANIM.blink > 0) {
    TIGER_ANIM.blink -= dt;
    blink = Math.max(0.08, Math.abs(TIGER_ANIM.blink / 0.13 - 0.5) * 2);
  }
  parts.eyeL.scale.y = blink; parts.eyeR.scale.y = blink;

  // telinga
  const tw = Math.sin(time * 3.2) * 0.06;
  parts.earL.rotation.z = 0.3 + tw;
  parts.earR.rotation.z = -0.3 - tw;

  // ekor
  parts.tail.rotation.z = Math.sin(time * (mode === 'idle' ? 2.2 : 5.5)) * 0.32;
  parts.tail.rotation.x = Math.sin(time * 1.7) * 0.08;

  // kepala
  if (mode === 'sad') {
    parts.head.rotation.x = lerp(parts.head.rotation.x, 0.32, 0.08);
    parts.head.rotation.z = Math.sin(time * 2.4) * 0.1;
  } else if (mode === 'happy') {
    parts.head.rotation.x = -0.16;
    parts.head.rotation.z = Math.sin(time * 7) * 0.08;
  } else {
    parts.head.rotation.x = lerp(parts.head.rotation.x, Math.sin(time * 1.5) * 0.04, 0.08);
    parts.head.rotation.z = lerp(parts.head.rotation.z, Math.sin(time * 1.1) * 0.06, 0.08);
  }

  // lengan
  if (mode === 'happy') {
    parts.armL.rotation.z = 2.35 + Math.sin(time * 10) * 0.2;
    parts.armR.rotation.z = -2.35 - Math.sin(time * 10) * 0.2;
    parts.legL.rotation.x = 0;
    parts.legR.rotation.x = 0;
    TIGER_ANIM.jump = (TIGER_ANIM.jump || 0);
  } else if (mode === 'walk' || mode === 'climb') {
    const amp = mode === 'climb' ? 0.7 : 0.55;
    parts.legL.rotation.x = Math.sin(time * 9 * speed) * amp;
    parts.legR.rotation.x = -Math.sin(time * 9 * speed) * amp;
    parts.armL.rotation.x = -Math.sin(time * 9 * speed) * amp * 0.7;
    parts.armR.rotation.x = Math.sin(time * 9 * speed) * amp * 0.7;
    parts.armL.rotation.z = 0.35 + (mode === 'climb' ? 0.8 : 0);
    parts.armR.rotation.z = -0.35 - (mode === 'climb' ? 0.8 : 0);
  } else if (mode === 'enter') {
    parts.legL.rotation.x = Math.sin(time * 10) * 0.5;
    parts.legR.rotation.x = -Math.sin(time * 10) * 0.5;
    parts.armL.rotation.z = 0.3;
    parts.armR.rotation.z = -0.3;
  } else if (mode === 'wave') {
    parts.armR.rotation.z = -2.2 + Math.sin(time * 8) * 0.35;
    parts.armL.rotation.z = 0.3;
    parts.legL.rotation.x = 0; parts.legR.rotation.x = 0;
  } else {
    // idle dengan lambaian sesekali
    const waveCycle = (time % 9);
    const waving = waveCycle > 6.2 && waveCycle < 8.2;
    parts.armR.rotation.z = waving ? -2.1 + Math.sin(time * 9) * 0.32 : -0.3 - Math.sin(time * 2.2) * 0.05;
    parts.armL.rotation.z = 0.3 + Math.sin(time * 2.2 + 1) * 0.05;
    parts.legL.rotation.x = 0; parts.legR.rotation.x = 0;
    parts.head.rotation.z += waving ? Math.sin(time * 8) * 0.03 : 0;
  }
  if (mode !== 'walk' && mode !== 'climb') {
    parts.armL.rotation.x = lerp(parts.armL.rotation.x, 0, 0.15);
    parts.armR.rotation.x = lerp(parts.armR.rotation.x, 0, 0.15);
  }
  parts.stars.visible = mode === 'happy';
  if (mode === 'happy') {
    parts.stars.rotation.y += dt * 2.4;
    parts.stars.position.y = 2.6 + Math.sin(time * 3) * 0.1;
  }

  // bob
  const bob = (mode === 'walk' || mode === 'climb' || mode === 'enter')
    ? Math.abs(Math.sin(time * 9 * speed)) * 0.09 : Math.sin(time * 2.1) * 0.012;
  WORLD.tigerHolder.position.y = bob;
}

let lastT = 0;
function animateWorld() {
  if (!WORLD.ok) return;
  requestAnimationFrame(animateWorld);
  const dt = Math.min(0.05, WORLD.clock.getDelta());
  const t = WORLD.clock.elapsedTime;

  if (WORLD.dir) {
    const cp = WORLD.camera.position;
    const len = Math.hypot(cp.x, cp.z) || 1;
    WORLD.dir.position.set(cp.x / len * 90 + 20, 120, cp.z / len * 90 + 20);
    WORLD.dir.target.position.set(0, 30, 0);
    WORLD.dir.target.updateMatrixWorld();
  }
  if (WORLD.heroLight) {
    const tp = WORLD.tigerRoot.position;
    const cp = WORLD.camera.position;
    const dx = cp.x - tp.x, dz = cp.z - tp.z;
    const len = Math.hypot(dx, dz) || 1;
    WORLD.heroLight.position.set(tp.x + (dx / len) * 2.2, tp.y + 2.4, tp.z + (dz / len) * 2.2);
  }
  // langit mengikuti kamera
  if (WORLD.skyRig) WORLD.skyRig.position.copy(WORLD.camera.position);
  if (WORLD.aurora) {
    WORLD.aurora.children.forEach((m, i) => {
      m.material.uniforms.uTime.value = t + i * 7;
      m.material.uniforms.uOpacity.value = 0.30 + Math.sin(t * 0.3 + i) * 0.1;
    });
  }
  if (WORLD.fireflies) {
    WORLD.fireflies.rotation.y = t * 0.01;
    const pos = WORLD.fireflies.geometry.attributes.position;
    for (let i = 0; i < pos.count; i += 7) {
      pos.setY(i, pos.getY(i) + Math.sin(t * 0.7 + i) * 0.0025);
    }
    pos.needsUpdate = true;
  }
  if (WORLD.hearts) {
    WORLD.hearts.forEach((h, i) => {
      if (!h.visible) return;
      h.position.y += dt * h.userData.v * 0.5;
      h.position.x += Math.sin(t * 1.3 + i) * dt * 0.08;
      if (h.position.y > 8) h.position.y = 1.2;
      h.material.opacity = 0.55 + Math.sin(t * 2 + i) * 0.35;
    });
  }

  // penanda
  if (WORLD.marker) {
    WORLD.marker.visible = !UI.introOpen && (!isPassed(state.cave) || state.cave === state.frontier);
    WORLD.marker.position.y = cavePose(state.cave).base.y + 3.42 + Math.sin(t * 2.2) * 0.12;
    WORLD.marker.rotation.y = t * 0.9;
  }

  // animasi goa aktif (denyut bintang)
  if (WORLD.caveCrystal) {
    WORLD.caveCrystal.material.emissiveIntensity = 0.78 + Math.sin(t * 2.4) * 0.18;
  }
  if (WORLD.caveGlow) {
    WORLD.caveGlow.material.opacity = 0.30 + Math.sin(t * 2.0) * 0.07;
  }

  // perpindahan
  if (travelAnim) updateTravel(dt, t);
  updateTigerAnim(dt, t);
  if (WORLD.mom) {
    const mp = WORLD.mom.userData.parts;
    mp.tail.rotation.z = Math.sin(t * 1.6) * 0.24;
    mp.head.rotation.y = Math.sin(t * 0.9) * 0.18;
    mp.body.scale.y = 1 + Math.sin(t * 1.7) * 0.015;
    if (WORLD.momHalo) WORLD.momHalo.rotation.z = t * 0.35;
    if (WORLD.finaleMode) {
      const dir = Math.atan2(
        WORLD.camera.position.x - WORLD.momRoot.position.x,
        WORLD.camera.position.z - WORLD.momRoot.position.z
      );
      WORLD.momRoot.rotation.y = lerpAngle(WORLD.momRoot.rotation.y, dir, 0.04);
    }
  }

  updateCamera(dt, t);
  WORLD.renderer.render(WORLD.scene, WORLD.camera);
}

function lerpAngle(a, b, t) {
  let d = ((b - a + Math.PI) % (Math.PI * 2)) - Math.PI;
  if (d < -Math.PI) d += Math.PI * 2;
  return a + d * t;
}

/* ---------- Kamera ---------- */
function aspectZoom() {
  const a = (WORLD.camera && WORLD.camera.aspect) || 1.6;
  return clamp(1.15 / a, 1, 2.0);
}
function followGoal() {
  const p = cavePose(state.cave);
  const yaw = p.th + CAM.yaw;
  const dist = CAM.dist * CAM.zoom * aspectZoom();
  const h = (2.05 + CAM.pitch * 2.5) * (1 + (aspectZoom() - 1) * 0.42);
  const goal = new THREE.Vector3(
    p.stand.x + Math.sin(yaw) * dist,
    p.stand.y + h,
    p.stand.z + Math.cos(yaw) * dist
  );
  const target = new THREE.Vector3(
    p.stand.x - p.outward.x * 0.55,
    p.stand.y + 1.28,
    p.stand.z - p.outward.z * 0.55
  );
  return { pos: goal, target };
}
function introGoal(t) {
  const p = cavePose(state.cave);
  const yaw = p.th + 0.26 + Math.sin(t * 0.09) * 0.16;
  const dist = 10.6 * aspectZoom();
  const pos = new THREE.Vector3(
    p.stand.x + Math.sin(yaw) * dist,
    p.stand.y + 2.95 + (aspectZoom() - 1) * 1.6,
    p.stand.z + Math.cos(yaw) * dist
  );
  const target = new THREE.Vector3(
    p.stand.x - p.outward.x * 0.9,
    p.stand.y + 0.95,
    p.stand.z - p.outward.z * 0.9
  );
  return { pos, target };
}
function overviewGoal() {
  const sumY = summitY();
  return {
    pos: new THREE.Vector3(0, sumY * 0.78, 188),
    target: new THREE.Vector3(0, sumY * 0.5, 0),
  };
}
function applyFrameShift() {
  const cam = WORLD.camera;
  const w = window.innerWidth, h = window.innerHeight;
  let shiftY = 0, shiftX = 0;
  if (UI.introOpen) {
    // teks pembuka di kiri: geser pemandangan agar Cilik tampil di sisi kanan
    if (w >= 1024) shiftX = -Math.round(w * 0.185);
    else shiftY = -Math.round(h * 0.12);
  } else if (!UI.stack.length && CAM.mode !== 'intro') {
    shiftY = Math.round(h * (isMobile ? 0.09 : 0.07));
  }
  if (CAM.override || (CAM.mode !== 'intro' && false)) { shiftX = 0; }
  const enabled = shiftX !== 0 || shiftY !== 0;
  if (cam.view && cam.view.enabled) {
    if (cam.view.offsetX === shiftX && cam.view.offsetY === shiftY) return;
    cam.clearViewOffset();
  } else if (!enabled) return;
  if (!enabled) return;
  cam.setViewOffset(w, h, shiftX, shiftY, w, h);
}
function updateCamera(dt, t) {
  let pos, target;
  if (CAM.override) {
    pos = CAM.override.pos;
    target = CAM.override.target;
  } else if (CAM.mode === 'intro') {
    const g = introGoal(t); pos = g.pos; target = g.target;
  } else if (CAM.mode === 'overview') {
    const g = overviewGoal(); pos = g.pos; target = g.target;
  } else if (CAM.mode === 'finale') {
    pos = CAM.posGoal; target = CAM.targetGoal;
  } else {
    if (travelAnim) {
      const tp = WORLD.tigerRoot.position;
      const th = Math.atan2(tp.x, tp.z);
      const yaw = th + CAM.yaw;
      const dist = CAM.dist * CAM.zoom * aspectZoom();
      const h = (2.05 + CAM.pitch * 2.5) * (1 + (aspectZoom() - 1) * 0.42);
      pos = new THREE.Vector3(tp.x + Math.sin(yaw) * dist, tp.y + h, tp.z + Math.cos(yaw) * dist);
      target = new THREE.Vector3(tp.x - Math.sin(th) * 0.55, tp.y + 1.26, tp.z - Math.cos(th) * 0.55);
    } else {
      const g = followGoal(); pos = g.pos; target = g.target;
    }
  }
  const speed = CAM.override ? 7 : 3.4;
  const k = REDUCED ? 1 : 1 - Math.exp(-Math.min(dt, 0.25) * speed);
  CAM.pos.lerp(pos, k);
  CAM.target.lerp(target, k);
  const shake = CAM.shake > 0 ? CAM.shake : 0;
  if (shake > 0) CAM.shake = Math.max(0, shake - dt * 2.2);
  const sx = shake ? (Math.random() - 0.5) * CAM.shake * 0.25 : 0;
  const sy = shake ? (Math.random() - 0.5) * CAM.shake * 0.25 : 0;
  WORLD.camera.position.set(CAM.pos.x + sx, CAM.pos.y + sy, CAM.pos.z);
  WORLD.camera.lookAt(CAM.target);
  applyFrameShift();
}

/* ---------- Kontrol kamera ---------- */
function bindCameraControls() {
  const pointers = new Map();
  let pinchDist = 0;
  let dragging = false;

  canvas.addEventListener('pointerdown', e => {
    pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (pointers.size === 1) {
      dragging = true;
      canvas.classList.add('dragging');
      canvas.setPointerCapture(e.pointerId);
    } else if (pointers.size === 2) {
      const pts = [...pointers.values()];
      pinchDist = Math.hypot(pts[0].x - pts[1].x, pts[0].y - pts[1].y);
    }
  });
  canvas.addEventListener('pointermove', e => {
    if (!pointers.has(e.pointerId)) return;
    const prev = pointers.get(e.pointerId);
    const cur = { x: e.clientX, y: e.clientY };
    pointers.set(e.pointerId, cur);
    if (pointers.size === 2) {
      const pts = [...pointers.values()];
      const d = Math.hypot(pts[0].x - pts[1].x, pts[0].y - pts[1].y);
      if (pinchDist > 0) {
        CAM.zoom = clamp(CAM.zoom * (pinchDist / Math.max(1, d)), 0.62, 1.7);
      }
      pinchDist = d;
      return;
    }
    if (!dragging) return;
    const dx = cur.x - prev.x, dy = cur.y - prev.y;
    CAM.yaw += dx * 0.006;
    CAM.pitch = clamp(CAM.pitch + dy * 0.004, -0.35, 0.95);
  });
  const end = e => {
    pointers.delete(e.pointerId);
    if (pointers.size < 2) pinchDist = 0;
    if (pointers.size === 0) {
      dragging = false;
      canvas.classList.remove('dragging');
    }
  };
  canvas.addEventListener('pointerup', end);
  canvas.addEventListener('pointercancel', end);
  canvas.addEventListener('wheel', e => {
    e.preventDefault();
    CAM.zoom = clamp(CAM.zoom + e.deltaY * 0.0009, 0.62, 1.7);
  }, { passive: false });
}

/* ---------- Inisialisasi dunia ---------- */
function startWorld() {
  const ok = initThree();
  if (!ok) {
    $('#scene-loader').classList.add('done');
    return false;
  }
  animateWorld();
  return true;
}
