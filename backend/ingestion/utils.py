EMISSION_FACTORS = {
    'diesel_liter': 2.68,
    'electricity_kwh': 0.82,
    'flight_km': 0.15,
}


def normalize_unit(value, unit):

    if unit.lower() == 'mwh':
        return value * 1000, 'kwh'

    if unit.lower() == 'gallon':
        return value * 3.785, 'liter'

    return value, unit


def calculate_emission(category, value):

    factor = EMISSION_FACTORS.get(category, 0)

    return factor, value * factor