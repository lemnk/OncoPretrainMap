$ErrorActionPreference = "Stop"

python src\seed_from_pathbench.py
python src\build_exposure_registry.py
python -m pytest -q
python src\make_manifest.py

