import yaml
import argparse
from easydict import EasyDict as edict


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="config/base.yaml")
    args = parser.parse_args()

    cfg = edict()
    cfg.config = args.config

    return cfg


def set_config():
    cfg_arg = parse_args()
    with open(cfg_arg.config, "r") as f:
        cfg_full = yaml.load(f, Loader=yaml.FullLoader)

    return edict(cfg_full)
