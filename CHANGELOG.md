# Changelog

Dated summaries of what changed each work session, in the order they happened. Newest first. This is separate from `GAME_DESIGN.md`, which describes the project's current state, not its history. For that, look here or at the git commit log.

---

## 2026-07-04

**Block signaling went from "designed" to "running."** Four signals in sequence now compute red/yellow/green from real 2-block lookahead occupancy, tracked by a single collider (tagged dynamically as "Coda" based on which locomotive the player isn't driving from) crossing a signal zone on exit, not on entry, and not by the front collider at all, after an earlier version using both got replaced with just this one. Verified against an 8-step hand-written state table covering a full departure-to-arrival cycle, not just spot-checked at rest.

**Two signal-adjacent bugs found and fixed, neither where they looked like they'd be:**
- The Italian-time calculation was right, but skipped forcing UTC interpretation before formatting it, meaning it was only correct by accident, because the dev machine's own timezone happened to already be Italian. Would have shown the wrong time on any server actually running in UTC.
- Renaming four signals to add a `(stazione)` tag silently broke the signal-ordering code, which matched a number at the *end* of each name. A name ending in `)` doesn't match. Not a signaling bug at all, a regex pattern several files removed from where the rename happened.

**Departure boards now know which station they're in, not just which platform number.** Porta Nuova's Platform 1 and Lingotto's Platform 1 used to be indistinguishable to the board-routing script. Fixed, and tested at the data layer (`Active`/`Station`/`Platform` attributes flip correctly as a train crosses each signal). **Not yet visible in-game**, because a separate, unrelated problem surfaced while testing: all 7 of Lingotto's departure boards are missing the internal template their Porta Nuova counterparts have, so there's nothing for the (now-correct) routing to display there yet. Content fix, not a script fix, and still open.

**Menu:** the platform selector went from 2 buttons to a 10×2 grid of 20 (only Platform 1 active, the rest visibly disabled rather than silently doing nothing on click). Cost two rounds of layout overlap with neighboring panels before landing on a position verified against actual rendered pixel coordinates in Play mode, not guessed from source offsets.

---
