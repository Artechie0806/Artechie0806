<!--
  github.com/Artechie0806 — profile README
  Assets: assets/cover.svg, strip-critic.svg, strip-verifier.svg, strip-dayjob.svg
  Hand-inked SVG, animating on their own — no JS, no third-party service.
  Regenerate or edit them with tools/comic.py.
  The snake image resolves once .github/workflows/snake.yml has run.
-->

<img src="./assets/cover.svg" width="100%" alt="Aryan Rane — software developer and AI/ML engineer, agentic AI systems and LLM inference infrastructure">

**AI Engineer at Innoviti Technologies, Navi Mumbai.** I build multi-agent LLM systems — and the guardrails
that stop them being confidently wrong. Routers, critics, verifiers, and deterministic checks that overrule
the model when it's wrong. Alongside that, I run the inference infrastructure they sit on.

[Email](mailto:aryanrane.dev@gmail.com) &nbsp;·&nbsp; [LinkedIn](https://www.linkedin.com/in/aryanrane0/) &nbsp;·&nbsp; [Portfolio](https://artechie0806.github.io/portfolio/) &nbsp;·&nbsp; [Résumé](https://drive.google.com/file/d/1-WEqHa_uEZNNibIU1Ulyc6HRxD-GHo0z/view)

<br>

## Projects

### DataScribe — a conversational data analyst

<img src="./assets/strip-critic.svg" width="100%" alt="A question in plain English, a critic agent rejecting the SQL author, an answer shipped with its SQL">

Upload a spreadsheet, CSV or SQLite file and ask questions in plain English. Seven agents — router, SQL
author, critic, chart agent, narrator — sit over a profiler that works out what each column means by
measuring it, so there is no data dictionary to write or maintain.

- Model-written SQL runs read-only behind a statement guard, with row caps and interrupt timeouts
- Charts are reconciled against the actual result shape before rendering — the model proposes, code decides
- Every answer arrives with the SQL that produced it and the source rows underneath

`Python` `FastAPI` `DuckDB` `Qwen` `NDJSON streaming` &nbsp;→&nbsp; [Repository](https://github.com/Artechie0806/DataScribe)

### Fact-Checked Research Agent — evidence, not just prose

<img src="./assets/strip-verifier.svg" width="100%" alt="A fluent claim, an isolated verifier seeing only the claim and its source, an unsupported verdict">

Researches a topic, breaks the draft into atomic claims, and hands each one to a separate verifier. The
agent that writes is never the agent that grades.

- The verifier sees one claim and its cited text only — never the surrounding draft that might talk it into agreeing
- Its supporting quote is located in the source by string search; when it isn't found, the verdict is downgraded automatically
- Runs on a self-hosted Qwen model with every call inside a 16k-token budget, reporting grounding rate and real token counts

`Python` `FastAPI` `Qwen` `DuckDuckGo` `Trafilatura` `SSE` &nbsp;→&nbsp; [Repository](https://github.com/Artechie0806/Research-Agent)

### AI Code Documentation & QA

Points a local LLM at a repository, splits the code along its syntax tree instead of by character count,
and writes the summaries back into the source as real docstrings.

- Every chunk is a complete class or function, carrying its file path, line range, parent class and imports
- Summaries are embedded alongside the source, so a plain-English question can actually find the right code
- Injection runs bottom-to-top so line numbers stay valid, and skips anything already documented — safe to re-run

`Python` `AST` `Ollama` `ChromaDB` `FastAPI` `Streamlit` &nbsp;→&nbsp; [Repository](https://github.com/Artechie0806/AI-code-Documentation-and-QA)

### Local Voice RAG Assistant

Ask questions about your own documents by voice or text and get answers with inline citations. Hybrid dense
+ BM25 retrieval behind a LangGraph agent, running fully offline — no cloud, no API keys, nothing leaves the
machine.

`Python` `LangGraph` `BM25` &nbsp;→&nbsp; [Repository](https://github.com/Artechie0806/Voice-Document-RAG)

<br>

## At work — AI Engineer, Innoviti Technologies (Dec 2025 – present)

<img src="./assets/strip-dayjob.svg" width="100%" alt="A 27B model on one 96GB box, quantized to 8-bit, sustaining ~150 tokens per second">

- Self-hosted Qwen3.6-27B (8-bit) on a 96GB machine — **~150 tokens/second**, a **~60% cut in inference cost**, with full control of the infrastructure
- Replaced a general vision-transformer pass with a task-specific **YOLOv11** checkbox detector — 94% detection accuracy at a fraction of the cost
- Trained a **ResNet-152** orientation classifier to clear an image-rotation bottleneck — 1,800+ images/hour at 97%
- Normalised messy free-text addresses with Gemini 2.5 Flash — 90% less processing time, **~$27,000 saved**

<br>

## Earlier projects

**[Hazardous Asteroid Detection](https://github.com/Artechie0806/Asteroid-prediction)** — Random Forest on NASA
JPL data that scored 99.99% and ROC-AUC 1.00. That was target leakage: a hazardous asteroid is *defined* by
MOID and H, and two of the five features were MOID and H. Published the finding instead of the number.

**[MURA X-Ray Classification](https://github.com/Artechie0806/MURA-X-Ray-Classification-Efficientnet-)** —
EfficientNetB0 on 36,808 radiographs. ~64% on the official patient-disjoint validation set; the flattering
85% came from a split where the same study landed on both sides.

**[Brain Stroke Detection](https://github.com/Artechie0806/Brain-Stroke-Classification)** — ViT-B/16 on brain CT
scans, ~90% on the held-out set, served through a Flask app.

**[Space Invaders, hands-only](https://github.com/Artechie0806/space-invader-using-hand-detection)** — the arcade
classic, flown with hand gestures over a webcam using MediaPipe's 21 hand landmarks.

<br>

## Skills

`agents` &nbsp; LangGraph · multi-agent orchestration · RAG · tool use · SSE / NDJSON streaming

`serving` &nbsp; vLLM · Ollama · CUDA · Docker · Linux · FastAPI · Django · Flask

`models` &nbsp; PyTorch · TensorFlow / Keras · Hugging Face · scikit-learn · Vision Transformers

`data & retrieval` &nbsp; PostgreSQL · DuckDB · SQLite · ChromaDB · Pandas · NumPy

`vision` &nbsp; OpenCV · YOLO · MediaPipe

`languages` &nbsp; Python · Java · JavaScript · SQL · Bash

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Artechie0806/Artechie0806/output/snake-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Artechie0806/Artechie0806/output/snake.svg">
  <img width="100%" alt="A snake eating my contribution graph" src="https://raw.githubusercontent.com/Artechie0806/Artechie0806/output/snake.svg">
</picture>

<sub>Happy to talk about agent systems, inference, or anything above — [aryanrane.dev@gmail.com](mailto:aryanrane.dev@gmail.com)</sub>
