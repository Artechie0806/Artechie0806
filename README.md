# Aryan Rane

BTech CS (AIML) graduate, now an AI engineer working full-time on LLM inference infrastructure — the unglamorous-but-satisfying work of making large models run fast and cheap on real hardware (quantization, vLLM, pushing a single 96GB box to ~150 tokens/sec and cutting inference cost ~60%). The rest of my time goes to applied ML and computer vision.

### A few things I've built

- **[DataScribe](https://github.com/Artechie0806/DataScribe)** — 7-agent LLM pipeline (router, SQL author, SQL critic, chart, narrator) over DuckDB. Read-only connection, single-SELECT guard, row caps, interrupt timeouts, and a deterministic layer that vetoes any model-proposed chart not matching the actual result shape. Exposes generated SQL and source rows behind every answer.
- **[Local Voice RAG Assistant](https://github.com/Artechie0806/Voice-Document-RAG)** — ask questions about your own documents by voice or text, fully offline, with inline citations. No cloud, no API keys. Hybrid dense + BM25 retrieval behind a LangGraph agent.
- **[Fact-Checked Research Agent](https://github.com/Artechie0806/Research-Agent)** — searches the web, drafts *atomic* claims, then hands each one to an isolated verifier that only sees that claim and its cited sources — and has to paste a verbatim supporting quote or the claim gets dropped. Runs entirely on a self-hosted Qwen model, with every LLM call budgeted to fit a 16k-token window. Keyless DuckDuckGo search, streamed live to a browser UI.
- **[Hazardous Asteroid Detection](https://github.com/Artechie0806/Asteroid-prediction)** — random forest trained on ~958k NASA records to spot potentially hazardous near-Earth objects. 94.7% accuracy after a lot of cleaning.
- **[MURA X-Ray Classification](https://github.com/Artechie0806/MURA-X-Ray-Classification-Efficientnet-)** — EfficientNet-B0 transfer-learning pipeline for musculoskeletal abnormalities, 85%+ on the MURA validation set.
- **[Space Invaders, hands-only](https://github.com/Artechie0806/space-invader-using-hand-detection)** — the arcade classic, except you fly the ship with hand gestures over your webcam (OpenCV + MediaPipe). Five enemy waves, basically no input lag.

### Tools I reach for

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Go](https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)
![vLLM](https://img.shields.io/badge/vLLM-5A189A?style=for-the-badge)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![YOLO](https://img.shields.io/badge/YOLO-111111?style=for-the-badge)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0097A7?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![FAISS](https://img.shields.io/badge/FAISS-0866FF?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![CUDA](https://img.shields.io/badge/CUDA-76B900?style=for-the-badge&logo=nvidia&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)

### Reach me

Open to AI / ML engineering roles. [Email](mailto:aryanrane.dev@gmail.com) · [LinkedIn](https://www.linkedin.com/in/aryanrane0/) · [Portfolio](https://artechie0806.github.io/portfolio/)
