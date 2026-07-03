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

<p align="center"><img src="docs/block-signaling.svg" alt="Diagramma del block signaling a 3 aspetti: segnale A verde con due blocchi liberi davanti, segnale B giallo con un blocco libero e uno occupato più avanti, segnale C rosso con il blocco protetto occupato dal treno" width="680"></p>

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
