# PyVRP quickstart for the SMIO-Hexaly Location Routing Challenge Monterrey 2026

This repository contains the [PyVRP](https://github.com/PyVRP/PyVRP/) quickstart for the [SMIO-Hexaly Location Routing Challenge Monterrey 2026](https://smiochallenge.com/).
It includes a modified version of PyVRP that supports location routing problems (LRPs) through depot fixed costs and capacities, as well as utility functions for the challenge.
The goal is to give participants of the challenge a working starting point to build and extend an LRP solver based on PyVRP.

## Installation

We recommend using this repository as template (click on the green button in the top-right corner).

This project uses [`uv`](https://docs.astral.sh/uv/) to manage its Python dependencies.
PyVRP is built from source during installation.
Make sure you have a reasonably modern C++ compiler available on your system.
Any recent version that supports most of the C++20 standard should work.
To install the project, run:

```bash
uv sync
```

## Solving instances

The default solving strategy is `direct`, which solves the full LRP instance with our modified PyVRP version.

```bash
uv run lrp data/mock/mock_small_loose.txt --strategy direct --sol_dir solutions --max_runtime 60
```

This writes a solution file to `solutions/mock_small_loose.sol`.

Use `--strategy decomposition` to use our decomposition heuristic, which first selects the candidate depots, and then uses PyVRP to route the restricted LRP instance:

```bash
uv run lrp data/mock/mock_small_loose.txt --strategy decomposition --sol_dir solutions --max_runtime 60
```

You can pass multiple instances at once and solve them in parallel with `--num_procs`:

```bash
uv run lrp data/mock/*.txt --num_procs 10
```

For all available parameters and their defaults, run:

```bash
uv run lrp --help
```

## Why use PyVRP for LRPs?

[PyVRP](https://github.com/PyVRP/PyVRP) is an open-source vehicle routing problem (VRP) solver.
It works well for routing problems with capacities, multiple depots, and time windows.
Out of the box, however, it does not support LRPs, which add fixed costs and capacities for depots.
We provide a modified version that does support these (see the [`pyvrp`](https://github.com/AppliedRouting/Location-Routing-Challenge/tree/pyvrp) branch).

This repository ships two solving strategies.

### Direct solve

The `direct` strategy solves the full LRP instance with PyVRP, which evaluates routes using the depot fixed costs and capacities in the problem data.
This works, but the support is barebones: PyVRP's search algorithm is built around classic vehicle routing problems, whereas depot selection is treated more as a side effect.
It is the default baseline, and works reasonably well on smaller instances (<1000 nodes).

### Decomposition

The `decomposition` strategy uses PyVRP as the routing solver and adds a depot-selection step around it.
It mainly helps on larger instances, where the `direct` approach is not tuned for the workload.

We implemented a simple cluster-first approach:

1. assign each customer to its nearest depot, and keep every depot that is nearest to at least one customer;
2. if that subset cannot serve all demand within depot and vehicle capacity, add depots in order of increasing fixed cost until it can;
3. pass the resulting candidate depots to PyVRP for routing.

Our decomposition strategy here is intentionally minimal, so think of it as a starting point for more advanced methods.

### Suggestions for participants

The `strategies/` folder is the easiest place to start experimenting.
Useful directions include:

- selecting better candidate depot subsets before routing;
- trying several depot subsets and keeping the best routed result;
- warm-starting routing runs from previous solutions;
- providing better initial solutions;
- tuning PyVRP parameters for short time limits.

For decomposition strategies from the literature, see:

- [Schneider, M., & Löffler, M. (2019). Large composite neighborhoods for the capacitated location-routing problem. _Transportation Science, 53(1)_, 301-318.](https://pubsonline.informs.org/doi/10.1287/trsc.2017.0770)
- [Arnold, F., & Sörensen, K. (2021). A progressive filtering heuristic for the location-routing problem and variants. _Computers & Operations Research, 129_, 105166.](https://www.sciencedirect.com/science/article/abs/pii/S0305054820302835)

More advanced work can be done inside the PyVRP fork itself, for example:
- adding perturbation operators that target depot usage;
- adding search operators that change depot usage directly.

## Results

The table below compares the `direct` strategy against the Hexaly baseline solutions on the mock instances.
Each instance was solved once with a 60 second runtime on a M3 Pro.
The Hexaly baselines are taken from the [challenge practice page](https://app.smiochallenge.com/practice).

| Instance | PyVRP | Hexaly | Gap |
| --- | ---: | ---: | ---: |
| mock_small_consolidation | 16522.66 | 16271.05 | +1.55% |
| mock_small_loose | 28996.74 | 29600.47 | -2.04% |
| mock_small_loose_clustered | 23608.01 | 23730.63 | -0.52% |
| mock_small_moderate | 39311.01 | 40181.44 | -2.17% |
| mock_small_tight | 40310.32 | 41676.97 | -3.28% |
| mock_small_asym_depot_binding | 36406.55 | 37436.32 | -2.75% |
| mock_small_asym_vehicle_binding | 39959.88 | 41559.40 | -3.85% |
| mock_medium_loose | 55646.47 | 56457.52 | -1.44% |
| mock_medium_moderate | 72810.21 | 73582.52 | -1.05% |
| mock_medium_tight | 61908.35 | 64802.84 | -4.47% |

PyVRP improves on the Hexaly baseline for 9 of the 10 instances, by about 2% on average.
Note that these mock instances are small, with up to 900 customers and 28 depots.
The real challenge includes much larger instances of up to 3000 customers and 50 depots, where depot selection plays a bigger role and the `direct` strategy is expected to struggle.
We provide additional instances generated with the official challenge generator in [`data/`](data/).

## Getting help

Support for this repository is limited.
For details on the challenge's LRP, please refer to [the challenge website](https://smiochallenge.com/).
Please do not email us with questions about this codebase. 
Open an issue only for reproducible bugs.

## License

This repository is provided under the MIT License by [Applied Routing](https://appliedrouting.com).
