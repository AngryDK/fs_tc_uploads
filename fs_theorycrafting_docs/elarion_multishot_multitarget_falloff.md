# Multishot — Cleave Geometry and Multi-Target Falloff (Elarion)

## Summary
Multishot resolves in two independent stages: a **geometry** stage that selects which enemies are hit, and a **damage** stage that scales each projectile by how many were hit. Two behaviors catch most players out — the splash is anchored on the **target**, not the player, and the damage cone follows the player's **facing**, so an enemy can be in range and still take **0**. Past 12 targets, per-projectile damage decays as **√(12 ÷ N)**.

## Geometry — which enemies are hit
Three gates, applied in order. Constants are from the hero ability table (`Bowguy.AoeProjectileDamage`); 100 game units = 1 yard.

1. **Range — 30 yd, from the player.** The primary target must be within `RangedRange` (3000).
2. **Radius — 6 yd, from the *target*.** Splash reaches every enemy within `MaxRadius` (600) of the **primary target**. So an enemy in front of you and well within range is skipped if it sits more than 6 yd from the primary — and re-targeting a more central enemy, without moving or turning, pulls the rest of the pack into the splash.
3. **Arc — 100°, from your *facing*.** Of the in-radius enemies, only those inside the `CleaveAngel` (100°) cone around the **direction you face** take damage — and you aim that independently of your target. An in-radius enemy outside the arc still receives a projectile, but for **0 damage**: a consumed arrow, not a miss.

The two anchors are distinct: **radius = target, arc = facing.**

## Damage — the target-count falloff
Each damaged enemy receives one projectile whose value depends only on **N**, the number of enemies *damaged* by the cast (`TargetCountThreshold` = 12):

- **N ≤ 12:** full damage.
- **N > 12:** full × **√(12 ÷ N)**.

Aggregate output is `full × √(12 · N)` — sub-linear. Doubling the pack above the threshold multiplies total damage by √2 (≈ 1.41×), while each enemy's share falls as 1/√N.

| N | per-projectile √(12 ÷ N) | aggregate √(12 · N) |
|---|---|---|
| 12 | 100.0% | 12.00 |
| 16 | 86.6% | 13.86 |
| 20 | 77.5% | 15.49 |
| 24 | 70.7% | 16.97 |

12 → 24 targets: **+41% total, −29% per enemy.**

## Evidence
- **Constants** (range, radius, arc, threshold, coefficient) — read directly from the hero ability table.
- **Anchoring** — combat-log positions: cleaved enemies reach ~30 yd from the player but cluster ≤6 yd from the primary (90th percentile = 6.1 yd, matching the 6-yd radius). In-game, re-targeting a central enemy without turning brings skipped enemies into the splash.
- **Arc as damage gate** — 0-damage Multishot hits appear in logs precisely where an enemy is in-radius but off-arc; 99.7% of *damaging* hits fall inside the 100° cone. Those 0s are ~0.1% of hits in real combat (players face their packs), which is why the falloff validates cleanly without modeling the arc.
- **Falloff** — counting **distinct enemy instances** per cast (instance, not type — one pull holds many copies of a single type): N ≤ 12 matches full damage; N = 17–24 lands ~20% low, and √(12 ÷ N) recovers it to within ~1%.

## Play implications
- **≤ 12 targets (bosses, small packs):** no penalty.
- **Target the pack's center.** Because the splash is target-anchored, a central primary maximizes how many enemies fall in the 6-yd radius and the facing arc; an edge target leaves the far side untouched — or hit for 0.
- **Priority target in a big pull** takes only √(12 ÷ N) of a full projectile (~71% at N = 24). Engaging so fewer enemies fall in the radius/arc raises its per-hit damage.
