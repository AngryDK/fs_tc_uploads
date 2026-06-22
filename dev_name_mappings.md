# Fellowship Dev Name Mappings
Sourced from `script_libs/fs_constants.py`. FSL dev names → display names + supplemental FSL IDs.

---

## Hero Name Mapping
Dev name (FSL class) → in-game display name.
```py
hero_name_mapping = {
	'Bowguy':    'Elarion',
	'Firemage':  'Ardeos',
	'Gunde':     'Gunde',
	'Ink':       'Tariq',
	'Lisa':      'Aeona',
	'Mara':      'Mara',
	'Meiko':     'Meiko',
	'Mosse':     'Sylvie',
	'Rime':      'Rime',
	'Sune':      'Xavian',
	'Vigor':     'Vigour',
	'Warmaster': 'Helena',
}
```

## Hero Roles
```py
hero_roles = {
	'Aeona':   'healer',
	'Ardeos':  'rdps',
	'Elarion': 'rdps',
	'Gunde':   'mdps',
	'Helena':  'tank',
	'Mara':    'mdps',
	'Meiko':   'tank',
	'Rime':    'rdps',
	'Sylvie':  'healer',
	'Tariq':   'mdps',
	'Vigour':  'healer',
	'Xavian':  'tank',
}
```

## Hero Resource Types
First entry is the spendable resource. Resource IDs defined in `resource_list` below.
```py
hero_resource_types = {
	'Aeona':   [1, 2, 4],
	'Ardeos':  [2, 4],
	'Elarion': [2, 4],
	'Gunde':   [2, 4],
	'Helena':  [3, 4],
	'Mara':    [2, 3, 4],
	'Meiko':   [3, 4],
	'Rime':    [2, 4, 5],
	'Sylvie':  [1, 4, 5],
	'Tariq':   [2, 4],
	'Vigour':  [1, 2, 4],
	'Xavian':  [1, 4],
}
```

## Resource List
Resource type ID → readable name. Note: Gunde's resource 2 is called "Feathers" in-game (all others call it "Primary").
```py
resource_list = {
	1: 'Mana',
	2: 'Primary',
	3: 'Toughness',
	4: 'Spirit',
	5: 'Secondary',
	7: 'Stagger',
}
```

---

## Zone Name Mapping
Dev folder name → [display name, FSL encounter id, FSL zone id, status, zone_type].
- `status`: "live" = in game now; "dead" = in files but not live
- `zone_type`: "adventure" = normal scoring key; "capstone" = capstone dungeon; "pinnacle" = pinnacle dungeon; "practice" = non-scoring; None = unverified

```py
zone_name_mapping = {
	# -- live zones (alphabetical by dev name) --
	'DesertDunes'        : ['Empyrean Sands',         6,     50006, 'live', 'adventure'],
	'DemonicRitual'      : ['The Heart of Tuzari',    5,     50005, 'live', 'capstone'],
	'ElfMines'           : ['Godfall Quarry',         25,    50025, 'live', 'adventure'],
	'ForestMeadow'       : ['Woodland Glade',         28,    50028, 'live', 'practice'],
	'FrozenKingdom'      : ["Cithrel's Fall",         7,     50007, 'live', 'capstone'],
	'IceCave'            : ['Wyrmheart',              8,     50008, 'live', 'adventure'],
	'MoorCastle'         : ['Ruins of Regath',         None,  None,  'live', 'adventure'],  # FSL IDs TBD; fill after launch logs
	'MythicForest'       : ['Everdawn Grove',         11,    50011, 'live', 'adventure'],
	'NightPatrol'        : ['Stormwatch',             12,    50012, 'live', 'adventure'],
	'PirateRaid'         : ['Wraithtide Vault',       13,    50013, 'live', 'capstone'],
	'SandTomb'           : ['Xul, The Blood Monolith', None, None,  'live', 'pinnacle'],  # FSL IDs TBD; fill after launch logs
	'ShipGraveyard'      : ["Sailor's Abyss",         15,    50015, 'live', 'adventure'],
	'SilkenHollow'       : ['Silken Hollow',          24,    50024, 'live', 'adventure'],
	'SnowPeak'           : ["Scryer's Peak",           None,  None,  'live', 'adventure'],  # FSL IDs TBD; fill after launch logs
	'UrrakMarkets'       : ['Urrak Markets',          21,    50021, 'live', 'adventure'],
	'VikingVillage'      : ['Ransack of Drakheim',    23,    50023, 'live', 'capstone'],
	# -- not live (in game files) --
	'CrystalMines'       : ['Crystal Mines',          1,     50001, 'dead', None],
	'JourneyToStronghold': ['Journey to Stronghold',  9,     50009, 'dead', None],
	'UndeadBattlefield'  : ['Undead Battlefield',     19,    50019, 'dead', None],
	'UndeadCathedral'    : ['Undead Cathedral',       20,    50020, 'dead', None],
	'VampireCastle'      : ['Vampire Castle',         22,    50022, 'dead', None],
}
```

## Zone Dev Prefix → Folder
Used to identify which zone a mob belongs to from its dev name prefix.
```py
prefix_to_zone = {
	'CM'  : 'CrystalMines',
	'DD'  : 'DesertDunes',
	'DR'  : 'DemonicRitual',
	'EM'  : 'ElfMines',
	'FK'  : 'FrozenKingdom',
	'FM'  : 'ForestMeadow',
	'IC'  : 'IceCave',
	'JS'  : 'JourneyToStronghold',
	'MC'  : 'MoorCastle',
	'MF'  : 'MythicForest',
	'NP'  : 'NightPatrol',
	'PR'  : 'PirateRaid',
	'SG'  : 'ShipGraveyard',
	'SH'  : 'SilkenHollow',
	'SP'  : 'SnowPeak',
	'BM'  : 'SandTomb',
	'UB'  : 'UndeadBattlefield',
	'UC'  : 'UndeadCathedral',
	'UM'  : 'UrrakMarkets',
	'VC'  : 'VampireCastle',
	'VV'  : 'VikingVillage',
}
```

## Zone Short Names
Folder name → short label (used in FoundInZones tracking).
```py
zone_short_names = {
	'DesertDunes'    : 'ES',
	'DemonicRitual'  : 'HOT',
	'ElfMines'       : 'GFQ',
	'ForestMeadow'   : 'FM',
	'FrozenKingdom'  : 'CF',
	'IceCave'        : 'WH',
	'MoorCastle'     : 'MC',
	'MythicForest'   : 'EG',
	'NightPatrol'    : 'SW',
	'PirateRaid'     : 'WTV',
	'SandTomb'       : 'ST',
	'ShipGraveyard'  : 'SA',
	'SilkenHollow'   : 'SH',
	'SnowPeak'       : 'SP',
	'UrrakMarkets'   : 'UM',
	'VikingVillage'  : 'RAN',
}
```

---

## Weapon Name Mapping
Dev ability class → in-game weapon display name. (Source: FSL / game files — not in fs_constants.)
```py
weapon_name_mapping = {
	'AbsorbDelayedAoeDamage':              "Sahril's Aegis",
	'CastedBuffStacksHealOnDamage':        'Repository of Frozen Light',
	'CastedChainHealDamage':               "Nature's Fury",
	'CastedHealAndDamageChannel':          "Zeraleth's Hunger",
	'CastedRepetitivelyAOEDamageDebuff':   "Icicles of An'zhyr",
	'ChanneledCooldownReducer':            'Chronoshift',
	'CleaveDamageBuffCooldownReduction':   'Fated Strike',
	'FrontalAOEConeRepeatingStunDamage':   'Earthbreaker',
	'InstantAoeDamageBuff':                "Sahril's Wrath",
	'InstantChargedProjectileHealOrDamage': 'Twilight Skybolt',
	'InstantDamageAccumulativeDebuff':     "Voidbringer's Touch",
	'StunDotAoeDamageSlow':               "Al'zerac's Shackle",
}
```

## Weapon Trait Name Mapping
Dev class → in-game trait display name.
```py
weapon_trait_name_mapping = {
	# 'CooldownRecoveryOnWeaponAbility'   : '',  # removed
	# 'GemCooldownRecoveryOnAbilityProc'  : '',  # removed
	'AbilityToIncreasedMainStat'         : 'Hidden Power',
	'BigBlowMitigation'                  : 'Against All Odds',
	'CommitToHasteRatingAndWeaponCooldown': 'Inspired Allegiance',
	'CritsToIncreasedCritRating'         : 'Seized Opportunity',
	'CritsToIncreasedPrimaryStatBuff'    : 'Vengeful Soul',
	'DamageReductionWhenHealthy'         : 'King of the Hill',
	'DeathPreventionWithImmunity'        : 'Ancestral Intervention',
	'DispelAndInterrupt'                 : "Elheryn's Exile",
	'ExtraDotHotOnEffectApplicationProc' : 'Kindling',
	'FirstIncomingHitToReducedIncomingDamageBuff': 'First Man Standing',
	'GemDotHotOnCrit'                    : 'Amethyst Splinters',
	'GemPulsatingOnAbilityTotemProc'     : 'Sapphire Aurastone',
	'GemSingleTargetProcOnDamageHeal'    : 'Diamond Strike',
	'GemTargetedSpikeProc'              : 'Emerald Judgement',
	'GemWhirlwind'                       : 'Ruby Storm',
	'IncomingDamageToDefenceAndDamage'   : 'Iron Spikes',
	'IncomingDamageToHotAndAbsorb'       : 'Divine Mediation',
	'IncomingHealToStackingHealWithThreshold': 'Latent Resurgence',
	'IncreasedMainStatAndSpiritRating'   : 'Willful Momentum',
	'IncreasedStaminaToHealthConversion' : 'Heart of Stone',
	'NoDamageToDamageReduction'          : 'Stalwart Readiness',
	'OffensiveAbilityHasteRatingStacking': "Hunter's Focus",
	'OffensiveAbilityToHighestStatBuff'  : "Navigator's Intuition",
	'RelicToDamageReduction'             : "Treasure Hunter's Delight",
	'StandingStillHealStacking'          : 'Grounded Spirit',
	'StandingStillStaminaExpertiseRatingIncrease': 'Patient Soul',
	'WeaponAndSpiritPoints'              : 'Visions of Grandeur',
	'WeaponCritChanceCooldownReduction'  : 'Brave Machinations',
	'WeaponDamageReductionPrimaryStatIncrease': 'Martial Initiative',
	'WeaponHealDamageIncrease'           : 'Heroic Brand',
}
```

---

## Affix Mapping
Dev affix class → in-game display name.
```py
affix_mapping = {
	# 'AbilityUnlock'                : '',
	'AnomalousOrbs'                  : 'Anomalous Orbs',
	'BloodShardVolley'               : 'Blood Shards',
	# 'Carnage'                      : 'Carnage',  # removed in S3
	'Challenge'                      : 'Challenge',
	'ColdSnap'                       : 'Binding Ice',
	'DM_WinterGiant'                 : 'Ghorn the Avalanche',
	'DM_WinterGiantFriendly'         : 'Ghorn the Avalanche - Friendly',
	'DM_WinterTrickster'             : 'Krumbug the Naughty',
	'DM_WinterWitch'                 : 'Eira the White Witch',
	'DispelAndInterrupt'             : "Elheryn's Exile",
	'EmpoweredMinions'               : 'Empowered Minions',
	'EnemyNewAbilities'              : "Vayr's Legacy",
	'LessMagicDamageTakenLessHealing': "Celestia's Retreat",
	'MalevolentSpirits'              : 'Malevolent Spirits',
	'MeteorRain'                     : 'Meteor Rain',
	'NoDispelNoInterrupt'            : "Elheryn's Exile",
	'PathFinder'                     : "Pathfinder's Guidance",
	# 'ReducedHealingAndAbsorb'      : '',
	'Shadowlord'                     : "Shadow Lord's Trial",
	'StoneSkin'                      : 'Stone Skin',
	'StormShield'                    : 'Storm Shield',
	'ThreatManagement'               : "Sahril's Madness",
	'TimerKillScore'                 : "Asha's Dilemma",
	'Ultimatum'                      : 'Ultimatum',
	# TODO: confirm S3 new affix dev names from launch logs
}
```

---

## Hero Ults (FSL Spell IDs)
FSL spell ID for each hero's ultimate ability.
```py
ult_ids = {
	'Aeona':   1002613,
	'Ardeos':  1001270,  # doesn't track properly in FSL
	'Elarion': 1002312,
	'Gunde':   None,     # TODO: fill after S3 launch logs
	'Helena':  1002192,
	'Mara':    1002039,
	'Meiko':   1001547,
	'Rime':    1001387,
	'Sylvie':  1001439,
	'Tariq':   1001766,
	'Vigour':  1001333,
	'Xavian':  1002558,
}
```
