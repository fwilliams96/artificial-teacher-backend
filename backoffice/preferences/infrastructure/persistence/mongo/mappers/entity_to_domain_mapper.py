from backoffice.preferences.domain.preference import Preference

def map_entity_to_domain(preference: dict) -> Preference:

    return Preference(
        id=str(preference["_id"]),
        preference=preference["preference"]
    )