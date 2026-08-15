# Week 2 Practice — HMAF: Fusing Hand-crafted and Deep Features

Practice material for **Week 2** of the HIMLT undergraduate training program
(Kennesaw State University). In this exercise you will build a **positive vs. negative
nucleus classifier** — the same binary setting used in our HIMLT tool — and see how
**HMAF (Hybrid Modality Attention-based Fusion)** combines hand-crafted and deep-learned
features to improve classification.

Based on the paper:

> S. Barua, S. Yellu, S. C. Koganti, J. Yun, and S. Lee,
> "HMAF: Hybrid Modality Attention for Fusing Hand-crafted and Deep-learned Features,"
> *2026 International Conference on Semantic Computing (ICSC)*, pp. 124–127, 2026.

## What's in this repository

| File | Description |
|------|-------------|
| `Week2_HMAF_Practice.ipynb` | The practice notebook — run it cell by cell, top to bottom |
| `results/` | Reference outputs (comparison table and plots) so you can check your run |

The feature file (`consep_features_24hand_128deep.csv`, ~61 MB — 24 hand-crafted +
128 deep features per nucleus, with cell-type labels and train/test split) is hosted on
Google Drive: [download link](https://drive.google.com/file/d/1_UttTq217yQrwliRKfUbvNGAfA0HkuRR/view?usp=sharing).
**You normally don't need to download it yourself** — the notebook's first cell fetches it
automatically.

## How to run (Google Colab — recommended, no installation needed)

1. Download `Week2_HMAF_Practice.ipynb` from this repository.
2. Go to [colab.research.google.com](https://colab.research.google.com) and open the notebook
   (**File → Upload notebook**).
3. Run the cells one at a time with `Shift+Enter`, reading the text between them.
   The first cell downloads the feature CSV for you (a few seconds); the whole notebook
   takes only a few minutes on the free CPU runtime.

> **Note:** files downloaded into Colab disappear when the session ends. If you come back
> later, just run the first cell again — it re-downloads the CSV automatically.

Running locally also works if you have Python 3 with `pandas`, `numpy`, `matplotlib`,
`scikit-learn`, `xgboost`, `torch`, and `gdown` installed — open the notebook with Jupyter
and run it the same way (or download the CSV from the Drive link into the same folder first).

## What you should get

Task: **Epithelial vs. Others** (image-level train/test split, XGBoost classifier):

| Approach | Accuracy | F1 | ROC-AUC |
|----------|----------|-----|---------|
| A. Hand-crafted only (24 features) | 0.8023 | 0.7297 | 0.8798 |
| B. Deep only (128 features) | 0.8523 | 0.7982 | 0.9166 |
| C. Simple concatenation (152 features) | 0.8531 | 0.7982 | 0.9208 |
| **D. HMAF fusion (ours)** | **0.8550** | **0.8009** | **0.9239** |

Your numbers should match these exactly (random seeds are fixed in the notebook).
The notebook ends with take-home exercises — try them during the week and bring your
results to the next session.

## Data credit and usage

The features in the CSV are derived from the **CoNSeP dataset**:

> S. Graham, Q. D. Vu, S. E. A. Raza, A. Azam, Y. W. Tsang, J. T. Kwak, and N. Rajpoot,
> "HoVer-Net: Simultaneous segmentation and classification of nuclei in multi-tissue
> histology images," *Medical Image Analysis*, vol. 58, p. 101563, 2019.

CoNSeP is released for research use. This material is provided **for educational purposes**
within the HIMLT training program; please do not redistribute the data outside that context.

## Acknowledgment

This work was supported by the National Science Foundation under Grant No. 2409704.
