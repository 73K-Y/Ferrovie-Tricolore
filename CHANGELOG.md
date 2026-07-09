# Changelog

Dated summaries of what changed each work session, in the order they happened. Newest first. This is separate from `GAME_DESIGN.md`, which describes the project's current state, not its history. For that, look here or at the git commit log.

---

## 2026-07-09

**Client-set attributes don't reach the server. This explained half of today's bugs at once.** Roblox doesn't replicate attribute changes from client to server by default, only server to client. The departure-board data (train number, destination, which platform is active) was being written by the menu, a client script, and read by server-side signal logic that could never see it. Two hours of chasing "the client can't see this content yet" turned out to be the wrong direction entirely for several of these bugs, once this was found: the fix was moving the writes server-side (into the script that already validates and spawns the train), not chasing streaming timing further.

**Moved departure-board management from the client to the server entirely.** Previously, a client-side script scanned the whole map once at startup and populated board displays; a second, newer client script listened for physical trigger blocks at each platform. Both depended on distant content having streamed to that specific client, which repeatedly failed to happen reliably and was never fully explained even after eliminating every plausible cause (forced streaming, teleporting the character, saving the place, comparing instance properties, tagging with `CollectionService` as an independent check). The board logic now lives in the same server script that already reliably detects a train's head and tail crossing each signal, and writes directly to the physical `SurfaceGui` objects in the world, which the server can always see without any streaming dependency. The two invisible trigger blocks built earlier in the session were removed entirely, along with the client script that used them.

**A blinking indicator that was permanently on, then permanently off, then finally blinking.** Fixed the same underlying bug (a template gets cloned into a live copy, and the clone inherits whatever visibility the template happened to have baked in) three separate times as it moved between different scripts during the day's refactor. The actual blink state turned out to depend on a `Boarded` flag that nothing was setting server-side, for the same client-to-server replication reason above; fixed by setting it directly from the existing seat-detection script, which already runs on the server.

**Two boards with the same visible fields, built with completely different internal structure.** Porta Nuova's platform sign groups several fields (destination, train number, departure time) inside one row. Lingotto's identically-purposed sign splits the same fields across several separate rows, one field each. Neither is wrong, they're just not interchangeable, and code written assuming the first layout silently failed to find anything on the second. Fixed by scanning every template in a board rather than assuming there's exactly one, not by making the two boards match (that's still open, and would remove a category of bug like this one for good if done).

**Departure and platform assignment is hardcoded, not computed, and that's worth being honest about here too.** Today's system recognizes exactly one route: Porta Nuova platform 1 to Lingotto platform 2. Nothing determines which platform a train is heading to from game state; it's two fixed values written directly in the signal-crossing code. This is fine for what's being tested right now, but it is not a foundation to build multiple simultaneous trains or a real platform-selection menu on without rewriting this part.

---

## 2026-07-04

**Block signaling went from "designed" to "running."** Four signals in sequence now compute red/yellow/green from real 2-block lookahead occupancy, tracked by a single collider (tagged dynamically as "Coda" based on which locomotive the player isn't driving from) crossing a signal zone on exit, not on entry, and not by the front collider at all, after an earlier version using both got replaced with just this one. Verified against an 8-step hand-written state table covering a full departure-to-arrival cycle, not just spot-checked at rest.

**Two signal-adjacent bugs found and fixed, neither where they looked like they'd be:**
- The Italian-time calculation was right, but skipped forcing UTC interpretation before formatting it, meaning it was only correct by accident, because the dev machine's own timezone happened to already be Italian. Would have shown the wrong time on any server actually running in UTC.
- Renaming four signals to add a `(stazione)` tag silently broke the signal-ordering code, which matched a number at the *end* of each name. A name ending in `)` doesn't match. Not a signaling bug at all, a regex pattern several files removed from where the rename happened.

**Departure boards now know which station they're in, not just which platform number.** Porta Nuova's Platform 1 and Lingotto's Platform 1 used to be indistinguishable to the board-routing script. Fixed, and tested at the data layer (`Active`/`Station`/`Platform` attributes flip correctly as a train crosses each signal). **Not yet visible in-game**, because a separate, unrelated problem surfaced while testing: all 7 of Lingotto's departure boards are missing the internal template their Porta Nuova counterparts have, so there's nothing for the (now-correct) routing to display there yet. Content fix, not a script fix, and still open.

**Menu:** the platform selector went from 2 buttons to a 10×2 grid of 20 (only Platform 1 active, the rest visibly disabled rather than silently doing nothing on click). Cost two rounds of layout overlap with neighboring panels before landing on a position verified against actual rendered pixel coordinates in Play mode, not guessed from source offsets.

---
