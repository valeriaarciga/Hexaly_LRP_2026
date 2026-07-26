# Instances and solutions

This directory stores LRP instance data, following the format specification from the official [_SMIO-Hexaly Location Routing Challenge Monterrey 2026_](https://github.com/eduardosalaz/smio_hexaly_challenge_26_generator#) repository.

Included are three instance sets:
- `mock/`: Mock instance files that were published before the start of the competition, and with 90-900 clients.
- `train/`: Development set of 30 COORDS instances for tuning, generated from [`dev-30.yaml`](dev-30.yaml) with `--seed-base 0` (seeds 30001-30030).
- `test/`: Holdout set of 30 COORDS instances for evaluation, generated from the same [`dev-30.yaml`](dev-30.yaml) with `--seed-base 100000` (seeds 130001-130030). Disjoint seeds from `train/`.

The `train/` and `test/` sets share the same config, so each holds the same 30 instance configurations: 10 small (220-400 clients), 10 medium (640-1100 clients), and 10 large (1500-3000 clients). 
They span the loose, moderate, tight, and asymmetric tightness regimes, with uniform, clustered, and mixed spatial layouts and uniform, bimodal, and cluster-proportional demand distributions. 
The large tier is large-n COORDS standing in for the official FULL_MATRIX/ZMM tier (see the config header for details).
