CORE DRILLERS — COMPLETE CONSOLIDATED UPDATE

QUICK START — SOLO
1. Extract the entire ZIP.
2. Open index.html in a current desktop browser with WebGL enabled.
3. Play solo. The game engine and procedural assets are embedded in the HTML.
   No Python, server, or dependency installation is required for solo play.
   Optional web fonts need internet; system fonts are used if unavailable.

CO-OP / LOCAL SERVER
A compatible local/LAN relay server is included as server.py.
Requires Python 3.10+ and the aiohttp dependency.
From the extracted folder, run:
  python -m pip install -r requirements.txt
  python server.py
On macOS/Linux, use python3 instead of python if necessary.
Open http://127.0.0.1:8080 in your browser.
After installing dependencies, START-WINDOWS.bat or start-mac-linux.sh
can be used to start the server. On macOS/Linux: sh start-mac-linux.sh

TRUSTED SAME-WIFI / LAN CO-OP
Run:
  python server.py --host 0.0.0.0
Each player opens http://SERVER-LAN-IP:8080 and uses the same room code.
The host creates a camp; guests join before the host launches.
Allow port 8080 through your firewall only on a trusted private network.
The relay URL fills automatically when the game is opened through this server.
If a previously saved relay URL overrides it, change it under ONLINE SETUP.
An HTML file or room code alone cannot connect remote computers.

PUBLIC INTERNET CO-OP
The included relay is intended for local/trusted-LAN use, not direct public
exposure. It has no account authentication, TLS, persistence, or production
abuse protection. Internet deployment needs a properly configured HTTPS/WSS
host/reverse proxy and appropriate security hardening. Do not expose this
local development server directly to the public internet.
The Python runtime and aiohttp are not bundled; installing requirements
normally needs an internet connection. After installation the local server
can run without internet.

CONTROLS
WASD / Arrow keys: move; mouse drag: look
Space: jump on foot; brake while driving
Left Shift / Right Shift / Left mouse: equipped tool action
  Sword fights, pickaxe mines. Equipped gun fires instead of swinging.
1: sword; 2: pickaxe; 3: gun
Right mouse: fire gun; G: grenade
E: interact, enter/leave cockpit, collect loot, accept nearby dungeon beacon
B: loot sack; U: upgrades; C: camera; Enter: chat; Escape: pause
Touch controls remain available on supported devices.

CURRENT BALANCE
Day: 90 seconds. Night: 40 seconds. Cycle: 130 seconds of active simulation.
Paused/cutscene time does not count like active gameplay time.
HUD shows phase time remaining. Camp sunlight follows the unequal phases.
Caves are underground: the surface sun is visible in camp, not through rock.
Gem prices per ore: emerald 200c, diamond 400c, ruby 550c, rainbow 1000c.
Prices are fixed tiers, not random ranges.
Half of generated ore-vein candidates remain on average, with additional
rarity multipliers for emerald .5, diamond .35, ruby .25 and rainbow .1.
These are weighted-selection multipliers, not absolute spawn percentages.
Arrival-chamber veins are also subject to rarity and thinning.

DUNGEONS
Purple side beacons offer optional wave challenges. Walk near a beacon
and press E to accept. Unaccepted dungeons do not block the route.
Boss walls and the final boss are separate progression encounters.

CHEST TREASURES ADDED
Ancient Ammonite — Common — 35c
Sapphire Geode — Uncommon — 125c
Sunken Idol — Rare — 300c
Void Prism — Epic — 750c
Heart of the Core — Legendary — 2000c
These are physical collectibles that can be stored in the sack and sold.
Existing chest drops remain available.

PERFORMANCE
High-quality shadows, rock bump detail, lighting strips, and polished rig
parts are enabled. Browser/GPU capability limits still apply. If needed,
reduce the graphics quality in Settings. No claim of maximum possible
visual quality or universal frame rate is made.

TEST COVERAGE
Embedded JavaScript syntax checked; browser boot and seeded expedition
initialization tested; prices, phase boundaries, loot models, optional
entrances, collision sweep, and disabled trophies checked.
Local relay host/join and sender tagging checked.
Full playthroughs, long-session performance, public hosting, and full
multiplayer combat/loot/collision synchronization are not exhaustively tested.

FILES
index.html: complete editable game, styles, bundled libraries, and assets
server.py: local/LAN HTTP + WebSocket relay
requirements.txt: server dependency
START-WINDOWS.bat / start-mac-linux.sh: server launch helpers
CHANGELOG.txt: consolidated requested changes
VALIDATION.json: automated smoke-test results
SHA256SUMS.txt: integrity checksums for package contents

THIRD-PARTY CODE
Bundled library license notices are retained inside index.html. This package
is an update to the user-provided game and makes no new ownership claim
over the original game, assets, or bundled libraries.
