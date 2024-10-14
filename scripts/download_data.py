from argparse import ArgumentParser

from process.isimip import create_input_link, create_output_link
from process.utils import read_cfg


def main(workdir: str, cfg_path: str):
    cfg = read_cfg(cfg_path)
    create_input_link(cfg["input"], workdir=workdir)
    create_output_link(cfg["output"], workdir=workdir)


if __name__ == "__main__":
    parser = ArgumentParser(description="Creating NZ data")

    parser.add_argument(
        "--workdir",
        type=str,
        required=False,
        default="/tmp/data",
        help="Working directory",
    )
    parser.add_argument(
        "--cfg_path",
        type=str,
        required=False,
        default="etc/download.yml",
        help="Input data configuration",
    )

    args = parser.parse_args()
    main(args.workdir, args.cfg_path)
