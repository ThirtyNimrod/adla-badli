import sys
import unittest
import shutil
import io
from pathlib import Path

# Add project root to python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from app.workspace import ConversionWorkspace

class TestConversionWorkspace(unittest.TestCase):
    def setUp(self):
        self.test_temp_dir = project_root / "tests" / "temp_workspace_tests"
        self.test_temp_dir.mkdir(exist_ok=True)

    def tearDown(self):
        if self.test_temp_dir.exists():
            shutil.rmtree(self.test_temp_dir)

    def test_workspace_creation_and_auto_cleanup(self):
        # Test that entering and exiting the context manager cleans up files automatically
        with ConversionWorkspace("svg", "jpg", base_temp_dir=self.test_temp_dir) as ws:
            self.assertTrue(ws.workspace_dir.exists())
            self.assertEqual(ws.input_path.name, "input.svg")
            self.assertEqual(ws.output_path.name, "output.jpg")
            
            # Write dummy data
            dummy_data = io.BytesIO(b"<svg></svg>")
            in_path, out_path = ws.write_input(dummy_data)
            
            self.assertTrue(in_path.exists())
            self.assertEqual(in_path.read_bytes(), b"<svg></svg>")
            self.assertFalse(out_path.exists())  # Output shouldn't exist yet
            
        # Outside context block: entire directory should be purged
        self.assertFalse(ws.workspace_dir.exists())

    def test_workspace_release_prevents_cleanup(self):
        # Test that calling release() prevents cleanup on exit
        with ConversionWorkspace("md", "docx", base_temp_dir=self.test_temp_dir) as ws:
            dummy_data = io.BytesIO(b"# Hello")
            ws.write_input(dummy_data)
            ws.release()
            
        # Outside context block: directory must still exist because we released it
        self.assertTrue(ws.workspace_dir.exists())
        self.assertTrue(ws.input_path.exists())
        
        # Execute deferred cleanup task
        cleanup_task = ws.get_cleanup_task()
        cleanup_task()
        
        # Directory must be gone now
        self.assertFalse(ws.workspace_dir.exists())

    def test_workspace_exception_cleanup(self):
        # Test that directory is cleaned up even if an exception occurs inside the context
        try:
            with ConversionWorkspace("svg", "jpg", base_temp_dir=self.test_temp_dir) as ws:
                workspace_dir = ws.workspace_dir
                self.assertTrue(workspace_dir.exists())
                raise ValueError("Simulated error")
        except ValueError:
            pass
            
        # Directory must be purged even after error
        self.assertFalse(workspace_dir.exists())

if __name__ == "__main__":
    unittest.main()
