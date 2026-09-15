import numpy as np

from astrolab.pipeline import compose_image


def test_compose_image_shape():
    frame = np.random.default_rng(0).normal(size=(128, 128))
    out = compose_image(frame)
    assert out.shape == frame.shape


def test_compose_image_values_in_unit_range():
    frame = np.random.default_rng(0).normal(size=(128, 128))
    out = compose_image(frame)
    assert out.min() >= 0.0
    assert out.max() <= 1.0


def test_compose_image_constant_frame_is_black():
    frame = np.full((16, 16), 42.0)
    out = compose_image(frame)
    np.testing.assert_array_equal(out, np.zeros_like(frame))


def test_compose_image_maps_bright_pixels_higher():
    # Percentile stretch maps the 2nd/98th percentiles to 0/1. Two very bright
    # pixels would BOTH saturate to 1.0, breaking a strict `>` comparison. So
    # place them at mid ± 1, inside the stretch range where neither clips.
    rng = np.random.default_rng(7)
    frame = rng.normal(10.0, 2.0, size=(32, 32))
    low, high = np.percentile(frame, [2, 98])
    mid = (low + high) / 2.0
    frame[5, 5] = mid - 1.0
    frame[10, 10] = mid + 1.0
    out = compose_image(frame)
    assert out[10, 10] > out[5, 5]
    assert 0.0 < out[5, 5] < 1.0
