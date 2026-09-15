import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class PipelineEndToEndTest(unittest.TestCase):
    def test_module_run_completes_and_produces_readme_image(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "output.png"
            environment = os.environ.copy()
            environment["OUT_PATH"] = str(output_path)

            result = subprocess.run(
                [sys.executable, "-m", "astrolab.pipeline"],
                cwd=REPOSITORY_ROOT,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )

            combined_output = f"{result.stdout}\n{result.stderr}"
            self.assertEqual(result.returncode, 0, combined_output)
            self.assertNotIn("NotImplementedError", combined_output)
            self.assertTrue(output_path.is_file())
            self.assertGreater(output_path.stat().st_size, 0)

        readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("![Composite star field](outputs/output.png)", readme)


if __name__ == "__main__":
    unittest.main()