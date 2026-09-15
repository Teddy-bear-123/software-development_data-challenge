import numpy as np

from astrolab.io import load_frame, save_frame


def test_save_then_load_roundtrip(tmp_path):
    frame = np.ones((8, 8))
    path = tmp_path / "frame.npy"
    save_frame(path, frame)
    loaded = load_frame(path)
    np.testing.assert_array_equal(loaded, frame)


def test_save_frame_creates_parent_dirs(tmp_path):
    frame = np.ones((4, 4))
    path = tmp_path / "a" / "b" / "frame.npy"
    save_frame(path, frame)
    assert path.exists()
