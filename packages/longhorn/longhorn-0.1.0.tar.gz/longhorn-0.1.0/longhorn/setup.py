import asyncio
import logging

from argparse import ArgumentParser

from .config import install_or_upgrade


def build_parser():
    parser = ArgumentParser("Setups your longhorn blog")
    return parser


def main():
    _ = build_parser().parse_args()
    logging.basicConfig(level=logging.INFO)
    asyncio.run(install_or_upgrade())


if __name__ == "__main__":
    main()
