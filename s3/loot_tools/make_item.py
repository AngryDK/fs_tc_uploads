#!/usr/bin/env python3
"""make_item.py: build a Fellowship season 3 item's displayed stat lines and armor from the game's own tables.

    python3 make_item.py items.json --list [--heroes heroes.json]
    python3 make_item.py items.json --template Back_A_Crit --il 315 --armor Cloth --temper 4
    python3 make_item.py items.json --heroes heroes.json --template Weapon_A_Haste_Bowguy --il 315 --armor Mail
    python3 make_item.py items.json --slot Chest --variant 22.22.40 --fixed stam,prim,sec --il 300 --armor Plate
    add --teal sec --teal stam to append bonus (teal) lines

Everything numeric comes from items.json (slot weights, armor types, the three stat-weight configurations, the
stamina multiplier at item level 315) through loot.tables_from_game_files; the formula is loot.py. Weapon templates
live in heroes.json, not items.json, so pass --heroes to list or build a weapon. Rarity is not an input: it never
changes a stat value, only the temper cap and the number of bonus slots.
"""
import argparse
import json
import sys

import loot

VARIANT_BY_WEIGHTS = {"22.22.40": "Big_Secondary", "40.17.27": "Big_Stamina", "28.28.28": "Evens"}
# the game's item-type enum names a few slots differently from the slot-weight table: Waist items use the Legs row
SLOT_BY_TYPE = {"Necklace": "Neck", "Neck": "Neck", "Gloves": "Hands", "Hands": "Hands", "Trinket": "Relic",
                "Relic": "Relic", "Waist": "Legs"}
KIND_BY_SLOTNAME = {"StatStamina": ("stam", "Stamina"), "HeroRelativePrimaryStat": ("prim", "Primary")}
# cloaks carry a display name for Cloth only, so their armor is computed as Cloth whatever the hero wears
CLOTH_ONLY_SLOTS = {"Back"}
# the files name heroes by their dev keys; the in-game names, from the public hero_data.json feed (season 3)
HERO_NAME = {"Lisa": "Aeona", "FireMage": "Ardeos", "Bowguy": "Elarion", "Gunde": "Gunde", "Warmaster": "Helena",
             "Mara": "Mara", "Meiko": "Meiko", "Rime": "Rime", "Mosse": "Sylvie", "Ink": "Tariq", "Vigor": "Vigour",
             "Sune": "Xavian"}


def _text(v):
    return v.get("SourceString") or v.get("LocalizedString") or v.get("CultureInvariantString") or "" if isinstance(v, dict) else ""


def templates(items, heroes=None):
    """name -> {slot, variant, fixed:[(kind,label)], rarities, heroes, names:{armor type: display name}}."""
    out = {}

    def take(name, props):
        t = props.get("HeroItemType", "ECRHeroItemType::Head").split("::")[-1]   # Head is enum 0 and omitted
        fixed = []
        for s in props.get("FixedSlots", []):
            kind, label = KIND_BY_SLOTNAME.get(s, ("sec", s.replace("Stat", "", 1)))
            fixed.append((kind, label))
        # real names: armor pieces one per armor type; jewelry under the armor type "None" (one name for all);
        # legendaries one per hero (DisplayNameByHero); weapons one DisplayName. A dev string is not a name.
        names = {}
        for e in props.get("DisplayNameByArmorType") or []:
            k, v = e["Key"].split("::")[-1], _text(e.get("Value"))
            if v and v != name:
                names["Any" if k == "None" else k] = v
        for e in props.get("DisplayNameByHero") or []:
            v = _text(e.get("Value"))
            if v and v != name:
                dev = e["Key"]["TagName"].split(".")[-1]
                names["hero:" + HERO_NAME.get(dev, dev)] = v
        if not names and _text(props.get("DisplayName")) not in ("", name):
            names = {"Any": _text(props.get("DisplayName"))}
        out[name] = {
            "slot": SLOT_BY_TYPE.get(t, t),
            "variant": VARIANT_BY_WEIGHTS.get(props.get("StatWeights", ""), props.get("StatWeights")),
            "fixed": fixed,
            "rarities": [r.split("::")[-1] for r in props.get("DropsInSpecificRarities", [])],
            "heroes": [HERO_NAME.get(h["TagName"].split(".")[-1], h["TagName"].split(".")[-1])
                       for h in props.get("AllowedHeroes", [])] or None,
            "names": names,
        }

    for name, entries in items["dynamicLoot"].items():
        if name.startswith("DT_") or name.startswith("CT_") or name.startswith("DA_"):
            continue
        for e in entries if isinstance(entries, list) else []:
            p = e.get("Properties") if isinstance(e, dict) else None
            if isinstance(p, dict) and "FixedSlots" in p:
                take(name, p)
    if heroes:
        for hero, block in heroes.items():
            if not isinstance(block, dict):
                continue
            for name, entries in block.items():
                for e in entries if isinstance(entries, list) else []:
                    p = e.get("Properties") if isinstance(e, dict) else None
                    if isinstance(p, dict) and "FixedSlots" in p:
                        take(name, p)
    return out


def build(tables, slot, variant, fixed, il, armor_type, temper, teal):
    kinds = [k for k, _ in fixed]
    core = loot.fixed_slot_lines(kinds, slot, il, variant, tables, temper=temper)
    lines = [(f"+{v} {label}", "core") for v, (_, label) in zip(core, fixed)]
    for kind in teal:
        v = loot.stat_value(kind, slot, il, variant, tables, is_dynamic=True)
        lines.append((f"+{v} {'Stamina' if kind == 'stam' else 'Primary' if kind == 'prim' else 'secondary'}", "bonus"))
    armor = loot.armor_value(slot, armor_type, il, tables)
    return lines, armor


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("items")
    ap.add_argument("--heroes", help="heroes.json, for the 48 weapon templates")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--template")
    ap.add_argument("--slot"); ap.add_argument("--variant", help="22.22.40 | 40.17.27 | 28.28.28 or a dev name")
    ap.add_argument("--fixed", help="comma list of stam,prim,sec in FixedSlots order", default="stam,prim,sec")
    ap.add_argument("--il", type=int, default=315)
    ap.add_argument("--armor", default="Cloth", help="Plate | Mail | Leather | Cloth (the hero's armor type)")
    ap.add_argument("--temper", type=int, default=0)
    ap.add_argument("--hero", help="for a legendary: whose name to print (e.g. Elarion)")
    ap.add_argument("--teal", action="append", default=[], choices=["stam", "prim", "sec"])
    a = ap.parse_args()

    items = json.load(open(a.items))
    heroes = json.load(open(a.heroes)) if a.heroes else None
    tables = loot.tables_from_game_files(items)
    tpl = templates(items, heroes)

    if a.list:
        for name in sorted(tpl):
            t = tpl[name]
            names = "; ".join(f"{k}: {v}" for k, v in t["names"].items())
            print(f"{name:34s} {t['slot']:9s} {t['variant']:13s} {'/'.join(l for _, l in t['fixed']):30s}"
                  f" {','.join(t['rarities'])}{'  heroes=' + ','.join(t['heroes']) if t['heroes'] else ''}"
                  f"{'  ' + names if names else ''}")
        print(f"{len(tpl)} templates" + ("" if heroes else " (weapons need --heroes heroes.json)"))
        return

    if a.template:
        if a.template not in tpl:
            sys.exit(f"no template {a.template!r} (weapons need --heroes; see --list)")
        t = tpl[a.template]
        slot, variant, fixed = t["slot"], t["variant"], t["fixed"]
        hero_names = {k[5:]: v for k, v in t["names"].items() if k.startswith("hero:")}
        name = (t["names"].get(a.armor) or t["names"].get("Any")
                or (hero_names.get(a.hero) if a.hero else None)
                or (" / ".join(f"{h}: {v}" for h, v in hero_names.items()) if hero_names else "")
                or f"(no in-game name in the files; dev name {a.template})")
    else:
        if not (a.slot and a.variant):
            sys.exit("give --template, or --slot and --variant (and --fixed)")
        slot = SLOT_BY_TYPE.get(a.slot, a.slot)
        variant = VARIANT_BY_WEIGHTS.get(a.variant, a.variant)
        fixed = [(k, {"stam": "Stamina", "prim": "Primary", "sec": "secondary"}[k]) for k in a.fixed.split(",")]
        name = ""

    armor_type = "Cloth" if slot in CLOTH_ONLY_SLOTS else a.armor
    lines, armor = build(tables, slot, variant, fixed, a.il, armor_type, a.temper, a.teal)
    print(f"{a.template or slot}{'  ' + name if name else ''}  il {a.il}  {variant}  temper {a.temper}  {armor_type}"
          + ("  (cloaks are Cloth for every hero)" if armor_type != a.armor else ""))
    for text, kind in lines:
        print(f"  {text}  ({kind})")
    print(f"  armor {armor}")


if __name__ == "__main__":
    main()
