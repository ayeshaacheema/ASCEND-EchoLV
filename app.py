
from pathlib import Path
import importlib.util
import sys
import os

ROOT = Path(__file__).resolve().parent

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

# Load the unchanged frozen inference implementation
frozen = load_module(
    "ascend_frozen_inference",
    ROOT / "frozen_inference.py"
)

# Load the original Gradio interface
echolv = load_module(
    "echolv_app",
    ROOT / "echolv_app.py"
)

# Create records directory
records_dir = ROOT / "records"
records_dir.mkdir(parents=True, exist_ok=True)

demo, launch_kwargs = echolv.build_app(
    frozen=frozen,
    records_dir=records_dir,
    demo_paths=None
)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", "8080")),
        share=False,
        show_error=True,
        **launch_kwargs
    )
