# Industrialists - agreed design and implementation

Part of the developer notes; architecture, hooks, patterns and tools are in [README_NR.md](../README_NR.md).

## Feature industrialists_contracts - state contracts instead of money (negotiation option 1 for the Industrialists)
Agreed design; same scheme as the landowners' grants (`nr_softbribe_roll`, expenses x form factor, campaign slots, form event a week later: default + 3 random, 10 years decaying, follow-ups, interruption popups). Numbers are drafts.
- Roll: 80 / 20 money or contract (unchanged). Always a contract: leader Honorable or Ambitious. Always money: Grifter / Expensive Tastes / Hedonist, or no free slot.
- Rules agreed with the user: temporary bonuses to railways are pointless (railways are unprofitable, subsidised, their product is infrastructure), so the railway concession builds lines at once; cost-structure effects only in amendments.

| Form | Cost | Available | Effects | Ended by | Follow-up (10 years) |
|---|---|---|---|---|---|
| State Order (default) | x1 | always | base effects only | - | - |
| Railway Concession (France 1842, Main Society of Russian Railways 1857) | x1.25 | tech railways, an incorporated state without a railway | at once: railway level 1 in up to 2 different incorporated states without a railway (most populous; 1 if only one such state, the form is not offered if none); campaign: Industrialists +1 approval | - | amendment Guaranteed Return (economic system laws): infrastructure +5%, loan interest +0.25%, Industrialists +5% strength |
| Arms Contracts (Krupp, Armstrong, Putilov) | x1 | always | military industry throughput +10%, Armed Forces +1 | - | amendment Private Arsenals (army laws): military goods cost -5% |
| Iron Tariff (German tariff 1879, McKinley 1890) | x0.25 | no Free Trade | heavy industry throughput +10%; lower strata SoL -0.25, Petty Bourgeoisie -1 | Free Trade | Protectionism: amendment Iron Tariff (heavy industry +5%, Industrialists +1; lower strata SoL -0.25, Petty Bourgeoisie -1); otherwise petition for Protectionism |
| Mining Concession | x0.5 | always | mining throughput +10%; laborers mortality +5%, Rural Folk -1 | - | thanks |
| Colonial Charter (British South Africa Company 1889, Royal Niger Company 1886) | x0.75 | a colonial law other than no colonial affairs | colony growth +25%, Industrialists +1; infamy generation +10% | no colonial affairs | Colonial Exploitation: amendment Chartered Companies (colony growth +10%, Industrialists +5% strength, infamy generation +5%); otherwise petition for Colonial Exploitation |
| Strike Suppression (Combination Acts, Pinkertons) | x0.5 | Combination Acts or no labour associations law granting rights | Trade Unions -10% strength, turmoil effects -5%; radicals from movements +5% | a law granting the right to associate | Combination Acts: amendment Strike Law (Trade Unions -5% strength, turmoil effects -3%); otherwise petition |
| Contract Labour (Chinese workers on American and Peruvian lines) | x0.5 | no migration controls | migration attraction +10%, construction sector +5%; Petty Bourgeoisie -1 | migration controls / closed borders | thanks |

Tested in game (Industrialists): contracts form event, railway concession (two different states), Strike Suppression interruption popup, commissions form event, patent office follow-up (3 technologies + refusal), Factory Care with canteens, room in the law on economic laws (Land Bank vs Independent Bank).

### Industrialists: "Factory Care" (option 9)
Clone of the Landowners' "Paternal Care" (same SoL bar, `promise_quest_type` 105, files `nr_industrialists_sol_*`); option 9 weight 5 + 5 = 10. Campaign (button in the journal entry, 1 year + 1 year of rest, ~0.015% of GDP per week, ended early: Industrialists -2 for 2 years; files `nr_industrialists_canteens_*`):
- Factory Canteens (Owen at New Lanark, Krupp in Essen): lower strata SoL +1, food security +2%, radicals from movements -10%, throughput of all buildings -5%. The only campaign (the user removed the company store).

### Industrialists: heavy industry that pays (options 5 and 6)
Agreed with the user. When vanilla gives the Industrialists a heavy industry building (option 5) or the heavy industry group (option 6), the promise becomes ours (`promise_quest_type` 103, journal entry `je_nr_industrialists_healthy`):
- always a specific building type: option 5 keeps the vanilla type (heavy industry: steel mill, chemical plant, explosives factory, synthetics plant, motor industry, automotive industry, electrics industry); option 6 picks one of those types the country already has instead of the whole group;
- target X = the type's current levels + N, so X is always above what exists; N is the vanilla increase (option 5: `building_level_increase`; option 6: the group increase), both with our logarithmic scaler;
- completed when X levels of the type are healthy (`occupancy >= 0.9`, `weekly_profit > 0`, `is_subsidized = no`, `nr_industrialists_healthy_levels`) for 6 months in a row (progress bar `nr_industrialists_healthy_bar` 0-6, +1 per month at the target, reset to 0 otherwise; the bar reads country copies `_type_c` / `_target_c`); trade subventions and tariffs are the player's levers, only building subsidies are excluded; 10 years as a vanilla timeout (visible countdown), +3 with the vanilla extension button; vanilla completion / failure effects; wording "profitable";
- hooks: `nr_industrialists_healthy_prepare` in `nr_negotiation_after_options` (targets for the option tooltips, vars `_type_5 / _target_5 / _type_6 / _target_6` on the group), options `negotiation.1.o5` / `.o6` call `nr_industrialists_healthy_start` instead of the vanilla promise when prepared. Railways and power plants (option 5) stay vanilla.

## Feature industrialists_commissions - places in the commissions (negotiation option 2 for the Industrialists)
Agreed design; same scheme as the Devout church officials and the landowners' places in the provinces (vanilla bureaucracy penalty x form factor, Industrialists +12 / 24 / 36% strength, form event a week later, slots 1 / 2 / 3).

| Form | Cost | Available | Effects (10 years, decaying) | Ended by | Follow-up |
|---|---|---|---|---|---|
| Exchange Committee (default) | x1 | always | base effects only | - | - |
| Ministry of Ways and Communications (Russia 1865) | x1.25 | always | infrastructure construction efficiency +20%, Industrialists +5% strength; Landowners -1 | - | thanks |
| Patent Office (US 1836, German patent law 1877) | x0.75 | always | tech spread +10%, Intelligentsia +1; Petty Bourgeoisie -1 | - | three random researchable production technologies to choose from (fewer if not enough), the chosen one gets a third of its era cost (2500 / 3500 / 4150 / 5000 / 5850, vanilla convention); none: thanks; a neutral refusal is always available (roleplay) |
| Company Law Commission (British Companies Act 1862, French 1867) | x1 | no Command Economy / Cooperative Ownership | company throughput +5%, company construction efficiency +10%; Petty Bourgeoisie -1 | those laws | amendment Limited Liability (Laissez-Faire / Interventionism): company throughput +3%, private construction allocation +5% |
| Factory Inspection in the Owners' Hands | x0.75 | Regulatory Bodies / Worker Protections | manufacturing throughput +5%; laborers mortality +5%, Trade Unions -2 | No Workers' Rights | amendment Mild Oversight (same laws): manufacturing +3%, Trade Unions -5% strength |
| Consular Service | x0.75 | always | leverage generation +10%, influence +5% | - | thanks |
| State Bank in the Bankers' Hands (Bank of England, Banque de France 1800, Russian State Bank 1860) | x1 | no Command Economy | private construction allocation +10%, Industrialists +5% strength; minting -10% | Command Economy | amendment Independent Bank (Laissez-Faire / Interventionism): loan interest -0.5%, minting -5% |

- Room in the law: new opposing pairs - economic system laws: Industrialists - Landowners; labour laws (workers' rights, labour associations): Industrialists - Trade Unions.
- Enactment events `nr_industrialists_enact.1` - `.8` (pattern of the Landowners'; c: Guaranteed Return / Iron Tariff / Limited Liability - Petty Bourgeoisie, Private Arsenals - Armed Forces, Chartered Companies - Intelligentsia, Strike Law / Mild Oversight - Trade Unions, Independent Bank - Landowners).
- Petitions (4 years, +25% speed, timeout -2): Protectionism, Colonial Exploitation, Combination Acts (`je_nr_industrialists_<key>_petition`).
- Interruption popups: contracts `.21` - `.24` (Iron Tariff, Colonial Charter, Strike Suppression, Contract Labour), commissions `.31` - `.33` (Company Law, Factory Inspection, State Bank).
- Files: `common/scripted_effects/nr_industrialists_effects.txt`, `common/scripted_triggers/nr_industrialists_triggers.txt`, `common/script_values/nr_industrialists_values.txt`, `common/static_modifiers/nr_industrialists_modifiers.txt`, `common/amendments/nr_industrialists_amendments.txt`, `common/journal_entries/nr_industrialists_je.txt`, `events/nr_industrialists_contracts_events.txt`, `events/nr_industrialists_commissions_events.txt`, `events/nr_industrialists_enact_events.txt`, `localization/*/nr_industrialists_l_*.yml`, concepts in `nr_game_concepts.txt`. Debug: `event nr_debug.9` (contracts), `event nr_debug.10` (commissions).
