from os import makedirs
from os.path import basename, exists, join

from requests import get as requests_get

from process import URL_TEMPLATE


def create_input_link(
    cfg: dict,
    workdir: str = "/tmp/climate_model_esr/data",
    allowed_forcing_type: list = ["climate"],
    allowed_sub_forcing_type: list = ["ocean", "atmosphere"],
):
    if not exists(workdir):
        makedirs(workdir)

    for forcing_type in cfg:
        if allowed_forcing_type is not None:
            if forcing_type not in allowed_forcing_type:
                continue
        for sub_forcing_type in cfg[forcing_type]:

            if allowed_sub_forcing_type is not None:
                if sub_forcing_type not in allowed_sub_forcing_type:
                    continue

            proc_cfg = cfg[forcing_type][sub_forcing_type]
            proc_url = URL_TEMPLATE["input"][forcing_type][sub_forcing_type]

            # Get the maximum length of the paramaters
            total_len = 0
            for proc_key in proc_cfg:
                if len(proc_cfg[proc_key]) > total_len:
                    total_len = len(proc_cfg[proc_key])

            for param_index in range(total_len):
                if not proc_cfg["enable"][param_index]:
                    continue

                proc_url_to_download = proc_url.format(
                    TEMPORAL_RES=proc_cfg["temporal_resolution"][param_index],
                    SCENARIO=proc_cfg["scenario"][param_index],
                    CLIMATE_MODEL_UPPER=proc_cfg["climate_model"][param_index].upper(),
                    CLIMATE_MODEL=proc_cfg["climate_model"][param_index],
                    ENS_MEMBERS=proc_cfg["ensemble_member"][param_index],
                    VARIABLE=proc_cfg["variable"][param_index],
                    SPATIAL_RES=proc_cfg["spatial_resolution"][param_index],
                    COVERAGE=proc_cfg["coverage"][param_index],
                    YEAR_RANGE=proc_cfg["year_range"][param_index].replace("-", "_"),
                )

                print(
                    f"Download {forcing_type}-{sub_forcing_type}: {proc_url_to_download}"
                )
                proc_url_to_download_filename = basename(proc_url_to_download)
                proc_data_local = join(workdir, proc_url_to_download_filename)

                if exists(proc_data_local):
                    continue

                response = requests_get(proc_url_to_download)
                if response.status_code == 404:
                    raise Exception("No data found ....")
                    # continue

                with open(proc_data_local, "wb") as file:
                    file.write(response.content)

                print(f"File downloaded as {proc_data_local}")


def create_output_link(cfg: dict, workdir: str = "/tmp/climate_model_esr/data"):

    if not exists(workdir):
        makedirs(workdir)

    for sector in cfg:
        for isimip_stage in cfg[sector]:
            proc_cfg = cfg[sector][isimip_stage]
            proc_url = URL_TEMPLATE["output"][sector]

            # Get the maximum length of the paramaters
            for proc_key in proc_cfg:
                if proc_key == "sector":
                    continue

                total_len = 0
                if len(proc_cfg[proc_key]) > total_len:
                    total_len = len(proc_cfg[proc_key])

            for param_index in range(total_len):

                if not proc_cfg["enable"]:
                    continue

                proc_url_to_download = proc_url.format(
                    ISIMIP_STAGE=isimip_stage,
                    IMPACT_MODEL_UPPER=proc_cfg["impact_model"][param_index].upper(),
                    CLIMATE_MODEL=proc_cfg["climate_model"][param_index],
                    IMPACT_MODEL=proc_cfg["impact_model"][param_index],
                    BIAS_ADJUSTMENT=proc_cfg["bias_adjustment"][param_index],
                    SCENARIO=proc_cfg["scenario"][param_index],
                    DIRECT_HUMAN_FORCING=proc_cfg["direct_human_forcing"][param_index],
                    SENSITIVITY=proc_cfg["sensitivity"][param_index],
                    VARIABLE=proc_cfg["variable"][param_index],
                    CROP_TYPE=proc_cfg["crop_type"][param_index],
                    IRRIGATION_TYPE=proc_cfg["irrigation_type"][param_index],
                    YEAR_START=proc_cfg["year_range"][param_index][0:4],
                    YEAR_END=proc_cfg["year_range"][param_index][5:] + "123213",
                )

                proc_url_to_download_filename = basename(proc_url_to_download)
                proc_data_local = join(workdir, proc_url_to_download_filename)

                response = requests_get(proc_url_to_download)

                if response.status_code == 404:
                    continue

                with open(proc_data_local, "wb") as file:
                    file.write(response.content)

                print(f"File downloaded as {proc_data_local}")
