"""
Project for Week 3 of "Python Data Visualization".
Unify data via common country name.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal

def reconcile_countries_by_name(plot_countries, gdp_countries):
    """
    Inputs:
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country names used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country names from
      gdp_countries The set contains the country codes from
      plot_countries that were not found in gdp_countries.
    """
    res_dict = {}
    missing_countries = set()

    for key, value in plot_countries.items():
        if value in gdp_countries:
            res_dict[key] = value
        else:
            missing_countries.add(key)

    return res_dict, missing_countries


def test():
    """
    test function
    """
    #pgl_countries = pygal.maps.world.COUNTRIES
    res = reconcile_countries_by_name({'IN':'India', 'US':'America', 'PGL_XYZ':'A B C',\
     'PGL_2':'a s d f'}, {'India':'xxx', 'America':'yyy', 'CC_XYZ':'X Y Z'})
    print(res)

#test()

def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """

    result = {}
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in reader:
            result[row.get(keyfield)] = row

    return result

def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    res_map_dict = {}
    missing_plot_country = set()
    missing_gdp_value = set()

    # Read csv file into nested dictionary
    nested_dict = read_csv_as_nested_dict(gdpinfo.get("gdpfile"),\
    gdpinfo.get("country_name"), gdpinfo.get("separator"), gdpinfo.get("quote"))

    #print(nested_dict)

    for code, country in plot_countries.items():
        #print(country)
        if country in nested_dict:
            tmp_country_gdpdata = nested_dict.get(country)
            #print(tmp_country_gdpdata)
            gdp_data_year = tmp_country_gdpdata.get(year)
            #print(gdp_data_year)
            if (gdp_data_year == ""):
                missing_gdp_value.add(code)
            else:
                log_gdp = math.log10(float(gdp_data_year))
                res_map_dict[code] = log_gdp
        else:
            missing_plot_country.add(code)
    return res_map_dict, missing_plot_country, missing_gdp_value

def test_build_map_dict_by_name():
    """
    Test the code for several years.
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    # Get pygal country code map
    pygal_countries = {'KEN':'Kenya', 'IDN':'Indonesia'}

    # 1960
    res = build_map_dict_by_name(gdpinfo, pygal_countries, "1960")
    print(res)

#test_build_map_dict_by_name()


def render_world_map(gdpinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for
      map_file       - Name of output file to create

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data for the given year and
      writes it to a file named by map_file.
    """


    # Initialise map
    world_map = pygal.maps.world.World()
    world_map.title = 'Counry GDP Chart'

    # get XY plot dictionary for the given country lists
    world_plot_dict = build_map_dict_by_name(gdpinfo, plot_countries, year)

    world_map.add("GDP", world_plot_dict[0])
    world_map.add("Missing Country", world_plot_dict[1])
    world_map.add("Missing GDP", world_plot_dict[2])

    # render Character
    world_map.render_to_file(map_file)
    #world_map.render_in_browser()
    #return


def test_render_world_map():
    """
    Test the project code for several years.
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES
    #pygal_countries = {'KEN':'Kenya', 'IDN':'Indonesia', 'IND':'India', \
    #'USA':'United States of America'}

    # 1960
    #render_world_map(gdpinfo, pygal_countries, "1960", "isp_gdp_world_name_1960.svg")

    # 1980
    #render_world_map(gdpinfo, pygal_countries, "1980", "isp_gdp_world_name_1980.svg")

    # 2000
    #render_world_map(gdpinfo, pygal_countries, "2000", "isp_gdp_world_name_2000.svg")

    # 2010
    render_world_map(gdpinfo, pygal_countries, "2010", "isp_gdp_world_name_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

test_render_world_map()
