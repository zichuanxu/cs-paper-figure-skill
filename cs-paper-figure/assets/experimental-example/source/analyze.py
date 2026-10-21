#!/usr/bin/env python3
"""Paired seed-block analysis of the preserved synthetic episode observations."""
from __future__ import annotations
import csv
import gzip
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
METRICS = ['success', 'total_model_tokens', 'corrupt_read', 'repeat_invalid_write',
           'blocked_by_history', 'checked', 'invalid_write', 'valid_read']


def analyze():
    cfg = json.loads((ROOT/'inputs/study_config.json').read_text())
    families = [f['id'] for f in cfg['task_families']]
    shape = (cfg['n_seeds'], len(families), len(cfg['budgets_tokens']), len(cfg['policies']))
    sums = np.zeros(shape+(len(METRICS),), dtype=float)
    n = np.zeros(shape, dtype=int)
    f_index = {f:i for i,f in enumerate(families)}
    b_index = {b:i for i,b in enumerate(cfg['budgets_tokens'])}
    p_index = {p:i for i,p in enumerate(cfg['policies'])}
    unique = set()
    scenario_by_key = {}
    with gzip.open(ROOT/'inputs/scenarios.csv.gz', 'rt', newline='') as f:
        for row in csv.DictReader(f):
            key = (int(row['seed']), row['family'], int(row['episode']))
            assert key not in scenario_by_key
            scenario_by_key[key] = row
    family_parameters = {f['id']:f for f in cfg['task_families']}
    with gzip.open(ROOT/'inputs/observations.csv.gz', 'rt', newline='') as f:
        for row in csv.DictReader(f):
            idx = (int(row['seed']), f_index[row['family']], b_index[int(row['budget_tokens'])], p_index[row['policy']])
            key = idx+(int(row['episode']),)
            if key in unique:
                raise ValueError(f'Duplicate observation: {key}')
            unique.add(key)
            n[idx] += 1
            sums[idx] += np.array([float(row[m]) for m in METRICS])
            assert 0 <= int(row['resident_memory_tokens_before_update']) <= int(row['budget_tokens'])
            assert 0 <= float(row['success_probability']) <= 1
            assert int(row['repeat_invalid_write']) <= int(row['invalid_write']) <= int(row['accepted_update'])
            assert int(row['corrupt_read'])+int(row['valid_read']) <= 1
            scenario = scenario_by_key[(int(row['seed']),row['family'],int(row['episode']))]
            assert int(row['key']) == int(scenario['key'])
            for field in ['proposed','invalid_proposal','repeat_invalid_proposal']:
                assert int(row[field]) == int(scenario[field])
            assert int(row['success']) == int(float(scenario['success_uniform']) < float(row['success_probability']))
            pars=family_parameters[row['family']]
            expected_probability=np.clip(float(scenario['baseline_probability'])+
                int(row['valid_read'])*pars['valid_benefit']-int(row['corrupt_read'])*pars['invalid_harm'],.02,.98)
            assert abs(float(row['success_probability'])-expected_probability)<1e-8
            expected_tokens=(int(scenario['base_model_tokens'])+int(row['resident_memory_tokens_before_update'])+
                int(row['checked'])*cfg['verifier_model_tokens']+int(row['accepted_update'])*cfg['memory_write_model_tokens']+
                (cfg['history_lookup_model_tokens'] if row['policy']=='verified' and int(row['proposed']) else 0))
            assert int(row['total_model_tokens']) == expected_tokens
    assert np.all(n == cfg['episodes_per_stream']), (n.min(), n.max())
    rates = sums / n[..., None]
    # This baseline is replicated by assignment, not independent evidence.
    np.testing.assert_allclose(rates[:, :, :, p_index['none'], :],
        np.repeat(rates[:, :, :1, p_index['none'], :], len(cfg['budgets_tokens']), axis=2), atol=0)
    rng = np.random.default_rng(cfg['bootstrap_seed'])
    bootstrap = rng.integers(0, cfg['n_seeds'], size=(cfg['bootstrap_replicates'], cfg['n_seeds']))

    def estimate(seed_values):
        # The seed remains the resampling unit for every plot. Within each
        # sampled seed all families, budgets, policies and episodes stay paired.
        seed_values = np.asarray(seed_values)
        draws = seed_values[bootstrap].mean(axis=1)
        lo, hi = np.quantile(draws, [.025, .975], axis=0)
        return {'mean': np.mean(seed_values, axis=0).tolist(),
                'lo': lo.tolist(), 'hi': hi.tolist(), 'seed_values': seed_values.tolist()}

    macro = rates.mean(axis=(1,2))
    success = macro[:, :, METRICS.index('success')]*100
    pairs = [('verified', 'unfiltered'), ('verified', 'no_history'),
             ('verified', 'none'), ('unfiltered', 'none')]
    contrasts = [{'left': left, 'right': right,
                  **estimate(success[:, p_index[left]]-success[:, p_index[right]])} for left,right in pairs]
    heterogeneity = estimate((rates[:, :, :, p_index['verified'], 0]-rates[:, :, :, p_index['unfiltered'], 0])*100)
    tradeoff = {}
    for policy, pi in p_index.items():
        per_budget = rates[:, :, :, pi, :].mean(axis=1)
        tradeoff[policy] = {
            'success': estimate(per_budget[:, :, METRICS.index('success')]*100),
            'tokens': estimate(per_budget[:, :, METRICS.index('total_model_tokens')]/1000)}
    diagnostics = {}
    for metric in ['corrupt_read', 'repeat_invalid_write']:
        diagnostics[metric] = estimate(macro[:, :, METRICS.index(metric)]*100)
    result = {'data_status': cfg['data_status'], 'config': cfg,
              'raw_observation_count': int(n.sum()), 'shared_scenario_count': cfg['n_seeds']*len(families)*cfg['episodes_per_stream'],
              'shape_seed_family_budget_policy': list(shape), 'observations_per_cell': int(n.min()),
              'primary_estimand': 'Mean over independent seed blocks of the within-seed equal-weight mean over the 4 fixed task families and 4 fixed budgets of verified minus unfiltered success, in percentage points.',
              'interval_method': 'Pointwise 95% percentile bootstrap, 20,000 draws, resampling all 24 matched seed blocks as intact clusters; no family/episode resampling; no multiplicity adjustment.',
              'contrasts': contrasts, 'heterogeneity': heterogeneity, 'tradeoff': tradeoff,
              'diagnostics': diagnostics, 'macro_success': estimate(success)}
    (ROOT/'analysis.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    checks = {'complete_design': True, 'unique_observations': len(unique), 'observations_per_cell': int(n.min()),
              'independent_seed_blocks': cfg['n_seeds'], 'no_memory_exactly_repeated_across_budgets': True,
              'memory_capacity_respected': True, 'legal_probabilities': True,
              'invalid_write_subset_invariants': True, 'pointwise_intervals': True,
              'all_outcomes_link_to_identical_shared_scenarios': True,
              'all_successes_recomputed_from_shared_uniforms': True,
              'all_success_probabilities_recomputed': True,
              'all_token_costs_recomputed': True,
              'resampling_unit': 'intact matched seed block', 'bootstrap_draws': cfg['bootstrap_replicates'],
              'data_status': 'SYNTHETIC DATA'}
    (ROOT/'qa/numerical_checks.json').write_text(json.dumps(checks, indent=2)+'\n')
    return result


if __name__ == '__main__':
    a = analyze()
    for c in a['contrasts']:
        print(c['left'], '-', c['right'], f"{c['mean']:+.2f} [{c['lo']:.2f}, {c['hi']:.2f}] pp")
    for p, d in a['tradeoff'].items():
        print(p, 'success', np.round(d['success']['mean'], 2), 'tokens', np.round(d['tokens']['mean'], 2))
    print('Heterogeneity', np.round(a['heterogeneity']['mean'],2))
    print('Diagnostics', {m:np.round(v['mean'],2).tolist() for m,v in a['diagnostics'].items()})
