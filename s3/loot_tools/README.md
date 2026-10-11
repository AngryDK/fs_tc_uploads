# Fellowship season 3 item stats, from the game's own tables

What this is: the stat and armor formula for season 3 dynamic loot, as one Python module (`loot.py`) and a small
command-line driver (`make_item.py`). The numbers it needs (slot weights, armor-type weights, the three stat-weight
configurations, the stamina multiplier at item level 315) are read from the game's `items.json`, so a retune in the
game data changes the output with no code change. Weapon templates live in `heroes.json`; pass it for weapons.

What it is not: a loot roller. It does not pick which bonus slots, traits, gems or set bonus an item gets; it gives
the displayed stat lines and armor for a template (or a slot and configuration), an item level, a temper level and
the hero's armor type. Rarity is deliberately not an input: it changes the temper cap and how many bonus slots an
item has, never a stat value.

## Run

    python3 make_item.py items.json --heroes heroes.json --list
    python3 make_item.py items.json --template Back_A_Crit --il 315 --armor Cloth --temper 4
    python3 make_item.py items.json --heroes heroes.json --template Weapon_A_Haste_Bowguy --il 315 --armor Mail
    python3 make_item.py items.json --slot Chest --variant 22.22.40 --il 315 --armor Mail --teal sec

Python 3.8 or later, standard library only.

## The formula (what loot.py computes)

    stat = round( pool * stat_weight * stat_mul / 0.15 * variant_weight * slot_stat_weight ) + temper
      pool, primary and stamina: 1.03^(il // 15) * sqrt(il) * 10      (integer division)
      pool, secondary:           sqrt(72 * il) * 2.4
      stat_weight: primary 0.25, stamina 0.5, secondary 0.3 ; stat_mul: primary and stamina 0.7, secondary 0.6
      stamina at il >= 315: multiplied by the asset's StaminaMultiplierAtThreshold (1.5) before the round
      round: half away from zero
    bonus (teal) lines: flat weight 0.16 instead of the variant weight, multipliers 0.525 (primary and stamina)
      and 1.125 (secondary); they do not temper
    rings and necks have no fixed primary: the first secondary sits in the primary position and takes that
      position's variant weight
    armor = ceil( slot_armor_weight * (il * type_armor_weight + type_flat) )   no temper, no rarity

The three configurations (`DT_StatWeightConfiguration`) are positional to the item's three FixedSlots:
22.22.40 (Big_Secondary), 40.17.27 (Big_Stamina), 28.28.28 (Evens). Every template names its own.

## Names, slots and armor types, as the files have them

- Real item names are inside the templates. Armor: `DisplayNameByArmorType`, one name per armor type (Chest_A_Crit
  is Webbed Robe in Cloth, Tribal Hauberk in Leather, Skittershard Bound Chestpiece in Mail, Venom Pitted
  Chestpiece in Plate). Jewelry: the same field under the armor type `None`, one name for everyone (Rubellite
  Ring, Drowned Deckhand's Locket). Legendaries: `DisplayNameByHero`, one name per hero (`--hero` picks it).
  Weapons: one `DisplayName`. Every one of the 237 templates resolves to a real name this way; `--list` shows them
  and a built item prints its name. Heroes appear under their in-game names (the files use dev keys: Bowguy is
  Elarion, Mosse is Sylvie, Ink is Tariq, Vigor is Vigour, Lisa is Aeona, FireMage is Ardeos, Warmaster is Helena,
  Sune is Xavian).
- The item-type enum says Waist; the slot-weight table has no Waist row and the Waist templates use the Legs
  row (there are no Legs templates). The tool maps Waist to Legs.
- Cloaks (Back) carry a Cloth name only, so the tool computes their armor as Cloth for every hero. That is what the
  files say; we have not confirmed it against a non-cloth hero's cloak tooltip.

## Worked example, item level 315, Mail hero

    Chest, 22.22.40, no temper:   +25 Stamina, +8 Primary, +17 secondary, armor 113
    Ring,  22.22.40:              +15 Stamina, +6 secondary (primary position), +10 secondary
    Chest bonus secondary line:   +13

## How sure

- Core stats: 5,146 of 5,146 live item lines exact on patch 0.4.2.0 logs; stamina at 315: 1,814 of 1,814;
  bonus secondaries: 981 of 981; armor tooltip-exact across all four armor types.
- The constants are those of the compiled stat-calculation code as relayed by a developer in June 2026 and as
  carried in `DA_StatCalculationSettings` in `items.json`; the 0.4.7.0 (CL-115701) files carry the same values.
- Open: item level 360 (legendaries) is not validated by us; the formula's 360 values run about 1% under another
  community fit. Cloak armor as Cloth for non-cloth heroes is read from the names, not yet from a tooltip.

## Files

- `loot.py`: the formula and `tables_from_game_files(items_json)`.
- `make_item.py`: the driver; `--list` prints every template with slot, configuration, fixed slots, rarities
  and (for weapons) the hero.
- `items.json`, `heroes.json`: the game's data files from build 0.4.7.0 (CL-115701), as extracted; the
  `dynamicLoot` block of `items.json` and the per-hero weapon templates of `heroes.json` are what the tool reads.
