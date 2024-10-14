GOOGLE_EARTH = {
    "SERVICE_ACCOUNT": "climate-risk-esr@climate-risk-esr.iam.gserviceaccount.com",
    "SERVICE_ACCOUNT_CRED": "etc/keys/climate-risk-esr-db7773eae0fe.json",
}


URL_TEMPLATE = {
    "input": {
        "climate": {
            "ocean": "https://files.isimip.org/ISIMIP3b/InputData/climate/ocean/uncorrected/global/{TEMPORAL_RES}/{SCENARIO}/{CLIMATE_MODEL_UPPER}/{CLIMATE_MODEL}_{ENS_MEMBERS}_{SCENARIO}_{VARIABLE}_{SPATIAL_RES}_{COVERAGE}_{TEMPORAL_RES}_{YEAR_RANGE}.nc",
            "atmosphere": "https://files.isimip.org/ISIMIP3b/InputData/climate/atmosphere/bias-adjusted/global/{TEMPORAL_RES}/{SCENARIO}/{CLIMATE_MODEL_UPPER}/{CLIMATE_MODEL}_{ENS_MEMBERS}_w5e5_{SCENARIO}_{VARIABLE}_{COVERAGE}_{TEMPORAL_RES}_{YEAR_RANGE}.nc",
        }
    },
    "output": {
        "agriculture": "https://files.isimip.org/{ISIMIP_STAGE}/OutputData/agriculture/{IMPACT_MODEL_UPPER}/{CLIMATE_MODEL}/future/{IMPACT_MODEL}_{CLIMATE_MODEL}_{BIAS_ADJUSTMENT}_{SCENARIO}_{DIRECT_HUMAN_FORCING}_{SENSITIVITY}_{VARIABLE}-{CROP_TYPE}-{IRRIGATION_TYPE}_global_monthly_{YEAR_START}_{YEAR_END}.nc"
    },
}
