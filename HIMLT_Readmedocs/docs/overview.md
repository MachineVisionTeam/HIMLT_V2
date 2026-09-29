# Project Overview

## Software Stack & Why

Each component was chosen for a specific reason rather than as a default choice:

| Component | Technology | Why this choice |
|---|---|---|
| Frontend | React + TypeScript + OpenSeadragon | OpenSeadragon is a deep-zoom viewer built specifically for gigapixel images — necessary here since a single slide can span tens of thousands of pixels in each dimension, far too large to load or render as a normal image. React + TypeScript gives a maintainable, typed UI for the labeling interactions (clicking nuclei, toggling positive/negative, retraining). |
| Backend API | Flask + Gunicorn | Flask is lightweight and fast to iterate on for a research-driven tool; Gunicorn serves it with multiple worker processes in production so the API stays responsive while training jobs run. |
| Database | MySQL | Stores slide metadata, nuclei boundary coordinates, and labeled/predicted state — a relational model fits well since nuclei, slides, and datasets have clear structured relationships. |
| Job queue | Redis | Decouples the "train model" request from the web request/response cycle — training runs as a queued background job so the UI stays responsive instead of the browser waiting on a synchronous training call. |
| ML engine | Random Forest | Chosen specifically because it trains in well under a second on small labeled sets (4–8 examples), which is what makes the interactive labeling loop feel instant. A deep learning model would need far more labeled examples and far more training time per iteration, breaking the fast feedback loop the tool depends on. |
| Image server | IIPImage v1.3 | Serves only the visible tile/zoom-level of the whole-slide image on demand, rather than sending the full multi-gigapixel file to the browser. |
| Web server | Nginx | Routes requests to the right service (`/himlt/` to the React app, `/api/` to Flask, `/iiif/` to IIPImage) behind a single port, and handles the URL rewrites automatically. |

## How the Active Learning Workflow Works

End-to-end, a labeling round moves through the stack like this:

```text
1. User clicks nuclei as Positive/Negative in the React UI
        ↓
2. Flask API records the labels in MySQL
        ↓
3. A "train" request is queued in Redis
        ↓
4. ML Worker picks up the job, trains a Random Forest
   on the labeled examples (<1 second)
        ↓
5. Predictions for all nuclei on the slide
   are written back to MySQL
        ↓
6. React UI re-renders the slide with color-coded
   predictions (magenta = positive, cyan = negative)
        ↓
7. User reviews, labels a few more nuclei to correct
   mistakes, and repeats from step 1
```

Because each round only takes a few seconds end-to-end, a handful of
rounds (often 3–5) is usually enough to reach a usable classifier for a
given slide — without needing a large, separately-labeled training set up
front.

## Data & the ML Model

The Docker images ship pre-loaded with a sample dataset for evaluation and demos:

- **GBM dataset** — Glioblastoma Multiforme tissue
- **1 whole-slide image** — TCGA-19
- **Nuclei** across the slide, each with boundary coordinates already segmented
- **64-dimensional feature vector** per nucleus (shape, texture, and intensity
  features extracted ahead of time) — this is what the Random Forest actually
  trains on; the model never sees raw pixels directly, only these precomputed
  features per nucleus

!!! note "Testing scope"
    HIMLT was validated against two whole-slide images during development.
    Only one (TCGA-19) is bundled with the Docker deployment, since each
    additional whole-slide image adds a significant amount of storage to the
    image — it was left out here specifically to keep the Docker images
    within a manageable size.


