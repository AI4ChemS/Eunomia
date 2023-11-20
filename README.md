![example workflow](https://github.com/github/docs/actions/workflows/test.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://eunomia.streamlit.app/)
# Eunomia
AI Agent Chemist for Developing Materials Datasets

![TOC](https://github.com/AI4ChemS/Eunomia/assets/51170839/9fa4d4a7-4997-4a8a-9483-8bea6911b131)

## Iterative-Chain-of-Verification (CoV)
Eunomia employs a chain-of-verification process iteratively to minimize the likelihood of hallucination, as well as integrating chemistry-informed knowledge into decision-making and action-taking plannings.

![cov_with_flow](https://github.com/AI4ChemS/Eunomia/assets/51170839/2db06b6f-327c-462d-a2c5-7d69737f9ce9)


Live App
--------
[https://eunomia.streamlit.app/](https://eunomia.streamlit.app/)

Example 1: Molecular Targets and Peptide Sequences
--------

[VEGFR example](https://github.com/AI4ChemS/Eunomia/assets/51170839/26350a96-e7ba-47ad-90e0-4b388d58223d)

Example 2: Water Stable Metal-organic Frameworks
--------

[Water stability example](https://github.com/AI4ChemS/Eunomia/assets/51170839/ccd89e31-e7b4-49e8-b90f-c420438e751d)

Example 3: Thermal Conductivity of Metal-organic Frameworks
--------

[Thermal conductivity example](https://github.com/AI4ChemS/Eunomia/assets/51170839/d12afb51-669c-4a3f-b9be-171bec830915)


Installation
--------

```python
pip install Eunomia@git+https://github.com/AI4ChemS/Eunomia.git
```

or you can clone the source code and install in developer mode:

```python
git clone https://github.com/AI4ChemS/Eunomia.git && cd Eunomia
pip install -e .
```
