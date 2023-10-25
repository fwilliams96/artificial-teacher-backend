from backoffice.preferences.domain.preference import Preference

def map_domain_to_entity(preference: Preference) -> dict:
    return {
        "preference": preference.preference
    }