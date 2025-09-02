import os
import re
import sys
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from statistics import mean, median, pstdev

CORES = 10  # set to your logical core count
PROJECT_DIR = os.path.dirname(__file__)
PLAY_GAME = os.path.join(PROJECT_DIR, "play_game.py")
RUNS_ROOT = os.path.join(PROJECT_DIR, "batch_runs")

os.makedirs(RUNS_ROOT, exist_ok=True)
PNL_RE = re.compile(r"PNL:\s*([-+]?\d+(?:\.\d+)?)")

def run_once(idx: int) -> float | None:
    run_id = f"batch_{idx}_{os.getpid()}_{int(time.time()*1000)}"
    out_dir = os.path.join(RUNS_ROOT, run_id)
    os.makedirs(out_dir, exist_ok=True)

    env = os.environ.copy()
    env["RUN_ID"] = run_id
    env["OUTPUT_DIR"] = out_dir
    # isolate caches/temp to avoid collisions
    env.setdefault("PYTHONPYCACHEPREFIX", os.path.join(out_dir, "__pycache__"))
    env.setdefault("PYTHONDONTWRITEBYTECODE", "1")
    env.setdefault("TEMP", out_dir)
    env.setdefault("TMP", out_dir)
    env.setdefault("OMP_NUM_THREADS", "1")
    env.setdefault("MKL_NUM_THREADS", "1")
    env.setdefault("OPENBLAS_NUM_THREADS", "1")

    try:
        res = subprocess.run(
            [sys.executable, PLAY_GAME],
            cwd=PROJECT_DIR,
            env=env,
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"[Run {idx}] FAILED")
        if e.stdout:
            print(f"[Run {idx}] STDOUT:\n{e.stdout}")
        if e.stderr:
            print(f"[Run {idx}] STDERR:\n{e.stderr}")
        return None

    m = PNL_RE.search(res.stdout)
    if not m:
        print(f"[Run {idx}] Could not parse PNL from output.\n{res.stdout}")
        return None
    pnl = float(m.group(1))
    print(f"[Run {idx}] PNL = {pnl:.4f}")
    return pnl

def run_batch() -> tuple[list[float], float, float, float]:
    results: list[float] = []
    with ThreadPoolExecutor(max_workers=CORES) as ex:
        futures = [ex.submit(run_once, i) for i in range(CORES)]
        for fut in as_completed(futures):
            val = fut.result()
            if val is not None:
                results.append(val)
    if results:
        avg = mean(results)
        med = median(results)
        sd = pstdev(results) if len(results) > 1 else 0.0
        print(f"\nCompleted {len(results)}/{CORES} runs")
        print(f"Average PNL: {avg:.4f}")
        print(f"Median  PNL: {med:.4f}")
        print(f"Stdev   PNL: {sd:.4f}")
        return results, avg, med, sd
    else:
        print("All runs failed or produced no PNL.")
        return [], float("nan"), float("nan"), float("nan")

if __name__ == "__main__":
    BATCHES = 10  # repeat the whole process N times
    batch_avgs: list[float] = []
    for b in range(1, BATCHES + 1):
        print(f"\n===== Batch {b}/{BATCHES} =====")
        _, avg, _, _ = run_batch()
        if not (avg != avg):  # filter NaN
            batch_avgs.append(avg)

    if batch_avgs:
        overall_avg = mean(batch_avgs)
        overall_med = median(batch_avgs)
        print(f"\nOverall average of batch averages ({len(batch_avgs)} batches): {overall_avg:.4f}")
        print(f"Overall median  of batch averages ({len(batch_avgs)} batches): {overall_med:.4f}")
    else:
        print("\nNo successful batches.")