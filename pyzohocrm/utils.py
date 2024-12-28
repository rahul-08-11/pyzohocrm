


def get_header(token : str ) -> dict:
    """Returns the headers for the Zoho API request.

    Args:
        token (str): The access token for the Zoho API.

    Returns:
        dict: The headers for the Zoho API request.
    """
    return {
        "Authorization": f"Zoho-oauthtoken {token}"
    }