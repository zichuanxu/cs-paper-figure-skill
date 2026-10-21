# Previous expansion: recent research figure atlas

## Contents

- [Coverage and counting](#coverage-and-counting)
- [Select a figure by design task](#select-a-figure-by-design-task)
- [The 35 additional source studies](#the-35-additional-source-studies)
- [Evidence and production cautions](#evidence-and-production-cautions)
- [Retrieve exact records](#retrieve-exact-records)

## Coverage and counting

This atlas records the **previous 35-paper / 75-anchor expansion**. At the completion of that batch, the corpus contained **76 distinct papers/reports** and **171 inspected figure anchors**, including **57 papers from 2025–2026** (37 from 2025 and 20 from 2026). The table below is that historical snapshot. For the current **120-paper / 261-anchor** coverage and latest detailed studies, use [dense-paper-atlas.md](dense-paper-atlas.md). All 35 papers added in this earlier batch were from 2025–2026.

Count each canonical paper once across arXiv versions and each numbered or explicitly identified native-web figure once. Do not count subpanels as separate figures. Assign one primary corporate family per paper for the table below while preserving actual affiliations and collaborations in the records. The year is the original submission/publication year, not a later PDF revision date. These counts describe a curated design study; they do not assert a venue ranking, acceptance status, exhaustive coverage, or uniformly good design.

| Primary corporate family | Papers/reports | From 2025–2026 | Figure anchors |
| --- | ---: | ---: | ---: |
| Alibaba / Qwen | 10 | 9 | 21 |
| Anthropic | 7 | 4 | 16 |
| DeepSeek | 9 | 8 | 23 |
| Google / DeepMind | 10 | 6 | 22 |
| Meta / FAIR | 9 | 6 | 21 |
| Microsoft Research | 5 | 4 | 9 |
| NVIDIA | 8 | 6 | 20 |
| OpenAI | 9 | 6 | 16 |
| Tencent | 9 | 8 | 23 |
| **Total** | **76** | **57** | **171** |

The original four user-selected sources remain in [the initial modern atlas](modern-paper-atlas.md): DeepSeek-V4 (`2606.19348`), Qwen3.8-Next (`2608.30320`), Cosmos 3 (`2606.02800`), and Harness² (`2610.14224`). They are useful choices for their respective tasks, not a mandatory style for every figure.

## Select a figure by design task

| Reader's task | Relevant inspected anchors | Transferable design decision |
| --- | --- | --- |
| Follow an algorithm in both a diagram and code | AlphaEvolve Fig. 2, p. 4 | Reuse the same semantic accents on modules and corresponding code identifiers; group human setup separately from the loop. |
| See what a variant changes | mHC Fig. 1, p. 1; Circuit Tracing methods diagram | Align unchanged operations and positions; allocate width by real complexity and highlight only the changed structure. |
| Track types through a multimodal model | Phi-4-Mini Fig. 1, p. 4; GR00T N1 Figs. 2/3; Qwen3-VL Fig. 1 | Carry modality identity through tokens, encoders, adapters and outputs; use token shapes and labels as redundant cues. |
| Distinguish new and reused modules | SAM 3 Figs. 4/10 | Assign a stable novelty palette, use different shapes for encoders/state/operators, and reserve a visible memory return corridor. |
| Follow a four-stage system | HY-World 2.0 Fig. 2, p. 5 | Equal stage cards with meaningful internal artifacts, repeated model footers and open gutters; each stage has a different scientific role. |
| Relate an answer to evaluation evidence | HealthBench Figs. 1/2; Monitoring Monitorability Fig. 2 | Separate generated text from rubric/evaluator evidence and use correspondence leaders rather than accidental process arrows. |
| Compare the same conditions across tasks | Perception Encoder Fig. 8, p. 11; Monitoring Monitorability Fig. 8, p. 17 | A task-by-model matrix or shared-condition small multiples replaces overlapping traces; align reference lines and scales where meaningful. |
| Explain persistent state or cached context | WorldPlay Figs. 2/4/5; Harness² | Separate the persistent memory ribbon from transient computation and give retrieval/update distinct routes. |
| Explain parallel decoding or verification | Nemotron-Labs-Diffusion Figs. 3/5; DeepSeek-V4.1-Flash Fig. 4 | Use discrete token states and aligned time/iteration rows; state whether widths encode real duration. |
| Compare operating points and resource costs | gpt-oss Fig. 3, p. 8; Phi-4-reasoning-vision Fig. 2 | Pair model colors with marker shapes; label compute settings; distinguish measured trajectories from a Pareto frontier. |

Read [reference-selection.md](reference-selection.md) for choosing complementary references and [style-recipes.md](style-recipes.md) for authored dimensions, palette roles, typography and routing. Source measurements describe an inspected figure; recipe values are recommendations for a new figure at its intended physical size.

## The 35 additional source studies

Each detailed study contains the actual figure anchor, one-based PDF page or native SVG identifier, role-based palette, typography evidence, composition, geometry, strokes, routing, transferable rules and cautions. The JSON retains exact version, PDF hash where applicable, crop bounds and evidence levels.

### OpenAI, Anthropic and Microsoft

[11 source studies, 22 figure anchors](study-openai-anthropic-microsoft.md).

| Paper/report | Year | Inspected anchors |
| --- | ---: | --- |
| [gpt-oss-120b & gpt-oss-20b Model Card](study-openai-anthropic-microsoft.md#gpt-oss) | 2025 | Figure 1 (p. 6); Figure 3 (p. 8) |
| [Monitoring Monitorability](study-openai-anthropic-microsoft.md#monitorability) | 2025 | Figure 2 (p. 4); Figure 8 (p. 17) |
| [GPT-6 Astra System Card](study-openai-anthropic-microsoft.md#astra) | 2026 | Figure 5 (p. 20); Figure 22 (p. 52) |
| [HealthBench: Evaluating Large Language Models Towards Improved Human Health](study-openai-anthropic-microsoft.md#healthbench) | 2025 | Figure 1 (p. 2); Figure 2 (p. 2) |
| [Magma: A Foundation Model for Multimodal AI Agents](study-openai-anthropic-microsoft.md#magma) | 2025 | Figure 1 (p. 1); Figure 7 (p. 8) |
| [Agent Lightning: Train ANY AI Agents with Reinforcement Learning](study-openai-anthropic-microsoft.md#agent-lightning) | 2025 | Figure 1 (p. 2); Figure 4 (p. 9) |
| [Phi-4-Mini Technical Report: Compact yet Powerful Multimodal Language Models via Mixture-of-LoRAs](study-openai-anthropic-microsoft.md#phi-mini) | 2025 | Figure 1 (p. 4); Figure 3 (p. 17) |
| [Phi-4-reasoning-vision-15B Technical Report](study-openai-anthropic-microsoft.md#phi-vision) | 2026 | Figure 2 (p. 3); Figure 3 (p. 4) |
| [Reasoning Models Don't Always Say What They Think](study-openai-anthropic-microsoft.md#reasoning-faithfulness) | 2025 | Figure 1 (p. 2); Figure 2 (p. 3) |
| [Circuit Tracing: Revealing Computational Graphs in Language Models](study-openai-anthropic-microsoft.md#anthropic-circuit-tracing) | 2025 | Opening diagram: methods-diagram-svg; Multiplicative patching: crosscoder-patching-tutorial-svg |
| [On the Biology of a Large Language Model](study-openai-anthropic-microsoft.md#anthropic-biology) | 2025 | Multi-step reasoning: dallas-capitial-big-svg; Planning in poems: poems-hero-svg |

### Google, Meta and NVIDIA

[12 source studies, 26 figure anchors](study-google-meta-nvidia.md).

| Paper/report | Year | Inspected anchors |
| --- | ---: | --- |
| [Gemma 3 Technical Report](study-google-meta-nvidia.md#gemma3) | 2025 | Figure 2 (p. 6); Figure 5 (p. 7) |
| [Gemma 4 Technical Report](study-google-meta-nvidia.md#gemma4) | 2026 | Figure 1 (p. 3) |
| [AlphaEvolve: A coding agent for scientific and algorithmic discovery](study-google-meta-nvidia.md#alphaevolve) | 2025 | Figure 2 (p. 4); Figure 3 (p. 6); Figure 8 (p. 18) |
| [Gemini Robotics: Bringing AI into the Physical World](study-google-meta-nvidia.md#gemini-robotics) | 2025 | Figure 1 (p. 2); Figure 2 (p. 3) |
| [DINOv3](study-google-meta-nvidia.md#dinov3) | 2025 | Figure 5 (p. 10); Figure 9 (p. 14) |
| [SAM 3: Segment Anything with Concepts](study-google-meta-nvidia.md#sam3) | 2025 | Figure 4 (p. 4); Figure 10 (p. 19) |
| [Perception Encoder: The best visual embeddings are not at the output of the network](study-google-meta-nvidia.md#perception-encoder) | 2025 | Figure 5 (p. 5); Figure 8 (p. 11) |
| [Efficient Universal Perception Encoder](study-google-meta-nvidia.md#eupe) | 2026 | Figure 1 (p. 2); Figure 2 (p. 4); Figure 3 (p. 5) |
| [GR00T N1: An Open Foundation Model for Generalist Humanoid Robots](study-google-meta-nvidia.md#gr00t-n1) | 2025 | Figure 2 (p. 3); Figure 3 (p. 4) |
| [Cosmos-Reason1: From Physical Common Sense To Embodied Reasoning](study-google-meta-nvidia.md#cosmos-reason1) | 2025 | Figure 1 (p. 2); Figure 6 (p. 11) |
| [Nemotron 3 Super: Open, Efficient Mixture-of-Experts Hybrid Mamba-Transformer Model for Agentic Reasoning](study-google-meta-nvidia.md#nemotron3-super) | 2026 | Figure 1 (p. 2); Figure 3 (p. 5) |
| [Nemotron-Labs-Diffusion: A Tri-Mode Language Model Unifying Autoregressive, Diffusion, and Self-Speculation Decoding](study-google-meta-nvidia.md#nemotron-diffusion) | 2026 | Figure 1 (p. 1); Figure 3 (p. 3); Figure 5 (p. 7) |

### DeepSeek, Tencent and Alibaba/Qwen

[12 source studies, 27 figure anchors](study-deepseek-tencent-alibaba.md).

| Paper/report | Year | Inspected anchors |
| --- | ---: | --- |
| [mHC: Manifold-Constrained Hyper-Connections](study-deepseek-tencent-alibaba.md#deepseek-mhc) | 2025 | Figure 1 (p. 1); Figure 4 (p. 12) |
| [DeepSeek-OCR: Contexts Optical Compression](study-deepseek-tencent-alibaba.md#deepseek-ocr) | 2025 | Figure 1 (p. 1); Figure 3 (p. 5); Figure 13 (p. 19) |
| [DeepSeek-OCR 2: Visual Causal Flow](study-deepseek-tencent-alibaba.md#deepseek-ocr2) | 2026 | Figure 3 (p. 5); Figure 5 (p. 7) |
| [DeepSeek-V4.1-Flash: Pushing the Limits of KV Cache Compression](study-deepseek-tencent-alibaba.md#deepseek-v41-flash) | 2026 | Figure 1 (p. 1); Figure 3 (p. 7); Figure 4 (p. 10) |
| [HunyuanWorld 1.0: Generating Immersive, Explorable, and Interactive 3D Worlds from Words or Pixels](study-deepseek-tencent-alibaba.md#hunyuanworld1) | 2025 | Figure 2 (p. 5); Figure 3 (p. 6) |
| [HY-World 2.0: A Multi-Modal World Model for Reconstructing, Generating, and Simulating 3D Worlds](study-deepseek-tencent-alibaba.md#hunyuanworld2) | 2026 | Figure 2 (p. 5); Figure 7 (p. 10) |
| [Hunyuan3D 2.5: Towards High-Fidelity 3D Assets Generation with Ultimate Details](study-deepseek-tencent-alibaba.md#hunyuan3d25) | 2025 | Figure 3 (p. 3); Figure 5 (p. 4) |
| [WorldPlay: Towards Long-Term Geometric Consistency for Real-Time Interactive World Modeling](study-deepseek-tencent-alibaba.md#worldplay) | 2025 | Figure 2 (p. 4); Figure 4 (p. 5); Figure 5 (p. 5) |
| [Qwen-Image Technical Report](study-deepseek-tencent-alibaba.md#qwen-image) | 2025 | Figure 6 (p. 7); Figure 10 (p. 11) |
| [Qwen3-VL Technical Report](study-deepseek-tencent-alibaba.md#qwen3-vl) | 2025 | Figure 1 (p. 3); Figure 3 (p. 25) |
| [Qwen3-TTS Technical Report](study-deepseek-tencent-alibaba.md#qwen3-tts) | 2026 | Figure 2 (p. 3); Figure 3 (p. 4) |
| [Qwen3.5-Omni Technical Report](study-deepseek-tencent-alibaba.md#qwen35-omni) | 2026 | Figure 2 (p. 3); Figure 3 (p. 4) |

## Evidence and production cautions

- **Inspect rendered figures.** An abstract or text-only PDF extraction does not establish visual style. The new records are based on inspected source figures; inaccessible candidates are excluded. The excluded Anthropic Opus 4.6 and Sonnet 4.6 cards are not part of the count.
- **Keep color and opacity together.** Qwen-Image Figure 6 includes raw red at roughly 0.2 alpha that appears pale pink. Opaque raw RGB would give a very different result. Keep the background or sample the rendered appearance and label that evidence appropriately.
- **Do not turn extraction artifacts into design tokens.** The same Qwen-Image crop returned widths of 15,875–25,400 from the PDF drawing API. These are physically implausible as page-point strokes. The inspector now flags and excludes such widths from summaries and crop padding while preserving raw values.
- **Distinguish visible fonts from metadata.** Invisible search text is not a visible font. Outlined glyphs or raster text can leave the exact family unknown. Native Anthropic SVGs declare Roboto/Roboto Mono, but a local preview used a fallback; SVG user units are not PDF points.
- **Do not copy unreadable density.** Some inspected source labels are about 3.6–5 pt. Preserve the useful structure while enlarging type, shortening excerpts, or splitting panels. Use source geometry as a relationship, not an unconditional scale.
- **Do not infer measurement from appearance.** Schedule block widths can be schematic, Sankey-like bands need not prove counts, and a connected sequence of settings is not automatically a statistical fit or Pareto frontier.
- **Define edge styles locally.** Qwen3-TTS uses dashed routes for training-only paths in one figure and optional paths in another. Record each new figure's vocabulary explicitly.
- **Keep sources reproducible and rights-aware.** The package contains original study notes and metadata, not redistributed paper PDFs or source artwork. Intermediate artifact basenames in JSON are study evidence identifiers; reproduce them from URLs, versions, hashes, pages and crops. Do not assume those intermediates are bundled files.

## Retrieve exact records

```bash
python <skill-root>/scripts/reference_catalog.py stats
python <skill-root>/scripts/reference_catalog.py search --query "modality tokens" --since 2025 --limit 6
python <skill-root>/scripts/reference_catalog.py search --company NVIDIA --query "decoding" --limit 4
python <skill-root>/scripts/reference_catalog.py show alphaevolve --figure "Figure 2"
python <skill-root>/scripts/reference_catalog.py show anthropic-circuit-tracing
```

The catalog validates duplicate canonical papers and figure anchors across [source-index.json](source-index.json), [modern-source-index.json](modern-source-index.json), and [recent-expansion-index.json](recent-expansion-index.json). Search uses transparent lexical relevance, not a quality score. Treat the structured evidence record as authoritative when a compact prose summary omits a qualification.

