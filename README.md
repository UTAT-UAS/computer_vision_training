# Computer Vision Training

Simple scaffold for training a YOLO26n model for object detection.

## Model Training Tutorial

Install dependencies, OS specific see `pyproject.toml` and `flake.nix` for required packages.

If `nix` is installed:

```sh
nix develop
uv venv
source .venv/bin/activate
uv sync
```

Scripts **require and use** a CUDA-compatible GPU. See your OS documenation on how to configure. Test with `python -c "import torch; print(torch.cuda.is_available())"`

### Training Data

Go and take some photos of your desired object, try to get a representative dataset of ~100 photos (more is better).

Make sure you install(ed) `label-studio` an OSS web based labeling tool.

After installing run with `label-studio`, presumably you are running local only so just use `test@test.com` and `testtest` or something as the user.

Alternatively use CVAT or something.

Label your data and export as YOLO with images.

### Hyperparameter tuning

Add your dataset to `./annotated/set1` and run `python train.py --tune` to find optimal hyperparameters. This is needed because you likely have a small dataset and thus we need to find optimal parameters to train the model with.

Then run `python train.py --train` to train the model.

## misc

If ultralyics keeps notifying you that your images are corrupted use this script to fix.

```py
from pathlib import Path
from PIL import Image, ImageOps
root = Path("./images") # image directory
for im_file in root.rglob("*.jpg"):
    try:
        ImageOps.exif_transpose(Image.open(im_file)).save(
            im_file, "JPEG", subsampling=0, quality=100
        )
    except Exception as e:
        print(f"Skipping {im_file}: {e}")
```
