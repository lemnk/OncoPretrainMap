$ErrorActionPreference = "Stop"

function Invoke-CheckedPython {
    & python @args
    if ($LASTEXITCODE -ne 0) {
        throw "Python stage failed with exit code ${LASTEXITCODE}: $($args -join ' ')"
    }
}

Invoke-CheckedPython src\seed_from_pathbench.py
Invoke-CheckedPython src\build_exposure_registry.py
Invoke-CheckedPython src\audit_pathbench.py
Invoke-CheckedPython src\analyze_registry_strata.py
Invoke-CheckedPython src\analyze_performance_by_exposure.py
Invoke-CheckedPython src\create_validation_sample.py
Invoke-CheckedPython src\summarize_human_verification.py
Invoke-CheckedPython src\freeze_review_versions.py
Invoke-CheckedPython src\acquire_campanella_benchmark.py
Invoke-CheckedPython src\audit_campanella_transport.py
Invoke-CheckedPython src\sensitivity_campanella_blanket.py
Invoke-CheckedPython src\make_figures.py
Invoke-CheckedPython -m pytest -q
Invoke-CheckedPython src\make_manifest.py
