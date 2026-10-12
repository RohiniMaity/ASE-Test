# ASE-Test

`check_deps.py` checks every line of a requirements file against the PyPI JSON API
and reports packages that don't exist, pinned versions that don't exist, and the
oldest pinned release.

```
python3 check_deps.py requirements.txt
```

Standard library only (`urllib`, `json`).

## Note on the sample output

The task's sample input (`sample_requirements.txt`) is expected to give
`Packages not on PyPI: 1` and `Versions not on PyPI: 1`. Run today (October 2026),
the script gives:

```
Dependencies checked: 5
Packages not on PyPI: 3
Versions not on PyPI: 0
Oldest pinned release: numpy==1.16.0 (2019)
```

This is because PyPI has changed, not because of a bug. `f1ask`, `huggingface-cli`
and `pyyam1` all return 404 from both `https://pypi.org/pypi/<name>/json` and
`https://pypi.org/simple/<name>/`. These are typo or invented names of the kind the
task describes; they were most likely registered on PyPI when the sample was
written and have since been taken down. (`huggingface-cli` is a known case: a
security researcher registered it in 2024 to demonstrate this attack.) The script
reports what PyPI says when it runs, so it does not hardcode any names.
