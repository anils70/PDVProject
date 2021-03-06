"""
Project for Week 2 of "Python Data Visualization".
Read World Bank GDP data and create some basic XY plots.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import pygal


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



def build_plot_values(gdpinfo, gdpdata):
    """
    Inputs:
      gdpinfo - GDP data information dictionary
      gdpdata - A single country's GDP stored in a dictionary whose
                keys are strings indicating a year and whose values
                are strings indicating the country's corresponding GDP
                for that year.

    Output:
      Returns a list of tuples of the form (year, GDP) for the years
      between "min_year" and "max_year", inclusive, from gdpinfo that
      exist in gdpdata.  The year will be an integer and the GDP will
      be a float.
    """

    result_list = []
    temp = ()
    for key, value in gdpdata.items():
        if is_number(key) and is_number(value) and int(key) >= \
        gdpinfo.get("min_year") and int(key) <= gdpinfo.get("max_year"):
            temp = (int(key), float(value))
            result_list.append(temp)
    return sorted(result_list)

def is_number(numbr):
    """
    Inputs:
      numbr - any number value

    Output:
      Returns true if input is really a number else return false
    """
    try:
        float(numbr)
        return True
    except ValueError:
        return False

def build_plot_dict(gdpinfo, country_list):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names

    Output:
      Returns a dictionary whose keys are the country names in
      country_list and whose values are lists of XY plot values
      computed from the CSV file described by gdpinfo.

      Countries from country_list that do not appear in the
      CSV file should still be in the output dictionary, but
      with an empty XY plot value list.
    """

    result_dict = {}

    # Read svg file into nested dictionary
    nested_dict = read_csv_as_nested_dict(gdpinfo.get("gdpfile"),\
    gdpinfo.get("country_name"), gdpinfo.get("separator"), gdpinfo.get("quote"))

    for country in country_list:
        if country in nested_dict:
            temp_country_plot_list = build_plot_values(gdpinfo, nested_dict.get(country))
            result_dict[country] = temp_country_plot_list
        else:
            result_dict[country] = []

    return result_dict


def render_xy_plot(gdpinfo, country_list, plot_file):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names
      plot_file    - String that is the output plot file name

    Output:
      Returns None.

    Action:
      Creates an SVG image of an XY plot for the GDP data
      specified by gdpinfo for the countries in country_list.
      The image will be stored in a file named by plot_file.
    """
    # Initialise chart
    xy_chart = pygal.XY()
    xy_chart.title = 'Counry GDP Chart'
    xy_chart.x_title = 'Year'
    xy_chart.y_title = 'GDP'

    # get XY plot dictionary for the given country lists
    xy_plot_dict = build_plot_dict(gdpinfo, country_list)

    # plot for each country_code
    for country in country_list:
        xy_chart.add(country, xy_plot_dict.get(country))

    # render Character
    ##xy_chart.render_to_file(plot_file)
    xy_chart.render_in_browser()



def test_build_plot_values(country):
    """
    Code to exercise render_xy_plot and generate plots from
    actual GDP data.
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
    test_dict = read_csv_as_nested_dict("isp_gdp.csv", "Country Name", ",", "'")
    country_dict = test_dict.get(country)
    del country_dict["Country Name"]
    del country_dict["Country Code"]
    del country_dict["Indicator Name"]
    del country_dict["Indicator Code"]
    result_list = build_plot_values(gdpinfo, test_dict.get(country))
    return result_list

#testDict = read_csv_as_nested_dict("isp_gdp.csv", "Country Name", ",", "'")
#test_result_list = test_build_plot_values("Hungary")
#print(test_result_list)

def test_render_xy_plot():
    """
    Code to exercise render_xy_plot and generate plots from
    actual GDP data.
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

    render_xy_plot(gdpinfo, [], "isp_gdp_xy_none.svg")
    ### uc_b_S render_xy_plot(gdpinfo, ["China"], "isp_gdp_xy_china.svg")
    ### render_xy_plot(gdpinfo, ["United Kingdom", "United States"], "isp_gdp_xy_uk+usa.svg")



# Make sure the following call to test_render_xy_plot is commented out
# when submitting to OwlTest/CourseraTest.

test_render_xy_plot()
