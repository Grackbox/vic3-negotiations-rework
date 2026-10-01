# Negotiations: rules for every group - agreed design and implementation

Part of the developer notes; architecture, hooks, patterns and tools are in [README_NR.md](../README_NR.md).

## Negotiation difficulty (reference)
- Amenability (0-100) is computed in code; factor weights are not exposed.
- Level thresholds: `NPolitics` in `common/defines/00_defines.txt` — MIN_AMENABILITY_TENSE/NORMAL/FRIENDLY_NEGOTIATION = 25/50/75 → levels 4/2/1.
- `promise_quest_degree = amenability_level` in the `immediate` of `negotiation.1`.

## Building promises (negotiation options 5 and 6, all interest groups)
- Vanilla asks for (GDP / 4M) x cost factor x negotiation level (1 / 2 / 4) new levels - linear in GDP, hundreds of levels in the late game.
- `building_scaler` (vanilla `negotiation_values.txt`) now returns `nr_building_scaler` (`common/script_values/nr_building_promise_values.txt`): vanilla up to GDP 50M (`nr_building_linear_gdp`), above it the value at the threshold x (1 + 0.3 x log2(GDP / 50M)) (`nr_building_doubling_share`). log2 is piecewise linear per doubling (`nr_building_gdp_log2`, error < 0.09). Cost factors and the 1 / 2 / 4 level multiplier stay vanilla; option 6 (building groups) uses the same scaler.
- University (cost 400), new levels at open / pragmatic / tense: GDP 30M 12 / 24 / 48 (vanilla), 50M 20 / 40 / 80, 100M 26 / 52 / 104, 300M 36 / 71 / 142, 1B 46 / 92 / 184 (vanilla 400 / 800 / 1600), 2B 52 / 104 / 208.

### Devout: fishing wharves (feature devout_fish)
- The Devout of countries with a Christian state religion (`heritage_christian`) can ask for fishing wharves in option 5: weight 25 (Catholic, Orthodox, Oriental Orthodox) or 10 (Protestant) next to the vanilla choice (university 50 + administration 35 = 85); if vanilla picked nothing, the wharf is the only entry. Only if the country already has a fishing wharf and not in tense negotiations, like the vanilla Devout requests. Unlike vanilla, no State Religion law is required: fasting is the flock's, not the law's.
- Hooks: `nr_after_promised_building_type` right after vanilla `set_promised_building_type` in `negotiation.1`; `nr_promised_building_cost_scale` in `building_levels_to_increase_value` - the wharf (cost 200) counts as a 400-cost building, like a university; lore line `nr_devout_fish_lore` in option 5 via `nr_neg_option_5_flavor`, concept `concept_nr_lenten_fish`.
- Files: `common/scripted_effects/nr_devout_fish_effects.txt`, `common/scripted_triggers/nr_devout_fish_triggers.txt`, `common/script_values/nr_devout_fish_values.txt`, `localization/*/nr_devout_fish_l_*.yml`.

## Regular bribe (negotiation option 1, all interest groups)
- `bribed_ig_benefits` is overridden in `common/static_modifiers/00_negotiation_modifiers.txt` (copy of the vanilla file): no pop attraction, +10% political strength (vanilla: +25% attraction, +5% strength).
- Multiplier `nr_neg_level_scale` (`common/script_values/nr_negotiation_hooks_values.txt`): amenability_level 1 / 2 / 4 -> 1 / 2 / 3, i.e. +10% / +20% / +30% political strength, decaying over 10 years. Hooked in `events/iberia_events/negotiation_events.txt`, option `negotiation.1.o1`.
- The modifier name is kept: vanilla `generic_laws.2` (corruption exposed) triggers on it.

### One-time bribe (every group) and the Devout leader's vices
- Files: `common/scripted_effects/nr_bribe_effects.txt`, `events/nr_bribe_events.txt`, values in `common/script_values/nr_bribe_values.txt`, triggers in `common/scripted_triggers/nr_bribe_triggers.txt`. Hooked in `negotiation.1.o1` (`nr_bribe_pay`, `nr_bribe_exposure_roll`). No group gets the vanilla weekly `negotiation_bribes` any more.
- Payment (`nr_bribe_lump_sum`, `add_treasury`, computed directly so the tooltip shows it): the vanilla slow sum (`neg_bribe_amount` x 260.7 weeks of linear decay over 10 years) / 2.5 (`nr_bribe_lump_divisor`), i.e. about 3.9% / 7.8% / 15.6% of GDP by level 1 / 2 / 4. Capped by 10% / 20% / 30% of max credit (`credit`). Rounded to 100.
- A bribe that would cause a default is not offered (`nr_bribe_affordable`: `gold_reserves + credit - principal - payment >= 0`): option 1 is not rolled for other groups (`nr_neg_option_1_allowed`); for the Devout the roll `nr_softbribe_roll` gives charity instead (even for greedy leaders); the option `negotiation.1.o1` is hidden if the money ran out during the negotiation (`nr_neg_option_1_affordable`).
- `generic_laws.2` option c ("corruption is good") needs vanilla `negotiation_bribes`, so it is no longer shown (the money is already paid).
- Exposure: vanilla chances (10%, 20% under Protected Speech), `generic_laws.2` in 300 days. Devout only: the leader gets `nr_bribe_taken` (and `nr_bribe_exposed` if the roll hit), 330 days.
- Devout only: 310 days after the bribe, hidden `nr_bribe.1`: every character of the country with `nr_bribe_taken` and without `nr_bribe_exposed` has a 20% chance of a trait (`nr_bribe_add_vice_trait`): Grifter 25, Expensive Tastes 25, Alcoholic 20, Opium Addiction 15, Syphilis 15 (only traits he does not have). Grifter and Expensive Tastes make the leader always take a regular bribe afterwards (`nr_bribe_leader_loves`). Tooltip `nr_bribe_vice_risk_tt`.
- AI (option `negotiation.1.o1`, every group; the vanilla income checks are switched off by `nr_neg_option_1_vanilla_ai = no`): +35 if the payment fits in gold reserves (`nr_bribe_ai_good`); +15 if partly on credit but at least 50% of the credit stays free (`nr_bribe_ai_fair`); -50 if on credit while in deficit or with less than 25% of the credit left (`nr_bribe_ai_bad`).
- Refund: the paid amount is stored on the bribed group (`nr_bribe_paid`, 330 days), so two bribed groups do not overwrite each other. The money is assumed to be spent evenly over 2 years (`nr_bribe_spend_days` = 730), exposure comes after 300 days, so ~59% is unspent (`nr_bribe_refund`, group scope). Returned in `generic_laws.2` option b ("deal with it", overridden in `events/law_events/law_events_01.txt`, copy of the vanilla file) for the exposed group (`scope:corrupt_ig_scope`). Option a (ignore) returns nothing.

## Feature ruler_pressure - the ruler presses the group (extra negotiation option, all interest groups)
Agreed design. An extra button in `negotiation.1` (not part of the random three options), shown when available. The AI never takes it.
- Available: the ruler is not against the law being enacted (`ruler` `law_stance` >= neutral) and the country is authoritarian or a monarchy. Ruler type:
  - monarch: `law_monarchy` (and variants), `law_chiefdom` - whatever the distribution of power;
  - `law_social_monarchy` is a non-factor: the ruler type comes from the distribution of power, as in a republic;
  - theocrat: `law_theocracy` - whatever the distribution of power;
  - otherwise by distribution of power: autocrat - `law_autocracy` (and variants), `law_single_party_state`; oligarchs - `law_oligarchy` (and variants), `law_elder_council`; technocrats - `law_technocracy`. Other distributions (voting laws, anarchy): no option.
- Cost: 400 authority for 5 years (`country_authority_add`, cost slot, see "Authority cost slots"); needs a free cost slot only - authority may go negative, as in vanilla.
- A group cannot be pressed again while its pressure lasts: 5 years (country variable list `nr_ruler_pressure_pressed`, the group as target, 5 years).
- Shown when the ruler type and the stance allow it (`nr_ruler_pressure_available`); greyed out with the reason (option `trigger` = `_available` and not `_blocked`; `show_as_unavailable` = `_available` and `_blocked` - in vanilla `show_as_unavailable` only decides whether an option whose `trigger` fails is still shown greyed, it blocks nothing by itself) when this group is on cooldown or no cost slot is free. The election promise does the same (`nr_election_promise_available` / `_blocked`: already promised to this group, no slot). No free-authority requirement: authority may go negative.
- A monarch or theocrat with elections (`country_has_voting_franchise`, trigger `nr_ruler_pressure_constitutional`) meddles in the affairs of parliament: every penalty of the tables below (group cells, own-group cells, Armed Forces approval/coup penalties at loyalty below 75, infamy) x1.5 (`nr_ruler_pressure_scale` as the modifier multiplier), plus legitimacy -5 for 5 years (`nr_ruler_pressure_constitutional`). Absolute monarchies and theocracies without a franchise use the tables as they are. Bonuses are never scaled: each mixed cell is split into `<modifier>` (penalties, scaled) and `<modifier>_bonus` (bonuses: higher approval, legitimacy, prestige, loyalists, throughput, conversion, education, growing group strength; lower radicals, tax waste, military goods cost). Also not scaled: the loyal-army bonuses, the ruler's popularity -25.
- Result: the group supports the law like after any successful negotiation (`finish_negotiation`, `improve_law_stance`), plus the effects below for 5 years (infamy is one-time). Every effect is shown in the option tooltip; a lore line per ruler type.

Armed Forces (any ruler type), by the loyalty of their leader (0-100, vanilla thresholds 25/50/75):

| Loyalty | Effect |
|---|---|
| 75+ ("reliable") | order carried out, no penalty; monarch: morale recovery +5% (`unit_morale_recovery_mult`); autocrat: coup resistance +0.10 |
| 50-75 | Armed Forces approval -2 |
| below 50 | Armed Forces approval -3, coup resistance -0.10, leader loyalty -15 (`character_loyalty_add` on the leader) |

Other groups (approval / strength through `interest_group_ig_<group>_approval_add` / `_pol_str_mult`; radicals and loyalists are `state_radicals_from_political_movements_mult` / `state_loyalists_from_political_movements_mult`):

| Group | Monarch | Theocrat | Autocrat | Oligarchs | Technocrats |
|---|---|---|---|---|---|
| Devout | approval -2, legitimacy -5 | conversion +10% | approval -3, legitimacy -5 | approval -3 | Devout strength -5%, education access +0.02 |
| Landowners | approval -3, agriculture throughput -5% | approval -2 | approval -3, agriculture -5% | approval -2 | approval -3, agriculture +5% |
| Industrialists | approval -3, manufacturing throughput -5% | approval -3, manufacturing -5% | approval -3, military goods cost -10% | approval -1, manufacturing +5%, Industrialists strength +10% | approval -2, manufacturing +5% |
| Petty Bourgeoisie | approval -2, tax waste +5% | approval -2, tax waste +5% | approval -2, government buildings throughput -5% | approval -3 | approval -2, government buildings -5% |
| Intelligentsia | infamy +10, radicals +10% | infamy +10, radicals +15%, research -10% | infamy +5, radicals +10%, research -5% | infamy +5, radicals +10% | approval -3 |
| Trade Unions | radicals +10% | radicals +10% | radicals +10%, approval -3 | radicals +15%, throughput of all buildings -3% | approval -2, throughput -2% |
| Rural Folk | no penalty, loyalists +5% | no penalty | approval -2 | approval -3, agriculture -3% | approval -3 |

The ruler presses their own group (`ruler.interest_group` = the group) - replaces the cell above: always the group's strength -10% and the ruler's popularity -25 (`character_popularity_add`), plus:

| Own group | Monarch | Theocrat | Autocrat | Oligarchs | Technocrats |
|---|---|---|---|---|---|
| Armed Forces | prestige -5%, coup resistance -0.10 | legitimacy -5, morale recovery -5% | coup resistance -0.15 | legitimacy -5, coup resistance -0.10 | legitimacy -5, military research -10% |
| Devout | legitimacy -10, conversion -5% | legitimacy -10, conversion -10% | legitimacy -5, Devout approval -3 | legitimacy -5, Devout approval -2 | legitimacy -5, education access -0.02 |
| Landowners | prestige -10% | legitimacy -5, agriculture -3% | legitimacy -10, agriculture -5% | Landowners approval -3, agriculture -3% | legitimacy -10, agriculture +5% |
| Industrialists | prestige -5%, legitimacy -5 | legitimacy -5, manufacturing -3% | legitimacy -10, military goods cost -10% | legitimacy -10, manufacturing -5% | Industrialists approval -3, manufacturing +5% |
| Petty Bourgeoisie | legitimacy -5, tax waste +5% | legitimacy -5, tax waste +3% | legitimacy -10, tax waste +5% | legitimacy -5, government buildings -5% | legitimacy -5, government buildings -5% |
| Intelligentsia | prestige -10%, radicals +5% | legitimacy -5, research -10% | legitimacy -10, radicals +5% | research -5%, radicals +5% | legitimacy -10, government buildings -5% |
| Trade Unions | legitimacy -5, loyalists -5% | legitimacy -5, radicals +5% | legitimacy -10, radicals +10% | legitimacy -5, throughput -3% | legitimacy -5, throughput -2% |
| Rural Folk | prestige -5%, loyalists -5% | legitimacy -5, conversion -5% | legitimacy -10, agriculture -3% | legitimacy -5, agriculture -3% | legitimacy -10, agriculture +3% |

Own Armed Forces with a leader of loyalty 75+: only strength -10% and popularity -25; an autocrat from the Armed Forces gets instead legitimacy +10 and no penalty at all (a general's order carried out by his own army). Positive outcomes are allowed where they fit (user: "some combinations may give positive results").

Tested in game: pressure on the Intelligentsia and the Armed Forces, x1.5 with legitimacy -5 for a constitutional monarch, the 5-year limit per group, no election option without elections (Russia).

## Feature election_promise - promise to back the group's party at the next election (extra negotiation option)
Agreed design. An extra button in `negotiation.1`, a promise like the vanilla ones (`promise_quest`, `promise_quest_type` 102, journal entry `je_nr_election_promise`). The AI never takes it.
- Available: the country has elections (vanilla `country_has_voting_franchise`: any voting power - Portugal votes under Oligarchy thanks to its charter modifier; any form of government, so a monarchy or theocracy with a franchise may get both options), not `law_single_party_state`, no Tradition of Free Elections (`modifier:country_forbid_electoral_fraud_bool = no`), the ruler is not against the law, this group holds no election promise yet and a free cost slot (authority may go negative).
- Promises can be given to any number of groups; one journal entry per group (`je_nr_election_promise_<group>`), state in group variables (`nr_election_promise`, `_campaign`, `_kept`, `_broken`, `_void`). The party is not remembered at the negotiation: it is the group's party at the election (groups may change party meanwhile). Backing one party keeps the promises of every promised group that is in it.
- Cost: 50 authority for 5 years. Result: the group supports the law (vanilla `promise_quest`).
- Kept or broken at the next election campaign that starts after the promise, in the vanilla rigging event (`caciquismo.1` / `caciquismo.2`, fired at the start of every campaign while fraud is possible: chosen party +150% momentum, all others -50%):
  - kept: the player chose the party the group is a member of -> vanilla `promise_quest_completed`;
  - broken: another party, no rigging, the event expired, the promise abandoned (vanilla button), or the Tradition of Free Elections appeared before the election -> vanilla `promise_quest_failed`;
  - a promised group's party is not among the parties listed in the event: an extra option "Back [party], as promised" per such party (vanilla effect: +150% / -50%, `add_caciquismo_effect`);
  - withdrawn without penalty: the group is in no party when the campaign starts, or the campaign ended without the rigging event (vanilla conditions, e.g. fewer than two parties with members).
  - notifications (toasts, `common/messages/nr_messages.txt`): kept - the engine's `journal_entry_completed` toast (fires for every completed journal entry); broken - vanilla `neg_failed_quest_toast` (from `promise_quest_failed`); the group was in no party - `nr_election_promise_void_toast` (neutral outcome: toast, neutral color, sound `diplomatic_treaties_revoke_neutral`).
- Tested in game: a kept promise (vanilla completion toast), a broken promise, a group without a party (`nr_election_promise_void_toast`). Not yet: the extra option for an unlisted party.
- Needs hooks in a copy of vanilla `events/iberia_events/ip4_election_rigging.txt` (each option reports the chosen party). Brazil's `coffee_with_milk.7` is not touched.

## Authority cost slots (shared)
Timed authority costs of our options: static modifiers `nr_authority_cost_1` - `_10` (`country_authority_add` = -1, applied with `multiplier` = cost, 5 years). `nr_authority_cost_add = { COST = ... }` takes the first free slot; an option with an authority cost is offered only if a slot is free.
