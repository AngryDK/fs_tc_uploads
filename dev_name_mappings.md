```py
hero_name_mapping = {
	'Lisa': 'Aeona', 
	'Firemage': 'Ardeos', 
	'Bowguy': 'Elarion', 
	'Gunde': 'Gunde (WIP)', 
	'Warmaster': 'Helena', 
	'Mara': 'Mara', 
	'Meiko': 'Meiko', 
	'Rime': 'Rime', 
	'Mosse': 'Sylvie', 
	'Ink': 'Tariq', 
	'Vigor': 'Vigour', 
	'Sune': 'Xavian'
	}
```
```py
zone_name_mapping = {
	'FrozenKingdom': ["Cithrel's Fall", 7, 50007], 
	'DesertDunes': ['Empyrean Sands', 6, 50006], 
	'MythicForest': ['Everdawn Grove', 11, 50011], 
	'ElfMines': ['Godfall Quarry', 25, 50025], 
	'DemonicRitual': ['Heart of Tuzari', 5, 50005], 
	'VikingVillage': ['Ransack of Drakheim', 23, 50023], 
	'ShipGraveyard': ["Sailor's Abyss", 15, 50015], 
	'SilkenHollow': ['Silken Hollow', 24, 50024], 
	'NightPatrol': ['Stormwatch', 12, 50012], 
	'UrrakMarkets': ['Urrak Markets', 21, 50021], 
	'PirateRaid': ['Wraithtide Vault', 13, 50013], 
	'IceCave': ['Wyrmheart', 8, 50008]
	}
```
```py
weapon_name_mapping = {
	'AbsorbDelayedAoeDamage': "Sahril's Aegis", 
	'InstantChargedProjectileHealOrDamage': "Twilight Skybolt", 
	'InstantAoeDamageBuff': "Sahril's Wrath", 
	'CastedChainHealDamage': "Nature's Fury", 
	'InstantDamageAccumulativeDebuff': "Voidbringer's Touch",
	'CastedHealAndDamageChannel': "Zeraleth's Hunger", 
	'CastedBuffStacksHealOnDamage': "Repository of Frozen Light", 
	'CleaveDamageBuffCooldownReduction': "Fated Strike", 
	'StunDotAoeDamageSlow': "Al'zerac's Shackle", 
	'ChanneledCooldownReducer': "Chronoshift", 
	'FrontalAOEConeRepeatingStunDamage': "Earthbreaker", 
	'CastedRepetitivelyAOEDamageDebuff': "Icicles of An'zhyr",
	}
```
```py
weapon_trait_name_mapping = {
	# "CooldownRecoveryOnWeaponAbility": "",  # not in game anymore
	# "GemCooldownRecoveryOnAbilityProc": "",  # not in game anymore
	"BigBlowMitigation": "Against All Odds", 
	"GemDotHotOnCrit": "Amethyst Splinters", 
	"DeathPreventionWithImmunity": "Ancestral Intervention", 
	"WeaponCritChanceCooldownReduction": "Brave Machinations", 
	"GemSingleTargetProcOnDamageHeal": "Diamond Strike", 
	"IncomingDamageToHotAndAbsorb": "Divine Mediation", 
	"GemTargetedSpikeProc": "Emerald Judgement", 
	"FirstIncomingHitToReducedIncomingDamageBuff": "First Man Standing", 
	"StandingStillHealStacking": "Grounded Spirit", 
	"IncreasedStaminaToHealthConversion": "Heart of Stone", 
	"WeaponHealDamageIncrease": "Heroic Brand", 
	"AbilityToIncreasedMainStat": "Hidden Power", 
	"OffensiveAbilityHasteRatingStacking": "Hunter's Focus", 
	"CommitToHasteRatingAndWeaponCooldown": "Inspired Allegiance", 
	"IncomingDamageToDefenceAndDamage": "Iron Spikes", 
	"ExtraDotHotOnEffectApplicationProc": "Kindling", 
	"DamageReductionWhenHealthy": "King of the Hill", 
	"IncomingHealToStackingHealWithThreshold": "Latent Resurgence", 
	"WeaponDamageReductionPrimaryStatIncrease": "Martial Initiative", 
	"OffensiveAbilityToHighestStatBuff": "Navigator's Intuition", 
	"StandingStillStaminaExpertiseRatingIncrease": "Patient Soul", 
	"GemWhirlwind": "Ruby Storm", 
	"GemPulsatingOnAbilityTotemProc": "Sapphire Aurastone", 
	"CritsToIncreasedCritRating": "Seized Opportunity", 
	"NoDamageToDamageReduction": "Stalwart Readiness", 
	"RelicToDamageReduction": "Treasure Hunter's Delight", 
	"CritsToIncreasedPrimaryStatBuff": "Vengeful Soul", 
	"WeaponAndSpiritPoints": "Visions of Grandeur", 
	"IncreasedMainStatAndSpiritRating": "Willful Momentum"
	}
```
```py
affix_mapping = {
	# "AbilityUnlock": "",
	"AnomalousOrbs": "Anomalous Orbs",
	"BloodShardVolley": "Blood Shards",
	"Carnage": "Carnage",
	"Challenge": "Challenge",
	"ColdSnap": "Binding Ice",
	"DM_WinterGiant": "Ghorn the Avalanche",
	"DM_WinterGiantFriendly": "Ghorn the Avalanche - Friendly",
	"DM_WinterTrickster": "Krumbug the Naughty",
	"DM_WinterWitch": "Eira the White Witch",
	"DispelAndInterrupt": "Elheryn's Exile",
	"EmpoweredMinions": "Empowered Minions",
	"EnemyNewAbilities": "Vayr's Legacy",
	"LessMagicDamageTakenLessHealing": "Celestia's Retreat",
	"MalevolentSpirits": "Malevolent Spirits",
	"MeteorRain": "Meteor Rain",
	"NoDispelNoInterrupt": "Elheryn's Exile",
	"PathFinder": "Pathfinder's Guidance",
	# "ReducedHealingAndAbsorb": "",
	"Shadowlord": "Shadow Lord's Trial",
	"StoneSkin": "Stone Skin",
	"StormShield": "Storm Shield",
	"ThreatManagement": "Sahril's Madness",
	"TimerKillScore": "Asha's Dilemma",
	"Ultimatum": "Ultimatum"
	}
```
Hero Ults (FSL codes)
```py
ult_ids = {
	'Aeona': 1002613,
	'Ardeos': 1001270, # Doesn't track proper?
	'Elarion': 1002312,
	'Helena': 1002192,
	'Mara': 1002039,
	'Meiko': 1001547,
	'Rime': 1001387,
	'Sylvie': 1001439,
	'Tariq': 1001766,
	'Vigour': 1001333,
	'Xavian': 1002558
	}
```