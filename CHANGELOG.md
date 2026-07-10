# Changelog

Dated summaries of what changed each work session, in the order they happened. Newest first. This is separate from `GAME_DESIGN.md`, which describes the project's current state, not its history. For that, look here or at the git commit log.

---

## 2026-07-10

**A ticker's scroll math was reading the wrong number as its own width.** The departure board ticker computes how far to scroll from the label's own rendered size. With `TextScaled` on, that size is the label's fixed container, not the text's real width, so text of any length looped at the wrong point and overlapped itself mid-sentence. Fixed by turning `TextScaled` off, giving the label a real fixed font size, and resizing the label itself to the text's actual measured width every time the text changes, using `TextService:GetTextSize` with a fallback font in case the label's own font isn't one the service recognizes. The same bug, and the same fix, applied to both the platform signs and the station-wide boards, which name this field differently (`SLIDING_TrainInfo` vs `SLIDING_INFO`).

**The admin panel that sets that ticker text only ever reached the platform signs, never the station boards, because of that same naming difference.** Fixed by having the one handler check both names.

**A departure board field named `TrainInfo` turned out to be the information row itself, not a label for the train number.** Writing the train number into it made the number appear jammed into the middle of the scrolling text, not next to it. The actual number field is `Train`/`Code`; `TrainInfo` was left alone once this was understood.

**Six category icons (R, RV, IC, ICN, Frecciarossa, Italo) and a company logo were prepared, uploaded, and wired to the departure boards**, white-on-transparent, uniform canvas size, positioned next to the train number rather than replacing it. Went through three logo re-uploads and two icon re-uploads as sizing was adjusted; each swap was a one-line asset ID change once the pattern was established.

**Train control buttons had no icons at all, on any of the eight buttons, confirmed by reading the actual button-definition code rather than assuming from the screenshot.** All eight (front/rear lights, horn, pantograph, both doors) were blank `icon=""` placeholders. Fixed once real icon assets were uploaded and identified by name search.

**Built an admin-only panel for editing the departure boards' information text project-wide**, gated by Roblox user ID, checked independently on both the client (so the panel doesn't even get built for anyone else) and the server (so the check can't be bypassed by a modified client). One update from the panel now reaches every platform sign and every station board in the game at once, not just the one being tested.

**The "next signal" cab display was showing the nearest signal, which after passing one is usually the signal behind the train, not ahead of it, and its search only checked workspace's direct children, where no signal actually lives.** Both problems were in code whose own comment claimed it was "no longer a placeholder." Rewrote the search to be recursive and to pick the closest signal strictly ahead of the train along the line, then confirmed live: crossing a signal correctly flips the display to the next one, not back to the one just passed.

**The main menu appeared correctly, then didn't, then didn't at all, for three different reasons in a row.** First: the tratta-selection screen was visible behind the menu from the moment the game started, because its `ScreenGui.Enabled` was never explicitly set to false and the earlier code that was supposed to reveal it on "Play" was actually toggling a `LocalScript`'s own `Enabled` property, a property that controls whether a script runs, not anything visual, since "UI" is the script's name, not the screen's; the real screen is `TrattaSelectionGui`, found by digging into what the script creates rather than assuming the object named "UI" was itself the interface. Second, once a real font was wired in to match the departure boards' actual typeface (`Inconsolata`, discovered by reading a live label's `FontFace` rather than guessing), the whole menu silently failed to build past its title card, because the new `Font` datatype value was being assigned to the legacy `.Font` property, which expects an `Enum.Font` and fails without a caught error; fixed by assigning to `.FontFace` instead, everywhere the code used it. Both were found only by comparing what should exist against what was actually present in a live session, not by reading the code and assuming it worked.

**Switched ~3,700 mesh parts from non-default collision fidelity to default**, after finding that count directly rather than guessing at a performance cause. Precise collision shapes cost meaningfully more to simulate than the default hull approximation, and the map has grown enough (a first draft of Lingotto's own platforms added this session) that the difference is no longer negligible. Spot-checked afterward that nothing started falling through geometry; a full pass across the newly larger map wasn't feasible in one sitting and should be treated as spot-checked, not exhaustively verified.

**Still open, not touched this session:** a repeating error in the cab HUD script (`attempt to call a nil value`, likely firing before the character exists), the tratta-selection screen's cramped layout, an unused 251-object "Test" folder never confirmed safe to delete, and audio/HUD-visibility settings that save correctly but aren't wired to anything yet.

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
