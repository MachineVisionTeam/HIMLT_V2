# HIMLT Documentation

**Publication Details** : 
**Kondreddy, D., Barua, S., Yellu, S., Elghazzali, H. and Lee, S., 2026, August. HIMLT: *A Hybrid Interactive Machine Learning Tool for Whole Slide Image Analysis.* In 2026 International Conference on Intelligent Multimedia, Networking, and Security (IMNS) (pp. 1-6). IEEE.**

**Hybrid Interactive Machine Learning Tool for Histopathology Image Analysis**


Whole-slide histopathology scans present a well-known challenge in digital
pathology: a single slide can contain hundreds of thousands of individual
cell nuclei, making manual labeling impractical at scale. At the same time,
a model trained entirely without human oversight frequently falls short of
the accuracy required for a specific slide, tissue type, or research
objective. HIMLT was designed to address this gap.

The platform's core approach is **active learning**. Rather than requiring
a large, pre-labeled dataset before training can begin, a pathologist or
researcher labels a small set of nuclei directly on the slide — as few as
four positive and four negative examples — and HIMLT trains a model on that
sample in under a second. Predictions are displayed immediately,
color-coded across the entire slide, allowing the user to review the
results and correct or supplement the labeled examples where needed.
Because each training cycle completes in seconds, this iterative process
typically converges on an accurate, slide-specific classifier within a
handful of rounds, rather than requiring substantial labeling effort
upfront.

## Where to go from here

<div class="grid cards" markdown>

- **[Project Overview](overview.md)**
  What HIMLT is built from, why each piece was chosen, and how the
  active-learning workflow moves through the stack end to end.

- **[Deployment Guide](deployment.md)**
  Step-by-step instructions to deploy HIMLT with Docker Desktop, from
  installing prerequisites through opening the app in your browser.

- **[Using HIMLT](using.md)**
  The labeling workflow, the color legend, and the day-to-day commands for
  running and managing the deployment.

- **[Troubleshooting](troubleshooting.md)**
  Common problems and their fixes, plus deeper diagnostic commands.

</div>

---


