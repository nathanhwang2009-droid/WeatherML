#!/usr/bin/env python3
"""Train the weather prediction model."""

import argparse
from pathlib import Path

import numpy as np

from weatherml.model import save_model, train_model

try:
    import wandb

    WANDB_AVAILABLE = True
except ImportError:
    WANDB_AVAILABLE = False


def main() -> None:
    pass


if __name__ == "__main__":
    main()
