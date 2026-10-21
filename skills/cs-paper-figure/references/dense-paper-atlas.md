# Dense scientific figure atlas

## Coverage and counting

**120 distinct primary papers/reports; 261 inspected figure anchors.** This revision adds 44 papers and 90 anchors to the prior 76-paper / 171-anchor collection. Of the full corpus, **96 papers (80%) first appeared in 2025–2026: 67 in 2025 and 29 in 2026**. Twenty-four earlier sources retain foundational or unusually useful visual patterns. The 44 new papers include 39 first submitted in 2025–2026 and five from 2024; later revisions do not inflate their original year.

These are curated design studies, not a ranking of the best 120 papers or a claim that all source figures are flawless. Each counted figure was inspected visually in its source study. Metadata searches alone do not count. A numbered figure is one anchor even if it has multiple panels. A paper is counted once across versions and one primary corporate family; collaborators remain in its record.

| Primary corporate family | Papers/reports | First published 2025–2026 | Figure anchors |
| --- | ---: | ---: | ---: |
| Alibaba / Qwen | 15 | 14 | 32 |
| Anthropic | 12 | 8 | 26 |
| DeepSeek | 13 | 11 | 32 |
| Google / DeepMind | 15 | 10 | 32 |
| Meta / FAIR | 14 | 10 | 31 |
| Microsoft Research | 11 | 9 | 21 |
| NVIDIA | 13 | 11 | 30 |
| OpenAI | 13 | 10 | 24 |
| Tencent | 14 | 13 | 33 |
| **Total** | **120** | **96** | **261** |

Use [paper-corpus.csv](paper-corpus.csv) for the complete 120-paper inventory, [figure-corpus.csv](figure-corpus.csv) for all 261 anchors, and [corpus-coverage.json](corpus-coverage.json) for reproducible counts. The four JSON indexes retain source-level evidence. Source PDFs and cropped artwork are not redistributed.

## What makes the new study different

The new records explicitly analyze information layers, concrete detail devices, composition, and density. A complex figure must expose its mechanism and preserve scientific correspondence across views; additional boxes and decoration are not a substitute. Read [dense-composition.md](dense-composition.md) for the production workflow.

| Design task | Strong source anchors | Original production decision |
| --- | --- | --- |
| Couple a system to a concrete instance | IdeaScientist Fig. 1; SkillOpt Fig. 2 | Give the overview, local operation, and replay distinct but connected regions. |
| Expose the exact operator | Fast BLT Fig. 5; Wan-Animate-2 Fig. 1; NSA Figs. 2/3 | Keep token IDs, tensor axes and mask semantics registered across the architecture and matrix. |
| Explain different memory timescales | Titans Fig. 2; Nested Learning Fig. 2; MIRAS Fig. 2 | Separate lifetime/scope from the forward computation and show the object being read or updated. |
| Show changing conditional objectives | Cosmos Policy Figs. 2/12 | Hold the object schema fixed; move only the conditioning/target boundary. |
| Connect search to an implemented step | R&D-Agent Fig. 2; R&D-Agent-Quant Fig. 4 | Use a budget band, a search topology, and one expanded local transformation. |
| Preserve actual transformed content | Prover-V2 Figs. 2/3; Qwen3-ASR Fig. 3; Data Formulator 2 Fig. 6 | Show concrete proof/code/token/schema fragments and exactly what changes. |
| Explain streaming and cached state | Wan Fig. 6; Wan-Animate-2 Fig. 2; DeepSeek-V3 Fig. 5 | Label time or schedule axes, availability, retained data, and return endpoints. |
| Combine intervention, case and evidence | Reward-seeking Figs. 1/5; Emergent Misalignment Fig. 6 | Preserve evidence status and controlled conditions in separate visual layers. |
| Ground a multimodal mechanism | UFO2 Figs. 7/11; DreamDojo Fig. 3; Foley Fig. 4; WorldMirror Fig. 5 | Use matched scenes and explicit time/view/scale; selected examples need selection rules. |

## Detailed studies

- [openai-anthropic-microsoft: 14 papers / 28 anchors](dense-study-openai-anthropic-microsoft.md)
- [google-meta-nvidia: 14 papers / 28 anchors](dense-study-google-meta-nvidia.md)
- [deepseek-tencent-alibaba: 14 papers / 30 anchors](dense-study-deepseek-tencent-alibaba.md)
- [user-anchors: 2 papers / 4 anchors](dense-user-anchor-study.md)

The earlier [recent atlas](recent-paper-atlas.md), [modern atlas](modern-paper-atlas.md), and [foundational atlas](paper-atlas.md) remain available. They describe previous study batches; use the current counts above.

## The 44 additional papers

| Paper/report | Corporate association | First year | Inspected anchors |
| --- | --- | ---: | --- |
| [Qwen3-ASR Technical Report](https://arxiv.org/pdf/2601.21337v1) | Alibaba / Qwen | 2026 | Figure 2 (p. 3); Figure 3 (p. 6) |
| [Wan-Animate-2: Pushing the Application Boundaries of Character Animation](https://arxiv.org/pdf/2608.06009v1) | Alibaba / Qwen | 2026 | Figure 1 (p. 5); Figure 2 (p. 7) |
| [Qwen2.5-Omni Technical Report](https://arxiv.org/pdf/2503.20215v1) | Alibaba / Qwen | 2025 | Figure 2 (p. 3); Figure 3 (p. 4); Figure 4 (p. 5) |
| [Wan-Animate: Unified Character Animation and Replacement with Holistic Replication](https://arxiv.org/pdf/2509.14055v1) | Alibaba / Qwen | 2025 | Figure 2 (p. 4); Figure 3 (p. 6) |
| [Wan: Open and Advanced Large-Scale Video Generative Models](https://arxiv.org/pdf/2503.20314v1) | Alibaba / Qwen | 2025 | Figure 6 (p. 11); Figure 21 (p. 31) |
| [AuditBench: Evaluating Alignment Auditing Techniques on Models with Hidden Behaviors](https://arxiv.org/pdf/2602.22755v4) | Anthropic | 2026 | Figure 1 (p. 2); Figure 5 (p. 8) |
| [Auditing language models for hidden objectives](https://arxiv.org/pdf/2503.10965v2) | Anthropic | 2025 | Figure 1 (p. 2); Figure 2 (p. 2) |
| [Natural Emergent Misalignment from Reward Hacking in Production RL](https://arxiv.org/pdf/2511.18397v1) | Anthropic | 2025 | Figure 1 (p. 2); Figure 6 (p. 8) |
| [SHADE-Arena: Evaluating Sabotage and Monitoring in LLM Agents](https://arxiv.org/pdf/2506.15740v2) | Anthropic | 2025 | Figure 1 (p. 2); Figure 2 (p. 2) |
| [Alignment faking in large language models](https://arxiv.org/pdf/2412.14093v2) | Anthropic | 2024 | Figure 1 (p. 2); Figure 2 (p. 4) |
| [DeepSeek-Prover-V2: Advancing Formal Mathematical Reasoning via Reinforcement Learning for Subgoal Decomposition](https://arxiv.org/pdf/2504.21801v1) | DeepSeek | 2025 | Figure 2 (p. 3); Figure 3 (p. 4) |
| [Janus-Pro: Unified Multimodal Understanding and Generation with Data and Model Scaling](https://arxiv.org/pdf/2501.17811v1) | DeepSeek | 2025 | Figure 3 (p. 3); Figure 4 (p. 8) |
| [Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention](https://arxiv.org/pdf/2502.11089v1) | DeepSeek | 2025 | Figure 2 (p. 3); Figure 3 (p. 9) |
| [DeepSeek-V3 Technical Report](https://arxiv.org/pdf/2412.19437v1) | DeepSeek | 2024 | Figure 3 (p. 10); Figure 4 (p. 12); Figure 5 (p. 13) |
| [Gold-medalist Performance in Solving Olympiad Geometry with AlphaGeometry2](https://arxiv.org/pdf/2502.03544v3) | Google / DeepMind | 2025 | Figure 4 (p. 10); Figure 14 (p. 27) |
| [It's All Connected: A Journey Through Test-Time Memorization, Attentional Bias, Retention, and Online Optimization](https://arxiv.org/pdf/2504.13173v1) | Google / DeepMind | 2025 | Figure 1 (p. 3); Figure 2 (p. 14) |
| [Nested Learning: The Illusion of Deep Learning Architectures](https://arxiv.org/pdf/2512.24695v1) | Google / DeepMind | 2025 | Figure 2 (p. 4); Figure 5 (p. 30) |
| [Towards a Science of Scaling Agent Systems](https://arxiv.org/pdf/2512.08296v3) | Google / DeepMind | 2025 | Figure 1 (p. 1); Figure 3 (p. 16) |
| [Titans: Learning to Memorize at Test Time](https://arxiv.org/pdf/2501.00663v1) | Google / DeepMind | 2024 | Figure 1 (p. 7); Figure 2 (p. 8) |
| [Fast Byte Latent Transformer](https://arxiv.org/pdf/2605.08044v1) | Meta / FAIR | 2026 | Figure 1 (p. 2); Figure 5 (p. 9) |
| [IdeaScientist: Orchestrating Agents for Grounded Scientific Ideation](https://arxiv.org/pdf/2610.04074v1) | Meta / FAIR | 2026 | Figure 1 (p. 2); Figure 2 (p. 8) |
| [PerceptionLM: Open-Access Data and Models for Detailed Visual Understanding](https://arxiv.org/pdf/2504.13180v3) | Meta / FAIR | 2025 | Figure 5 (p. 6); Figure 6 (p. 7) |
| [Pushing the Frontier of Audiovisual Perception with Large-Scale Multimodal Correspondence Learning](https://arxiv.org/pdf/2512.19687v1) | Meta / FAIR | 2025 | Figure 2 (p. 3); Figure 13 (p. 27) |
| [Movie Gen: A Cast of Media Foundation Models](https://arxiv.org/pdf/2410.13720v2) | Meta / FAIR | 2024 | Figure 8 (p. 11); Figure 17 (p. 27) |
| [Fara-7B: An Efficient Agentic Model for Computer Use](https://arxiv.org/pdf/2511.19663v1) | Microsoft | 2025 | Figure 2 (p. 3); Figure 4 (p. 5) |
| [R&D-Agent-Quant: A Multi-Agent Framework for Data-Centric Factors and Model Joint Optimization](https://arxiv.org/pdf/2505.15155v2) | Microsoft | 2025 | Figure 3 (p. 3); Figure 4 (p. 4) |
| [R&D-Agent: An LLM-Agent Framework Towards Autonomous Data Science](https://arxiv.org/pdf/2505.14738v2) | Microsoft | 2025 | Figure 2 (p. 4); Figure 3 (p. 9) |
| [UFO2: The Desktop AgentOS](https://arxiv.org/pdf/2504.14603v2) | Microsoft | 2025 | Figure 7 (p. 8); Figure 11 (p. 10) |
| [Data Formulator 2: Iterative Creation of Data Visualizations, with AI Transforming Data Along the Way](https://arxiv.org/pdf/2408.16119v2) | Microsoft | 2024 | Figure 2 (p. 3); Figure 6 (p. 7) |
| [SkillOpt: Executive Strategy for Self-Evolving Agent Skills](https://arxiv.org/pdf/2605.23904v2) | Microsoft Research | 2026 | Figure 2 (p. 4); Figure 3 (p. 12) |
| [Cosmos Policy: Fine-Tuning Video Models for Visuomotor Control and Planning](https://arxiv.org/pdf/2601.16163v1) | NVIDIA | 2026 | Figure 2 (p. 4); Figure 12 (p. 21) |
| [DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos](https://arxiv.org/pdf/2602.06949v1) | NVIDIA | 2026 | Figure 1 (p. 3); Figure 3 (p. 6) |
| [Cosmos-Transfer1: Conditional World Generation with Adaptive Multimodal Control](https://arxiv.org/pdf/2503.14492v2) | NVIDIA | 2025 | Figure 2 (p. 3); Figure 6 (p. 10) |
| [DreamGen: Unlocking Generalization in Robot Learning through Video World Models](https://arxiv.org/pdf/2505.12705v2) | NVIDIA | 2025 | Figure 2 (p. 2); Figure 3 (p. 4) |
| [World Simulation with Video Foundation Models for Physical AI](https://arxiv.org/pdf/2511.00062v2) | NVIDIA | 2025 | Figure 1 (p. 5); Figure 2 (p. 10) |
| [Measuring Reward-Seeking via Contrastive Belief Updates](https://arxiv.org/pdf/2607.18966v1) | OpenAI | 2026 | Figure 1 (p. 2); Figure 5 (p. 6) |
| [PaperBench: Evaluating AI's Ability to Replicate AI Research](https://arxiv.org/pdf/2504.01848v3) | OpenAI | 2025 | Figure 1 (p. 2); Figure 2 (p. 3) |
| [SWE-Lancer: Can Frontier LLMs Earn $1 Million from Real-World Freelance Software Engineering?](https://arxiv.org/pdf/2502.12115v4) | OpenAI | 2025 | Figure 1 (p. 2); Figure 2 (p. 2) |
| [Trading Inference-Time Compute for Adversarial Robustness](https://arxiv.org/pdf/2501.18841v1) | OpenAI | 2025 | Figure 1 (p. 3); Figure 2 (p. 5) |
| [HunyuanCustom: A Multimodal-Driven Architecture for Customized Video Generation](https://arxiv.org/pdf/2505.04512v1) | Tencent | 2025 | Figure 2 (p. 4); Figure 3 (p. 5) |
| [HunyuanPortrait: Implicit Condition Control for Enhanced Portrait Animation](https://arxiv.org/pdf/2503.18860v1) | Tencent | 2025 | Figure 2 (p. 3); Figure 3 (p. 5) |
| [HunyuanVideo-Avatar: High-Fidelity Audio-Driven Human Animation for Multiple Characters](https://arxiv.org/pdf/2505.20156v1) | Tencent | 2025 | Figure 2 (p. 4); Figure 3 (p. 5) |
| [HunyuanVideo-Foley: Multimodal Diffusion with Representation Alignment for High-Fidelity Foley Audio Generation](https://arxiv.org/pdf/2508.16930v1) | Tencent | 2025 | Figure 2 (p. 4); Figure 4 (p. 12) |
| [WorldMirror: Universal 3D World Reconstruction with Any-Prior Prompting](https://arxiv.org/pdf/2510.10726v1) | Tencent | 2025 | Figure 2 (p. 4); Figure 5 (p. 8) |

## Retrieve evidence without loading the whole corpus

```bash
python <skill-root>/scripts/reference_catalog.py stats
python <skill-root>/scripts/reference_catalog.py search --query "attention mask streaming" --since 2025 --limit 6
python <skill-root>/scripts/reference_catalog.py show ideascientist --figure "Figure 1"
python <skill-root>/scripts/reference_catalog.py show skillopt --figure "Figure 2"
```

The lookup is lexical, not a quality-ranking model. Read only the relevant study sections, then inspect the original figure when making new visual claims. Source crop sizes are not recommended reproduction sizes. A PDF font name can belong to a hidden text layer, and an opaque path can sit in a transparent group; preserve those distinctions.
