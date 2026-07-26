import argparse
from functools import partial
from pathlib import Path

import numpy as np
from tqdm.contrib.concurrent import process_map

from lrp import read, write
from lrp.strategies import STRATEGIES


def tabulate(headers: list[str], rows: np.ndarray) -> str:
    """
    Creates a simple table from the given header and row data.
    """
    # These lengths are used to space each column properly.
    lens = [len(header) for header in headers]

    for row in rows:
        for idx, cell in enumerate(row):
            lens[idx] = max(lens[idx], len(str(cell)))

    header = [
        "  ".join(f"{hdr:<{ln}s}" for ln, hdr in zip(lens, headers)),
        "  ".join("-" * ln for ln in lens),
    ]
    content = [
        "  ".join(f"{c!s:>{ln}s}" for ln, c in zip(lens, r)) for r in rows
    ]

    return "\n".join(header + content)


def _solve(
    instance: Path,
    strategy: str,
    seed: int,
    scale: int,
    max_runtime: float,
    sol_dir: Path | None,
) -> tuple[str, str, float, int, float]:
    """
    Solves a single instance and optionally writes its solution.

    Returns a tuple with the instance name, whether the solution is feasible,
    the solution cost, the number of iterations, and the runtime.
    """
    data = read(instance, scale=scale)
    result = STRATEGIES[strategy](data, max_runtime, seed)

    if sol_dir is not None:
        sol_dir.mkdir(parents=True, exist_ok=True)
        write(sol_dir / f"{instance.stem}.sol", data, result, scale=scale)

    return (
        instance.stem,
        "Y" if result.is_feasible() else "N",
        round(result.cost() / scale, 2),
        result.num_iterations,
        round(result.runtime, 3),
    )


def benchmark(instances: list[Path], num_procs: int, **kwargs):
    """
    Solves the given instances and prints a table with the results.
    """
    args = sorted(instances)
    func = partial(_solve, **kwargs)

    if len(args) == 1:
        res = [func(args[0])]  # type: ignore[misc]
    else:
        res = process_map(func, args, max_workers=num_procs, unit="instance")

    dtypes = [
        ("inst", "U37"),
        ("ok", "U1"),
        ("obj", float),
        ("iters", int),
        ("time", float),
    ]
    data = np.asarray(res, dtype=dtypes)
    headers = ["Instance", "OK", "Obj.", "Iters. (#)", "Time (s)"]

    print("\n", tabulate(headers, data), "\n", sep="")
    print(f"     Avg. objective: {data['obj'].mean():.2f}")
    print(f"    Avg. iterations: {data['iters'].mean():.0f}")
    print(f"      Avg. run-time: {data['time'].mean():.2f}s")
    print(f"       Total not OK: {np.count_nonzero(data['ok'] == 'N')}")


def main():
    parser = argparse.ArgumentParser()

    msg = "One or more paths to the instance(s) to solve."
    parser.add_argument("instances", nargs="+", type=Path, help=msg)

    msg = "Solving strategy to use. Default 'direct'."
    parser.add_argument(
        "--strategy", choices=STRATEGIES, default="direct", help=msg
    )

    msg = "Seed to use for reproducible results. Default 0."
    parser.add_argument("--seed", type=int, default=0, help=msg)

    msg = "Factor for scaling costs and distances to integers. Default 100."
    parser.add_argument("--scale", type=int, default=100, help=msg)

    msg = "Maximum runtime per instance, in seconds. Default 60."
    parser.add_argument("--max_runtime", type=float, default=60, help=msg)

    msg = "Number of processors to use for solving. Default 1."
    parser.add_argument("--num_procs", type=int, default=1, help=msg)

    msg = "Directory to write solution files to. Default 'solutions'."
    parser.add_argument(
        "--sol_dir", type=Path, default=Path("solutions"), help=msg
    )

    benchmark(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
