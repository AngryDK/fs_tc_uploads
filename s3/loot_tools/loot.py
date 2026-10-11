"""The s3 dynamic-loot stat formula: displayed stat lines and armor of an item from slot, item level and variant.

The formula structure and the native constants are here; the table numbers (slot weights, armor-type weights, stat
weight variants, the stamina multiplier at the threshold) arrive as a `tables` dict, built from a dump's items.json by
`tables_from_game_files`, so a retune in the game data needs no code change. Stat lines round half away from zero,
armor rounds up. Output reproduces the old module exactly (tests/fs_engine_test.py).

Source tags as recorded with the formula in the old tree's formula-recovery study; not re-read for this port.
"""

import math

# native: compiled constants, in no shipped asset
PRIMARY_DIVISIBLE = 15  # native
PRIMARY_POWER_BASE = 1.03  # asset: DA_StatCalculationSettings.PrimaryPowerBase
PRIM_STAM_MULT = 10.0  # asset: PrimaryAndStaminaMultiplier
SECONDARY_MULT = 2.4  # native
SECONDARY_BASE_MULT = 72.0  # native
ROLLED_WEIGHT = 0.16  # native ITEM_VARIANTS rolled weight, the same for all three variants

# per path: (prim_weight, sec_weight, stam_weight, prim_mult, sec_mult, weight_mult). DYNAMIC's sec_w, stam_w, w_mul and
# both multipliers equal items.json DynamicSlotCalculationSettings; prim_w is in no asset block. The FIXED multipliers
# 0.7 and 0.6 differ from the asset's FixedSlotCalculationSettings (0.525, 1.125) [src: items.json, CL-114580]: the
# old record calls them native and validated them on live items [UNVERIFIED here].
FIXED = dict(prim_w=0.25, sec_w=0.3, stam_w=0.5, prim_mul=0.7, sec_mul=0.6, w_mul=0.15)
DYNAMIC = dict(prim_w=0.25, sec_w=0.3, stam_w=0.5, prim_mul=0.525, sec_mul=1.125, w_mul=0.15)

# from this item level stamina takes tables["stam_mult_at_threshold"] before rounding (0.4.2.0); the level is not in
# the asset and was pinned by live data
STAM_THRESHOLD_IL = 315


def _round_half_away(x):
    # the native round(): half away from zero, not Python's round-half-even
    return math.floor(x + 0.5) if x >= 0 else math.ceil(x - 0.5)


def stat_value(kind, slot, il, variant, tables, is_dynamic=False, temper=0):
    """One displayed stat line. kind in {stam, prim, sec}; variant is a tables['variants'] key.
    is_dynamic=True = a teal/bonus roll (does NOT temper; temper arg ignored there)."""
    if il < 1:
        return 0
    v = tables["variants"][variant]
    s = DYNAMIC if is_dynamic else FIXED
    if kind in ("prim", "stam"):
        amt = (PRIMARY_POWER_BASE ** (il // PRIMARY_DIVISIBLE)) * math.sqrt(il) * PRIM_STAM_MULT
        amt *= s["prim_mul"] / s["w_mul"]
        amt *= s["stam_w"] if kind == "stam" else s["prim_w"]
        if kind == "stam" and il >= STAM_THRESHOLD_IL:
            amt *= tables["stam_mult_at_threshold"]
    else:
        amt = math.sqrt(il * SECONDARY_BASE_MULT) * SECONDARY_MULT
        amt *= s["sec_w"] * s["sec_mul"] / s["w_mul"]

    # a rolled line takes the flat rolled weight; a fixed line the variant weight of its stat
    amt *= ROLLED_WEIGHT if is_dynamic else v[kind]
    amt *= tables["slot_stat_weights"][slot]
    base = _round_half_away(amt)
    return base if is_dynamic else base + temper


def fixed_slot_lines(fixed_kinds, slot, il, variant, tables, temper=0):
    """All core lines for an item, in FixedSlots order. fixed_kinds e.g. ['stam','prim','sec'].
    Handles the jewelry positional rule: on Ring/Neck ([stam, sec, sec]) the FIRST sec sits in
    the primary POSITION and takes the prim-position variant weight; the second keeps sec."""
    v = tables["variants"][variant]
    out = []
    sec_seen = 0
    for kind in fixed_kinds:
        if kind == "sec":
            sec_seen += 1
            if slot in ("Ring", "Neck") and sec_seen == 1:
                # secondary magnitude, weighted by the primary position it occupies
                amt = math.sqrt(il * SECONDARY_BASE_MULT) * SECONDARY_MULT
                amt *= FIXED["sec_w"] * FIXED["sec_mul"] / FIXED["w_mul"]
                amt *= v["prim"]
                amt *= tables["slot_stat_weights"][slot]
                out.append(_round_half_away(amt) + temper)
                continue
        out.append(stat_value(kind, slot, il, variant, tables, temper=temper))
    return out


def armor_value(slot, armor_type, il, tables):
    """Displayed armor. Does NOT temper, does NOT scale with rarity. ceil, own layer."""
    aw = tables["slot_armor_weights"].get(slot, 0.0)
    tw, flat = tables["armor_types"].get(armor_type, (0.0, 0.0))
    if not aw or not tw:
        return 0
    return math.ceil(aw * (il * tw + flat))


def tables_from_game_files(items_json):
    """The tables dict from a loaded items.json; the site's gear catalog embeds the same block."""

    def rows(section, name):
        for r in section[name]:
            if "Rows" in r:
                return r["Rows"]
        raise KeyError("no Rows in %s" % name)

    root = items_json["root"]
    slot_rows = rows(root, "DT_SlotWeights")
    armor_rows = rows(root, "DT_ArmorTypeWeights")
    weight_rows = rows(items_json["dynamicLoot"], "DT_StatWeightConfiguration")

    # DT_SlotWeights row name -> the formula's slot key
    slot_key = {
        "Head": "Head",
        "Shoulders": "Shoulders",
        "Back": "Back",
        "Chest": "Chest",
        "Wrists": "Wrists",
        "Gloves": "Hands",
        "Legs": "Legs",
        "Feet": "Feet",
        "Weapon": "Weapon",
        "Necklace": "Neck",
        "Ring": "Ring",
        "Trinket": "Relic",
    }
    stat_w, armor_w = {}, {}
    for row_name, r in slot_rows.items():
        k = slot_key.get(row_name)
        if k:
            stat_w[k] = r["StatWeight"]
            armor_w[k] = r["ArmorWeight"]

    # weight rows are positional [stam, prim, sec] over 100
    variant_name = {"22.22.40": "Big_Secondary", "40.17.27": "Big_Stamina", "28.28.28": "Evens"}
    variants = {}
    for key, r in weight_rows.items():
        st, pr, se = r["Weights"]
        variants[variant_name.get(key, key)] = dict(stam=st / 100.0, prim=pr / 100.0, sec=se / 100.0)

    da = items_json["dynamicLoot"]["DA_StatCalculationSettings"][0]["Properties"]
    stam_mult = (da.get("FixedSlotCalculationSettings") or {}).get("StaminaMultiplierAtThreshold", 1.0)

    return {
        "slot_stat_weights": stat_w,
        "slot_armor_weights": armor_w,
        "armor_types": {name: (r["ArmorWeight"], r["FlatArmor"]) for name, r in armor_rows.items()},
        "variants": variants,
        "stam_mult_at_threshold": stam_mult,
    }
