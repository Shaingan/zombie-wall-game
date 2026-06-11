# Zombie Wall Game — Project Context

## What this is
A multiplayer browser game built with **Phaser 3 + Matter.js** (client) and **Socket.io + Express** (server).
Players control zombies trying to climb a castle wall and reach a human at the top.

## Repo structure
```
zombie-wall-game/
  client/        Vite + TypeScript + Phaser 3 frontend
  server/        Node.js + Socket.io backend
  .gitignore
```

## Running locally
```bash
# Terminal 1 — server (port 2567)
cd server && npm install && npm run dev

# Terminal 2 — client (port 3000)
cd client && npm install && npm run dev
```

## Deployment
- **GitHub:** https://github.com/Shaingan/zombie-wall-game
- **Server:** deploy to Railway — root dir `server`, build `npm install && npm run build`, start `npm start`
- **Client:** deploy to Vercel — root dir `client`, env var `VITE_SERVER_URL=<railway-url>`
- Client auto-detects: uses `VITE_SERVER_URL` if set, else `localhost:2567` on local, else `window.location.origin`

---

## Client — `client/src/scenes/GameScene.ts`

### Key constants
```typescript
const W = 1280, H = 600, GROUND = 565;
const WALL_X = 1150, WALL_H = 540, CASTLE_W = 100;
const TARGET_Y = GROUND - WALL_H;  // = 25 (top of wall)
const ZW = 26, ZH = 40;            // player physics body size
const CORPSE_W = 52, CORPSE_H = 18;
const LIFESPAN = 5000;             // ms before zombie dies
const SPR_SCALE = 1.5;
```

### Physics setup (Matter.js, gravity y:1.4)
- **Player body:** `friction:0, frictionStatic:0, frictionAir:0.03, inertia:Infinity`
  - Friction is 0 to prevent tangential impulse when sliding against the wall (was causing slow-fall bug)
  - Horizontal movement is fully programmatic (direct velocity set, not physics-driven)
- **Wall body:** `friction:0, frictionStatic:0, isStatic:true` — completely frictionless
- **Dynamic corpse body:** `friction:0, frictionStatic:0, frictionAir:0.02, inertia:Infinity`
  - Settles to static body once speed < 0.3 and age > 800ms
  - Static settled corpse: `friction:1.2, frictionStatic:1.2` — high friction so players can stand on them

### Jumpable surfaces (allow-list)
Only `"ground"` and `"corpse"` labels allow jumping. The wall and bots do not.
This prevents wall-jumping and players jumping off each other.

### Player controls
- A / Left arrow: move left
- D / Right arrow: move right (blocked when `atWall` = touching wall face)
- Space / Up arrow: jump (only when `contacts > 0`)
- Player has 5 seconds before dying; respawns as next generation

### Camera
Lerp-follows player up the wall:
```typescript
const camTargetY = Phaser.Math.Clamp(mySprite.y - H * 0.6, -200, -30);
cameras.main.scrollY = Phaser.Math.Linear(scrollY, camTargetY, 0.06);
```
Background (sky, stars, moon) and all UI use `.setScrollFactor(0)`.

### Corpse lifecycle
1. Player dies → `spawnCorpse()` creates dynamic physics body immediately (so others can land on it mid-fall)
2. Die animation plays on sprite
3. On animation complete → `attachCorpseSprite()` attaches static sprite frame `zombified_13`
4. In `update()` loop: once body speed < 0.3 and age > 800ms → replace dynamic body with static body
5. Corpse sprite faces the direction the zombie was moving when it died (`facing` field)

### Bots (client-side only, 3 bots)
- Tinted red (`0xffaaaa`), staggered starting life timers (100%, 75%, 50%)
- AI: always move right; jump whenever `contacts > 0` and `jumpCooldown <= 0`
- Die and leave corpses just like the player
- Respawn from left side (x = 60 + id*100 + random)
- Do NOT sync to server (local simulation only)

### Sprite sheet (`zombie.png`, 1008×720)
- White background removed at runtime via canvas pixel manipulation (alpha = 0 for pixels > 215,215,215)
- Sprites face LEFT by default — `setFlipX(facing === 1)` to face right
- Animations: `z-idle`, `z-walk`, `z-crawl`, `z-jump`, `z-fall`, `z-die`

### Remote players (other real players via socket)
- Tinted green (`0xbbffdd`)
- Synced via `player_move`, `player_die`, `player_respawn`, `player_leave` socket events
- Die animation plays on their sprite, then corpse sprite is attached

### Win condition
First player/bot to reach `TARGET_Y + 8` while `x >= WALL_X - ZW*3` triggers win.
Player emits `"win"` to server → server broadcasts to all → `showWin()` shows overlay.

---

## Server — `server/src/index.ts`

Socket.io events:
- `connection` → assigns spawn position, emits `init` to new player, broadcasts `player_join`
- `move` → broadcasts `player_move` with x, y
- `die` → stores dead state + facing, broadcasts `player_die` with x, y, facing
- `respawn` → clears dead state, broadcasts `player_respawn`
- `win` → sets global won flag, broadcasts `win` to all
- `disconnect` → removes player, broadcasts `player_leave`

Port: `process.env.PORT || 2567`

---

## Known issues / decisions

| Issue | Fix |
|---|---|
| Player falls slower against wall | Set player body `friction:0` (not just wall). Matter.js combines friction of both bodies. |
| Corpses sticking to wall | `friction:0` on dynamic corpse body + spawn position clamped away from wall (`Math.min(x, WALL_X - CORPSE_W/2 - 2)`) |
| Game pausing when browser tab loses focus | `disableVisibilityChange: true` in Phaser game config |
| Human at castle top invisible | Camera clamp max set to -30 (not 0) so viewport always shows 30px above world top |
| Wall jumping | Jumpable allow-list: only `"ground"` and `"corpse"` labels count |

---

## `client/src/main.ts`
```typescript
new Phaser.Game({
  type: Phaser.AUTO, width: 1280, height: 600,
  backgroundColor: "#111122",
  disableVisibilityChange: true,
  physics: { default: "matter", matter: { gravity: { x: 0, y: 1.4 }, debug: false } },
  scene: [GameScene],
  scale: { mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH },
});
```
