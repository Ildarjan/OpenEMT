# Article material and figure export

Read `article_material.md` for the English abstract, mathematical explanation, article outline and figure captions. Read `results_summary.md` for measured numerical comparisons.

Reproduce from the repository root:

```
node papers/lv_prosumer_instability/export_runs.js
python papers/lv_prosumer_instability/make_figures.py
```

The `figures` directory contains 300 dpi PNG previews and vector PDF/SVG versions. The `data` directory contains CSV traces, exact circuit inputs and calculated metrics. No solver or shipped example is modified by these scripts. Python requires NumPy and Matplotlib; Node uses the repository public API.

This is an English manuscript preparation package, not a submission-ready claim of a validated commercial inverter model. Read the model limitations and proposed further validation in the article material.
