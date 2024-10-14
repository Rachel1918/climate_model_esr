from process.isimip import create_input_link, create_output_link
from process.utils import read_cfg

workdir: str = "etc/climate_model_esr/data3"

cfg = read_cfg("etc/download.yml")
create_input_link(cfg["input"], workdir=workdir)
# create_output_link(cfg["output"], workdir=workdir)
