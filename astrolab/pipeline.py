"""Pipeline orchestration - the shared entry point everyone's work plugs into.

This file is intentionally incomplete: most steps below are stubs. Each
stub is a task in the Session 5 backlog (see 5-data-challenge/README.md
in the course repo). Expect this file to be a frequent source of merge
conflicts during the Day 2 integration session - that's by design, not a
bug: it's the one place every team's PR touches.
"""

import os
from datetime import datetime, UTC

import matplotlib.pyplot as plt
import numpy as np

from astrolab.io import load_frame_set
from astrolab.synth import SAMPLE_FRAMES_DIR, regenerate_sample_data


def _ensure_sample_frames():
    """Generate the sample frames if missing.

    data/frames/ is gitignored (generated, not source) - a fresh clone or
    fork starts without it, so regenerate deterministically from the same
    seed rather than requiring a manual step.
    """
    if not SAMPLE_FRAMES_DIR.is_dir() or not any(SAMPLE_FRAMES_DIR.glob("*.npy")):
        regenerate_sample_data()


def stack_frames(frames):
    """Combine several noisy frames of the same field into one.

    TODO(backlog): implement mean or median stacking to reduce noise.
    """
    raise NotImplementedError("stack_frames: implement frame stacking")


def detect_sources(frame):
    """Find point sources (stars) in a frame.

    TODO(backlog): implement threshold + local-maxima detection,
    returning a list of (x, y) pixel coordinates.
    """
    raise NotImplementedError("detect_sources: implement source detection")


def measure_photometry(frame, sources):
    """Measure the brightness of each detected source.

    TODO(backlog): implement simple aperture photometry, returning a
    table (e.g. a pandas DataFrame) of source -> flux.
    """
    raise NotImplementedError("measure_photometry: implement aperture photometry")


def compose_image(frame: np.ndarray) -> np.ndarray:
    """Contrastive stretch to turn a stacked frame into a (good) display image

    Args:
        frame: np.ndarray

    Returns:
        np.ndarraya, values in [0.0, 1.0]

    Applies a percentile-based contrast stretch: the 2nd percentile maps
    to black, the 98th percentile maps to white, everything in between is
    linearly scaled.
    """
    low, high = np.percentile(frame, [2, 98])
    if high <= low:
        return np.zeros_like(frame)
    stretched = np.clip((frame - low) / (high - low), 0.0, 1.0)
    return stretched


def run():
    """Run the full pipeline end to end, printing progress as it goes."""
    print("Loading frames...")
    _ensure_sample_frames()
    frames = load_frame_set()
    print(f"  loaded {len(frames)} frames of shape {frames[0].shape}")

    print("Stacking frames...")
    stacked = stack_frames(frames)

    print("Detecting sources...")
    sources = detect_sources(stacked)
    print(f"  found {len(sources)} sources")

    print("Measuring photometry...")
    table = measure_photometry(stacked, sources)
    print(table)

    print("Composing final image...")
    out = compose_image(stacked)

    out_path = os.environ.get("OUT_PATH", "outputs/output_time.png")
    plt.imsave(out_path, out, cmap="gray")
    print(f"  saved hero image to {out_path}")

    out_path = os.environ.get("OUT_PATH")
    if out_path is None:
        out_dir = "outputs"
        os.makedirs(out_dir, exist_ok=True)
        timestamp = datetime.now(UTC).isoformat()
        out_path = os.path.join(out_dir, f"output_{timestamp}.png")
    plt.imsave(out_path, out, cmap="gray")
    print(f"  saved output image to {out_path}")


if __name__ == "__main__":
    run()
