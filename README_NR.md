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
| `negotiation.1.o1` | `nr_neg_option_1_is_custom = no`; otherwise option `negotiation.1.nr_o1_soft` → `nr_neg_option_1_custom` |

Routing by interest group: `common/scripted_effects/nr_negotiation_hooks.txt`, `common/scripted_triggers/nr_negotiation_hooks.txt`, `common/script_values/nr_negotiation_hooks_values.txt`.

## Overridden vanilla files (after every game patch: take the new vanilla file and re-add the hooks)
- `events/iberia_events/negotiation_events.txt`
- `common/scripted_triggers/ip4_negotiation_triggers.txt`
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
| devout_schools | `events/nr_devout_schools_events.txt`, `common/journal_entries/nr_devout_schools_je.txt`, `common/scripted_effects/nr_devout_schools_effects.txt`, `common/scripted_triggers/nr_devout_schools_triggers.txt`, `common/static_modifiers/nr_devout_schools_modifiers.txt`, `localization/*/nr_devout_schools_l_*.yml` |
| devout_sisters | `common/amendments/nr_devout_sisters_amendments.txt`, `events/nr_devout_sisters_events.txt`, `common/journal_entries/nr_devout_sisters_je.txt`, `common/scripted_effects/nr_devout_sisters_effects.txt`, `common/scripted_triggers/nr_devout_sisters_triggers.txt`, `common/static_modifiers/nr_devout_sisters_modifiers.txt`, `localization/*/nr_devout_sisters_l_*.yml` |
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
- Negotiation option "Allocate funds for the church's needs." (`nr_devout_softbribe_start`): expenses `nr_devout_softbribe_expenses` = vanilla bribe amount (`neg_bribe_amount`); +10% conversion (`nr_devout_softbribe_base`); Devout get `nr_devout_softbribe_patronage` (+35% attraction, +5% political strength x `nr_devout_softbribe_patronage_multiplier` = 1 / 2 / 3 by level, i.e. 5/10/15%; the regular bribe gives no attraction and +10/20/30% strength, see "Regular bribe"); law stance improves. Everything lasts 10 years and decays.
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
- Money spent through `country_expenses_add` leaves the economy; nobody receives it (same as vanilla bribes).

## Pattern: IG amendment pair (reusable)
An IG-themed amendment reaches a law in two ways:
1. **Enactment event** in the vanilla `on_law_checkpoint_debate` random pool (like vanilla `education_laws.2`, Prussian Education). Added in `common/on_actions/nr_on_actions.txt` - on_action data merges across files, no vanilla override. One non-default option calls `nr_amendment_add_to_enacting_law = { AMENDMENT = ... IG = ... }`.
2. **After the IG's soft-bribe campaign**: the campaign option schedules a popup (`trigger_event days = 3650`) that offers `nr_amendment_add_to_active_law = { AMENDMENT = ... LAW = ... IG = ... }` (default: decline). Vanilla attaches amendments to active laws the same way (`active_law:<group> = { add_amendment }`).
- Guard: `nr_amendment_is_present = { AMENDMENT = ... }` (active on any law, or on the law being enacted).
- New instance checklist: amendment in `common/amendments/nr_<group>_<topic>_amendments.txt`; events `nr_<group>_<topic>.1` (enactment, 3 options) and `.2` (post-campaign); pool entry in `nr_on_actions.txt`; schedule `.2` from the campaign form; localization `nr_<group>_<topic>_l_*.yml`.

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

## Negotiation difficulty (reference)
- Amenability (0-100) is computed in code; factor weights are not exposed.
- Level thresholds: `NPolitics` in `common/defines/00_defines.txt` — MIN_AMENABILITY_TENSE/NORMAL/FRIENDLY_NEGOTIATION = 25/50/75 → levels 4/2/1.
- `promise_quest_degree = amenability_level` in the `immediate` of `negotiation.1`.

## Regular bribe (negotiation option 1, all interest groups)
- `bribed_ig_benefits` is overridden in `common/static_modifiers/00_negotiation_modifiers.txt` (copy of the vanilla file): no pop attraction, +10% political strength (vanilla: +25% attraction, +5% strength).
- Multiplier `nr_bribe_benefits_multiplier` (`common/script_values/nr_bribe_values.txt`): amenability_level 1 / 2 / 4 -> 1 / 2 / 3, i.e. +10% / +20% / +30% political strength, decaying over 10 years. Hooked in `events/iberia_events/negotiation_events.txt`, option `negotiation.1.o1`.
- The modifier name is kept: vanilla `generic_laws.2` (corruption exposed) triggers on it.

### Devout: one-time bribe and the leader's vices
- Files: `common/scripted_effects/nr_bribe_effects.txt`, `events/nr_bribe_events.txt`, values in `common/script_values/nr_bribe_values.txt`. Hooked in `negotiation.1.o1` (`nr_bribe_pay`, `nr_bribe_exposure_roll`); other groups keep the vanilla weekly bribe and exposure.
- Payment (`nr_devout_bribe_lump_sum`, `add_treasury`): the vanilla slow sum (`neg_bribe_amount` x 260.7 weeks of linear decay over 10 years) / 2.5 (`nr_bribe_lump_divisor`), i.e. about 3.9% / 7.8% / 15.6% of GDP by level 1 / 2 / 4. Capped by 10% / 20% / 30% of max credit (`credit`). Rounded to 100.
- A bribe that would cause a default is not offered (`nr_devout_bribe_affordable`: `gold_reserves + credit - principal - payment >= 0`): the roll `nr_devout_softbribe_roll` gives charity instead (even for greedy leaders), and the option `negotiation.1.o1` is hidden if the money ran out during the negotiation.
- `generic_laws.2` option c ("corruption is good") needs `negotiation_bribes`, so it is not shown for a Devout bribe (the money is already paid).
- Exposure: vanilla chances (10%, 20% under Protected Speech), `generic_laws.2` in 300 days. The Devout leader gets `nr_bribe_taken` (and `nr_bribe_exposed` if the roll hit), 330 days.
- 310 days after the bribe, hidden `nr_bribe.1`: every character of the country with `nr_bribe_taken` and without `nr_bribe_exposed` has a 20% chance of a trait (`nr_bribe_add_vice_trait`): Grifter 25, Expensive Tastes 25, Alcoholic 20, Opium Addiction 15, Syphilis 15 (only traits he does not have). Grifter and Expensive Tastes make the leader always take a regular bribe afterwards (`nr_devout_softbribe_leader_loves`).
- AI (option `negotiation.1.o1`, Devout only; vanilla income checks kept for other groups): +35 if the payment fits in gold reserves (`nr_devout_bribe_reserves_after >= 0`); +15 if partly on credit but at least 50% of the credit stays free; -50 if on credit while in deficit or with less than 25% of the credit left (`nr_devout_bribe_room_after_share`).
- Refund: the paid amount is stored on the country (`nr_devout_bribe_paid`, 330 days) before paying. The money is assumed to be spent evenly over 2 years (`nr_bribe_spend_days` = 730), exposure comes after 300 days, so ~59% is unspent (`nr_devout_bribe_refund`). Returned in `generic_laws.2` option b ("deal with it", overridden in `events/law_events/law_events_01.txt`, copy of the vanilla file) when the exposed group is the Devout (`nr_bribe_refund`). Option a (ignore) returns nothing.

## Feature devout_officials (negotiation option 2: church officials instead of places in the administration)
- Files: `events/nr_devout_officials_events.txt`, `common/scripted_effects/nr_devout_officials_effects.txt`, `common/scripted_triggers/nr_devout_officials_triggers.txt`, `common/script_values/nr_devout_officials_values.txt`, `common/static_modifiers/nr_devout_officials_modifiers.txt`, localization `nr_devout_officials_l_*.yml`, concepts in `nr_game_concepts.txt`.
- Hooks: `set_neg_options` option 2 gets `nr_neg_option_2_allowed` (Devout: no bureaucracy deficit) and weight `nr_neg_option_2_modifier` (Devout leader traits, `nr_devout_officials_leader_weight`). In `negotiation.1` the vanilla option 2 is hidden for the Devout (`nr_neg_option_2_is_custom`), they get `negotiation.1.nr_o2_devout` -> `nr_neg_option_2_custom` -> `nr_devout_officials_start`.
- Option: vanilla `negotiation_bureaucracy` x negotiation level (1 / 2 / 4, -7.5% bureaucracy per point, decaying 10 years); Devout get `nr_devout_officials_benefits` (+12% political strength x 1 / 2 / 3, no attraction); form event `nr_devout_officials.1` in 7 days.
- Never offered if the x1 penalty would cause a bureaucracy deficit (`nr_devout_officials_affordable`: produced x (1 - 0.075 x level) - usage >= 0; approximation, multipliers stack additively in the game). Forms with x1.25 / x1.5 are only shown if they fit too.
- AI (option): base 5, +25 if spare bureaucracy after the penalty >= 25% of usage, -30 if < 10%.
- Leader weight for option 2: Ambitious / Imperious / Master Bureaucrat / Political Appointee +10, political operator +5 / 10 / 15, Pious / Bigoted / prominent +5; Honorable -10, Reserved -5, Grifter / Expensive Tastes / Hedonist -5.
- Form event: Clerical Advisers (always, default, base effects only) + 2 random of the available forms. The form rescales `negotiation_bureaucracy` (x0.75 / x1 / x1.25 / x1.5) and adds its modifier for 10 years:

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
- Not done yet: end events after 10 years, petitions and amendments (censorship, slavery, church tax A/B, police x3, Sunday rest, clerical census, synod), enactment events `.1`, yearly liberation of slaves, `improve_stance` for petitioned laws, the leader rule for older features.
