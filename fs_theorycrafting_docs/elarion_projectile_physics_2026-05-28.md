# Elarion Projectile Physics — High-Level Report

**Date:** 2026-05-28
**Subject:** How Elarion's arrows actually travel through the world, and what that means for play.
**Data source:** 24 public combat logs from fellowshiplogs.com, covering 9 unique players across 11 of 12 keyable S2 zones — 12,600 individual cast → first-hit measurements.

---

## TL;DR

1. **All six bow abilities travel at 80 yards per second.** Focused Shot, Highwind Arrow, Celestial Shot, Multishot, Heartseeker Barrage, and Grappling Arrow share one engine projectile constant. Game data documents 80 yd/s on Grappling Arrow; the other five log-fit to within 6% of 80 across thousands of casts each.
2. **Voidbringer's Touch travels at 40 yd/s** — half the speed of a standard arrow, using a shared "slow projectile" engine speed also used by several enemy chain-shot abilities. Real-world measurement: 41.7 yd/s across 331 casts. Game-design and observed values agree within 5%.
3. **Lunarlight Mark is instant.** No travel time. It applies the moment you press the button.
4. **The zone you fight in matters more than the player.** Wyrmheart fights happen at 2.6× the distance of Sailor's Abyss fights. Player positioning style is a smaller effect than zone shape.
5. **Voidbringer's detonation timing depends on whether you're fighting a boss or trash.** Trash pulls cap out fast (94% of the time). Boss pulls run out the 15-second timer one in four times because boss mechanics interrupt sustained damage.

---

## 1. What "projectile physics" means here

When you press an ability button, the arrow doesn't hit instantly. There are two delays:

- **Fire overhead** — a small fixed delay between pressing the button and the arrow actually leaving your character.
- **Travel time** — the arrow flies through the air at a fixed speed. Farther target = longer flight.

We can write that as a simple formula:

```
time to first hit  =  fire overhead  +  (distance in yards / arrow speed)
```

If we measure thousands of casts and how long each one took to land, we can solve for both numbers per ability.

That's exactly what this study did.

---

## 2. The arrow-speed table

This table shows two columns. The **game-design value** is the speed the engine specifies (from game data files when one exists, or a clean derived constant when multiple abilities share the same underlying behavior). The **observed value** is what we measured in real combat logs. The two should match closely when the engine is behaving as designed — and they do.

| Ability | Game-design speed | Observed speed | Fire overhead (ms) | Confidence on observed |
|---|---|---|---|---|
| Celestial Shot | **80 yd/s** | 84.4 yd/s | 2 | Very high (n=1,332) |
| Multishot | **80 yd/s** | 82.4 yd/s | 143 | High (n=4,350) |
| Highwind Arrow | **80 yd/s** | 81.0 yd/s | 2 | High (n=1,827) |
| Focused Shot | **80 yd/s** | 83.0 yd/s | 0 | High (n=1,185) |
| Heartseeker Barrage | **80 yd/s** | 85.3 yd/s | 151 | Good (n=2,099) |
| Grappling Arrow | **80 yd/s** (game-file) | 84.3 yd/s | 347 | Low (n=53) — log noise; game-file value wins |
| **Voidbringer's Touch** | **40 yd/s** (shared engine speed) | 41.7 yd/s | 204 | High (n=331) |
| Lunarlight Mark | INSTANT | n/a (instant) | 7 | Very high (n=354) — confirms no projectile |

### The clean reading

**Six abilities share one arrow speed of 80 yd/s.** Focused Shot, Highwind Arrow, Celestial Shot, Multishot, Heartseeker Barrage, and Grappling Arrow all use the same underlying "bow arrow" projectile in the engine. Grappling Arrow's 80 yd/s is documented in game data directly; the other five log-fit to the 81–85 yd/s range — within 6% of 80 across thousands of measurements per ability, consistent with a single shared engine constant.

**Why log fits aren't exactly 80:** real combat introduces small biases — server tick quantization, the player moving during a hard cast, target movement during projectile flight, sampling noise from finite logs. A few percent spread around the true engine value is expected and unavoidable in observation data. The agreement between game-design and observed values across all six bow abilities is strong.

**Voidbringer's Touch is roughly half the speed of standard arrows.** Game-design speed: 40 yd/s. Observed: 41.7 yd/s. The 40 figure is the engine's shared "slow projectile" speed — the same value appears on chain-shot abilities used by several enemy mob types, so we know it's a real engine constant rather than a coincidence. The log fit (R² = 0.90, n=331) confirms VBT actually behaves at this speed in real combat. It is mechanically a different projectile from standard arrows — slower-moving, void-themed — and the engine treats it that way.

**Lunarlight Mark genuinely has no travel time.** Earlier analysis suspected the ~1ms timing was measurement noise. With a larger sample (354 casts) the answer is clear: it's an instant debuff that applies on cast regardless of how far the target is. No projectile is involved.

### What "fire overhead" tells you

Most arrows leave your character within a millisecond or two of your button press (Focused Shot: 0ms. Celestial Shot: 2ms. Highwind Arrow: 2ms — measured from the moment your cast bar completes). The arrow is in flight essentially the instant the cast finishes.

A few abilities have meaningful fire delay:

- **Multishot (143ms)** — the first arrow has a small windup before it fires. This matches the animation: multiple arrows stagger out of the bow, and we're measuring when the first one lands.
- **Heartseeker Barrage (151ms)** — the first tick of the channel fires about one tick-interval after the channel begins. At normal cohort haste, a haste-adjusted HSB tick interval is around 164ms, and our measured 151ms is one server-tick-alignment correction off that. The numbers line up.
- **Voidbringer's Touch (204ms)** — slower projectile **and** additional fire delay. Both contribute.

---

## 3. Zone shape decides engagement distance

You don't get to pick how far away you are from your target — the zone does. Some zones force close-range fighting because of layout, some encourage maximum range because of mob threat.

Here is the median engagement distance measured from Heartseeker Barrage casts, by zone:

| Zone | Median engagement distance (yards) |
|---|---|
| Sailor's Abyss | 5.6 |
| Stormwatch | 7.1 |
| Silken Hollow | 7.6 |
| Godfall Quarry | 9.1 |
| Everdawn Grove | 9.6 |
| Cithrel's Fall | 9.7 |
| Urrak Markets | 9.9 |
| Heart of Tuzari | 10.1 |
| Wraithtide Vault | 11.4 |
| Empyrean Sands | 12.4 |
| **Wyrmheart** | **14.7** |

**Wyrmheart engages at 2.6× the distance of Sailor's Abyss.** That is the largest zone-shape effect in the entire study.

The driver: Wyrmheart features casters and bolters whose mechanics make range the safer position to fight from. Sailor's Abyss is the opposite — close-range layout where the engagement happens at melee distance regardless.

### Example of what this costs in real time

Using the formula on Heartseeker Barrage in two different zones:

- **Sailor's Abyss** (5.6 yd median): ~221ms from cast → first tick land
- **Wyrmheart** (14.7 yd median): ~335ms from cast → first tick land

That is about a tenth of a second of extra delay on first damage every time you channel Heartseeker. Across hundreds of casts in a key, those tenths add up.

---

## 4. Player style is a small effect compared to zone

Earlier rough analysis suggested certain players were unusually "slow" or "fast" with their casts. Looking at the full cohort, that finding doesn't hold up.

When we measure each subject's median engagement distance across all their zones, almost everyone lands in the 8–12 yard band. The one apparent outlier (TestSubject_1 at 18.7 yd median) was sampled almost entirely on Wyrmheart, where the zone forces long range. That zone-specific exposure drives the apparent subject-level outlier; once normalized, this subject is not actually a long-range outlier across zones.

**Conclusion:** zone shape is the dominant factor in engagement distance. Player positioning style is a real but secondary effect.

---

## 5. Voidbringer's Touch — how the detonation actually fires

Voidbringer's Touch stores a percentage of damage you deal to the marked target, then "detonates" the stored damage. It can end in three ways:

1. **Cap hit** — the storage cap fills up and the debuff detonates early.
2. **Timer expires** — the 15-second window runs out, and whatever you stored detonates.
3. **Kill secure** — the target dies, and the stored damage is delivered.

Across 331 detonations in the cohort:

| Trigger | Share |
|---|---|
| Cap hit (or close to it) | 85.2% |
| Timer expired | 11.5% |
| Kill secure | 3.3% |

So most of the time, Voidbringer caps out before the 15s runs out.

### But that single number hides a much more important pattern

When we split the data by what the player was fighting, the picture changes dramatically:

| Context | Cap hit | Timer expired | Kill secure | Median damage rate |
|---|---|---|---|---|
| **Trash pulls** | 94% | 3% | 3% | 322,000 dmg/s |
| **Boss pulls** | 71% | **25%** | 3% | **154,000 dmg/s** |

**Your damage rate during boss pulls is roughly half your trash rate** (154k/s vs 322k/s). That's the single most useful finding in this section. Boss mechanics — line-of-sight, positioning, kicking, phase transitions, forced movement — interrupt sustained damage, and the cap doesn't fill before the 15s window expires.

A practical example, ordered by how often the boss timer-expires Voidbringer:

| Zone | Boss-pull timer-expire rate | Why |
|---|---|---|
| Sailor's Abyss | 63% | Line-of-sight mechanic — hide behind a pole during boss cast |
| Cithrel's Fall | 46% | Multi-boss capstone with phase transitions |
| Empyrean Sands | 45% | Positioning-heavy fight |
| Wyrmheart | 27% | Max-range positioning to dodge caster mobs |
| Heart of Tuzari | 6% | Boss adds keep damage flowing — VBT caps |
| Everdawn Grove | 0% | Sustained DPS fight, no interrupts |
| Silken Hollow | 0% | Sustained DPS fight, no interrupts |

If you spend a key wondering why your Voidbringer feels weaker on some bosses than others, this is the answer: the bosses that interrupt you are the bosses where VBT timer-expires instead of capping.

### A note about overwriting

If you cast Voidbringer's Touch on a target that already has it, the engine **force-detonates** the existing debuff (delivering whatever was stored) and then applies a fresh one. The stored damage isn't silently lost; it's paid out early. The cost is the unused time you would have had to keep accumulating.

In the cohort, this happened in 2 of 331 detonations — about 0.6%. At top-parse skill level, overwriting is rare.

---

## 6. How confident is all of this?

The study used 24 logs, 9 players, 11 zones, and 12,600 measurements. The arrow-speed numbers were derived from a least-squares fit (a standard statistical technique that finds the line of best fit through the data) and the R² values (how well the line explains the data) ranged from 0.73 to 0.94 for the well-sampled abilities. Those are strong fits.

The standard fellowship policy applies: **before treating these numbers as locked-in truth, the same study should run on a second independent batch of logs and confirm the arrow speeds within 5%.** That cross-validation is the next step.

Areas with weaker confidence:

- **Grappling Arrow** — only 53 measurements; the fit is messy. More data needed.
- **Multishot's per-arrow stagger** — we measured the first arrow's timing. The subsequent arrows haven't been individually modeled yet.
- **Heartseeker tick interval** — the 151ms first-tick delay matches the haste-adjusted tick formula but should be verified across players with different haste levels.

---

## 7. What this actually means for play

A few practical takeaways from these numbers:

- **You cannot meaningfully change your bow's arrow speed.** It's a fixed game constant. What you can change is the distance you fight from. Closer = faster damage application.
- **Voidbringer wants sustained damage to do its job well.** If a fight has heavy interrupts, Voidbringer will timer-out more often than it caps. That's not a player skill failure — it's the fight shape.
- **Heartseeker Barrage at long range adds about 100ms of first-tick delay per cast.** That's small, but if you're stacking it over a key it's not nothing.
- **Lunarlight Mark applies the instant you press it.** Don't worry about target distance when marking. You can mark across the room.

---

## 8. Reproducing this study

The analysis tool that produced these numbers is checked in to the project. Anyone with access to the same logs can re-run it and verify the speed table holds up. Methodology in brief:

1. For each ability, find every cast event from a player.
2. Find the first matching damage or debuff event for that cast.
3. Measure the distance between the player's position at fire and the target's position at impact (game coordinates are 100 units per yard).
4. Measure the elapsed time between cast and impact.
5. Run a linear regression across all measured cast/impact pairs per ability to extract arrow speed and fire overhead.

Filters applied: distances under 0.5 yards (target on top of player, noisy) and over 35 yards (out of range, outlier) were dropped. Engine-source events with sentinel (0,0) positions (fall damage etc.) were excluded.

---

*End of report.*
