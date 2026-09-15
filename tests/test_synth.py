"""
Tests for astrolab.synth.

The module promises deterministic star-field generation from a seed.
These tests verify three things:

  Slice A — Determinism         : same seed → same output; different seed → different
  Slice B — Shape / edge cases  : n_stars=0, single star, non-square shapes
  Slice C — Statistical sanity  : frame count, per-frame shape/dtype, noise centered
                                   on background, stacking reduces noise

Run with:  python -m pytest tests/test_synth.py -v
"""

import numpy as np
import pytest

from astrolab.synth import (
    FRAME_SHAPE,
    DEFAULT_N_STARS,
    DEFAULT_NOISE_SIGMA,
    DEFAULT_BACKGROUND,
    SAMPLE_SEED,
    SAMPLE_N_FRAMES,
    generate_star_field,
    generate_frame_set,
)


# SLICE A — DETERMINISM
# The docstring says: "Deterministic: the same seed always produces the same
# frame." These tests pin that contract.

def test_same_seed_produces_identical_frames():
    """Two calls with the same seed return byte-identical arrays."""
    a = generate_star_field(shape=(32, 32), n_stars=5, seed=42)
    b = generate_star_field(shape=(32, 32), n_stars=5, seed=42)
    np.testing.assert_array_equal(a, b)


def test_different_seeds_produce_different_frames():
    """Different seeds must produce different noise realizations."""
    a = generate_star_field(shape=(32, 32), n_stars=5, seed=1)
    b = generate_star_field(shape=(32, 32), n_stars=5, seed=2)
    assert not np.array_equal(a, b)


def test_default_seed_is_deterministic():
    """Calling without an explicit seed still returns the same frame."""
    a = generate_star_field(shape=(16, 16))
    b = generate_star_field(shape=(16, 16))
    np.testing.assert_array_equal(a, b)


def test_reproducible_across_many_seeds():
    """A parametrized sweep across many seeds must remain reproducible."""
    for seed in [0, 1, 17, 99, 12345, 99999]:
        a = generate_star_field(shape=(32, 32), n_stars=3, seed=seed)
        b = generate_star_field(shape=(32, 32), n_stars=3, seed=seed)
        np.testing.assert_array_equal(a, b, err_msg=f"seed={seed} not reproducible")


def test_frame_set_is_deterministic():
    """The same seed produces the same list of frames, frame by frame."""
    a = generate_frame_set(n_frames=3, shape=(32, 32), seed=42)
    b = generate_frame_set(n_frames=3, shape=(32, 32), seed=42)
    assert len(a) == len(b)
    for i, (fa, fb) in enumerate(zip(a, b)):
        np.testing.assert_array_equal(fa, fb, err_msg=f"frame {i} differs")


def test_frame_set_different_seeds_differ():
    """Different seeds should change at least the first frame."""
    a = generate_frame_set(n_frames=3, shape=(32, 32), seed=1)
    b = generate_frame_set(n_frames=3, shape=(32, 32), seed=2)
    assert not np.array_equal(a[0], b[0])


# SLICE B — SHAPE AND PARAMETER EDGE CASES

@pytest.mark.parametrize("shape", [
    (1, 1),
    (2, 3),
    (3, 2),
    (16, 16),
    (32, 64),
    (64, 32),
    (128, 128),
])
def test_generate_star_field_respects_shape(shape):
    """The output array's shape matches the requested shape exactly."""
    frame = generate_star_field(shape=shape, n_stars=3, seed=1)
    assert frame.shape == shape


def test_default_shape_is_used_when_not_specified():
    """With no shape argument, the module constant FRAME_SHAPE is used."""
    frame = generate_star_field(seed=1)
    assert frame.shape == FRAME_SHAPE


def test_zero_stars_with_zero_noise_is_exactly_background():
    """
    With n_stars=0 and noise_sigma=0, every pixel should equal `background`.
    This is the cleanest possible edge case.
    """
    background = 7.5
    frame = generate_star_field(
        shape=(16, 16),
        n_stars=0,
        seed=1,
        noise_sigma=0.0,
        background=background,
    )
    assert np.all(frame == background)


def test_single_star_runs_without_error():
    """One star is the smallest non-trivial field — verify it doesn't crash."""
    frame = generate_star_field(shape=(32, 32), n_stars=1, seed=1)
    assert frame.shape == (32, 32)
    assert np.isfinite(frame).all()


def test_single_star_creates_a_bright_peak():
    """
    With no noise and one star, the brightest pixel should stand out
    well above the background.
    """
    background = 10.0
    frame = generate_star_field(
        shape=(64, 64),
        n_stars=1,
        seed=1,
        noise_sigma=0.0,
        background=background,
    )
    brightest = frame.max()
    assert brightest > background + 50.0


def test_non_square_shape_preserved():
    """A tall-narrow and short-wide shape must both be honoured."""
    tall = generate_star_field(shape=(100, 20), n_stars=3, seed=1)
    wide = generate_star_field(shape=(20, 100), n_stars=3, seed=1)
    assert tall.shape == (100, 20)
    assert wide.shape == (20, 100)


def test_custom_background_used_when_no_stars_no_noise():
    """A user-specified background is the value of every pixel."""
    frame = generate_star_field(
        shape=(16, 16), n_stars=0, seed=1,
        noise_sigma=0.0, background=99.0,
    )
    assert np.allclose(frame, 99.0)


def test_more_stars_means_more_total_brightness():
    """Summing intensity over the frame increases with n_stars (no noise)."""
    dim = generate_star_field(shape=(64, 64), n_stars=0, seed=1,
                              noise_sigma=0.0, background=0.0)
    bright = generate_star_field(shape=(64, 64), n_stars=20, seed=1,
                                 noise_sigma=0.0, background=0.0)
    assert bright.sum() > dim.sum()


def test_returns_numpy_array_of_floats():
    """The contract: an ndarray with a floating dtype."""
    frame = generate_star_field(shape=(16, 16), n_stars=3, seed=1)
    assert isinstance(frame, np.ndarray)
    assert np.issubdtype(frame.dtype, np.floating)


# SLICE C — STATISTICAL SANITY CHECKS ON generate_frame_set

def test_frame_set_returns_list():
    frames = generate_frame_set(n_frames=3, shape=(32, 32), seed=1)
    assert isinstance(frames, list)


@pytest.mark.parametrize("n_frames", [1, 2, 5, 10])
def test_frame_set_returns_requested_number_of_frames(n_frames):
    frames = generate_frame_set(n_frames=n_frames, shape=(32, 32), seed=1)
    assert len(frames) == n_frames


def test_frame_set_default_count():
    """With no argument, the module default of 5 frames is used."""
    frames = generate_frame_set(shape=(32, 32), seed=1)
    assert len(frames) == 5


def test_frame_set_empty_when_zero_frames_requested():
    frames = generate_frame_set(n_frames=0, shape=(32, 32), seed=1)
    assert frames == []


def test_all_frames_have_requested_shape_and_float_dtype():
    shape = (32, 64)
    frames = generate_frame_set(n_frames=4, shape=shape, seed=1)
    for f in frames:
        assert f.shape == shape
        assert np.issubdtype(f.dtype, np.floating)


def test_noise_is_centered_on_background():
    """
    With n_stars=0, the mean of each frame should be close to `background`.
    Gaussian noise with mean 0 does not shift the expected value.
    """
    background = 10.0
    frames = generate_frame_set(
        n_frames=5, shape=(128, 128), n_stars=0,
        seed=1, noise_sigma=5.0, background=background,
    )
    for i, f in enumerate(frames):
        assert abs(f.mean() - background) < 0.5, (
            f"frame {i} mean={f.mean():.3f}, expected ≈{background}"
        )


def test_noise_std_matches_requested_sigma():
    """
    On a large frame with no stars, the empirical standard deviation of the
    pixels should approximate `noise_sigma`.
    """
    sigma = 8.0
    frames = generate_frame_set(
        n_frames=1, shape=(256, 256), n_stars=0,
        seed=1, noise_sigma=sigma, background=0.0,
    )
    frame = frames[0]
    assert abs(frame.std() - sigma) < 0.5


def test_frames_are_independent_draws():
    """
    Each frame in a set uses its own noise RNG, so the frames should differ
    from one another when n_stars=0 (no shared signal).
    """
    frames = generate_frame_set(
        n_frames=3, shape=(32, 32), n_stars=0,
        seed=1, noise_sigma=5.0,
    )
    assert not np.array_equal(frames[0], frames[1])
    assert not np.array_equal(frames[0], frames[2])
    assert not np.array_equal(frames[1], frames[2])


def test_stacking_reduces_noise():
    """
    The whole point of frame stacking: averaging N independent frames
    reduces the noise standard deviation by roughly sqrt(N).
    We assert the average frame's stddev is meaningfully lower than a single frame's.
    """
    frames = generate_frame_set(
        n_frames=10, shape=(128, 128), n_stars=0,
        seed=1, noise_sigma=5.0, background=0.0,
    )
    single_std = frames[0].std()
    stacked_std = np.mean(frames, axis=0).std()
    assert stacked_std < single_std * 0.6, (
        f"stacked std={stacked_std:.3f}, single std={single_std:.3f}"
    )


def test_star_signal_is_shared_across_frames():
    """
    With noise_sigma=0 and the same field, all frames should be *identical*
    because the stars (the only signal) are drawn once from `seed`.
    """
    frames = generate_frame_set(
        n_frames=4, shape=(64, 64), n_stars=5,
        seed=1, noise_sigma=0.0, background=0.0,
    )
    for i in range(1, len(frames)):
        np.testing.assert_array_equal(frames[0], frames[i])


# MODULE CONSTANTS — small guard against accidental renames

def test_frame_shape_constant_is_2d_tuple():
    assert isinstance(FRAME_SHAPE, tuple)
    assert len(FRAME_SHAPE) == 2
    assert all(isinstance(d, int) and d > 0 for d in FRAME_SHAPE)


def test_numeric_defaults_are_positive():
    assert DEFAULT_N_STARS > 0
    assert DEFAULT_NOISE_SIGMA > 0
    assert DEFAULT_BACKGROUND >= 0


def test_sample_defaults_are_meaningful():
    assert isinstance(SAMPLE_SEED, int)
    assert SAMPLE_N_FRAMES > 0