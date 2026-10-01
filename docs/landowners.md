# Landowners - agreed design and implementation

Part of the developer notes; architecture, hooks, patterns and tools are in [README_NR.md](../README_NR.md).

## Feature landowners_grants - grants instead of money (negotiation option 1)
- Roll (`nr_softbribe_roll`): 50 / 50 money or grant. Always a grant: leader Honorable, Ambitious, Imperious or Arrogant (status and land matter more than cash), or the bribe is unaffordable. Always money: Grifter / Expensive Tastes / Hedonist, or no free grant slot.
- Option: Landowners +10 / 20 / 30% political strength by level (like the bribe), no attraction; expenses = vanilla bribe amount (`neg_bribe_amount`) weekly, decaying over 10 years, x form factor; form event a week later: default form + 2 random of the available ones. Slots 1 / 2 / 3 by clout; a running form is not offered again.
- Forms (10 years, decaying; effects are drafts):

| Form | Cost | Plus | Minus | Movements | Available |
|---|---|---|---|---|---|
| Ranks and Orders (default, base effects only) | x1 | - | - | - | always |
| Crown Lands | x0.5 | agriculture self-investment +10%, aristocrats' shares + | subsistence peasants SoL -1 | land reform support +10% | always |
| Tax Exemptions for Estates | x0.25 | aristocrats SoL +1 | agriculture and plantation taxes -20% | liberal support +10% | always |
| Corn Laws | x0.25 | agriculture throughput +10% | lower strata SoL -0.5, Industrialists -2 approval | liberal support +15% | not Free Trade |
| Noble Land Bank | x1.25 | agriculture self-investment +20% | loan interest +1% | - | always |
| Corvee | x0.25 | agriculture throughput +10%, aristocrats SoL +1 | peasants SoL -1, peasants political strength -10% | land reform support +15%, radicalism +0.1 | Serfdom or Manorialism |
| Redemption Operation | x1.5 | aristocrats SoL +1, agriculture self-investment +10% | peasants SoL -1 | land reform radicalism -0.15 | no Serfdom / Manorialism, landlord farming (not Homesteading, not collectivized) |
| Return of Fugitives | x0.75 | slave revolt support -15%, plantation slave mortality -5% | abolitionist support in free states +15% | abolitionists radicalism +0.15, pro-slavery radicalism -0.15 | slavery legal |
| Slave Import | x0.25 | slave import +30%, plantation throughput +5% | abolitionist support +10% | abolitionists radicalism +0.1, pro-slavery radicalism -0.1 | Slave Trade law |

- Movement radicalism is a modifier on the movement itself, applied when the form is chosen and refreshed yearly while the form runs (movements that appear later get it too); support is a country modifier.
- Interruption (like Censorship Committees): Corn Laws end with Free Trade; Corvee ends when Serfdom / Manorialism is replaced; Return of Fugitives ends with Slavery Banned; Slave Import ends with Slavery Banned or when the Slave Trade law is replaced. The form modifier is removed, its expenses stop, its slot is freed (each form remembers its slot), no follow-up event.
- Interruption popup: events `nr_landowners_grants.21` - `.24` (corn laws, corvee, fugitives, slave import) tell what happened; text and option depend on whether the Landowners are in government, and the option applies the penalty below (`nr_campaign_react_gave_up` / `nr_campaign_react_overruled`, see "Pattern: campaign interruption").
- Interruption penalty: Landowners in government ("gave it up themselves"): -1 approval for 5 years. Landowners in opposition ("the order was broken over their heads", e.g. a revolutionary government): -5 approval for 5 years, -15% political strength decaying over 5 years, and a backlash - Corn Laws / Corvee: reactionary movement support +10% for 5 years; Return of Fugitives / Slave Import: pro-slavery radicalism +0.2 for a year. Historical notes: repeal of the Corn Laws 1846 split the Tories; emancipation from above in Russia 1861; Brazil's Golden Law 1888, the monarchy fell a year later.
- Every form: lore line + historical concept (Table of Ranks 1722; Bashkir lands scandal 1870s-1881; Prussian knightly estates exempt from land tax until 1861; Corn Laws 1815-1846, Anti-Corn Law League 1838, German tariff 1879; Silesian Landschaft 1770, Russian Noble Land Bank 1885; Prussian regulation edicts 1811 / 1816, Russian 1822 right to exile serfs to Siberia; Prussian Rentenbanken 1850, Russian redemption after 1861 over 49 years; US Fugitive Slave Act 1850; Brazilian slave trade 1831-1850, Eusebio de Queiros law). Dates to be re-checked before writing.
- Landowner law stances (vanilla ideologies, for follow-ups): hierarchic - Serfdom strongly approve, Tenant Farmers approve, Peasant Proprietorship strongly disapprove, land-based / consumption taxation approve, proportional disapprove; paternalistic - Traditionalism strongly approve, Agrarianism approve, Hereditary Bureaucrats approve, Local Police approve, Landed Voting strongly approve.
- Follow-ups after 10 years (only if the form was not interrupted; petitions use the petition framework, decline -1, thanks +2; the leader rule applies):

| Form | Follow-up |
|---|---|
| Ranks and Orders | none |
| Crown Lands | Peasant Proprietorship / Homesteading / Commercialized Agriculture: petition for Tenant Farmers; Tenant Farmers / Serfdom / Manorialism / Latifundias: thanks |
| Tax Exemptions | own amendment "Noble Privilege" on any taxation law (parent Land-Based Taxation): Landowners +2 approval, +5% political strength, agriculture self-investment +5%; agriculture and plantation taxes -10%, liberal support +5%; authority cost +50 |
| Corn Laws | no Protectionism: petition for Protectionism; Protectionism: own amendment "Grain Tariff": agriculture throughput +5%, Landowners +1 approval; lower strata SoL -0.25, Industrialists -1 approval, liberal support +5% |
| Noble Land Bank | own amendment "Noble Land Bank" on the economic system law (Traditionalism / Agrarianism / Interventionism / Laissez-Faire): agriculture self-investment +10%, Landowners +1 approval, +5% political strength; loan interest +0.5% |
| Corvee | Serfdom / Manorialism still in force: own amendment "Corvee Statute": agriculture throughput +5%, aristocrats SoL +1, Landowners +1 approval; peasants SoL -0.5, land reform support +10% |
| Redemption Operation | vanilla amendment_redemption_payments (allowed on Tenant Farmers / Commercialized / Homesteading / Peasant Proprietorship); otherwise thanks |
| Return of Fugitives | own amendment "Fugitive Slave Law" on any slavery law (vanilla amendment_american_fugitive_slaves_act is limited to yankee / dixie cultures): Landowners +1 approval, +10% political strength, abolitionist support in free states +15% |
| Slave Import | Slave Trade still in force: own amendment "Free Import": slave import +15%, plantation throughput +3%, abolitionist support +10%; pro-slavery radicalism -0.1 (movement modifier, refreshed yearly); no authority cost |

- Tested in game: the Corvee Statute follow-up (via `nr_debug.6`) attaches the amendment; Corn Laws interruption with its popup.
- Enactment events for the six amendments: `nr_landowners_enact.1` - `.6` (`events/nr_landowners_enact_events.txt`), the Devout .1 pattern applied to the Landowners: in the `on_law_checkpoint_debate` pool (weight 10), cooldown 5 years; not if the amendment is present, not while the grant whose follow-up offers it is running, not if the Landowners leader is against the amendment's parent law (`nr_leader_not_against_law`). Options: a (default) +15% enactment speed, Landowners -2 approval 5 years; b attach the amendment, -15% speed; c the other group +2, Landowners -2.

| Event | Amendment | While enacting | c: who decides |
|---|---|---|---|
| .1 | Noble Privilege | any taxation law | Petty Bourgeoisie |
| .2 | Grain Tariff | Protectionism | Industrialists |
| .3 | Noble Land Bank | Traditionalism / Agrarianism / Interventionism / Laissez-Faire | Industrialists |
| .4 | Corvee Statute | Serfdom / Manorialism | Rural Folk |
| .5 | Fugitive Slave Law | Slave Trade / Legacy / Colonial / Debt Slavery | Intelligentsia |
| .6 | Free Import | Slave Trade | Intelligentsia |
- Implementation: `common/scripted_effects/nr_landowners_grants_effects.txt` (start, forms, interruption, follow-up amendments), `common/scripted_triggers/nr_landowners_grants_triggers.txt`, `common/static_modifiers/nr_landowners_grants_modifiers.txt`, `common/amendments/nr_landowners_grants_amendments.txt`, `events/nr_landowners_grants_events.txt` (.1 form event, .11 - .18 follow-ups), journal entries `nr_landowners_tenant_je.txt` / `nr_landowners_protectionism_je.txt`, localization `nr_landowners_grants_l_*.yml`, concepts in `nr_game_concepts.txt`. Generic helpers used: `nr_softbribe_roll`, `nr_softbribe_option_allowed`, `nr_softbribe_set_cost` (`common/scripted_effects/nr_softbribe_framework.txt`), campaign slots, petition framework, `nr_movement_radicalism` (`common/scripted_effects/nr_movement_effects.txt`, modifiers `nr_movement_radicalism_up_010` ... in `nr_movement_modifiers.txt`). Each form remembers its slot (`nr_landowners_grants_<form>_slot`) and a running mark (`_running`, 3660 days) that its follow-up requires.

## Feature landowners_sol - "Paternal Care" (negotiation option 9 for the Landowners)
Agreed with the user: the overall average SoL (SoL by strata exists only for the interface, not for scripts; computing it from pops was rejected as too heavy). Clone of the Devout `devout_sol` mechanics (target = average SoL + 10%, 1..2, x1.5 tense; bar 0-36 with start 24 / 12 / 6; +1 at target, +0.5 within 0.25, drain below the SoL at the time of the promise; 7.5 / 10 years), without the charity buttons; `promise_quest_type` 104, journal entry `je_nr_landowners_sol`, files `nr_landowners_sol_*` (journal entry, bar, effects, values, localization).
- Weight of option 9 for the Landowners: vanilla 5 + 15 = 20 (hook `nr_neg_option_9_modifier` in the copied `neg_option_9_modifier`).
- Campaigns (buttons in the journal entry, one at a time, 1 year, then 1 year of rest, cost ~0.015% of GDP per week, ended early: Landowners -2 approval for 2 years, end together with the commitment; files `nr_landowners_dinners_*`):
  - Charity Dinners: upper strata SoL -1 (the nobility pays), middle +0.5, lower +0.5;
  - The Social Season: upper strata SoL +3, political movement radicalism +10% (`political_movement_radicalism_add` 0.1).

## Feature landowners_offices - places in the provinces (negotiation option 2 for the Landowners)
Agreed design; same scheme as the Devout church officials. Numbers are drafts.
- Option `negotiation.1.nr_o2_custom` ("Offer the estates places in the provinces"): vanilla bureaucracy penalty (`nr_landowners_offices_penalty_<slot>`, -7.5% x level 1 / 2 / 4, decaying 10 years) x form factor; Landowners +12 / 24 / 36% political strength (`nr_landowners_offices_benefits`, decaying); form event `nr_landowners_offices.1` a week later: Noble Elections (default) + 3 random available forms. Campaign slots 1 / 2 / 3 by clout (`KEY = nr_landowners_offices`), a running form is not offered again. No bureaucracy deficit check. Leader weight for option 2: Ambitious / Imperious / Master Bureaucrat / Political Appointee +10, political operator +5 / 10 / 15, Honorable +5; Reckless / Romantic -5, bribe lovers -5.
- Rule agreed with the user: cost-structure effects (institution / bureaucracy cost) go into the follow-up amendments, not into the 10-year forms.

| Form | Cost | Available | Effects (10 years, decaying) | Ended by |
|---|---|---|---|---|
| Noble Elections (default) | x1 | always | base effects only | - |
| Patrimonial Courts | x0.5 | Serfdom / Manorialism / Tenant Farmers / Latifundias | Landowners +5% strength, +1 approval, turmoil effects -5%; peasants SoL -0.25, land reform support +10% | none of those laws (popup .31, backlash reaction) |
| Justices of the Peace | x0.75 | no Serfdom / Manorialism | turmoil effects -5%, Landowners +1; Petty Bourgeoisie -5% strength | - |
| Estate Constabulary | x0.75 | No Police / Local Police | turmoil effects -10%, Landowners +5% strength; Rural Folk -10% strength, liberal support +5% | Dedicated / Militarized Police (.32, reaction) |
| Provincial Assemblies | x1.25 | no Universal Suffrage | bureaucracy +5%, Landowners +1; Rural Folk -5%, Intelligentsia -5% strength | Universal Suffrage (.33, reaction) |
| Tax Farming | x0.5 | no Proportional / Graduated Taxation | tax capacity +10%; tax waste +5%, peasants SoL -0.5 | those laws (.34, no backlash) |
| Slave Patrols | x0.5 | slavery legal | slave revolt support -15%, turmoil effects -5%; abolitionist support +10% | Slavery Banned (.35, planters) |
| State Slaves | x1 | slavery legal | construction sector +10%, mining +5%, Landowners +1; abolitionist support +10%, slave mortality +5% | Slavery Banned (.36, planters) |
| Noble Officer Corps | x1 | Peasant Levies / Professional Army | morale recovery +10%, Armed Forces +1, officers +10% strength; experience gain -10%, Intelligentsia -1 | National Militia / Mass Conscription (.37, reaction) |
| Recruit Quotas by Estate | x0.5 | Peasant Levies | conscription +10%, Landowners +1; Rural Folk -1, peasants SoL -0.25 | no Peasant Levies (.38, no backlash) |
| Naval Cadet Corps | x0.75 | coastal | prestige from navy power +10%, +1 unassigned admiral; Petty Bourgeoisie -1 | - |
| Chancery Posts for Noble Sons | x1 | Hereditary / Appointed Bureaucrats | bureaucracy +5%, aristocrats +10% strength, Landowners +1; Intelligentsia -1, tax waste +3% | Elected Bureaucrats (.39, reaction) |

- Changed from the discussion: Patrimonial Courts use peasants SoL -0.25 instead of "peasant radicals +10%" (no per-pop-type radicals modifier); Slave Patrols have no movement radicalism modifier.
- Interruption: form modifier, its bureaucracy penalty and its slot go, no follow-up; popup `nr_landowners_offices.31` - `.39` with a historical quote, options by government / opposition (`nr_campaign_react_gave_up` / `nr_campaign_react_overruled`). Called from `nr_on_law_activated` (`nr_landowners_offices_check_laws`).
- Follow-ups 10 years later (`.11` - `.21`, only with the running mark `nr_landowners_offices_<form>_running`): petition / amendment / decline -1 / thanks +2 / neutral close.

| Form | Follow-up |
|---|---|
| Patrimonial Courts | amendment Patrimonial Justice (Serfdom / Manorialism): population bureaucracy cost -5%, Landowners +5% strength, peasants SoL -0.25 |
| Justices of the Peace | thanks |
| Estate Constabulary | No Police: petition for Local Police (tech `tech_bureaucracy`); Local Police: amendment Noble Guard: police institution cost -10%, Landowners +5%, Rural Folk -5% strength |
| Provincial Assemblies | no Landed Voting (and no Universal Suffrage): petition for Landed Voting (tech `democracy`); Landed Voting: amendment Noble Curia: aristocrats voting power +50, Landowners +5% strength, liberal support +5% |
| Tax Farming | thanks |
| Slave Patrols | amendment Patrol Statute (any legal slavery law): slave revolt support -10%, Landowners +1, abolitionist support +5% |
| State Slaves | amendment Slaves of the Nation (any legal slavery law): construction sector +5%, Landowners +1, abolitionist support +5% |
| Noble Officer Corps | amendment Noble Commissions (Peasant Levies / Professional Army): military wages -10%, officers +10% strength, experience gain -5% |
| Recruit Quotas by Estate | thanks |
| Naval Cadet Corps | amendment Naval Census (any navy law): navy goods cost -5%, prestige from navy power +10% |
| Chancery Posts | Appointed Bureaucrats: petition for Hereditary Bureaucrats; Hereditary: amendment Service Census: population bureaucracy cost -5%, Intelligentsia -5% strength, Landowners +1 |

- Amendments: sponsor Landowners, no authority cost; the leader rule applies (not offered if the Landowners leader is against the parent law).
- Enactment events `nr_landowners_enact.7` - `.14` (same pattern as `.1` - `.6`; not while the form whose follow-up offers the amendment is running):

| Event | Amendment | While enacting | c: who decides |
|---|---|---|---|
| .7 | Patrimonial Justice | Serfdom / Manorialism | Rural Folk |
| .8 | Noble Guard | Local Police | Rural Folk |
| .9 | Noble Curia | Landed Voting | Intelligentsia |
| .10 | Patrol Statute | any legal slavery law | Intelligentsia |
| .11 | Slaves of the Nation | any legal slavery law | Industrialists |
| .12 | Noble Commissions | Peasant Levies / Professional Army | Armed Forces |
| .13 | Naval Census | any navy law | Petty Bourgeoisie |
| .14 | Service Census | Hereditary Bureaucrats | Intelligentsia |
- Every form: lore line + historical concept (noble assemblies after 1785; Prussian patrimonial courts until 1849, Russian until 1861; English JPs until the county councils of 1888; Prussian manorial police until 1872, Russian elected district police chief until 1862; zemstvos 1864; poll tax through the landowner, tax farming; Southern slave patrols; Brazil's slaves of the nation, El Cobre until 1800, Capitol built partly by hired slaves; Junker officer corps, purchase of commissions until 1871; Russian recruit levies until 1874; Naval Cadet Corps; Table of Ranks 1722, Prussian Landrat).
- Files: `common/scripted_effects/nr_landowners_offices_effects.txt`, `common/scripted_triggers/nr_landowners_offices_triggers.txt`, `common/script_values/nr_landowners_offices_values.txt`, `common/static_modifiers/nr_landowners_offices_modifiers.txt`, `common/amendments/nr_landowners_offices_amendments.txt`, `common/journal_entries/nr_landowners_offices_je.txt` (petitions police / landed / hereditary), `events/nr_landowners_offices_events.txt`, `localization/*/nr_landowners_offices_l_*.yml`, concepts in `nr_game_concepts.txt`. Debug: `event nr_debug.8` (form event and every follow-up).
