# ASE-Test

`check_deps.py` checks every line of a requirements file against the PyPI JSON API
and reports packages that don't exist, pinned versions that don't exist, and the
oldest pinned release.

```
python3 check_deps.py requirements.txt
```

Standard library only (`urllib`, `json`).
