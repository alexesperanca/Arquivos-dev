import json
from urllib.request import urlopen
import urllib.parse

API_URL = None


def json_search(
    keywords: list,
    config_level_dict: dict,
    api_url: str,
    writing_dir: str,
    init_year: int = 0,
    end_year: int = 0,
    search_level: int = 3,
    ret_max: int = 50,
):
    """JSON data search for the keyword, websites, and years passed on the API URL given.

    Args:
        keywords (list): Keyword to search for.
        config_level_dict (dict): Website searching through level configuration.
        api_url (str): API URL to use for the data searching.
        writing_dir (str): Directory to write the data in.
        init_year (int, optional): Initial year. Defaults to 0.
        end_year (int, optional): Final year. Defaults to 0.
        search_level (int, optional): Searching level. Defaults to 3.
        ret_max (int, optional): Number of searches retrieved. Defaults to 50.
    """
    # Assert defining
    assert search_level in [1, 2, 3], "Search level must be an integer between 1 and 3!"
    assert (
        type(init_year) == int and type(end_year) == int
    ), "Initial and final year passed must be Integers!"
    assert end_year > init_year, "Final year must be greater than the initial year!"

    # Attribute the url to the global variable to avoid unnecessary parameter passing
    global API_URL
    API_URL = api_url

    # Get list for the defined year
    search_list = config_level_dict[str(search_level)]

    # Range year usage defining
    use_years = init_year != 0 and end_year != 0

    for website in search_list:
        for keyword in keywords:
            print("Searching for:", keyword)
            # Format the keyword
            keyword = format_keyword(keyword)

            # If no year condition, normal search
            if not use_years:
                response_api(keyword, website, ret_max, writing_dir)
                continue

            # If year searching passed, search for all individually
            year = init_year
            while year != end_year:
                response_api(keyword, website, ret_max, writing_dir, year)
                year += 1

    return


# FIXME: May have a library that does this automatically
def format_keyword(keyword: str) -> str:
    """Format the keyword for correct url search.

    Args:
        keyword (str): Keyword to format.

    Returns:
        str: Final keyword formatted.
    """
    if '"' not in keyword:
        return keyword

    return keyword.replace('"', "").replace('"', "%27").replace(" ", "%20")


def response_api(
    keyword: str, website: str, ret_max: int, writing_dir: str, year: int = None
):
    """API response data obtainment and storage.

    Args:
        keyword (str): Keyword to search in the API.
        website (str): Website to search for.
        ret_max (int): Number of searches retrieved
        writing_dir (str): Directory to write the data.
        year (int, optional): Year to search the data from. Defaults to None.
    """
    try:
        # Construct the general url
        url = f"{API_URL}?q={keyword}&siteSearch={website}&maxItems={ret_max}"

        # Add to the url the passed year, if exists
        if year:
            url += f"&from={year}&to={year + 1}"

        # Get the response
        response = urlopen(url)
    except:
        # Format keyword and url in case of error
        query = "%s" % (urllib.parse.quote(keyword),)
        url_divided = url.split(keyword)
        new_url = url_divided[0] + query + url_divided[1]
        response = urlopen(new_url)

    # Read Response Data to dictionary
    data_json = json.loads(response.read().decode("utf-8"))
    final_data = json.dumps(data_json, indent=4)

    # Get only the website name. 0 and 1 value is to avoid the "www" access
    split_value = 1 if "www" in website else 0
    website_def = website.split("//")[1].split(".")[split_value]

    # Save the JSON data in the directory defined
    directory = (
        f"{writing_dir}\\{keyword}_{year}_{website_def}.json"
        if year
        else f"{writing_dir}\\{keyword}_{website_def}.json"
    )
    save_file_data(str(final_data), directory, "w")


def save_file_data(data: dict, file_dir: str, write_type: str = "w"):
    """Save the data in the desired directory.

    Args:
        data (dict): Data to save.
        file_dir (str): Directory to save the data.
        write_type (str, optional): Writing type, must be writing or append. Defaults to "w".
    """
    assert write_type in ["w", "a"], "Writing type defined invalid."
    file = open(file_dir, write_type)
    file.write(str(data))
    file.close()
