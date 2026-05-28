# Amethyst Splinters — High-Level Mechanic Report

**Tariq Cohort (N=40, S2 Eternal)**

## Summary

Amethyst Splinters is a weapon-tree Major trait that places a stacking-pool damage-over-time effect on enemies hit by critical strikes. Despite a sparse tooltip, the underlying mechanic is a pandemic-rolling DoT with a carryover damage pool and a fixed 8-second base duration. This report covers what the cohort data confirms, what the in-game engine adds to the picture (30Hz server tick), and the math you can rely on for sim modeling.

## Tooltip vs Reality

In-game tooltip text:

> When you deal critical damage to an enemy, you deal an additional 7% / 8% / 9% / 10% of that damage to them over 8 seconds.
>
> When you Critically heal an ally, an additional 7% / 8% / 9% / 10% of that heal's value is replicated over 8 seconds on that ally.
>
> Amethyst Splinters can not critically strike.

The tooltip omits four key mechanical details that we confirmed through cohort log analysis:

- Both regular critical strikes AND grievous critical strikes (overflow crits from >100% crit chance) trigger Splinters. The tooltip just says "critical damage."
- Reapplications during an active window do not overwrite. The remaining damage in the active DoT is carried forward into the new pool (pandemic-roll).
- The base tick interval is 2 seconds, modulated by player haste. Higher haste = faster ticks.
- Splinters confirmed cannot critically strike (100% of tick events are non-crit hits in the cohort).

## Server Tick and Timing

Fellowship's game engine runs at 30 Hz — one server frame every 33.33 ms. All tick events in the combat log are timestamped at the nearest frame boundary. This sets a hard precision floor for any log-only tick-timing analysis.

### Tick interval formula

```
tick_interval_ms = 2000 / (1 + live_haste_pct / 100)

    Base interval:  2000 ms (per ability design)
    Haste source:   sum of all active haste contributions on the player
    Frame:          33.3 ms (30 Hz server tick)
```

At a Tariq baseline of ~25% haste rating + persistent gem contributions, ticks fire every ~1450 ms. With Spirit of Heroism active (+30% during Raging Tempest cast) and full Harmonious Soul stacks, live haste swings to ~70% and tick interval compresses to ~1180 ms.

### What we measured

Across 162,242 within-segment tick deltas in N=40 Tariq reports:

- 43% of ticks land within 16.7 ms (one server half-frame) of predicted timing
- 88.6% land within 50 ms (1.5 frames)
- Median absolute error: 1.36%; P90: 3.82%

This is at the engine's quantization floor for log-only analysis. The remaining ~11% of ticks beyond 1.5 frames cluster at buff-transition moments (Spirit of Heroism applying, Harmonious Soul stack changes) where the engine's sub-frame scheduling cannot be reconstructed from log timestamps alone.

## How the Damage Works

### Per-crit pool contribution

Every critical hit by the wielder adds 10% (at trait rank 4) of that hit's damage to a per-target Splinters damage pool. The pool is then distributed across the next 8 seconds as roughly 6 ticks (haste-modulated), each tick delivering `pool/N` where N is the number of remaining scheduled ticks.

```
pool_added         = crit_damage * 0.10                  # at rank 4
ticks_per_window   = 8000 / tick_interval                # roughly 6
per_tick_damage    = current_pool / ticks_remaining
```

### Pandemic refresh

When a new crit lands during an active Splinters window, the engine does NOT discard the unticked portion of the previous pool. Instead it:

- Takes the remaining pool (damage that has not yet ticked out)
- Adds 10% of the new crit damage to that pool
- Resets the duration to 8 seconds and schedules a fresh 6 ticks

Result: in a pace where crits land at least once every 8 seconds, no Splinters damage is ever lost. The pool rolls forward continuously, and the per-tick value shifts each time a new crit refreshes it.

### Critical hit damage multiplier (Amethyst tier interactions)

At higher Amethyst gem ranks the player's critical hit damage multiplier increases:

```
base crit hit  = 2.0x normal
Sealed Fate R1 (target >50% HP): 2.0 * (1 + 0.05) = 2.10x
Sealed Fate R6 (target >50% HP): 2.0 * (1 + 0.15) = 2.30x
Blessing of the Deathdealer R10: + an additional 9% on top of that
```

This matters for Splinters because the pool input is 10% of the crit's actual logged damage — a hit doing 2.30x base instead of 2.0x base contributes 15% more to the Splinters pool. The cohort's observed Splinters-total / crit-total ratio of 12-13% (vs. tooltip 10%) is explained by the live expertise modifier and the pandemic carryover dynamic.

## Cohort-Level Findings (N=40 Tariq Splinters runs)

### Splinters total / crit total ratio

Across the full cohort (1,190 individual target-fights), the Splinters damage / crit damage ratio is tightly bounded:

- Median per-target ratio: 12.85%
- Mean: 12.31%
- Hard cap observed: ~17%
- No target exceeds this regardless of crit volume (51 crits vs. 17 crits produce the same ratio)

The bounded distribution rules out an accumulator-style mechanic (which would show unbounded growth on heavy-crit targets). The ratio is fundamentally fixed by the trait's 10% input per crit + the live expertise modifier applied to each tick.

### Tick interval distribution

Two peaks dominate the dt histogram across 96k+ within-segment deltas:

- 1400-1450 ms (28%) — steady state with Adrenaline Rush II + persistent gem haste
- 1500-1550 ms (21%) — intermediate windows between buff procs
- 1200-1300 ms — Spirit of Heroism active windows (~+30% haste)

No secondary peak at ~800 ms, confirming Splinters is a single-pool effect per target, not multi-instance.

### Lifecycle observations

- Single `applydebuff` per target lasts up to 125+ seconds when crits keep refreshing
- No explicit `refreshdebuff` events are emitted — all extension is silent in the log
- `removedebuff` only fires when crits stop for 8+ seconds or the target dies

## What Feeds Splinters (per cohort builds)

Splinters does not care which ability crit. Anything that produces a `hitType=2` (crit) or `hitType=22` (grievous crit) damage event from the wielder adds to the pool. Tariq examples observed feeding Splinters most heavily:

- Chain Lightning — dominant cast count; high crit rate
- Heavy Strike + Skull Crusher — main builder + spender combo
- Sahril's Wrath (Spirit ability) — AoE pulse + stacking +6% crit per enemy hit (Sundering Wrath)
- Raging Tempest — 20s window of additional lightning ticks at 1/sec; each can crit and trigger Splinters

### Cross-hero confirmation

Splinters is universal (it is a weapon-tree Major trait, not a hero trait). The cohort meta-build data shows Tariq picks it at the highest rate (~30% of S2 Eternal Tariq runs), followed by Ardeos and Rime at ~10-11%. The mechanic behaves identically across heroes — the differences come from each hero's crit cadence and what abilities they front-load.

## Open Questions / Uncaptured Detail

A handful of items remain inferred rather than directly observed — flagged for in-game testing or source-file confirmation:

- **Trait : Focused Haste** (effect 1002141) — emits as a buff but the tooltip omits the rating value. Source trait is unidentified.
- Exact pool-divide formula when refresh happens immediately after a tick fires (sub-frame timing not visible in logs).
- Whether the HoT side (Splinters on heal crits) follows the same pandemic-roll mechanic — cohort sparse on HoT side, only Tariq DPS data so far.

## Sim Modeling Recommendations

### What the sim can use directly

- Tick rate: `2000 / (1 + live_haste_pct/100)`, quantized to 30 Hz frames
- Per-crit pool input: 10% (rank 4) of the actual crit damage event amount
- Pool delivery: divide pool evenly across 6 ticks per 8s base duration (haste compresses interval, not tick count proportionally)
- Pandemic refresh: keep remaining pool, add new contribution, reschedule 6 fresh ticks

### What to treat as noise

- ±16.7 ms quantization on every tick (engine half-frame)
- ±50 ms on transition ticks (buff applying mid-interval)
- Outliers beyond 1.5 frames — track the count but accept as inherent log-side noise

---

*Generated from N=40 Tariq cohort, keys 25-36, S2 Eternal. live_stats validator median tick-interval prediction error: 1.36% (at engine quantization floor).*
