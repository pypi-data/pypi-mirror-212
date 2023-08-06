from hestia_earth.schema import MeasurementStatsDefinition, MeasurementMethodClassification
from hestia_earth.utils.model import find_term_match

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.measurement import _new_measurement, group_measurements_by_depth, measurement_value
from . import MODEL

REQUIREMENTS = {
    "Site": {
        "measurements": [
            {"@type": "Measurement", "value": "", "term.@id": "soilBulkDensity", "depthUpper": "", "depthLower": ""},
            {"@type": "Measurement", "value": "", "term.@id": "organicCarbonPerKgSoil", "depthUpper": "", "depthLower": ""}  # noqa: E501
        ]
    }
}
RETURNS = {
    "Measurement": [{
        "value": "",
        "depthUpper": "",
        "depthLower": "",
        "statsDefinition": "modelled",
        "methodClassification": "modelled using other physical measurements"
    }]
}
TERM_ID = 'organicCarbonPerHa'
BIBLIO_TITLE = 'Soil organic carbon sequestration rates in vineyard agroecosystems under different soil management practices: A meta-analysis'  # noqa: E501


def measurement(value: float, depthUpper: int, depthLower: int):
    data = _new_measurement(TERM_ID, None, BIBLIO_TITLE)
    data['value'] = [value]
    data['depthUpper'] = depthUpper
    data['depthLower'] = depthLower
    data['statsDefinition'] = MeasurementStatsDefinition.MODELLED.value
    data['methodClassification'] = MeasurementMethodClassification.MODELLED_USING_OTHER_PHYSICAL_MEASUREMENTS.value
    return data


def _run(measurements: list):
    soilBulkDensity = measurement_value(find_term_match(measurements, 'soilBulkDensity'))
    organicCarbonPerKgSoil = find_term_match(measurements, 'organicCarbonPerKgSoil')
    organicCarbonPerKgSoil_value = measurement_value(organicCarbonPerKgSoil)

    value = (
        organicCarbonPerKgSoil.get('depthLower') - organicCarbonPerKgSoil.get('depthUpper')
    ) * soilBulkDensity * (organicCarbonPerKgSoil_value/10) * 1000

    depthUpper = organicCarbonPerKgSoil.get('depthUpper')
    depthLower = organicCarbonPerKgSoil.get('depthLower')

    return measurement(value, depthUpper, depthLower)


def _should_run(site: dict, measurements: list):
    soilBulkDensity = find_term_match(measurements, 'soilBulkDensity', None)
    has_soilBulkDensity_depthLower = (soilBulkDensity or {}).get('depthLower') is not None
    has_soilBulkDensity_depthUpper = (soilBulkDensity or {}).get('depthUpper') is not None
    organicCarbonPerKgSoil = find_term_match(measurements, 'organicCarbonPerKgSoil', None)
    has_organicCarbonPerKgSoil_depthLower = (organicCarbonPerKgSoil or {}).get('depthLower') is not None
    has_organicCarbonPerKgSoil_depthUpper = (organicCarbonPerKgSoil or {}).get('depthUpper') is not None

    logRequirements(site, model=MODEL, term=TERM_ID,
                    has_soilBulkDensity=soilBulkDensity is not None,
                    has_soilBulkDensity_depthLower=has_soilBulkDensity_depthLower,
                    has_soilBulkDensity_depthUpper=has_soilBulkDensity_depthUpper,
                    has_organicCarbonPerKgSoil=organicCarbonPerKgSoil is not None,
                    has_organicCarbonPerKgSoil_depthLower=has_organicCarbonPerKgSoil_depthLower,
                    has_organicCarbonPerKgSoil_depthUpper=has_organicCarbonPerKgSoil_depthUpper)

    should_run = all([
        soilBulkDensity is not None, has_soilBulkDensity_depthLower, has_soilBulkDensity_depthUpper,
        organicCarbonPerKgSoil is not None, has_organicCarbonPerKgSoil_depthLower, has_organicCarbonPerKgSoil_depthUpper
    ])
    logShouldRun(site, MODEL, TERM_ID, should_run)
    return should_run


def run(site: dict):
    grouped_measurements = list(group_measurements_by_depth(site.get('measurements', [])).values())
    return [
        _run(measurements) for measurements in grouped_measurements if _should_run(site, measurements)
    ]
