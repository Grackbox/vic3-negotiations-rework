# Negotiations Rework — developer notes

Mod prefix: `nr_` (keys, files). Edits inside copied vanilla files are marked `NR`.

## Features (specs in docs/)
Each feature's agreed design (numbers, conditions, flavour notes, test status) lives in its area file:

| File | Features |
|---|---|
| [docs/devout.md](docs/devout.md) | Flock's Welfare (option 9) with charity; church funds (option 1); church officials (option 2) and their follow-ups: censorship, synod, church tax, Sunday rest, clerical census, police, slavery; chaplains, sisters of mercy, schools |
| [docs/landowners.md](docs/landowners.md) | grants (option 1) with enactment events; Paternal Care (option 9) with dinners / social season; places in the provinces (option 2) with enactment events |
| [docs/industrialists.md](docs/industrialists.md) | state contracts (option 1); Factory Care (option 9) with canteens; profitable heavy industry (options 5 and 6); seats in the commissions (option 2); enactment events |
| [docs/negotiations.md](docs/negotiations.md) | rules for every group: negotiation difficulty, building promises (incl. the Devout fishing wharves), the bribe and the Devout leader's vices, ruler pressure, election promise, authority cost slots |

## Architecture
Copied vanilla files contain only hooks; all mod logic lives in the mod's own files.

| Where (vanilla) | What it calls |
|---|---|
| `negotiation.1` → `immediate`, after `set_neg_options` | `nr_negotiation_after_options` — overrides precomputed option values, rolls bribe vs soft bribe |
| `negotiation.1` → `immediate`, right after `set_promised_building_type` | `nr_after_promised_building_type` (IG scope) — the Devout may ask for fishing wharves |
| `negotiation.1.o5` | `nr_neg_option_5_flavor` — lore line for the mod's building requests |
| `building_scaler`, `building_levels_to_increase_value` (`negotiation_values.txt`) | `nr_building_scaler` (logarithmic GDP scaling), `nr_promised_building_cost_scale` |
| `negotiation.1.o9` | `nr_neg_option_9_is_custom` → `nr_neg_option_9_custom`, otherwise vanilla |
| `neg_option_9_trigger` | `nr_has_custom_sol_promise = no` |
| `set_neg_options`, option 1 (bribe) in all three lists | `nr_neg_option_1_allowed` (condition) and `nr_neg_option_1_modifier` (weight) |
| `set_neg_options`, option 2 (bureaucracy) in all three lists | `nr_neg_option_2_allowed` (condition) and `nr_neg_option_2_modifier` (weight) |
| `negotiation.1.o1` | `nr_neg_option_1_is_custom = no`, `nr_neg_option_1_affordable`; AI: `nr_neg_option_1_vanilla_ai` gates the vanilla income checks, `nr_neg_option_1_ai_good` / `_fair` / `_bad` (+35 / +15 / -50) for groups with their own bribe. Otherwise option `negotiation.1.nr_o1_soft` → `nr_neg_option_1_custom` |
| `negotiation.1.o2` | `nr_neg_option_2_is_custom = no`; otherwise option `negotiation.1.nr_o2_custom` (name per group via custom loc `NR_OfficesLine`; `nr_neg_option_2_allowed`, AI `nr_neg_option_2_ai_good` / `_bad`) → `nr_neg_option_2_custom` (Devout: church officials, Landowners: places in the provinces) |
| `negotiation.1`, extra options before the cancel option | `negotiation.1.nr_pressure` (`nr_ruler_pressure_available` -> `nr_ruler_pressure_apply`), `negotiation.1.nr_election_promise` (`nr_election_promise_available` -> `nr_election_promise_start`) |
| `negotiation.1.o1`, `bribed_ig_benefits` | multiplier `nr_neg_level_scale` (level 1 / 2 / 4 → 1 / 2 / 3); the same value scales soft bribe patronage and church officials |

No interest group is named in the copied vanilla files; every group-specific check sits behind a hook. Routing by interest group: `common/scripted_effects/nr_negotiation_hooks.txt`, `common/scripted_triggers/nr_negotiation_hooks.txt`, `common/script_values/nr_negotiation_hooks_values.txt`.

## Overridden vanilla files (after every game patch: take the new vanilla file and re-add the hooks)
- `events/iberia_events/negotiation_events.txt`
- `common/scripted_triggers/ip4_negotiation_triggers.txt`
- `common/script_values/negotiation_values.txt` (hooks in `building_scaler`, `building_levels_to_increase_value` and `neg_option_9_modifier`)
- `common/scripted_effects/04_neg_event_options_scripted_effects.txt`
- `events/iberia_events/ip4_election_rigging.txt` (election promise: `nr_election_rigging_immediate` at the end of `immediate`, `nr_election_rigged = { PARTY = scope:party_N_scope }` in each party option, `nr_election_not_rigged` in the no-rigging options, extra options `caciquismo.nr_promised_<group>` before them)

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
| ruler_pressure | `common/scripted_effects/nr_ruler_pressure_effects.txt`, `common/scripted_triggers/nr_ruler_pressure_triggers.txt`, `common/script_values/nr_ruler_pressure_values.txt`, `common/static_modifiers/nr_ruler_pressure_modifiers.txt`, `localization/*/nr_ruler_pressure_l_*.yml` (also election_promise texts), custom loc `NR_PressureLine`; generated from the tables below |
| election_promise | `common/journal_entries/nr_election_promise_je.txt`, `common/scripted_effects/nr_election_promise_effects.txt`, `common/scripted_triggers/nr_election_promise_triggers.txt`, `events/iberia_events/ip4_election_rigging.txt` (copy with hooks), on_actions `nr_on_election_campaign_start` / `_end` |
| authority cost slots | `common/scripted_effects/nr_authority_cost.txt`, `common/scripted_triggers/nr_authority_cost.txt`, `common/static_modifiers/nr_authority_cost_modifiers.txt` |
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
| 104 | `landowners_sol` — Landowners, "Paternal Care": the same SoL bar |
| 105 | `industrialists_sol` — Industrialists, "Factory Care": the same SoL bar |
| 102 | `election_promise` — back the group's party at the next election |
| 103 | `industrialists_healthy` — X healthy levels of a heavy industry type held 6 months (Industrialists, options 5 and 6) |

## Pattern: IG amendment pair (reusable)
An IG-themed amendment reaches a law in two ways:
1. **Enactment event** in the vanilla `on_law_checkpoint_debate` random pool (like vanilla `education_laws.2`, Prussian Education). Added in `common/on_actions/nr_on_actions.txt` - on_action data merges across files, no vanilla override. One non-default option calls `nr_amendment_add_to_enacting_law = { AMENDMENT = ... IG = ... }`.
2. **After the IG's soft-bribe campaign**: the campaign option schedules a popup (`trigger_event days = 3650`) that offers `nr_amendment_add_to_active_law = { AMENDMENT = ... LAW = ... IG = ... }` (default: decline). Vanilla attaches amendments to active laws the same way (`active_law:<group> = { add_amendment }`).
3. **Vanilla negotiation option 8** ("add the amendment in fine print"): because the amendment has `would_sponsor` for its group, vanilla `neg_option_8_effects` can pick it when the player negotiates with that group during the enactment of an allowed law. Accepted as is (checked in game with Prison Ministry): this is how vanilla treats every IG-sponsored amendment.
- Guard: `nr_amendment_is_present = { AMENDMENT = ... }` (active on any law, or on the law being enacted).
- New instance checklist: amendment in `common/amendments/nr_<group>_<topic>_amendments.txt`; events `nr_<group>_<topic>.1` (enactment, 3 options) and `.2` (post-campaign); pool entry in `nr_on_actions.txt`; schedule `.2` from the campaign form; localization `nr_<group>_<topic>_l_*.yml`.

## Pattern: room in the law (all our amendments)
Agreed with the user. Applies only to our amendments (`amendment_nr_*`, list generated into `nr_amendment_is_ours`); vanilla and other mods' amendments do not count.
- A law carries at most 2 of our amendments.
- Two of our amendments on one law may not come from groups that oppose each other on that law. Opposition is per law group; two amendments of the same group never conflict:

| Law group | Opposing sponsors | Why |
|---|---|---|
| Slavery | Devout - Landowners | "Do Not Enslave Fellow Believers" frees slaves; the planters' amendments hold them |
| Policing | Devout - Landowners | whose police rules the village: the parish or the manor |
| Army (Devout chaplains, Landowners' noble commissions) | none | altar and noble officer are allies |
| Economic system | Industrialists - Landowners | iron against rye: bank, guarantees and company law against the land bank |
| Labour (workers' rights, labour associations) | Industrialists - Trade Unions | capital against labour |

New groups' amendments get their pairs per law group when they are designed (e.g. Education: Devout - Intelligentsia; Labour: Industrialists - Trade Unions).
- Enforcement: both framework helpers (`nr_amendment_add_to_enacting_law`, `nr_amendment_add_to_active_law`) check `nr_amendment_fits = { IG = ... }` (law scope). No room: `nr_amendment_no_room` stores the law, amendment and group and fires `nr_amendment_room.1` - strike an article (full law: either of the two; conflict: every article of the opposing group) and attach the new one, or leave the law as it is (default) - it repeats the refusal of the offering event: while the law is being enacted +15% enactment speed and the new article's sponsor -2 approval for 5 years (like option a of the enactment events); for an active law the sponsor -1 approval for 5 years (like declining a follow-up). The struck article's sponsor gets `nr_amendment_struck` (-3 approval, 5 years), unless it is the same group as the new article's (a group swapping its own articles pays nothing). Tested in game: conflict (Devout vs Landowners on Slave Trade), overflow, free same-group swap, leaving the law as it is. This covers every event that offers our amendments, the church tax transfer and the census attached with its petition.
- Vanilla negotiation option 8 picks amendments by `would_sponsor`: ours also require `owner.currently_enacting_law ?= { nr_amendment_fits = { IG = ... } }`, so it never offers one that does not fit (no striking there).
- Files: `common/scripted_triggers/nr_amendment_room.txt` (generated: our amendment list, opposition per law group), `events/nr_amendment_room_events.txt`, `common/static_modifiers/nr_amendment_room_modifiers.txt`, `localization/*/nr_amendment_room_l_*.yml`.

## Pattern: IG petition (reusable)
A post-campaign offer can open a 4-year journal entry asking for a law (schools, sisters).
- Helpers in `common/scripted_effects/nr_petition_framework.txt`, parameters `PETITION` (key prefix) and `LAW`: `nr_petition_boost` (at the start of the enactment via `nr_petition_boost_all` from `nr_on_law_enactment_started`, plus JE `immediate` and monthly pulse as a fallback: +enactment speed once per enactment attempt; every new petition must be added to `nr_petition_boost_all` and `nr_devout_petition_for_enacting_law`), `nr_petition_end` (`on_complete`), `nr_petition_timeout` (`on_timeout`: approval penalty on `scope:ig`).
- New instance checklist: journal entry `je_<PETITION>` saving the group as `scope:ig`; static modifiers `<PETITION>_speed` (enactment speed) and `<PETITION>_ignored` (approval); availability trigger `nr_<group>_<topic>_petition_available`.

## Pattern: money or the group's own form (negotiation option 1)
Every group will get its own soft form of option 1 instead of money (Devout: charity; landowners: grants, in design). Groups differ in how often they talk money at all and how often they prefer their own form.
- Weight of option 1 (base 10): `nr_neg_option_1_modifier` = `nr_bribe_ig_weight` (per group) + leader traits: `nr_bribe_leader_weight` (Grifter / Expensive Tastes / Hedonist +10, Honorable -10) for every group except the Devout, who use their own `nr_devout_softbribe_leader_weight`. Total never below 0.
- Money or own form: `nr_softbribe_roll = { KEY REFUSES }` (`common/scripted_effects/nr_softbribe_framework.txt`), called from `nr_negotiation_after_options` for each group that has a form: unaffordable bribe → own form; leader with a `REFUSES` trait → own form; no free campaign slot (`KEY`) → money; `nr_bribe_leader_loves` → money; otherwise `nr_softbribe_share` % own form. Groups without a form yet always take money.

| Group | Option 1 weight | Money / own form | Own form |
|---|---|---|---|
| Industrialists | +20 | 80 / 20 | state contracts (feature industrialists_contracts) |
| Petty Bourgeoisie | +10 | 60 / 40 | (to design: town privileges, patents) |
| Landowners | +10 | 50 / 50 | grants (in design) |
| Armed Forces | 0 | 50 / 50 | (to design: army orders, officers' pensions) |
| Intelligentsia | -5 | 30 / 70 | (to design: grants, universities, publications) |
| Trade Unions | -5 | 30 / 70 | (to design: mutual aid funds, workers' clubs) |
| Rural Folk | -5 | 30 / 70 | (to design: aid to communes, seed loans) |
| Devout | 0 (+ own leader weight) | 25 / 75 | charity (done) |

- New group checklist: its soft-form start effect (like `nr_devout_softbribe_start`), a `REFUSES` trigger, the call in `nr_negotiation_after_options`, `nr_neg_option_1_custom` routing, the option 1 roll condition in `nr_neg_option_1_allowed` (pending form event, free slot or affordable bribe), the option name in `NR_SoftBribeLine`.

## Pattern: campaign forms (shared framework, `nr_campaign_slots.txt`)
Every campaign with a form event uses the same effects with `KEY` (= the campaign key, e.g. `nr_landowners_offices`):
`nr_campaign_choose_form { KEY FORM }` (form modifier, 10 years decaying), `nr_campaign_mark_running { KEY FORM }` (mark for the follow-up), `nr_campaign_remember_slot { KEY FORM }` (only forms a law can end), `nr_campaign_set_penalty { KEY FACTOR }` (bureaucracy campaigns: `<KEY>_penalty_<slot>` = level x factor), `nr_campaign_interrupt { KEY FORM EVENT COST }` (COST = penalty / expenses; removes the form, frees its slot, fires `<KEY>.<EVENT>`), `nr_campaign_free_slot`. AI value `nr_campaign_spare_share` (`nr_campaign_values.txt`). Money campaigns set their cost with `nr_softbribe_set_cost { KEY FACTOR }`. Each feature keeps only its own forms, their availability, the form event, `<KEY>_offer_random_form`, `<KEY>_cleanup`, `<KEY>_check_laws` and texts.
- Leader rule everywhere: `nr_leader_not_against_law = { IG = ig_<group> LAW = <law> }`.

## Pattern: campaign slots
A group can run several 10-year campaigns of one kind at once, limited by its clout: 20%+ -> 3, 10-20% -> 2, below 10% -> 1.
- `nr_campaign_slot_free = { KEY }` (trigger, `common/scripted_triggers/nr_campaign_slots.txt`) checks the limit when the negotiation option is rolled; `nr_campaign_take_slot = { KEY }` (effect, `common/scripted_effects/nr_campaign_slots.txt`) takes the first free slot: country variable `<KEY>_slot_1..3` for `long_modifier_time`, and `<KEY>_current_slot` until the form event is done.
- Everything that must not be overwritten by the next campaign is a per-slot modifier (`<modifier>_1..3`), chosen by `<KEY>_current_slot`. Form modifiers stay single: a running form is simply not offered again.
- Used by `nr_devout_softbribe` (expenses) and `nr_devout_officials` (bureaucracy penalty), each with its own limit.

## Pattern: campaign interruption (every case, past and future)
When a law change ends a running campaign or form early, it never ends silently:
- the interrupt effect removes the form's modifier, its expenses and its campaign slot, clears the follow-up mark, and fires a popup event;
- the popup tells what happened, with a historical quote as flavor; its description and its single visible option depend on whether the group is in government (`first_valid` / `triggered_desc` on `is_in_government`);
- the option applies the group's reaction (`common/scripted_effects/nr_campaign_slots.txt`, modifiers in `nr_campaign_modifiers.txt`): in government `nr_campaign_react_gave_up = { IG }` (-1 approval, 5 years); otherwise `nr_campaign_react_overruled = { IG BACKLASH }` (-5 approval, -15% political strength decaying over 5 years, and a backlash: `reaction` = reactionary support +10% for 5 years, `planters` = pro-slavery radicalism +0.2 for a year, `none`).
- Cases: Censorship Committees (Protected Speech, `nr_devout_censorship.3`, backlash reaction); landowners' grants - Corn Laws, Corvee, Return of Fugitives, Slave Import (`nr_landowners_grants.21` - `.24`).

## Pattern: random forms in a choice event
- Every campaign form event offers 4 options: the default form + 3 random available forms (not already running); fewer if fewer are available (agreed with the user).
Soft bribe and church officials offer a default form plus 2 random ones. Each feature has `nr_<feature>_offer_random_form` (one `random_list` that sets `nr_<feature>_offer_<form>`; called twice), `nr_<feature>_cleanup` (in the event's `after`), and per-form helpers: `nr_devout_softbribe_add_form = { FORM }` + `nr_devout_softbribe_set_cost = { FACTOR }`; `nr_devout_officials_choose_form = { FORM FACTOR }` with availability `nr_devout_officials_<form>_available` checked through `nr_devout_officials_can_offer = { FORM }`.

## Tools
- `python tools/check_mod.py` - static checks, no game needed: braces and indentation, every `nr_` symbol defined and used, names built from parameters (`nr_devout_officials_$FORM$` etc.) exist for every value passed, localization BOM / EN-RU parity / duplicates / missing keys. `--fix-indent` rewrites indentation. Runs on GitHub on every push (`.github/workflows/check.yml`).
- `python tools/gen_amendment_room.py` - regenerates `common/scripted_triggers/nr_amendment_room.txt` (our amendment list and the opposing sponsors per law group, table inside the script). Run after adding an amendment; `check_mod` reports the file when it is out of date.
- `check_mod` also: reports definitions made twice, broken localization lines (a raw line break inside a value), and modifier keys that vanilla never uses (the engine docs list keys the game does not load; keys verified in game go into `KNOWN_VALID`).
- `pwsh tools/deploy.ps1` - mirrors the mod into `Documents/Paradox Interactive/Victoria 3/mod/negotiations_rework` for testing (without `.git`, `.github`, `tools`).
- Engine documentation (effects, triggers, modifiers, on_actions) is dumped by the game into `Documents/Paradox Interactive/Victoria 3/docs/*.log`.

## Debug (console)
- Game started with `-debug_mode`; console `~`. The console runs only its own commands (`event <id>`). Script effects (`activate_law = law_type:...`, `set_variable = {...}`) go to `inspect_country` → Script Runner → Effect (Parse, Run); its Trigger field checks a condition for the selected country.
`events/nr_debug_events.txt`, localization `nr_debug_l_*.yml`. Never fired by the game.
- `event nr_debug.1` - fires every enactment event `.1` at once (Devout and `nr_landowners_enact.1` - `.6`); only those matching the law being enacted appear (their 5-year cooldown still applies).
- `event nr_debug.2` / `event nr_debug.3` - menus of the post-campaign follow-ups `.2` (schools, sisters, chaplains, censorship, synod / church tax, Sunday Rest, Clerical Census, police, slavery). The censorship option also sets the campaign mark `nr_devout_censorship_campaign`. Each follow-up still checks its own trigger.
- `event nr_debug.4` - Devout regular bribe without a negotiation: pay it exactly as option `negotiation.1.o1` (payment, `bribed_ig_benefits`, exposure roll, vice check in 310 days), give the Devout leader a vice now (100%), or expose it now (`generic_laws.2`, needs a law being enacted).
- `event nr_debug.5` / `event nr_debug.6` - landowners' grants: the form event `nr_landowners_grants.1` and the follow-ups `.11` - `.18` (with the running mark of their form).
- `event nr_debug.8` - landowners' places in the provinces: the form event `nr_landowners_offices.1` and the follow-ups `.11` - `.21` (with the running mark of their form).
- `event nr_debug.9` / `event nr_debug.10` - the Industrialists' state contracts / commissions: form event and follow-ups.
- `event nr_debug.11` - promises without a negotiation (pragmatic level): Paternal Care, Factory Care, steel mills that pay (existing levels + 2), Landowners' election promise.
- `event nr_debug.7` - activate a law at once (`activate_law`): Free Trade, Protectionism, Tenant Farmers, Serfdom, Slavery Banned, Legacy Slavery, Slave Trade - to test interruptions.
- New follow-ups and enactment events should be added to these menus.
- Ruler pressure / election promise: form of government via Script Runner (`activate_law = law_type:law_autocracy` etc.); an election campaign starts with `call_election = { months = 1 }` (Script Runner, Effect) - the rigging event `caciquismo.2` fires at its start if electoral fraud is possible.

