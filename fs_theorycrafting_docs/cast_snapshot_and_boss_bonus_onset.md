# Cast-Time Snapshots, the Server Tick, and the Ruby Boss-Damage Bonus

## Summary
Two timing mechanics combine to slightly lower the damage of your *opening* shots on a boss:

1. A damaging ability locks in its stats and active buffs at the moment it is **cast**, not when it lands.
2. The ruby boss-damage bonus (Blessing of the Conqueror — +5% at rank 5 / +15% at rank 10 against bosses) does not switch on until your **first damage lands on the boss** — even though its buff appears earlier.

Together, any shot fired *before* your first hit connects lands **without** the boss-damage bonus, even if the bonus is live by the time that shot arrives.

## 1. Damage snapshots at cast, not at landing
The game world updates on a fixed **30 Hz server tick (about 33.3 ms per tick)**. When you cast a damaging ability, the game records your stats and active buffs at that instant. For projectiles with travel time, the moment of *casting* and the moment of *landing* can be several ticks apart — and the damage is decided by the **cast-time** snapshot. A buff that becomes active while your arrow is mid-flight does **not** retroactively apply to that arrow.

## 2. The boss-damage bonus activates on first hit
The ruby boss-damage bonus is delivered by a buff that appears as soon as you engage the boss. However, the **+5% / +15% itself does not apply until your first point of damage actually lands on the boss.** A buff showing as present is not the same as its effect being active — here, the effect is gated on that first hit. (This is the same distinction as a "while healthy" style buff, which can appear in a log even at a moment its condition is not met.)

## 3. The combined opener effect
On the pull, abilities are often fired in a tight burst. The first one to **land** is what flips the bonus on. Anything already **cast** before that first hit connects snapshots without the bonus.

**Example:** opening with Highwind Arrow and Multishot fired back-to-back. The Highwind Arrow lands first and activates the bonus — but the Multishot was launched roughly a third of a second earlier and is already in the air, so it lands at **base** boss damage (no +5% / +15%). The next cast, made after the bonus is live, carries it normally.

## 4. How this was confirmed
- The 30 Hz tick is defined in the game's configuration.
- The first-hit activation is confirmed by log comparison: shots cast **before** the first boss-damage timestamp match the no-bonus damage value, while shots cast **after** match the bonus value. The transition lines up with the first-hit moment — not with when the buff first appears.

## 5. What it means for play
- Your first one or two shots on a boss can read slightly under their fully-buffed value — a small, one-time opener effect.
- It cannot be fully avoided (something has to land first to enable the bonus), but it explains why the very start of a boss's damage looks a touch lower than steady-state.
- Everything after your first hit carries the bonus normally, so the effect is confined to the opener.
