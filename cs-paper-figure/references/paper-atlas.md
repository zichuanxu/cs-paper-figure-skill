# Paper atlas

**Scope:** A curated study of representative figure design: 23 papers and 48 inspected figure anchors. This is not an exhaustive survey, a current model leaderboard, or a claim that any company has one visual style. Company associations refer to historical paper affiliations; joint work remains attributed.

Every entry uses a version-pinned primary PDF. Pages are **1-based PDF pages**, not printed journal pagination. All listed figures were rendered and visually inspected on 2026-10-21. Observations describe source figures; recommendations are our interpretation. Preserve uncertainty, measurement, and schematic distinctions when adapting a pattern. Do not copy artwork.

The machine-readable [source index](source-index.json) preserves exact anchors, affiliation evidence, verification methods, and PDF hashes. No source PDFs, screenshots, or artwork are bundled.

## Contents

- [Find a visual pattern](#find-a-visual-pattern)
- [OpenAI](#openai)
- [Anthropic and collaborators](#anthropic-and-collaborators)
- [Google and DeepMind](#google-and-deepmind)
- [Meta and FAIR](#meta-and-fair)
- [NVIDIA and joint systems work](#nvidia-and-joint-systems-work)
- [DeepSeek](#deepseek)
- [Tencent](#tencent)
- [Alibaba and Qwen](#alibaba-and-qwen)
- [Microsoft Research](#microsoft-research)

## Find a visual pattern

| Scientific question | Representative entries |
|---|---|
| What computation changes? | [Residual unit](#microsoft-resnet), [Transformer decomposition](#google-transformer), [attention variants](#deepseek-v2) |
| How do representations transform? | [CLIP](#openai-clip-2021), [ViT](#google-vit), [multimodal tokenization](#qwen25-vl) |
| How do training stages and feedback connect? | [InstructGPT](#openai-instructgpt-2022), [Constitutional AI](#anthropic-constitutional-ai-2022), [Llama 3](#meta-llama3) |
| What changes with scale or budget? | [Scaling laws](#openai-scaling-laws-2020), [Chinchilla](#deepmind-chinchilla), [HunyuanVideo](#hunyuanvideo) |
| What tradeoff or bottleneck matters? | [Nemotron-H](#nvidia-nemotron-h), [parallel schedules](#nvidia-megatron-2021), [Qwen latency](#qwen25) |
| What survives aggregation or uncertainty? | [Statistical Precipice](#google-rliable), [SAM evaluation](#meta-sam), [Sleeper Agents](#anthropic-sleeper-agents-2024) |
| What dynamics do endpoints conceal? | [DeepSeek-R1](#deepseek-r1), [Sleeper Agents](#anthropic-sleeper-agents-2024) |
| What geometry or qualitative evidence is visible? | [Toy Models](#anthropic-toy-superposition-2022), [MAE](#meta-mae), [Hunyuan3D](#hunyuan3d-2) |
| Where is data retained or discarded? | [HunyuanVideo](#hunyuanvideo) |

## OpenAI

### openai-scaling-laws-2020

**Scaling Laws for Neural Language Models** — OpenAI / Johns Hopkins University; first released 2020. [Inspected PDF: 2001.08361v1](https://arxiv.org/pdf/2001.08361v1).

**Anchors:** Fig. 1 (PDF p. 3).

**Observed:** Aligned plots distinguish observations, fitted laws, and learning-curve envelopes across scaling factors.

**Adapt:** Separate scale variables and distinguish measurements from fits. **Caution:** Aligned panels can have different ranges; historical fits are not new evidence.

### openai-clip-2021

**Learning Transferable Visual Models From Natural Language Supervision** — OpenAI; first released 2021. [Inspected PDF: 2103.00020v1](https://arxiv.org/pdf/2103.00020v1).

**Anchors:** Fig. 1 (PDF p. 2).

**Observed:** Training and inference panels preserve text/image colors; a similarity matrix exposes matched pairs.

**Adapt:** Carry object identity across phases and show the key computation. **Caution:** Prune repeated labels when reducing to column width.

### openai-instructgpt-2022

**Training language models to follow instructions with human feedback** — OpenAI; first released 2022. [Inspected PDF: 2203.02155v1](https://arxiv.org/pdf/2203.02155v1).

**Anchors:** Fig. 1 (PDF p. 2); Fig. 2 (PDF p. 3).

**Observed:** Model-size comparisons include confidence intervals; a separate three-column workflow identifies training phases and update routes.

**Adapt:** Separate mechanism from evidence; define baseline, arrow types, and intervals. **Caution:** Check miniature icons and explanations at final size.

## Anthropic and collaborators

### anthropic-toy-superposition-2022

**Toy Models of Superposition** — Anthropic / Harvard; first released 2022. [Inspected PDF: 2209.10652v1](https://arxiv.org/pdf/2209.10652v1).

**Anchors:** Unnumbered opening sparsity/feature-vector triptych (PDF p. 2); Unnumbered linked weight matrices and feature norms (PDF p. 11); Unnumbered sparsity-relative-importance phase diagram (PDF p. 15).

**Observed:** Linked vectors, matrices, and feature bars connect local geometry with empirical and theoretical phase diagrams.

**Adapt:** Teach one representation, then reuse it across evidence. **Caution:** Unnumbered figures require descriptive anchors; toy geometry does not establish full-model geometry.

### anthropic-constitutional-ai-2022

**Constitutional AI: Harmlessness from AI Feedback** — Anthropic; first released 2022. [Inspected PDF: 2212.08073v1](https://arxiv.org/pdf/2212.08073v1).

**Anchors:** Fig. 1 (PDF p. 2); Fig. 2 (PDF p. 3); Fig. 3 (PDF p. 4).

**Observed:** Phase-separated workflow, annotated objective tradeoffs, and supporting uncertainty panels provide complementary views.

**Adapt:** Expose competing objectives and supply quantitative support for summaries. **Caution:** Schematic frontier arcs are not measured frontiers; summary uncertainty omission is not a default.

### anthropic-sleeper-agents-2024

**Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training** — Anthropic and research collaborators; first released 2024. [Inspected PDF: 2401.05566v3](https://arxiv.org/pdf/2401.05566v3).

**Anchors:** Fig. 1 (PDF p. 2); Fig. 2 (PDF p. 4).

**Observed:** Endpoint bars and checkpoint trajectories share condition encodings; captions define bootstrapped intervals.

**Adapt:** Pair endpoints with dynamics when they answer different questions. **Caution:** Constructed experimental rates do not estimate unmeasured deployment populations.

## Google and DeepMind

### google-transformer

**Attention Is All You Need** — Google; first released 2017. [Inspected PDF: 1706.03762v7](https://arxiv.org/pdf/1706.03762v7).

**Anchors:** Fig. 1 (PDF p. 3); Fig. 2 (PDF p. 4).

**Observed:** Repeated operation blocks, bypasses, multiplicity brackets, and an expanded attention operator expose topology.

**Adapt:** Reuse module grammar and show residual and masking paths. **Caution:** Verify the actual architecture; familiar silhouettes can misstate normalization or skips.

### deepmind-chinchilla

**Training Compute-Optimal Large Language Models** — DeepMind; first released 2022. [Inspected PDF: 2203.15556v1](https://arxiv.org/pdf/2203.15556v1).

**Anchors:** Fig. 1 (PDF p. 2); Fig. 3 (PDF p. 6).

**Observed:** Log-scale measurements, fits, model markers, and budget-colored loss valleys connect data to model-size decisions.

**Adapt:** Distinguish measurements, fits, and implied decisions. **Caution:** Mark extrapolation; FLOPs do not equal runtime or monetary cost.

### google-vit

**An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale** — Google; first released 2020. [Inspected PDF: 2010.11929v2](https://arxiv.org/pdf/2010.11929v2).

**Anchors:** Fig. 1 (PDF p. 3); Fig. 7 (PDF p. 9).

**Observed:** A worked image-to-token pipeline accompanies an encoder expansion and aligned representation diagnostics.

**Adapt:** Connect concrete inputs to abstract operations and diagnostic encodings. **Caution:** Attention or embedding patterns alone do not establish causality.

### google-rliable

**Deep Reinforcement Learning at the Edge of the Statistical Precipice** — Google Research / Mila, Université de Montréal; first released 2021. [Inspected PDF: 2108.13264v4](https://arxiv.org/pdf/2108.13264v4).

**Anchors:** Fig. 7 (PDF p. 7); Fig. 9 (PDF p. 8).

**Observed:** Performance profiles show pointwise bootstrap bands; aligned interval panels compare aggregate metrics.

**Adapt:** Make uncertainty and aggregation visible in the argument. **Caution:** Resampling units and estimands depend on the task/run hierarchy; RL procedures are not universal defaults.

## Meta and FAIR

### meta-mae

**Masked Autoencoders Are Scalable Vision Learners** — Facebook AI Research (FAIR; now Meta); first released 2021. [Inspected PDF: 2111.06377v3](https://arxiv.org/pdf/2111.06377v3).

**Anchors:** Fig. 1 (PDF p. 1); Fig. 2 (PDF p. 2); Fig. 3 (PDF p. 2).

**Observed:** A narrow visible-token path precedes token recombination; qualitative triplets repeat input, reconstruction, and target.

**Adapt:** Expose asymmetry through topology; match crops and processing across comparisons. **Caution:** Schematic token counts do not establish compute; disclose example selection and compositing.

### meta-sam

**Segment Anything** — Meta; first released 2023. [Inspected PDF: 2304.02643v1](https://arxiv.org/pdf/2304.02643v1).

**Anchors:** Fig. 1 (PDF p. 1); Fig. 4 (PDF p. 5); Fig. 9 (PDF p. 9).

**Observed:** Task/model/data views accompany encoder-decoder detail, signed dataset differences, ratings, and prompt-budget curves.

**Adapt:** Expose heterogeneous gains and losses; isolate reusable computation. **Caution:** Separate oracle outputs from deployable predictions and preserve sample provenance.

### meta-llama3

**The Llama 3 Herd of Models** — Meta; first released 2024. [Inspected PDF: 2407.21783v3](https://arxiv.org/pdf/2407.21783v3).

**Anchors:** Fig. 7 (PDF p. 15); Fig. 27 (PDF p. 54).

**Observed:** Typed data/model nodes explain feedback; parallel prefill/decode plots expose configurations and batching.

**Adapt:** Distinguish artifacts from operations and separate operational phases. **Caution:** Different latency definitions require hardware and batching context.

## NVIDIA and joint systems work

### nvidia-megatron-2019

**Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism** — NVIDIA; first released 2019. [Inspected PDF: 1909.08053v4](https://arxiv.org/pdf/1909.08053v4).

**Anchors:** Fig. 3 (PDF p. 4); Fig. 4 (PDF p. 5).

**Observed:** Aligned tensor-shard blocks and synchronization operators connect local computation with module-level communication.

**Adapt:** Expose boundaries that explain the bottleneck. **Caution:** Define synchronization semantics; avoid illegible equations and decorative gradients.

### nvidia-megatron-2021

**Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM** — NVIDIA / Stanford / Microsoft Research; first released 2021. [Inspected PDF: 2104.04473v5](https://arxiv.org/pdf/2104.04473v5).

**Anchors:** Fig. 3 (PDF p. 3); Fig. 4 (PDF p. 3); Fig. 6 (PDF p. 5).

**Observed:** Device timelines reveal idle regions; matched schedules accompany a quantitative bubble-fraction plot.

**Adapt:** Align timing conventions and support schematic schedules quantitatively. **Caution:** State timing assumptions; the source GPipe illustration assumes backward work takes twice forward work.

### nvidia-nemotron-h

**Nemotron-H: A Family of Accurate and Efficient Hybrid Mamba-Transformer Models** — NVIDIA; first released 2025. [Inspected PDF: 2504.03624v4](https://arxiv.org/pdf/2504.03624v4).

**Anchors:** Fig. 1 (PDF p. 2); Fig. 2 (PDF p. 3).

**Observed:** Directly labeled quality-throughput points accompany repeated hybrid-layer patterns with multiplicities.

**Adapt:** Show resource cost with quality and disclose benchmark conditions. **Caution:** Throughput depends on hardware, batching, precision, and sequence lengths; arrows do not establish universal frontiers.

## DeepSeek

### deepseek-v2

**DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model** — DeepSeek; first released 2024. [Inspected PDF: 2405.04434v1](https://arxiv.org/pdf/2405.04434v1).

**Anchors:** Fig. 2 (PDF p. 5); Fig. 3 (PDF p. 7).

**Observed:** A backbone links to mechanism zooms; aligned attention variants use hatching to identify cached state.

**Adapt:** Anchor detail to an overview and align invariant components. **Caution:** Schematic glyph counts are not quantities; dense labels need space.

### deepseek-r1

**DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning** — DeepSeek; first released 2025. [Inspected PDF: 2501.12948v1](https://arxiv.org/pdf/2501.12948v1).

**Anchors:** Fig. 2 (PDF p. 7); Fig. 3 (PDF p. 8).

**Observed:** Training trajectories compare fixed references; response length appears as a separate diagnostic.

**Adapt:** Separate performance and behavior while retaining their units. **Caution:** Sampling settings differ; the pale length region is not defined as a confidence interval in its caption.

## Tencent

### hunyuanvideo

**HunyuanVideo: A Systematic Framework For Large Video Generative Models** — Tencent; first released 2024. [Inspected PDF: 2412.03603v1](https://arxiv.org/pdf/2412.03603v1).

**Anchors:** Fig. 4 (PDF p. 4); Fig. 5 (PDF p. 5); Fig. 10 (PDF p. 9).

**Observed:** Retention/discard flows, modality lanes, and an image/video scaling grid encode distinct scientific questions.

**Adapt:** Match flow, architecture, and scaling layouts to their evidence. **Caution:** Sankey widths need defensible quantities; distinguish observations, fits, and extrapolation.

### hunyuan3d-2

**Hunyuan3D 2.0: Scaling Diffusion Models for High Resolution Textured 3D Assets Generation** — Tencent; first released 2025. [Inspected PDF: 2501.12202v1](https://arxiv.org/pdf/2501.12202v1).

**Anchors:** Fig. 2 (PDF p. 4); Fig. 7 (PDF p. 12).

**Observed:** Named shape/texture stages accompany a method-by-input grid with consistent blue mesh rendering.

**Adapt:** Separate geometry from appearance and control qualitative comparison conditions. **Caution:** Selected examples do not establish average quality; document selection and rendering.

## Alibaba and Qwen

### qwen2.5

**Qwen2.5 Technical Report** — Alibaba / Qwen; first released 2024. [Inspected PDF: 2412.15115v1](https://arxiv.org/pdf/2412.15115v1).

**Anchors:** Fig. 2 (PDF p. 17); Fig. 3 (PDF p. 18).

**Observed:** A saturated retrieval field accompanies hardware-by-model latency panels with absolute times and speedup labels.

**Adapt:** Keep absolute cost beside ratios and disclose panel scales. **Caution:** Declare sampling; saturation hides variation and red-green encoding limits accessibility.

### qwen2.5-vl

**Qwen2.5-VL Technical Report** — Alibaba / Qwen; first released 2025. [Inspected PDF: 2502.13923v1](https://arxiv.org/pdf/2502.13923v1).

**Anchors:** Fig. 1 (PDF p. 3).

**Observed:** Input dimensions, video timing, colored token spans, and an encoder expansion trace representation changes.

**Adapt:** Make input-to-token transformations explicit. **Caution:** Token-strip width can be schematic; dense detail needs decomposition.

## Microsoft Research

### microsoft-resnet

**Deep Residual Learning for Image Recognition** — Microsoft Research; first released 2015. [Inspected PDF: 1512.03385v1](https://arxiv.org/pdf/1512.03385v1).

**Anchors:** Fig. 2 (PDF p. 2).

**Observed:** A monochrome block exposes a transformation, identity bypass, addition, and mathematical labels.

**Adapt:** Explain the contribution through its smallest truthful computational unit. **Caution:** Check operation ordering before reusing the residual motif.
