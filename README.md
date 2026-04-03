# stats-w-kev

This is the home page for all the code for my videos!

---

## Lessons

| Lesson | Status |
|---|---|
| A/A Testing | Complete |
| Intro to A/B Testing | In Progress |
| Practical T-tests | In Progress |

---

## Replicating the Codebooks

The codebooks are built with [marimo](https://marimo.io), a reactive Python notebook. This project uses `uv` for dependency management.

### Setup

**1. Install `uv`** (if you don't have it):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**2. Clone the repo and install dependencies:**
```bash
git clone <repo-url>
cd stats-w-kev
uv sync
```

### Running a Codebook

To open a marimo notebook interactively:
```bash
uv run marimo edit AA-testing/AA_testing_simulation.py
```

To run a notebook as a read-only app:
```bash
uv run marimo run AA-testing/AA_testing_simulation.py
```

To export a notebook to HTML:
```bash
uv run marimo export html AA-testing/AA_testing_simulation.py -o output.html
```
