import yaml
from utils import data_mining

def main():
    # Read YAML file to get the configurations
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)

    search_config = config["search"]
    api_url, ret_max, keywords, years, search_levels, directory, search_level = (
        config["api_url"],
        config["ret_max"],
        search_config["keywords"],
        search_config["years"],
        search_config["levels"],
        search_config["directory"],
        search_config["search_level"],
    )

    # Year split
    init_year, end_year = years
    
    # Get JSON data
    data_mining.json_search(
        keywords,
        search_levels,
        api_url,
        directory,
        init_year,
        end_year,
        search_level,
        ret_max,
    )


if __name__ == "__main__":
    main()
