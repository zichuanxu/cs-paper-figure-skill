#!/usr/bin/env python3
"""Generate the explicitly SYNTHETIC inputs used by this figure.

The simulation is an explanatory fixture, not an agent evaluation. All stochastic
draws are preserved before policies run. Independent seed blocks are spawned from
one fixed master SeedSequence; a block's policies and budgets share random draws.
"""
from __future__ import annotations
import csv
import gzip
import json
from collections import OrderedDict
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def write_csv_gz(path, rows, fields):
    # Fixed gzip mtime makes exact input regeneration auditable.
    import io
    with path.open('wb') as raw:
        with gzip.GzipFile(filename='', fileobj=raw, mode='wb', mtime=0) as gz:
            with io.TextIOWrapper(gz, encoding='utf-8', newline='') as txt:
                out = csv.DictWriter(txt, fieldnames=fields)
                out.writeheader()
                out.writerows(rows)


def main():
    cfg = json.loads((ROOT/'inputs/study_config.json').read_text())
    scenarios, outcomes, seed_manifest = [], [], []
    seeds = np.random.SeedSequence(cfg['master_seed']).spawn(cfg['n_seeds'])
    for seed_id, ss in enumerate(seeds):
        rng = np.random.default_rng(ss)
        seed_manifest.append({'seed': seed_id, 'entropy': ss.entropy,
                              'spawn_key': list(ss.spawn_key)})
        block_effect = float(rng.normal(0, .045))
        for family in cfg['task_families']:
            task = family['id']
            family_effect = float(rng.normal(0, .025))
            weights = np.arange(1, family['key_space']+1, dtype=float)**(-family['zipf'])
            weights /= weights.sum()
            # A random permutation avoids privileged key IDs across seed blocks.
            key_order = rng.permutation(family['key_space'])
            seen_invalid = set()
            stream = []
            for episode in range(cfg['episodes_per_stream']):
                key = int(key_order[rng.choice(family['key_space'], p=weights)])
                difficulty = float(rng.normal(0, .075))
                baseline = float(np.clip(family['baseline']+block_effect+family_effect+difficulty, .08, .92))
                proposed = int(rng.uniform() < family['proposal_rate'])
                invalid = int(proposed and rng.uniform() < family['invalid_proposal_rate'])
                # A recurring invalid proposal has an identical (key, wrong-value)
                # signature, so the ledger is capable of recognizing it.
                signature = f'{key}:wrong' if invalid else (f'{key}:correct' if proposed else '')
                repeat = int(invalid and signature in seen_invalid)
                if invalid:
                    seen_invalid.add(signature)
                item = {'seed': seed_id, 'family': task, 'episode': episode,
                        'key': key, 'baseline_probability': round(baseline, 9),
                        'proposed': proposed, 'invalid_proposal': invalid,
                        'proposal_signature': signature, 'repeat_invalid_proposal': repeat,
                        'success_uniform': round(float(rng.uniform()), 9),
                        'checker_uniform': round(float(rng.uniform()), 9),
                        'base_model_tokens': int(round(family['base_tokens']*rng.lognormal(0, .12)))}
                scenarios.append(item)
                stream.append(item)
            for budget in cfg['budgets_tokens']:
                for policy in cfg['policies']:
                    keep_history = policy == 'verified'
                    record_cap = (int(budget*(1-cfg['history_fraction']))//cfg['record_tokens']
                                  if keep_history else budget//cfg['record_tokens'])
                    history_cap = (int(budget*cfg['history_fraction'])//cfg['rejection_hash_tokens']
                                   if keep_history else 0)
                    records, ledger = OrderedDict(), OrderedDict()
                    for item in stream:
                        key, invalid, proposed = item['key'], item['invalid_proposal'], item['proposed']
                        record = records.get(key)
                        valid_read = int(record is True)
                        corrupt_read = int(record is False)
                        # Reads update record recency; all initial states are empty.
                        if record is not None:
                            records.move_to_end(key)
                        occupancy = len(records)*cfg['record_tokens']+len(ledger)*cfg['rejection_hash_tokens']
                        probability = float(np.clip(item['baseline_probability']+
                            valid_read*family['valid_benefit']-corrupt_read*family['invalid_harm'], .02, .98))
                        success = int(item['success_uniform'] < probability)
                        checked = blocked = accepted = rejected = 0
                        if policy != 'none' and proposed:
                            signature = item['proposal_signature']
                            if keep_history and signature in ledger:
                                blocked = 1
                                ledger.move_to_end(signature)
                            elif policy == 'unfiltered':
                                accepted = 1
                            else:
                                checked = 1
                                accepted = int(item['checker_uniform'] < cfg['false_accept_probability']
                                               if invalid else item['checker_uniform'] >= cfg['false_reject_probability'])
                                rejected = 1-accepted
                                # The policy sees the checker result, never ground truth.
                                # False rejections are also remembered and can hurt.
                                if keep_history and rejected:
                                    ledger[signature] = True
                                    ledger.move_to_end(signature)
                                    while len(ledger)>history_cap:
                                        ledger.popitem(last=False)
                            if accepted:
                                records[key] = not bool(invalid)
                                records.move_to_end(key)
                                while len(records)>record_cap:
                                    records.popitem(last=False)
                        total_tokens = (item['base_model_tokens']+occupancy+
                            checked*cfg['verifier_model_tokens']+
                            accepted*cfg['memory_write_model_tokens']+
                            (cfg['history_lookup_model_tokens'] if keep_history and proposed else 0))
                        outcomes.append({'seed': item['seed'], 'family': task, 'budget_tokens': budget,
                            'policy': policy, 'episode': item['episode'], 'key': key, 'success': success,
                            'success_probability': round(probability, 9), 'valid_read': valid_read,
                            'corrupt_read': corrupt_read, 'proposed': proposed, 'invalid_proposal': invalid,
                            'repeat_invalid_proposal': item['repeat_invalid_proposal'], 'checked': checked,
                            'blocked_by_history': blocked, 'rejected_by_checker': rejected,
                            'accepted_update': accepted, 'invalid_write': accepted*invalid,
                            'repeat_invalid_write': accepted*invalid*item['repeat_invalid_proposal'],
                            'resident_memory_tokens_before_update': occupancy,
                            'record_capacity': record_cap if policy!='none' else 0,
                            'history_capacity': history_cap, 'total_model_tokens': total_tokens})
    write_csv_gz(ROOT/'inputs/scenarios.csv.gz', scenarios, list(scenarios[0]))
    write_csv_gz(ROOT/'inputs/observations.csv.gz', outcomes, list(outcomes[0]))
    (ROOT/'inputs/seed_manifest.json').write_text(json.dumps(seed_manifest, indent=2)+'\n')
    print(f'SYNTHETIC DATA: {len(scenarios):,} shared scenarios; {len(outcomes):,} policy/budget observations.')


if __name__ == '__main__':
    main()
