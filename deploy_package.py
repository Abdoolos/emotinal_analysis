import os
import shutil
import sys
import venv
from pathlib import Path
import zipfile

def create_deployment_package():
    # Create a clean deployment directory
    deploy_dir = Path("deploy_package")
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    deploy_dir.mkdir()

    # Copy necessary files
    files_to_copy = [
        "backend",
        "requirements.txt",
        "runtime.txt",
    ]
    
    for item in files_to_copy:
        src = Path(item)
        dst = deploy_dir / src.name
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

    # Create package zip
    with zipfile.ZipFile("deployment.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(deploy_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, deploy_dir)
                zipf.write(file_path, arcname)

    print("Created deployment.zip package")

if __name__ == "__main__":
    create_deployment_package()
