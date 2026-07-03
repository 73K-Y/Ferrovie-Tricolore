# Ferrovie Tricolore

*Working title during development: "Ita Rails" - scripts, folders, and variables inside the project still use this name and will be renamed at release, not before.*

A train simulator built in Roblox Studio, starting from Torino Porta Nuova. The goal isn't arcade-style train driving - it's getting the operational details right: real station positions pulled from OpenStreetMap, track geometry following actual GPX route data, block signaling that follows RFI conventions, and a station clock that's synced to whatever time it actually is in Italy right now.

---

## What's actually running

- **Dynamic train composition.** Carriages aren't baked into a fixed train model - the number of carriages is variable per spawn, built from a template stored in `ServerStorage`.
- **Cab controls that do something.** Front/rear lights, horn (3-phase, server-driven so it's audible to everyone nearby, not just the driver), pantograph toggle, doors, all wired through a `RemoteEvent` so state stays consistent across clients.
- **Stations from real data, not placed by hand.** A Python script (`genera_stazioni_v2.py`) hits the Overpass API for OpenStreetMap railway station data and drops ~3,000 markers into the world at 1:200 scale. Manually placing that many stations wasn't an option.
- **Track built from GPX, not eyeballed.** Real route data run through a Catmull-Rom spline generator produces the physical track. Getting tile placement gap-free took finding the correct `CFrame.fromMatrix` construction - an off-by-basis-vector error was leaving visible seams between tiles.
- **The station clock is the real time in Italy, not a prop.** `os.date("*t", os.time() + 3600)` - synced to the system clock with a DST adjustment. It drives the analog and digital clocks on the departure boards.
- **Departure boards, two of them.** A platform-side sign (`Cartello orari`) and a station-wide board (`Tabella orari`), both reading from one shared `DepartureBoardData` object in `ReplicatedStorage` so they never disagree with each other.
- **A basic red/yellow/green departure signal.** Manual "request departure" flow: yellow for 2 seconds as a warning, then green for a fixed window, then back to red. Not yet the full block-signaling system described below - this is one signal, not a chain.

---

## Two bugs worth writing down, because they were both wrong in ways that looked right

**The delay display showed "+636 minutes."** Early version of the on-time/late calculation compared the real-world clock against a hardcoded scheduled departure of `"08:05"`. That's fine if you start the game at 8:05am. Start it at any other time of day - which is every time, since the game runs on real Italian time - and the "delay" is just however many hours have passed since 8am, dressed up as a train running arbitrarily late. The fix wasn't a math correction, it was realizing the whole comparison had no anchor to reality. Fixed by tying scheduled departures to the same real-clock system the station clock already used, instead of a fake fixed value.

**A flashing departure indicator that never flashed.** Two platform signs, each supposed to alternate a "Depart 1 / Depart 2" light. One flashed, the other stayed permanently lit. Turned out the light-toggling code was correct - the bug was that a hidden `TEMPLATE` object (meant to be an invisible blueprint for cloning, per the existing pattern used elsewhere in the same model) had been left `Visible = true` on the duplicated sign, sitting exactly on top of the real, correctly-blinking light and masking it. Fixed by hiding the leftover templates, not by touching the blink logic, which had been right the whole time. 21 stray visible templates were found across both platform duplicates once this was checked properly instead of assumed.

---

## What isn't done yet, ranked by what breaks the experience first

1. **Train spawn position is off by ~176 studs on the X axis.** `PivotTo` is being applied against a different part than the one the template CFrame was captured from - `FindFirstChildWhichIsA("BasePart", true)` doesn't reliably return the same part twice on a multi-part model. Needs the template's pivot anchored explicitly before it's moved to `ServerStorage`, not resolved lazily at clone time.
2. **The red signal doesn't actually stop anything.** A train can run a red light right now - the signal changes color, nothing enforces it. Freeze-at-red (a forced but non-instant deceleration, not a hard stop, to avoid snapping the coupling) is designed but not built.
3. **Six of seven routes in the menu go nowhere.** Only Torino → Lingotto has real track behind it. The rest are selectable and silently spawn on the wrong track.
4. **Platform 2 has rails but no spawn point.** Same root cause as #1 - will get fixed alongside it, same logic, different platform.
5. **Coupling between carriages is a prototype, not a system.** A buffer-block pair exists on one joint as proof of concept (0.15-stud gap at rest, verified). The old `RopeConstraint`-based coupling is still present elsewhere and needs replacing, not just supplementing.

---

## What's designed but not started

**3-aspect block signaling.** Confirmed against how RFI actually does it (not assumed - checked, because the original assumption that Italian signals skip yellow was wrong): a signal shows green if the next two block sections are clear, yellow if the next section is clear but the one after is occupied, red if the next section is occupied. Double-yellow and flashing-yellow exist in the real system too, but only for edge cases (short platforms, reduced-distance signal spacing) - those come after the base 3-aspect version works, not alongside it.

<p align="center"><<svg width="680" height="220" viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" role="img">
<title>Block signaling a 3 aspetti</title>
<desc>Tre segnali in sequenza: A verde (2 blocchi liberi davanti), B giallo (blocco successivo libero, il seguente occupato), C rosso (il blocco che protegge è occupato dal treno).</desc>
<defs>
<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M2 1L8 5L2 9" fill="none" stroke="#3d3d3a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</marker>
</defs>
<rect width="680" height="220" fill="#ffffff"/>
<text x="30" y="24" font-family="sans-serif" font-size="12" fill="#73726c">senso di marcia</text>
<line x1="130" y1="20" x2="180" y2="20" stroke="#3d3d3a" stroke-width="1" marker-end="url(#arrow)"/>

<rect x="30" y="60" width="70" height="64" rx="8" fill="#EAF3DE" stroke="#639922" stroke-width="1"/>
<text x="65" y="86" font-family="sans-serif" font-size="14" font-weight="600" fill="#173404" text-anchor="middle">A</text>
<text x="65" y="104" font-family="sans-serif" font-size="12" fill="#27500A" text-anchor="middle">verde</text>
<line x1="100" y1="92" x2="118" y2="92" stroke="#3d3d3a" stroke-width="1" marker-end="url(#arrow)"/>

<rect x="118" y="60" width="70" height="64" rx="8" fill="#F1EFE8" stroke="#888780" stroke-width="1"/>
<text x="153" y="86" font-family="sans-serif" font-size="14" font-weight="600" fill="#2C2C2A" text-anchor="middle">B1</text>
<text x="153" y="104" font-family="sans-serif" font-size="12" fill="#444441" text-anchor="middle">libero</text>
<line x1="188" y1="92" x2="202" y2="92" stroke="#3d3d3a" stroke-width="1" marker-end="url(#arrow)"/>

<rect x="202" y="60" width="70" height="64" rx="8" fill="#FAEEDA" stroke="#BA7517" stroke-width="1"/>
<text x="237" y="86" font-family="sans-serif" font-size="14" font-weight="600" fill="#412402" text-anchor="middle">B</text>
<text x="237" y="104" font-family="sans-serif" font-size="12" fill="#633806" text-anchor="middle">giallo</text>
<line x1="272" y1="92" x2="286" y2="92" stroke="#3d3d3a" stroke-width="1" marker-end="url(#arrow)"/>

<rect x="286" y="60" width="70" height="64" rx="8" fill="#F1EFE8" stroke="#888780" stroke-width="1"/>
<text x="321" y="86" font-family="sans-serif" font-size="14" font-weight="600" fill="#2C2C2A" text-anchor="middle">B2</text>
<text x="321" y="104" font-family="sans-serif" font-size="12" fill="#444441" text-anchor="middle">libero</text>
<line x1="356" y1="92" x2="370" y2="92" stroke="#3d3d3a" stroke-width="1" marker-end="url(#arrow)"/>

<rect x="370" y="60" width="70" height="64" rx="8" fill="#FCEBEB" stroke="#A32D2D" stroke-width="1"/>
<text x="405" y="86" font-family="sans-serif" font-size="14" font-weight="600" fill="#501313" text-anchor="middle">C</text>
<text x="405" y="104" font-family="sans-serif" font-size="12" fill="#791F1F" text-anchor="middle">rosso</text>
<line x1="440" y1="92" x2="454" y2="92" stroke="#3d3d3a" stroke-width="1" marker-end="url(#arrow)"/>

<rect x="454" y="60" width="90" height="64" rx="8" fill="#FCEBEB" stroke="#A32D2D" stroke-width="1"/>
<text x="499" y="86" font-family="sans-serif" font-size="14" font-weight="600" fill="#501313" text-anchor="middle">B3</text>
<text x="499" y="104" font-family="sans-serif" font-size="12" fill="#791F1F" text-anchor="middle">treno</text>

<circle cx="40" cy="155" r="5" fill="#639922"/>
<text x="52" y="159" font-family="sans-serif" font-size="12" fill="#3d3d3a">verde: i 2 blocchi successivi sono entrambi liberi</text>
<circle cx="40" cy="177" r="5" fill="#BA7517"/>
<text x="52" y="181" font-family="sans-serif" font-size="12" fill="#3d3d3a">giallo: il prossimo blocco è libero, quello dopo è occupato</text>
<circle cx="40" cy="199" r="5" fill="#A32D2D"/>
<text x="52" y="203" font-family="sans-serif" font-size="12" fill="#3d3d3a">rosso: il blocco protetto da questo segnale è occupato</text>
</svg>></p>

Two real prerequisites this needs before it can be built, not after:
- A tail sensor attached to whichever carriage is actually last on a given train - a fixed-position world sensor can't detect "train fully passed" when trains vary in length.
- Generalizing the signal script from controlling one hardcoded signal to a list of N signals with per-block occupancy state. Current script isn't shaped to extend, it's shaped for exactly one signal.

**Incident detection**, in order of how hard each one actually is: buffer collision (cheap - velocity check on an existing `Touched` event) → train-on-train collision (same idea) → derailment. Derailment is the expensive one: the train's movement isn't physically coupled to the rail geometry, so "off the rails" isn't a concept the game currently has any way to detect. It needs distance-from-spline tracking built from scratch, not a flag that already exists somewhere.

**Scoring**, concept stage: points for passengers/cargo delivered, signal compliance, on-time arrival within a 2-minute window. Point values per event aren't decided yet. A "traffic controller" player role is tied to this - a human overriding the automated block signaling, same system as above with a manual layer on top.

**Cosmetic shop.** Deliberately not scoped alongside everything else above - `ProcessReceipt` handled wrong doesn't just create a bug, it can fail to deliver a paid purchase or let it be duplicated. Gets its own pass when it's actually next in line, not folded into a sprint with unrelated UI work.

---

## Built on

Roblox Studio (Luau) · Python for the OSM data pipeline · Blender for train and signal models · real GPX route data for track geometry
---

## Core Features (Implemented)

[#core-features](#core-features)

- **Dynamic train composition** - variable number of carriages per train, built from a reusable model template
- **Full cab controls** - front/rear lights, horn, pantograph, doors, 3-phase horn system, VehicleSeat-based driving
- **Real-time Italian clock** - synced to system time with DST logic, drives both the digital/analog station clocks and (soon) departure schedules
- **Departure board system** - dual-screen platform displays (`Cartello orari` at the platform, `Tabella orari` station-wide), alternating flashing departure indicators, scrolling info ticker
- **Basic block signaling** - red/yellow/green departure signal with a manual "request departure" flow, auto-reverting after a timed window
- **Station generation** - ~3,000 real Italian railway stations placed via the Overpass API (OpenStreetMap), scaled 1:200
- **Track generation** - Catmull-Rom spline-based track laying following real GPX route data
- **Trattas & train types** - route/train-type selection menu (Regionale, Intercity, Frecciarossa, Italo) with per-route availability and duration

---

## Roadmap

[#roadmap](#roadmap)

Ordered by dependency, not by excitement - foundational fixes come before new systems, because new systems built on broken foundations get rebuilt twice.

| # | Item | Status | Notes |
|---|------|--------|-------|
| 1 | Delay/early arrival system tied to real Italian clock | 🔧 In progress | Replaces a hardcoded fake schedule that produced nonsensical results |
| 2 | Train spawn position bug | 🐞 Open | Clone spawns ~176 studs off from the template position |
| 3 | Additional real routes (currently only Torino→Lingotto has physical track) | 📋 Planned | 7 routes exist in the menu but lead nowhere yet |
| 4 | Platform 2 spawn point | 📋 Planned | Track exists, spawn point does not |
| 5 | Menu redesign - route preview map, train preview art, per-type icons | 📋 Planned | |
| 6 | Train + carriage count selection in menu | 📋 Planned | Backend composition system already supports variable length |
| 7 | 3-aspect block signaling (red / yellow / green, 2-block lookahead) | 📋 Planned | Matches real RFI distant-signal logic; double-yellow/flashing-yellow deliberately deferred until the base 3-aspect system is solid |
| 8 | Incident detection - buffer collision → train-train collision → derailment | 📋 Planned | Derailment detection needs a spline-proximity system that doesn't exist yet; treated as the most expensive of the three, done last |
| 9 | Scoring system (passengers/cargo delivered, signal compliance, on-time arrival ±2min) | 💭 Concept | Numbers (points per event) still to be defined |
| 10 | Traffic controller player role | 💭 Concept | Tied to item 7 - human override of the automated signaling |
| 11 | Cosmetic shop (Robux) | 💭 Concept | Treated as its own project - `ProcessReceipt` handled incorrectly can cost real money, not scoped lightly |

**Legend:** 🐞 known bug · 🔧 in progress · 📋 planned, scoped · 💭 concept, not yet scoped

---

## Known Issues

[#known-issues](#known-issues)

- Train spawn clone appears at the wrong position (pivot/CFrame mismatch between template capture and clone application)
- Delay/anticipation display was comparing real-world time against a fixed fake schedule - being replaced by real-clock-anchored schedules
- No collision or derailment detection exists yet - required before any incident-based scoring
- Coupling system uses placeholder buffer parts; `RopeConstraint`-based coupling not yet replaced with a real mechanism
- Scene has 50,000+ Workspace descendants, not yet profiled for performance

---

## Tech Stack

[#tech-stack](#tech-stack)

- **Engine:** Roblox Studio (Luau)
- **Data pipeline:** Python (`genera_stazioni_v2.py`) - Overpass API → station placement
- **Track authoring:** Catmull-Rom spline generation from real-world GPX data
- **3D assets:** Blender-authored train models, custom signal geometry

---

## License

[#license](#license)

TBD.
