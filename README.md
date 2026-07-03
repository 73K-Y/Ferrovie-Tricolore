# Ferrovie Tricolore

**A realistic Italian railway simulator built in Roblox Studio.**

*Working title during development: "Ita Rails" — internal scripts, folders, and variable names still use this name and will be renamed at release, not before.*

Torino Porta Nuova → Lingotto and beyond — dynamic train composition, real-time Italian clock, block signaling, and a growing map generated from real OpenStreetMap station data.

---

## Overview

[#overview](#overview)

Ferrovie Tricolore simulates driving and dispatching trains across a scaled (1:200) recreation of Italian railway lines, starting from Torino. The game combines manual train operation (cab controls, horn, lights, doors) with a live departure-board system and station signaling modeled on real RFI (Rete Ferroviaria Italiana) conventions.

The world clock is synced to real Italian time (UTC+1) — what you see on the platform clock is what time it is in real life, right now.

---

## Core Features (Implemented)

[#core-features](#core-features)

- **Dynamic train composition** — variable number of carriages per train, built from a reusable model template
- **Full cab controls** — front/rear lights, horn, pantograph, doors, 3-phase horn system, VehicleSeat-based driving
- **Real-time Italian clock** — synced to system time with DST logic, drives both the digital/analog station clocks and (soon) departure schedules
- **Departure board system** — dual-screen platform displays (`Cartello orari` at the platform, `Tabella orari` station-wide), alternating flashing departure indicators, scrolling info ticker
- **Basic block signaling** — red/yellow/green departure signal with a manual "request departure" flow, auto-reverting after a timed window
- **Station generation** — ~3,000 real Italian railway stations placed via the Overpass API (OpenStreetMap), scaled 1:200
- **Track generation** — Catmull-Rom spline-based track laying following real GPX route data
- **Trattas & train types** — route/train-type selection menu (Regionale, Intercity, Frecciarossa, Italo) with per-route availability and duration

---

## Roadmap

[#roadmap](#roadmap)

Ordered by dependency, not by excitement — foundational fixes come before new systems, because new systems built on broken foundations get rebuilt twice.

| # | Item | Status | Notes |
|---|------|--------|-------|
| 1 | Delay/early arrival system tied to real Italian clock | 🔧 In progress | Replaces a hardcoded fake schedule that produced nonsensical results |
| 2 | Train spawn position bug | 🐞 Open | Clone spawns ~176 studs off from the template position |
| 3 | Additional real routes (currently only Torino→Lingotto has physical track) | 📋 Planned | 7 routes exist in the menu but lead nowhere yet |
| 4 | Platform 2 spawn point | 📋 Planned | Track exists, spawn point does not |
| 5 | Menu redesign — route preview map, train preview art, per-type icons | 📋 Planned | |
| 6 | Train + carriage count selection in menu | 📋 Planned | Backend composition system already supports variable length |
| 7 | 3-aspect block signaling (red / yellow / green, 2-block lookahead) | 📋 Planned | Matches real RFI distant-signal logic; double-yellow/flashing-yellow deliberately deferred until the base 3-aspect system is solid |
| 8 | Incident detection — buffer collision → train-train collision → derailment | 📋 Planned | Derailment detection needs a spline-proximity system that doesn't exist yet; treated as the most expensive of the three, done last |
| 9 | Scoring system (passengers/cargo delivered, signal compliance, on-time arrival ±2min) | 💭 Concept | Numbers (points per event) still to be defined |
| 10 | Traffic controller player role | 💭 Concept | Tied to item 7 — human override of the automated signaling |
| 11 | Cosmetic shop (Robux) | 💭 Concept | Treated as its own project — `ProcessReceipt` handled incorrectly can cost real money, not scoped lightly |

**Legend:** 🐞 known bug · 🔧 in progress · 📋 planned, scoped · 💭 concept, not yet scoped

---

## Known Issues

[#known-issues](#known-issues)

- Train spawn clone appears at the wrong position (pivot/CFrame mismatch between template capture and clone application)
- Delay/anticipation display was comparing real-world time against a fixed fake schedule — being replaced by real-clock-anchored schedules
- No collision or derailment detection exists yet — required before any incident-based scoring
- Coupling system uses placeholder buffer parts; `RopeConstraint`-based coupling not yet replaced with a real mechanism
- Scene has 50,000+ Workspace descendants, not yet profiled for performance

---

## Tech Stack

[#tech-stack](#tech-stack)

- **Engine:** Roblox Studio (Luau)
- **Data pipeline:** Python (`genera_stazioni_v2.py`) — Overpass API → station placement
- **Track authoring:** Catmull-Rom spline generation from real-world GPX data
- **3D assets:** Blender-authored train models, custom signal geometry

---

## License

[#license](#license)

TBD.
