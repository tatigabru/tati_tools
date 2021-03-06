import os
import random
from typing import Any, Dict, Tuple

import numpy as np
import torch
from torch.nn import Module
from torch.optim import Optimizer


def fix_seed(seed: int = 1234) -> None:
    """
    Fix all random seeds for reproducibility
    PyTorch
    """
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = True


def fix_seeds_tf(seed: int = 1234) -> None:
    """
    Fix all random seeds for reproducibility
    for Tensorflow
    """
    import tensorflow as tf

    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    os.environ["TF_DETERMINISTIC_OPS"] = str(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)


def load_optim(
    optimizer: Optimizer, checkpoint_path: str, device: torch.device
) -> Optimizer:
    """
    Load optimizer to continuer training
        Args:
            optimizer      : initialized optimizer
            checkpoint_path: path to the checkpoint
            device         : device to send optimizer to (must be the same as in the model)

        Note: must be called after initializing the model

        Output: optimizer with the loaded state
    """
    checkpoint = torch.load(checkpoint_path)
    optimizer.load_state_dict(checkpoint["optimizer"])
    for state in optimizer.state.values():
        for k, v in state.items():
            if torch.is_tensor(v):
                state[k] = v.to(device)

    for param_group in optimizer.param_groups:
        print("learning_rate: {}".format(param_group["lr"]))
    print("Loaded optimizer {} state from {}".format(optimizer, checkpoint_path))
    return optimizer


def save_ckpt(model: Module, optimizer: Optimizer, checkpoint_path: str) -> None:
    """
    Save model and optimizer checkpoint to continuer training
    """
    torch.save(
        {
            "model": model.state_dict(),
            "optimizer": optimizer.state_dict(),
        },
        checkpoint_path,
    )
    print("Saved model and optimizer state to {}".format(checkpoint_path))


def load_ckpt(checkpoint_path: str) -> Any:
    """
    Load checkpoint to continuer training
        Args:
            checkpoint_path: path to the checkpoint

        Output: (dict) 0f the checkpoint state

    """
    checkpoint = torch.load(checkpoint_path)
    return checkpoint


def load_model(model: Module, checkpoint_path: str) -> Tuple[Any, Dict[str, Any]]:
    """
    Load model weigths to continuer training
        Args:
            model          : nn model
            checkpoint_path: path to the checkpoint

        Output:
            (nn.Module) nn model with weights
            (dict) 0f the checkpoint state
    """
    checkpoint = torch.load(checkpoint_path)
    model.load_state_dict(checkpoint["model"])

    return model, checkpoint


def collate_fn(batch):
    return tuple(zip(*batch))


def load_weights(model: Module, weights_file: str):
    """Load weight to a torch model from file"""
    model.load_state_dict(torch.load(weights_file))
    return model
