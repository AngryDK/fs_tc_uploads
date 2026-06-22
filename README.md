# Welcome to Ângry's Fellowship API-ish Dump

## News
**S3 "Rise of the Heskyr" — LIVE 2026-06-22**
Season 3 is live. Full progression reset. New hero Gunde, Loot 2.0, stat squish, new zones.

**Guide + tool site:** https://fs-theorycrafting.com

**Data repo restructured** — season-first layout: `/s2/<resource>.json`, `/s3/<resource>.json`


It seems both Health and Dmg scaling follow the same rules.

S3 (current):
```
ROUND(ROUND(2856*BaseHealthMultiplier)*DifficultyScaleMultiplier)
ROUND(ROUND(120*Spell_CoEfficient)*DifficultyScaleMultiplier)
```

S2 (reference):
```
ROUND(ROUND(28560*BaseHealthMultiplier)*DifficultyScaleMultiplier)
ROUND(ROUND(1700*Spell_CoEfficient)*DifficultyScaleMultiplier)
```
*Base values from `CT_CharacterBaseAttributes` Default row. S3 base main stat 1700→120, base health 28560→2856.*

# Fellowship Formulas
### Stats
**Diminishing Returns**
Secondary attributes are affected by Diminishing Returns (DR). Beyond 10%, each rating point has less weight towards the stat percent.

S3 (current):
- From 0-10% you get full value.
- From 10-15% you get 0.98 value.
- From 15-20% you get 0.96 value.
- From 20-25% you get 0.94 value.
- Beyond 25% you get 0.92 value

*The default mod starts at .16 but each step the new value gets reduced by the next tier*

S2 (reference):
- From 0-10% you get full value.
- From 10-15% you get 0.95 value.
- From 15-20% you get 0.9 value.
- From 20-25% you get 0.85 value.
- Beyond 25% you get 0.8 value

*The default mod starts at .017 but each step the new value gets reduced by the next tier*

### Mechanic Math
**Value of Crit damage and Crit Mods**
```
(base_dmg * non_crit_chance)  + (base_dmg * crit_chance * crit_dmg_mod)
```
To factor this with elarion purple 30% crit and last light 30% just add `crit_pct + .3 * .8`
**Crit Damage Mods**
```
2 * (1 + mod + mod + mod)
```
**Spirit Proc Chance**
```
%spirit/1.%spirit
```
**Spirit Gain and Spirt**
So mobs have spirit. Take void lord 400. This is split between the group over time doing damage.
```
20 * 1.spirit
```
**Gem Overcap Mods**
```
0.01
12 * 0.01 / 100 + 1
1.0012
```
This is applied to the stam directly then the stamina to health mod is used on it.

**Magic DR**
```
(1 - .1) * (1 - .072)
1 - result = total dr
```
**Armor DR**
```
(armor * 0.0052) / (7 + armor * 0.0048)
```
![armor curve](pictures/armor_curve_formula.png)
**Damage and ability mods**
```
random(0.9, 1.1)
```
The ability mod will be the avg of the low/high values averaged
**Red/Diamond flat + main_stat**
Apparently this is just added to base before the other math.

*It seems that abilities all have a mod and this is then either plus or minus 10% either direction.*

**Focus Regen**
```
5/s
5 * 1.haste%
```
**Sqrt Scaling** (AoE target-count falloff)
All AoE abilities deal full damage up to a per-ability `TargetCountThreshold`. When N targets exceeds the threshold, each target takes reduced damage:
```
if N <= threshold:
    damage_per_target = base_damage

if N > threshold:
    damage_per_target = base_damage * sqrt(threshold / N)
```
Elarion Multishot threshold = **12** (from `AC_Hero_Bowguy.csv: Bowguy.AoeProjectileDamage.TargetCountThreshold`).

Example — MS hitting 20 targets:
```
damage × sqrt(12 / 20) = damage × sqrt(0.6) ≈ damage × 0.775
```
Each hero's threshold is set per-ability in their AC csv.
**Spirit Gen**
```
spirit = enemy.SpiritPointValue × min(dmg, enemyMaxHP)/enemyMaxHP × Hero.SpiritPointGain.SpiritPointsFromDamageScaler
```
