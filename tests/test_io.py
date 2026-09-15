import numpy as np
import pytest

from astrolab.io import load_frame, load_frame_set, save_frame


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


@pytest.mark.parametrize("directory", ["missing", "empty"])
def test_load_frame_set_raises_for_missing_or_empty_directory(tmp_path, directory):
    frame_directory = tmp_path / directory
    if directory == "empty":
        frame_directory.mkdir()

    with pytest.raises(FileNotFoundError):
        load_frame_set(frame_directory)


def test_load_frame_set_filters_paths_by_pattern(tmp_path):
    matching_frame = np.ones((2, 2))
    ignored_frame = np.zeros((2, 2))
    save_frame(tmp_path / "science_01.npy", matching_frame)
    save_frame(tmp_path / "calibration_01.npy", ignored_frame)

    loaded = load_frame_set(tmp_path, pattern="science_*.npy")

    assert len(loaded) == 1
    np.testing.assert_array_equal(loaded[0], matching_frame)
