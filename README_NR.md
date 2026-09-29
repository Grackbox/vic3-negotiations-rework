# Negotiations Rework — developer notes

Mod prefix: `nr_` (keys, files). Edits inside copied vanilla files are marked `NR`.

## Architecture
Copied vanilla files contain only hooks; all mod logic lives in the mod's own files.

| Where (vanilla) | What it calls |
|---|---|
| `negotiation.1` → `immediate`, after `set_neg_options` | `nr_negotiation_after_options` — overrides precomputed option values, rolls bribe vs soft bribe |
| `negotiation.1.o9` | `nr_neg_option_9_is_custom` → `nr_neg_option_9_custom`, otherwise vanilla |
| `neg_option_9_trigger` | `nr_has_custom_sol_promise = no` |
| `set_neg_options`, option 1 (bribe) in all three lists | `nr_neg_option_1_allowed` (condition) and `nr_neg_option_1_modifier` (weight) |
| `set_neg_options`, option 2 (bureaucracy) in all three lists | `nr_neg_option_2_allowed` (condition) and `nr_neg_option_2_modifier` (weight) |
| `negotiation.1.o1` | `nr_neg_option_1_is_custom = no`, `nr_neg_option_1_affordable`; AI: `nr_neg_option_1_vanilla_ai` gates the vanilla income checks, `nr_neg_option_1_ai_good` / `_fair` / `_bad` (+35 / +15 / -50) for groups with their own bribe. Otherwise option `negotiation.1.nr_o1_soft` → `nr_neg_option_1_custom` |
| `negotiation.1.o2` | `nr_neg_option_2_is_custom = no`; otherwise option `negotiation.1.nr_o2_devout` (`nr_neg_option_2_allowed`, AI `nr_neg_option_2_ai_good` / `_bad`) → `nr_neg_option_2_custom` |
| `negotiation.1.o1`, `bribed_ig_benefits` | multiplier `nr_neg_level_scale` (level 1 / 2 / 4 → 1 / 2 / 3); the same value scales soft bribe patronage and church officials |

No interest group is named in the copied vanilla files; every group-specific check sits behind a hook. Routing by interest group: `common/scripted_effects/nr_negotiation_hooks.txt`, `common/scripted_triggers/nr_negotiation_hooks.txt`, `common/script_values/nr_negotiation_hooks_values.txt`.

## Overridden vanilla files (after every game patch: take the new vanilla file and re-add the hooks)
- `events/iberia_events/negotiation_events.txt`
- `common/scripted_triggers/ip4_negotiation_triggers.txt`
- `common/script_values/negotiation_values.txt` (hook in `building_scaler`)
- `common/scripted_effects/04_neg_event_options_scripted_effects.txt`

## Naming
- Feature: `<group>_<feature>`, e.g. `devout_sol`, `devout_charity`, `devout_softbribe`.
- Files: `nr_<group>_<feature>_{je,bars,effects,values,modifiers,triggers,buttons,events}.txt`, localization `nr_<group>_<feature>_l_<language>.yml`.
- Keys, effects, triggers, values, modifiers, variables: prefix `nr_<group>_<feature>_`. Country variables only with that prefix so features never collide.
- Journal entries: `je_nr_<group>_<feature>`; events: namespace `nr_<group>_<feature>`.
- Shared hook code and texts: `nr_negotiation_hooks*`.

## File map
| Feature | Files |
|---|---|
| hooks | `common/scripted_effects/nr_negotiation_hooks.txt`, `common/scripted_triggers/nr_negotiation_hooks.txt`, `common/script_values/nr_negotiation_hooks_values.txt`, `common/customizable_localization/nr_negotiation_custom_loc.txt`, `localization/*/nr_negotiation_hooks_l_*.yml` |
| devout_sol | `common/journal_entries/nr_devout_sol_je.txt`, `common/scripted_progress_bars/nr_devout_sol_bars.txt`, `common/scripted_effects/nr_devout_sol_effects.txt`, `common/script_values/nr_devout_sol_values.txt`, `localization/*/nr_devout_sol_l_*.yml` |
| devout_charity | `common/scripted_buttons/nr_devout_charity_buttons.txt`, `common/scripted_effects/nr_devout_charity_effects.txt`, `common/script_values/nr_devout_charity_values.txt`, `common/static_modifiers/nr_devout_charity_modifiers.txt`, `localization/*/nr_devout_charity_l_*.yml` |
| amendment framework | `common/scripted_effects/nr_amendment_framework.txt`, `common/scripted_triggers/nr_amendment_framework.txt`, `common/on_actions/nr_on_actions.txt` |
| petition framework | `common/scripted_effects/nr_petition_framework.txt`, `common/scripted_triggers/nr_petition_framework.txt` (list of Devout petitions for `improve_stance`) |
| devout_censorship | `events/nr_devout_censorship_events.txt`, `common/journal_entries/nr_devout_censorship_je.txt`, `common/scripted_triggers/nr_devout_censorship_triggers.txt`, `common/static_modifiers/nr_devout_censorship_modifiers.txt`, `localization/*/nr_devout_censorship_l_*.yml` |
| devout_synod | `common/amendments/nr_devout_synod_amendments.txt`, `events/nr_devout_synod_events.txt`, `common/scripted_effects/nr_devout_synod_effects.txt`, `common/scripted_triggers/nr_devout_synod_triggers.txt`, `common/static_modifiers/nr_devout_synod_modifiers.txt`, `localization/*/nr_devout_synod_l_*.yml` |
| devout_church_tax | `common/amendments/nr_devout_church_tax_amendments.txt`, `events/nr_devout_church_tax_events.txt`, `common/scripted_effects/nr_devout_church_tax_effects.txt`, `common/scripted_triggers/nr_devout_church_tax_triggers.txt`, `common/static_modifiers/nr_devout_church_tax_modifiers.txt`, `localization/*/nr_devout_church_tax_l_*.yml` |
| devout_sunday | `common/amendments/nr_devout_sunday_amendments.txt`, `events/nr_devout_sunday_events.txt`, `common/journal_entries/nr_devout_sunday_je.txt`, `common/scripted_effects/nr_devout_sunday_effects.txt`, `common/scripted_triggers/nr_devout_sunday_triggers.txt`, `common/static_modifiers/nr_devout_sunday_modifiers.txt`, `localization/*/nr_devout_sunday_l_*.yml`, concept `concept_nr_sunday_rest` |
| devout_census | `common/amendments/nr_devout_census_amendments.txt`, `events/nr_devout_census_events.txt`, `common/journal_entries/nr_devout_census_je.txt`, `common/scripted_effects/nr_devout_census_effects.txt`, `common/scripted_triggers/nr_devout_census_triggers.txt`, `common/static_modifiers/nr_devout_census_modifiers.txt`, `localization/*/nr_devout_census_l_*.yml` |
| devout_police | `common/amendments/nr_devout_police_amendments.txt`, `events/nr_devout_police_events.txt`, `common/journal_entries/nr_devout_police_je.txt`, `common/scripted_effects/nr_devout_police_effects.txt`, `common/scripted_triggers/nr_devout_police_triggers.txt`, `common/static_modifiers/nr_devout_police_modifiers.txt`, `localization/*/nr_devout_police_l_*.yml`, concepts `concept_nr_parish_constables`, `concept_nr_prison_chaplaincy`, `concept_nr_gendarmerie_chaplains` |
| devout_slavery | `common/amendments/nr_devout_slavery_amendments.txt`, `events/nr_devout_slavery_events.txt`, `common/journal_entries/nr_devout_slavery_je.txt`, `common/scripted_effects/nr_devout_slavery_effects.txt`, `common/scripted_triggers/nr_devout_slavery_triggers.txt`, `common/static_modifiers/nr_devout_slavery_modifiers.txt`, `localization/*/nr_devout_slavery_l_*.yml`, concept `concept_nr_fellow_believers`; hooks in `nr_on_actions.txt` (`on_law_activated`, `on_yearly_pulse_country`) |
| campaign slots | `common/scripted_effects/nr_campaign_slots.txt`, `common/scripted_triggers/nr_campaign_slots.txt` |
| devout_schools | `events/nr_devout_schools_events.txt`, `common/journal_entries/nr_devout_schools_je.txt`, `common/scripted_triggers/nr_devout_schools_triggers.txt`, `common/static_modifiers/nr_devout_schools_modifiers.txt`, `localization/*/nr_devout_schools_l_*.yml` |
| devout_sisters | `common/amendments/nr_devout_sisters_amendments.txt`, `events/nr_devout_sisters_events.txt`, `common/journal_entries/nr_devout_sisters_je.txt`, `common/scripted_triggers/nr_devout_sisters_triggers.txt`, `common/static_modifiers/nr_devout_sisters_modifiers.txt`, `localization/*/nr_devout_sisters_l_*.yml` |
| devout_chaplains | `common/amendments/nr_devout_chaplains_amendments.txt`, `events/nr_devout_chaplains_events.txt`, `common/scripted_triggers/nr_devout_chaplains_triggers.txt`, `common/static_modifiers/nr_devout_chaplains_modifiers.txt`, `localization/*/nr_devout_chaplains_l_*.yml` |
| devout_softbribe | `events/nr_devout_softbribe_events.txt`, `common/game_concepts/nr_game_concepts.txt`, `common/scripted_effects/nr_devout_softbribe_effects.txt`, `common/scripted_triggers/nr_devout_softbribe_triggers.txt`, `common/script_values/nr_devout_softbribe_values.txt`, `common/static_modifiers/nr_devout_softbribe_modifiers.txt`, `localization/*/nr_devout_softbribe_l_*.yml` |

## promise_quest_type registry
Vanilla: 1 army, 2 law, 3 buildings, 4 taxes, 5 SoL. Ours start at 101.

| Type | Task |
|---|---|
| 101 | `devout_sol` — Devout, SoL with progress bar |

## Feature devout_sol — "Commitment: The Flock's Welfare"
- One journal entry `je_nr_devout_sol`, one bar `nr_devout_sol_bar` from 0 to 36 (`nr_devout_sol_bar_max`, keep in sync with `max_value`).
- Start point by negotiation level: 24 / 12 / 6 (`nr_devout_sol_bar_start`), set by `nr_devout_sol_set_bar_start` right after creation; fallback on the first monthly pulse (flag `nr_devout_sol_bar_set`).
- Monthly progress: +1 at SoL >= target; +0.5 at SoL >= target - `nr_devout_sol_near_margin` (0.25); `nr_devout_sol_drain` (-0.5 per full 0.5 below the SoL at promise time, max -2); otherwise 0 (explanation line).
- Target: `nr_devout_sol_target_value` = current SoL + clamp(10% of SoL, 1, 2), x1.5 in tense negotiations, rounded to the nearest 0.2.
- Complete: bar full. Fail: bar empty, abandoned, or timeout (7.5 years, +2.5 in tense negotiations, +3 after "Announce Delay").
- Penalty: `nr_devout_sol_failure_degree` — vanilla scheme, progress measured from the start point (below start = full penalty).

### Feature devout_charity — charity campaign (buttons in je_nr_devout_sol)
- Lasts 1 year (`nr_devout_charity_duration`): +5% food security, +10% welfare payments, +20% conversion, country-wide.
- Cost: `country_expenses_add` x `nr_devout_charity_cost` (~0.015% of GDP per week, fixed at launch).
- Ending early: -2 Devout approval for 2 years (`nr_devout_charity_cancel_penalty_time`). Next campaign only after a 1-year rest (`nr_devout_charity_rest`) from its end.
- Ends together with the commitment; the rest period is kept.

### Feature devout_softbribe — funds for the church's needs (negotiation option 1)
- Rolled once at the start of the negotiation (`nr_devout_softbribe_roll`): bribe unaffordable (would cause a default) → always charity; leader with Honorable, Pious, Cautious or Reserved → always charity; with Grifter, Expensive Tastes or Hedonist → always a regular bribe; otherwise 60% charity / 40% bribe. Flag `nr_soft_bribe` on the IG.
- Chance of option 1 (base weight 10) by Devout leader (`nr_devout_softbribe_leader_weight`): Grifter/Expensive Tastes/Hedonist +10, Ambitious +10, Charismatic +10, Arrogant +5, prominence 50+ +10, Reserved -5, Cautious -5 (total never below 0). Not guaranteed, like vanilla.
- Negotiation option "Allocate funds for the church's needs." (`nr_devout_softbribe_start`): expenses `nr_devout_softbribe_expenses_<slot>` (one modifier per campaign slot) = vanilla bribe amount (`neg_bribe_amount`); +10% conversion (`nr_devout_softbribe_base`); Devout get `nr_devout_softbribe_patronage` (+35% attraction, +5% political strength x `nr_neg_level_scale` = 1 / 2 / 3 by level, i.e. 5/10/15%; the regular bribe gives no attraction and +10/20/30% strength, see "Regular bribe"); law stance improves. Everything lasts 10 years and decays.
- 7 days later event `nr_devout_softbribe.1` picks the campaign form; all forms last 10 years and decay:

| Form | Effects | Cost | Shown |
|---|---|---|---|
| Church Propaganda | base effects only | x1 | always (default) |
| Asceticism | lower-strata expected SoL -1, +10% food security, -10% birth rate, -10% peasant consumption | x0.5 | 2 random of these 4 |
| Enlightening the Lost | +30% conversion, +15% peasant education access, +0.0005 literacy growth; after 10 years popup `nr_devout_schools.2` | x1.5 | |
| Sisters of Mercy | -5% mortality, -25% disease outbreak impact, -15% battle casualties (`battle_casualties_mult`; amendment gives -10%); after 10 years popup `nr_devout_sisters.2` | x1.25 | |
| Shelters for Newcomers | +20% assimilation, +10% migration pull | x1.5 | |
| Army Chaplains | -15% Armed Forces attraction, +15% Devout attraction, +15% morale recovery, -10% morale loss, -10% training rate; after 10 years popup `nr_devout_chaplains.2` offers the Chaplains amendment | x1 | Professional Army law and no chaplains yet (`nr_devout_chaplains_present`) |
| Let the Parishes Pay | +5% food security, -5 acceptance of other religions, +10% clergy political strength; legitimacy -2.5 x level (max -10, decays over 10 years); Devout approval -2.5 x level (max -10) for 2 years | x0.25 | budget deficit |
| Colonial Missions | yearly: 3% of the not-yet-converted pops of every colonial subject state converts to the overlord's religion, for 10 years (hidden event `nr_devout_softbribe.2`); colonies whose state religion differs get +0.1 liberty desire (decays over 10 years) | x1.25 | colonies or chartered companies with pops of another religion |

- AI weights: Propaganda 10; Asceticism 10, +20 if average SoL < 10, +10 in deficit; Enlightenment 0, +25 with discriminated religious minorities, -15 in deficit; Sisters 10, +30 during a disease outbreak, -5 in deficit; Shelters 0, +15 with no migration controls, +10 with unaccepted pops, -15 in deficit; Chaplains 10; Parishes 20.
- Every form has a lore line (`nr_devout_softbribe_lore_*`, `#lore` style) linking to historical concepts in `common/game_concepts/nr_game_concepts.txt`: `concept_nr_chaplains`, `concept_nr_sisters_of_mercy`, `concept_nr_church_charity`, `concept_nr_parish_education`, `concept_nr_missions`.
- `convert_population` converts that share of the pops that do not yet follow the target religion, so conversion slows down as it succeeds.
- Notes: no generic goods consumption or lower-strata education modifier exists (peasant-only versions used); no per-profession IG attraction exists (Armed Forces attraction is the proxy for soldiers/officers).
- While the form event is pending (flag `nr_devout_softbribe_pending`, 14 days), Devout option 1 is not rolled, so two soft bribes cannot overwrite each other's data.
- Campaign limit (at the moment option 1 is rolled, `nr_neg_option_1_allowed`): the Devout run at most 1 / 2 / 3 soft bribe campaigns at once by clout (<10% / 10-20% / 20%+), see "Pattern: campaign slots". When the limit is reached, option 1 is still rolled if a regular bribe is possible (affordable, leader does not refuse bribes), and the roll then always gives the regular bribe. A form already running in another campaign is not offered again.
- Money spent through `country_expenses_add` leaves the economy; nobody receives it (same as vanilla bribes).

## Pattern: IG amendment pair (reusable)
An IG-themed amendment reaches a law in two ways:
1. **Enactment event** in the vanilla `on_law_checkpoint_debate` random pool (like vanilla `education_laws.2`, Prussian Education). Added in `common/on_actions/nr_on_actions.txt` - on_action data merges across files, no vanilla override. One non-default option calls `nr_amendment_add_to_enacting_law = { AMENDMENT = ... IG = ... }`.
2. **After the IG's soft-bribe campaign**: the campaign option schedules a popup (`trigger_event days = 3650`) that offers `nr_amendment_add_to_active_law = { AMENDMENT = ... LAW = ... IG = ... }` (default: decline). Vanilla attaches amendments to active laws the same way (`active_law:<group> = { add_amendment }`).
- Guard: `nr_amendment_is_present = { AMENDMENT = ... }` (active on any law, or on the law being enacted).
- New instance checklist: amendment in `common/amendments/nr_<group>_<topic>_amendments.txt`; events `nr_<group>_<topic>.1` (enactment, 3 options) and `.2` (post-campaign); pool entry in `nr_on_actions.txt`; schedule `.2` from the campaign form; localization `nr_<group>_<topic>_l_*.yml`.

## Pattern: IG petition (reusable)
A post-campaign offer can open a 4-year journal entry asking for a law (schools, sisters).
- Helpers in `common/scripted_effects/nr_petition_framework.txt`, parameters `PETITION` (key prefix) and `LAW`: `nr_petition_boost` (at the start of the enactment via `nr_devout_petition_boost_all` from `nr_on_law_enactment_started`, plus JE `immediate` and monthly pulse as a fallback: +enactment speed once per enactment attempt; every new petition must be added to `nr_devout_petition_boost_all` and `nr_devout_petition_for_enacting_law`), `nr_petition_end` (`on_complete`), `nr_petition_timeout` (`on_timeout`: approval penalty on `scope:ig`).
- New instance checklist: journal entry `je_<PETITION>` saving the group as `scope:ig`; static modifiers `<PETITION>_speed` (enactment speed) and `<PETITION>_ignored` (approval); availability trigger `nr_<group>_<topic>_petition_available`.

## Pattern: campaign slots
A group can run several 10-year campaigns of one kind at once, limited by its clout: 20%+ -> 3, 10-20% -> 2, below 10% -> 1.
- `nr_campaign_slot_free = { KEY }` (trigger, `common/scripted_triggers/nr_campaign_slots.txt`) checks the limit when the negotiation option is rolled; `nr_campaign_take_slot = { KEY }` (effect, `common/scripted_effects/nr_campaign_slots.txt`) takes the first free slot: country variable `<KEY>_slot_1..3` for `long_modifier_time`, and `<KEY>_current_slot` until the form event is done.
- Everything that must not be overwritten by the next campaign is a per-slot modifier (`<modifier>_1..3`), chosen by `<KEY>_current_slot`. Form modifiers stay single: a running form is simply not offered again.
- Used by `nr_devout_softbribe` (expenses) and `nr_devout_officials` (bureaucracy penalty), each with its own limit.

## Pattern: random forms in a choice event
Soft bribe and church officials offer a default form plus 2 random ones. Each feature has `nr_<feature>_offer_random_form` (one `random_list` that sets `nr_<feature>_offer_<form>`; called twice), `nr_<feature>_cleanup` (in the event's `after`), and per-form helpers: `nr_devout_softbribe_add_form = { FORM }` + `nr_devout_softbribe_set_cost = { FACTOR }`; `nr_devout_officials_choose_form = { FORM FACTOR }` with availability `nr_devout_officials_<form>_available` checked through `nr_devout_officials_can_offer = { FORM }`.

## Feature devout_chaplains - Army Chaplains amendment
- `amendment_nr_devout_chaplains` (parent `law_state_religion`, allowed on `law_professional_army`): +10% morale recovery, -5% morale loss, +10% Devout attraction, -10% Armed Forces attraction, -5% training rate. Sponsor: Devout.
- `nr_devout_chaplains.1` (debate checkpoint while enacting Professional Army; not if chaplains already present - amendment or running campaign; cooldown 5 years):
  - a (default) "The army serves the regulations, not the altar": +15% enactment speed; Devout -2 approval for 5 years.
  - b "A chaplain in every regiment": attaches the amendment to the law being enacted; -15% enactment speed.
  - c "Let the officers' assembly decide": Armed Forces +2 approval, Devout -2 approval, 5 years.
- `nr_devout_chaplains.2` (10 years after the Army Chaplains campaign form, if Professional Army is active and the amendment is absent): a "Write the chaplains into the army law" / b (default) "That is enough".

## Feature devout_sisters - Sisters of Mercy: amendment and petition (post-campaign only)
- `amendment_nr_devout_sisters` (parent `law_charitable_health_system`, allowed on `law_public_health_insurance`): +2% birth rate (`state_birth_rate_mult`; no infant mortality modifier exists), +10% Devout political strength (`interest_group_ig_devout_pol_str_mult`, same as vanilla Charity Hospitals), +10% health system institution bureaucracy cost, +5% influence (`country_influence_mult`), -10% battle casualties (`battle_casualties_mult`), +100 authority cost (`country_authority_cost_add`, vanilla level-2 political concession price). No radicals modifiers on purpose. Sponsor: Devout.
- Deliberately not in the enactment pool: the amendment only appears after the Sisters of Mercy campaign form.
- `nr_devout_sisters.2`, 10 years after that form:
  - a "Send the sisters to the state hospitals" (Public Health Insurance active, amendment absent): attaches the amendment to the active law.
  - b "Hear the petition for charity hospitals" (`nr_devout_sisters_petition_available`: `medical_degrees` researched, no Charity Hospitals law yet, no petition running): journal entry `je_nr_devout_sisters_petition`, 4 years; enacting Charity Hospitals gets +25% speed (`nr_devout_sisters_petition_boost`, once per enactment attempt); timeout without the law: Devout -2 approval for 5 years. Same mechanics as the schools petition.
  - d (default) "The hospitals are already in church hands" (`nr_devout_sisters_church_runs_hospitals`): Devout +2 approval for 5 years.
  - c (default otherwise) "Thank them and see them off": Devout -1 approval for 5 years; shown only while something was on offer (`nr_devout_sisters_offer_available`: petition or amendment possible).
  - e (default) "Close": neutral, no penalty; shown when nothing is on offer and the church does not run the hospitals.

## Feature devout_schools - offer after Enlightening the Lost
- `nr_devout_schools.2`, 10 years after the Enlightening the Lost form (`.1` reserved for a possible enactment event):
  - a "Hear the petition for religious schools" (`nr_devout_schools_petition_available`: `rationalism` researched, no Religious Schools, none of the laws that disallow it - Total Separation, State Atheism, Serfdom - and no petition running): journal entry `je_nr_devout_schools_petition`, 4 years; enacting Religious Schools gets +25% speed (`nr_devout_schools_petition_boost`, once per enactment attempt); timeout without the law: Devout -2 approval for 5 years.
  - b "Entrust the public schools to the church" (Public Schools active, amendment absent): vanilla `amendment_church_organised_schools` on the active law, sponsor Devout.
  - c (default) "No, thank you": Devout -1 approval for 5 years; shown only while something was on offer (`nr_devout_schools_offer_available`: petition or amendment possible).
  - e (default) "Close": neutral, no penalty; shown when nothing is on offer and the church runs no schools.
  - d (default, replaces c) "The schools are already in good hands" - if Religious Schools or Church-Organized Schools are already in place (`nr_devout_schools_church_runs_schools`): Devout +2 approval for 5 years.

## Tools
- `python tools/check_mod.py` - static checks, no game needed: braces and indentation, every `nr_` symbol defined and used, names built from parameters (`nr_devout_officials_$FORM$` etc.) exist for every value passed, localization BOM / EN-RU parity / duplicates / missing keys. `--fix-indent` rewrites indentation. Runs on GitHub on every push (`.github/workflows/check.yml`).
- `pwsh tools/deploy.ps1` - mirrors the mod into `Documents/Paradox Interactive/Victoria 3/mod/negotiations_rework` for testing (without `.git`, `.github`, `tools`).
- Engine documentation (effects, triggers, modifiers, on_actions) is dumped by the game into `Documents/Paradox Interactive/Victoria 3/docs/*.log`.

## Debug (console)
`events/nr_debug_events.txt`, localization `nr_debug_l_*.yml`. Never fired by the game.
- `event nr_debug.1` - fires every enactment event `.1` at once; only those matching the law being enacted appear (their 5-year cooldown still applies).
- `event nr_debug.2` / `event nr_debug.3` - menus of the post-campaign follow-ups `.2` (schools, sisters, chaplains, censorship, synod / church tax, Sunday Rest, Clerical Census, police, slavery). The censorship option also sets the campaign mark `nr_devout_censorship_campaign`. Each follow-up still checks its own trigger.
- `event nr_debug.4` - Devout regular bribe without a negotiation: pay it exactly as option `negotiation.1.o1` (payment, `bribed_ig_benefits`, exposure roll, vice check in 310 days), give the Devout leader a vice now (100%), or expose it now (`generic_laws.2`, needs a law being enacted).
- New follow-ups and enactment events should be added to these menus.

## Negotiation difficulty (reference)
- Amenability (0-100) is computed in code; factor weights are not exposed.
- Level thresholds: `NPolitics` in `common/defines/00_defines.txt` — MIN_AMENABILITY_TENSE/NORMAL/FRIENDLY_NEGOTIATION = 25/50/75 → levels 4/2/1.
- `promise_quest_degree = amenability_level` in the `immediate` of `negotiation.1`.

## Building promises (negotiation options 5 and 6, all interest groups)
- Vanilla asks for (GDP / 4M) x cost factor x negotiation level (1 / 2 / 4) new levels - linear in GDP, hundreds of levels in the late game.
- `building_scaler` (vanilla `negotiation_values.txt`) now returns `nr_building_scaler` (`common/script_values/nr_building_promise_values.txt`): vanilla up to GDP 50M (`nr_building_linear_gdp`), above it the value at the threshold x (1 + 0.3 x log2(GDP / 50M)) (`nr_building_doubling_share`). log2 is piecewise linear per doubling (`nr_building_gdp_log2`, error < 0.09). Cost factors and the 1 / 2 / 4 level multiplier stay vanilla; option 6 (building groups) uses the same scaler.
- University (cost 400), new levels at open / pragmatic / tense: GDP 30M 12 / 24 / 48 (vanilla), 50M 20 / 40 / 80, 100M 26 / 52 / 104, 300M 36 / 71 / 142, 1B 46 / 92 / 184 (vanilla 400 / 800 / 1600), 2B 52 / 104 / 208.

## Regular bribe (negotiation option 1, all interest groups)
- `bribed_ig_benefits` is overridden in `common/static_modifiers/00_negotiation_modifiers.txt` (copy of the vanilla file): no pop attraction, +10% political strength (vanilla: +25% attraction, +5% strength).
- Multiplier `nr_neg_level_scale` (`common/script_values/nr_negotiation_hooks_values.txt`): amenability_level 1 / 2 / 4 -> 1 / 2 / 3, i.e. +10% / +20% / +30% political strength, decaying over 10 years. Hooked in `events/iberia_events/negotiation_events.txt`, option `negotiation.1.o1`.
- The modifier name is kept: vanilla `generic_laws.2` (corruption exposed) triggers on it.

### One-time bribe (every group) and the Devout leader's vices
- Files: `common/scripted_effects/nr_bribe_effects.txt`, `events/nr_bribe_events.txt`, values in `common/script_values/nr_bribe_values.txt`, triggers in `common/scripted_triggers/nr_bribe_triggers.txt`. Hooked in `negotiation.1.o1` (`nr_bribe_pay`, `nr_bribe_exposure_roll`). No group gets the vanilla weekly `negotiation_bribes` any more.
- Payment (`nr_bribe_lump_sum`, `add_treasury`, computed directly so the tooltip shows it): the vanilla slow sum (`neg_bribe_amount` x 260.7 weeks of linear decay over 10 years) / 2.5 (`nr_bribe_lump_divisor`), i.e. about 3.9% / 7.8% / 15.6% of GDP by level 1 / 2 / 4. Capped by 10% / 20% / 30% of max credit (`credit`). Rounded to 100.
- A bribe that would cause a default is not offered (`nr_bribe_affordable`: `gold_reserves + credit - principal - payment >= 0`): option 1 is not rolled for other groups (`nr_neg_option_1_allowed`); for the Devout the roll `nr_devout_softbribe_roll` gives charity instead (even for greedy leaders); the option `negotiation.1.o1` is hidden if the money ran out during the negotiation (`nr_neg_option_1_affordable`).
- `generic_laws.2` option c ("corruption is good") needs vanilla `negotiation_bribes`, so it is no longer shown (the money is already paid).
- Exposure: vanilla chances (10%, 20% under Protected Speech), `generic_laws.2` in 300 days. Devout only: the leader gets `nr_bribe_taken` (and `nr_bribe_exposed` if the roll hit), 330 days.
- Devout only: 310 days after the bribe, hidden `nr_bribe.1`: every character of the country with `nr_bribe_taken` and without `nr_bribe_exposed` has a 20% chance of a trait (`nr_bribe_add_vice_trait`): Grifter 25, Expensive Tastes 25, Alcoholic 20, Opium Addiction 15, Syphilis 15 (only traits he does not have). Grifter and Expensive Tastes make the leader always take a regular bribe afterwards (`nr_devout_softbribe_leader_loves`). Tooltip `nr_bribe_vice_risk_tt`.
- AI (option `negotiation.1.o1`, every group; the vanilla income checks are switched off by `nr_neg_option_1_vanilla_ai = no`): +35 if the payment fits in gold reserves (`nr_bribe_ai_good`); +15 if partly on credit but at least 50% of the credit stays free (`nr_bribe_ai_fair`); -50 if on credit while in deficit or with less than 25% of the credit left (`nr_bribe_ai_bad`).
- Refund: the paid amount is stored on the bribed group (`nr_bribe_paid`, 330 days), so two bribed groups do not overwrite each other. The money is assumed to be spent evenly over 2 years (`nr_bribe_spend_days` = 730), exposure comes after 300 days, so ~59% is unspent (`nr_bribe_refund`, group scope). Returned in `generic_laws.2` option b ("deal with it", overridden in `events/law_events/law_events_01.txt`, copy of the vanilla file) for the exposed group (`scope:corrupt_ig_scope`). Option a (ignore) returns nothing.

## Feature devout_officials (negotiation option 2: church officials instead of places in the administration)
- Files: `events/nr_devout_officials_events.txt`, `common/scripted_effects/nr_devout_officials_effects.txt`, `common/scripted_triggers/nr_devout_officials_triggers.txt`, `common/script_values/nr_devout_officials_values.txt`, `common/static_modifiers/nr_devout_officials_modifiers.txt`, localization `nr_devout_officials_l_*.yml`, concepts in `nr_game_concepts.txt`.
- Hooks: `set_neg_options` option 2 gets `nr_neg_option_2_allowed` (currently no extra conditions) and weight `nr_neg_option_2_modifier` (Devout leader traits, `nr_devout_officials_leader_weight`). In `negotiation.1` the vanilla option 2 is hidden for the Devout (`nr_neg_option_2_is_custom`), they get `negotiation.1.nr_o2_devout` -> `nr_neg_option_2_custom` -> `nr_devout_officials_start`.
- Option: bureaucracy penalty `nr_devout_officials_penalty_<slot>` (same as vanilla `negotiation_bureaucracy`, one per campaign slot so campaigns stack) x negotiation level (1 / 2 / 4, -7.5% bureaucracy per point, decaying 10 years); Devout get `nr_devout_officials_benefits` (+12% political strength x 1 / 2 / 3, no attraction); form event `nr_devout_officials.1` in 7 days.
- Campaign limit (at the moment option 2 is rolled, `nr_neg_option_2_allowed`): at most 1 / 2 / 3 officials campaigns at once by Devout clout (<10% / 10-20% / 20%+), separate from the soft bribe limit. The vanilla one-deal-at-a-time block (`negotiation_bureaucracy` in `neg_option_2_trigger`) is skipped for the Devout (`nr_neg_option_2_skips_vanilla_block`). A form already running is not offered again.
- No bureaucracy deficit check: the option and every form can push the country into a deficit, the player decides. The AI still weighs the spare bureaucracy (below).
- AI (option): base 5, +25 if spare bureaucracy after the penalty >= 25% of usage (`nr_devout_officials_ai_good`), -30 if < 10% (`nr_devout_officials_ai_bad`); spare share is `nr_devout_officials_spare_share`.
- Leader weight for option 2: Ambitious / Imperious / Master Bureaucrat / Political Appointee +10, political operator +5 / 10 / 15, Pious / Bigoted / prominent +5; leaders with no taste for office work -5 each: Reserved, Romantic, Reckless, Firebrand, Inspirational Orator; Grifter / Expensive Tastes / Hedonist -5 (want money, not posts).
- Form event: Clerical Advisers (always, default, base effects only) + 2 random of the available forms. The form rescales the campaign's penalty (`nr_devout_officials_set_penalty`, only for factors other than x1) (x0.75 / x1 / x1.25 / x1.5) and adds its modifier for 10 years:

| Form | Penalty | Available | Effects | AI |
|---|---|---|---|---|
| Clerical Advisers | x1 | always | base only | 10, +10 if spare < 10% |
| Censorship Committees | x1.25 | Right of Assembly, leader not against Censorship | movements -10% attraction, conversion +10%, Intelligentsia -10% strength / -2 approval, leverage resistance +15%, tech spread -5% | 10, +15 if Intelligentsia powerful |
| Parish Registers | x0.75 | always | population bureaucracy cost -5%, conscription +5%, incorporation +10%, acceptance without shared religious trait -5 | 10, +10 if spare < 10% |
| The Church and the Slaves | x0.75 | slavery legal | slave revolt support -15%, slave mortality -10%, abolitionist support in free states +10% | 10, +15 with a slave revolt movement |
| Church Tax | x1.25 | state religion (and variants) or freedom of conscience | clergy SoL +2, authority +50, tax collection -3%, conversion -5% | 10, +10 if authority < 100 |
| Prison Ministry | x1 | not state atheism | radicals from movements -5%, loyalists +5%, turmoil effects -5%, turmoil mortality +0.002 | 10, +15 if turmoil > 15% |
| Church Calendar | x1 | not state atheism | legitimacy +5, prestige +5%, SoL +0.5, throughput -2% | 10, +15 if legitimacy < 50 |
| Seminarists in the Chancelleries | x1.5 | always | authority +100, legitimacy +5, Intelligentsia -20% strength / -10% attraction / -3 approval | 5, +20 if Intelligentsia powerful, -20 if spare < 20% |
| Synodal Administration | x1.25 | state religion (and variants), leader not against it | authority +50, state religion acceptance +5, Devout -10% attraction | 10, +15 if authority < 100 |

- Censorship Committees end at once when Protected Speech is enacted (`on_law_activated` -> `nr_on_law_activated` -> `nr_devout_officials_check_censorship`).
- General rule: an IG never offers a form, petition or amendment its leader is against (`nr_ig_leader_not_against_law`, `common/scripted_triggers/nr_leader_stance_triggers.txt`).
- Follow-ups below: all implemented (censorship, synod, church tax, Sunday Rest, police, Clerical Census, slavery), plus `improve_stance` for petitions and the leader rule for older features. Not tested in game yet: police, slavery. Details per feature: petition laws and amendments as in the table; freeing slaves is `nr_devout_slavery_free_believers` (on adding the amendment to an active law, on activation of a law carrying it, and yearly via `nr_on_yearly_pulse_country`).

### Devout officials - follow-ups (agreed design)
Common to all: follow-up event 10 years after the form was chosen (scheduled from the form option, pattern of schools/sisters), namespace `nr_devout_<topic>`, `.2` = post-campaign, `.1` = enactment event in the `on_law_checkpoint_debate` pool (cooldown 5 years, options a default "+15% speed, Devout -2 approval 5 years" / b "attach the amendment, -15% speed" / c "let group X decide: X +2, Devout -2, 5 years"). Petitions use the petition framework (JE 4 years, +25% enactment speed, timeout: Devout -2 approval 5 years). Decline in `.2`: Devout -1 approval 5 years. Leader rule everywhere: no form, petition or amendment the Devout leader is against. Flavor: lore line + historical concept for every form and amendment (dates to be re-checked before writing).

Shared mechanics:
- `on_law_enactment_started` (vanilla code on_action, root = country) -> our `nr_on_law_enactment_started` (appended via `on_actions`, no vanilla override):
  - `improve_stance = 1` for the Devout if they have an active petition for the law being enacted (neutral -> approve, only for this enactment). Done: `nr_petition_improve_stance`, list of petitions in `nr_devout_petition_for_enacting_law`;
  - church tax: amendment A on the old church-and-state law -> amendment B attached to the enacting Freedom of Conscience / Total Separation (`nr_amendment_add_to_enacting_law`), with a notification;
  - seminarists: an active petition for Appointed Bureaucrats -> "Clerical Census" amendment attached automatically.

| Form | Follow-up `.2` (10 years) | Amendment(s) | `.1` enactment event |
|---|---|---|---|
| Censorship Committees | Right of Assembly + tech `law_enforcement`: petition for `law_censorship` (or decline -1); Censorship adopted during the campaign: thanks, Devout +2 approval 5 years; Outlawed Dissent adopted: no event; Protected Speech adopted: campaign aborted, no event | - | - |
| Parish Registers | none (decided: no follow-up) | - | - |
| The Church and the Slaves | only if slavery is still legal: a) petition for `law_slavery_banned`; b) amendment "Do Not Enslave Fellow Believers"; c) decline -1. Slavery banned during the campaign: no event | "Do Not Enslave Fellow Believers" on slave trade / legacy / colonial / debt slavery; parent `law_slavery_banned`, sponsor Devout. On adoption and then yearly: all slaves of the state religion are freed - working in `bg_agriculture`, `bg_staple_crops`, `bg_subsistence_agriculture`, `bg_ranching`, `bg_subsistence_ranching`, `bg_plantations` or without workplace -> peasants, elsewhere -> laborers (`change_poptype`). Modifiers: `state_pop_support_movement_anti_slavery_mult` +0.10, `state_bureaucracy_population_base_cost_factor_mult` +0.05, `interest_group_ig_landowners_approval_add` -2, `country_authority_cost_add` +100; yearly a modifier on `movement_anti_slavery` with radicalism -0.25 (~1 year) | while enacting slave trade / legacy / colonial / debt slavery, amendment and a campaign absent: a "A slave is a slave, whatever his faith" (default), b "The baptised cannot be a slave" (attach), c "Let the landowners decide" (Landowners +2, Devout -2) |
| Church Tax | state religion (and variants): amendment A; Freedom of Conscience / Total Separation: amendment B | A "Church Tax Guarantee" on state religion / millet / people of the book: `country_authority_add` +50; its description warns that B will follow automatically. B "Church Tax" on Freedom of Conscience / Total Separation: `country_authority_add` +50, `building_clergymen_standard_of_living_add` +1, `state_tax_collection_mult` -0.02, `state_conversion_mult` -0.03 (half of the form); parent `law_state_religion`. Transfer: `nr_devout_church_tax_transfer` -> event `nr_devout_church_tax.3`: a "A promise is a promise" (default, B attached to the law being enacted) or b betrayal (no B; Devout -10 approval, legitimacy -10, both 5 years) | while enacting Freedom of Conscience / Total Separation and A is absent: choice to attach B (a "The church will take care of itself" default, b "Keep the church's right to the tax" attach B, c "Let the taxpayers decide": Petty Bourgeoisie +2, Devout -2) |
| Prison Ministry | `law_no_police`: petition for a police law - the one the leader approves, otherwise a random available one (tech: `tech_bureaucracy` / `law_enforcement` / `mass_surveillance`), never one the leader is against; police law present: its amendment | different per police law, parent `law_state_religion`, cost `country_authority_cost_add` +50 each. Parish Constables (`law_local_police`): `state_turmoil_effects_mult` -0.05, `interest_group_ig_devout_pol_str_mult` +0.05, `interest_group_ig_landowners_pol_str_mult` -0.05. Prison Ministry (`law_dedicated_police`): `state_radicals_from_political_movements_mult` -0.03, `state_loyalists_from_political_movements_mult` +0.03, `state_mortality_turmoil_mult` +0.001, `interest_group_ig_devout_pol_str_mult` +0.05. Gendarmerie Chaplains (`law_militarized_police`): `state_mortality_turmoil_mult` -0.002, `interest_group_ig_devout_pol_str_mult` +0.05, `country_coup_resistance_add` +0.25 | - |
| Church Calendar | `law_no_workers_rights`: petition for `law_regulatory_bodies` (leader not against); Regulatory Bodies / Worker Protections: amendment | "Sunday Rest" on `law_regulatory_bodies`, `law_worker_protections`; parent `law_worker_protections`, sponsor Devout, no authority cost: `state_standard_of_living_add` +0.5, `building_throughput_add` -0.01, `interest_group_ig_devout_pol_str_mult` +0.05 | while enacting Regulatory Bodies / Worker Protections, amendment absent, no Calendar campaign, leader not against: a "Production knows no days off" (default), b "The seventh day belongs to the Lord" (attach), c "Let the industrialists decide" (Industrialists +2, Devout -2) |
| Seminarists in the Chancelleries | hereditary / elected bureaucrats: petition for `law_appointed_bureaucrats` (leader not against), the amendment attaches automatically when its enactment starts; Appointed Bureaucrats: amendment at once | "Clerical Census for Officials" on `law_appointed_bureaucrats`, parent `law_state_religion`, sponsor Devout, no cost: `interest_group_ig_intelligentsia_pol_str_mult` -0.10, `interest_group_ig_intelligentsia_approval_add` -1, `interest_group_ig_devout_pol_str_mult` +0.10 | while enacting Appointed Bureaucrats, amendment absent, no Seminarists campaign, no petition, leader not against: a "The civil service is secular" (default), b "Clerical census" (attach), c "Let the universities decide" (Intelligentsia +2, Devout -2) |
| Synodal Administration | state religion still active: amendment; otherwise no event | "Synodal Administration" on `law_state_religion`: `country_authority_add` +25, `country_acceptance_state_religion_add` +5, `interest_group_ig_devout_pop_attraction_mult` -0.05, no cost | while enacting State Religion or its variants, amendment absent, no Synod campaign, leader not against: a "The church governs itself" (default), b attach, c "Let the intelligentsia decide" (Intelligentsia +2, Devout -2) |

Also: the leader rule applied to the older features (schools, sisters, chaplains) - done with `nr_devout_leader_not_against_law` (works without scope:ig, e.g. in event triggers); amendments check their parent law.
