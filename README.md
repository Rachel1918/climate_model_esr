# Climate_model_ESR

The **Climate_Model_ESR** repository hosts scripts to download climate change related data for New Zealand from _ISIMIP_


## Installation
The repository working environment can be installed via:
```
make env
```
[Conda](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html) must be installed as the package manager for this repository.


## Usage

The data can be downloaded by running:
```
python scripts/download_data.py --workdir /tmp/data
```

After the data is being downloaded, the file can be posprocessed using `scripts/read_nc.py`.

User should understand some basic climate change model knowledge, for example,

- Climate models: many centres run climate projections. The usual climate models include:
    - ``MRI-ESM2-0``: it is a climate model developed by the Meteorological Research Institute (MRI) of the Japan Meteorological Agency (JMA). It stands for "MRI Earth System Model version 2.0".
    - ``GFDL-ESM4``: a climate model developed by the Geophysical Fluid Dynamics Laboratory (GFDL), which is part of the National Oceanic and Atmospheric Administration (NOAA) in the United States. GFDL-ESM4 stands for "GFDL Earth System Model version 4".
    - ``HadGEM2-ES``: it is Hadley Centre Global Environment Model version 2—Earth System, which is a climate model developed by the UK Met Office's Hadley Centre. 

- Climate variables: some usuall climate variables include:
    - ``tas``: Near surface temperature
    - ``tasmin``: Near surface minimum temperature
    - ``tasmax``: Near surface maximum temperature
    - ``tos``: Sea surface temperature
    - ``so``: Sea water salinity
    - ``pr``/``rain``: rainfall
    - ``wind``/``sfcwind``: Near surface wind speed

The data to be downloaded must be specifed in a configuration file, an example is given in ``etc/download.yml``.


