from .functions import get_random_string


async def mock_auth_user():
    return {}


def mock_address() -> dict:
    return {
        'main_street': get_random_string(),
        'secondary_street': None,
        'house_number': 1,
        'zip_code': get_random_string(),
        'city': get_random_string(),
        'state': get_random_string(),
        'country': get_random_string(),
    }
