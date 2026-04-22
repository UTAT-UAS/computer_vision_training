import os
import yaml
import argparse
from ultralytics import YOLO

DATASET_PATH = os.path.abspath("annotated/set1")


def main():
    parser = argparse.ArgumentParser(description="YOLO Training and Tuning Script")
    parser.add_argument("--tune", action="store_true", help="Run hyperparameter tuning")
    parser.add_argument("--train", action="store_true", help="Run normal training")
    parser.add_argument(
        "--cfg",
        type=str,
        default="hyperparameters.yaml",
        help="Path to custom hyperparameters yaml (e.g., from tuning)",
    )
    args = parser.parse_args()

    if not args.tune and not args.train:
        parser.print_help()
        print("\nError: Please specify either --tune or --train")
        return

    # Define the YAML file needed by YOLO
    # Assuming path has 'images' and 'labels' subfolders
    dataset_config = {
        "path": DATASET_PATH,
        "train": "images",
        "val": "images",  # No validation set (small dataset)
        "names": {0: "Target"},  # From classes.txt
    }
    yaml_path = os.path.abspath(os.path.join(DATASET_PATH, "dataset.yaml"))
    with open(yaml_path, "w") as f:
        yaml.dump(dataset_config, f, sort_keys=False)

    print(f"Created dataset config at {yaml_path}")

    # Initialize the model
    model = YOLO("yolo26n.pt")

    if args.tune:
        print("Starting hyperparameter tuning...")

        result = model.tune(
            data=yaml_path,
            use_ray=True,
            epochs=100,  # Reduce if too long
            iterations=300,  # Reduce if too long
            optimizer="auto",
            imgsz=640,
            batch=16,  # Lower batch size often generalizes better on small datasets
            # Ray specific tuning parameters
            gpu_per_trial=1,  # Use GPU (assume 1 GPU)
            device=0,  # Use the first GPU
            project="runs/tune",
            name="yolo26n",
            plots=False,
            save=False,
            val=False,
        )

        assert result is not None, (
            "Tuning failed to return results. Check logs for errors."
        )
        best = result.get_best_result("metrics/mAP50-95(B)", "max", "last")

        print("\nBest Hyperparameters found:")
        for k, v in best.config.items():
            print(f"  {k}: {v}")
        with open("hyperparameters.yaml", "w") as f:
            yaml.dump(best.config, f)

        print(
            "\nTuning complete! The best hyperparameters are saved in: hyperparameters.yaml"
        )
        print(
            f"To train the final model, run: python {__file__} --train --cfg hyperparameters.yaml"
        )

    elif args.train:
        print("Starting normal training...")
        train_args = {
            "data": yaml_path,
            "epochs": 300,
            "patience": 50,
            "imgsz": 640,
            "batch": 16,
            "device": 0,
            "project": "runs/train",
            "name": "yolo26n",
        }

        # If a custom config is provided, add it to the training args
        if args.cfg:
            print(f"Using hyperparameters from {args.cfg}")
            train_args["cfg"] = os.path.abspath(args.cfg)

        model.train(**train_args)


if __name__ == "__main__":
    main()
