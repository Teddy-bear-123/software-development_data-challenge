"""Fetch a real telescope image - the "hero image" bonus feature.

Unlike astrolab.synth (deterministic, no network), this queries a real
public sky-survey archive live via astroquery. That's a deliberate
contrast with the rest of the pipeline: it raises the reproducibility
question modules 2/3 talk about explicitly - pin the survey name,
target, and image size, and consider caching the result to disk, so a
network hiccup during the workshop doesn't block the demo.

Confirmed working during course prep:

    from astroquery.skyview import SkyView
    imgs = SkyView.get_images(position="M42", survey=["DSS"], pixels=200)
    imgs[0][0].data  # -> a 2D numpy array, dtype float32

TODO(backlog): implement fetch_sky_image below, returning a plain 2D
numpy array so it can flow through the same detect_sources /
measure_photometry / compose_image steps as a stacked synthetic frame.
"""

DEFAULT_TARGET = "M42"  # the Orion Nebula - bright, iconic, DSS-covered
DEFAULT_SURVEY = "DSS"
DEFAULT_PIXELS = 200

try:
    from astroquery.skyview import SkyView
except ImportError:
    SkyView = None


def fetch_sky_image(position=DEFAULT_TARGET, survey=DEFAULT_SURVEY, pixels=DEFAULT_PIXELS):
    """Fetch a real image of the sky around ``position`` from a public
    archive (the Digitized Sky Survey, via astroquery's SkyView client).

    TODO(backlog): call astroquery.skyview.SkyView.get_images(...), pull
    the 2D array out of the returned HDUList, and return it. Consider
    caching the result to disk (e.g. as .npy or .fits) so re-running the
    demo doesn't depend on network access every time.
    """
    if SkyView is None:
        raise ImportError(
            "astroquery is required for fetch_sky_image. "
            "Install it with: conda install -c conda-forge astroquery"
        )

    raise NotImplementedError("fetch_sky_image: implement a real astroquery fetch")