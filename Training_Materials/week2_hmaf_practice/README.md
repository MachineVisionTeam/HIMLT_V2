# Week 2 Practice — HMAF: Fusing Hand-crafted and Deep Features

Practice material for **Week 2** of the HIMLT undergraduate training program
(Kennesaw State University). You will start from a raw tissue image, extract both kinds of
features yourself, then build a **positive vs. negative nucleus classifier** — the same binary
setting used in our HIMLT tool — and see how **HMAF (Hybrid Modality Attention-based Fusion)**
combines hand-crafted and deep-learned features to improve classification.

Based on the paper:

> S. Barua, S. Yellu, S. C. Koganti, J. Yun, and S. Lee,
> "HMAF: Hybrid Modality Attention for Fusing Hand-crafted and Deep-learned Features,"
> *2026 International Conference on Semantic Computing (ICSC)*, pp. 124–127, 2026.

## What the notebook covers

**Part 1 — From images to features (Steps 1–4).**
Load a real CoNSeP tissue image and its expert annotation, then extract features from it
yourself: 24 hand-crafted measurements with `scikit-image`, and 2048 deep features with
ResNet-50, compressed to 128 with PCA. You end up with your own feature file in exactly the
same format as the prepared dataset used in Part 2.

**Part 2 — Using the features (Steps 5–12).**
Doing Part 1 for all 41 images takes about half an hour, so it has been done in advance.
Load the prepared dataset and compare four approaches:

| # | Approach | Features used |
|---|----------|---------------|
| A | Hand-crafted only | 24 |
| B | Deep only | 128 |
| C | Simple concatenation | 24 + 128 = 152 |
| D | **HMAF fusion** | attention-fused + originals |

The notebook finishes by inspecting the attention weights and showing the model's predictions
on real nuclei, side by side with the expert annotation — including the mistakes.

**Task:** *Epithelial vs. Others* — is a nucleus an epithelial cell (positive) or not (negative)?

## What's in this repository

| File | Description |
|------|-------------|
| `Week2_HMAF_Practice.ipynb` | The practice notebook — run it cell by cell, top to bottom |
| `results/` | Reference outputs (comparison table and plots) so you can check your run |

## Files you need in Google Drive

The notebook reads its data from your Google Drive, so put these in **`MyDrive`** before you
start:

| File | Where it goes | Needed for |
|------|---------------|------------|
| `consep_features_24hand_128deep.csv` (~61 MB) | `MyDrive/` | Part 2 |
| `sample_data/` folder (`train_1.png`, `train_1.mat`, `test_12.png`) | `MyDrive/sample_data/` | Parts 1 and 2 |

Both are shared with you by your instructor. The CSV is also available here:
[download link](https://drive.google.com/file/d/1_UttTq217yQrwliRKfUbvNGAfA0HkuRR/view?usp=sharing).

> If Step 1 fails with a *file not found* error, the `sample_data` folder is not in your Drive
> yet, or it is in a subfolder. It must sit directly inside `MyDrive`.

## How to run (Google Colab — required)

1. Download `Week2_HMAF_Practice.ipynb` from this repository.
2. Go to [colab.research.google.com](https://colab.research.google.com) and open it
   (**File → Upload notebook**).
3. Run the first cell and **allow Colab to mount your Google Drive** when prompted.
4. Run the remaining cells one at a time with `Shift+Enter`, reading the text between them.

Every library the notebook uses is pre-installed on Colab: `numpy`, `pandas`, `matplotlib`,
`scikit-learn`, `scikit-image`, `scipy`, `opencv`, `xgboost`, `torch`, `torchvision`, `Pillow`
and `gdown`.

**Timing.** Part 2 runs in a couple of minutes. Part 1 is slower because it pushes every
nucleus through ResNet-50 — expect around **3 minutes on the free CPU runtime** for the 850
nuclei in `train_1`. If you want it faster, switch to a GPU runtime
(**Runtime → Change runtime type → T4 GPU**).

> The notebook is written for Colab and uses `/content/drive/...` paths throughout. To run it
> locally you would need to change those paths and install the libraries yourself.

## What you should get

Part 1 produces `my_extracted_features_train_1.csv` — 850 nuclei × 153 columns
(24 hand-crafted + 128 deep + label), the same structure as the prepared dataset.

Part 2, on the *Epithelial vs. Others* task (image-level train/test split, XGBoost classifier):

| Approach | Accuracy | F1 | ROC-AUC |
|----------|----------|-----|---------|
| A. Hand-crafted only (24 features) | 0.8023 | 0.7297 | 0.8798 |
| B. Deep only (128 features) | 0.8523 | 0.7982 | 0.9166 |
| C. Simple concatenation (152 features) | 0.8531 | 0.7982 | 0.9208 |
| **D. HMAF fusion (ours)** | **0.8550** | **0.8009** | **0.9239** |

Your numbers should match these exactly — random seeds are fixed in the notebook.

The notebook also writes plots into a `results/` folder as it runs: the four-approach
comparison, the attention-weight histogram, the confusion matrix, example nucleus predictions,
and a full-image prediction overlay. Compare them with the reference copies in this repository.

## Take-home exercises

The last cell lists four exercises — changing the positive class, swapping the classifier,
changing the projection size, and (challenge) training the attention end to end. Each is a small
edit to a single cell. Try them during the week and bring your results to the next session.

## Data credit and usage

The images and features come from the **CoNSeP dataset**:

> S. Graham, Q. D. Vu, S. E. A. Raza, A. Azam, Y. W. Tsang, J. T. Kwak, and N. Rajpoot,
> "HoVer-Net: Simultaneous segmentation and classification of nuclei in multi-tissue
> histology images," *Medical Image Analysis*, vol. 58, p. 101563, 2019.

CoNSeP is released for research use. This material is provided **for educational purposes**
within the HIMLT training program; please do not redistribute the data outside that context.

## Acknowledgment

This work was supported by the National Science Foundation under Grant No. 2409704.
