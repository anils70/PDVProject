"""
Week 2 practice project template for Python Data Visualization
Compute county centers from an SVG image of USA that includes county boundaries
Output a CSV file with FIPS code and county centers
"""

import math
import csv



# Parse the XMLin USA SVG file extract county attributes
# Derive from example code - https://stackoverflow.com/questions/15857818/python-svg-parser

from xml.dom import minidom

def get_county_attributes(svg_file_name):
    """
    Given SVG file associate with string svg_file_name, extract county attributes from associated XML
    Return a list of tuples consisting of FIPS codes (strings) and county boundaries (strings)
    """
    svg_doc = minidom.parse(svg_file_name)
    county_attribute_list = []
    for path in svg_doc.getElementsByTagName('path'):
        FIPS_code = path.getAttribute('id')
        county_boundary_data = path.getAttribute('d')
        county_attribute_list.append((FIPS_code, county_boundary_data))
    svg_doc.unlink()
    return county_attribute_list
    doc.unlink()
    return path_strings


def test_get_attributes(svg_file_name):
    """
    """
    county_attribute_list = get_county_attributes(svg_file_name)
    print(len(county_attribute_list))
    print(county_attribute_list[30])
    print()
    print(county_attribute_list[100])
    print()
    print(county_attribute_list[1000])

## test_get_attributes("USA_Counties_2014.svg")

# Code to compute the center of a county from its boundary (as a string)

def get_boundary_coordinates(boundary_data):
    """
    Given the country boundary data as a string,
    Return the county boundary as a list of coordinates
    Ignores 'M', 'L, 'z'
    """
    boundary_data = boundary_data.replace('z', '')
    boundary_data = boundary_data.replace('M', 'L')
    boundary_list = boundary_data.split('L')[1:]

    boundary_coordinates = []
    for entry in boundary_list:
        temp = entry.split(',')
        if len(temp) == 2:
            (xcoord, ycoord) = temp
        else:
            print(len(temp))
            print(temp)
        boundary_coordinates.append((float(xcoord), float(ycoord)))
    return boundary_coordinates


# Provided code to estimate a county center from a list of coordinates on county boundary

def dist(pt1, pt2):
    """
    Compute Euclidean distance between two points
    """
    return math.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)

def compute_county_center(boundary_coordinates):
    """
    Given a list of coordinates (tuples of two floats) on the county boundary,
    Return an estimate of the center of the county as a tuple of two floats
    Assumes the list of coordinates forms a closed polygon with first and last point repeated
    """
    centroid = [0, 0]
    perimeter = 0
    for idx in range(len(boundary_coordinates) - 1):
        edge_length = dist(boundary_coordinates[idx], boundary_coordinates[idx + 1])
        centroid[0] += 0.5 * (boundary_coordinates[idx][0] + boundary_coordinates[idx + 1][0]) * edge_length
        centroid[1] += 0.5 * (boundary_coordinates[idx][1] + boundary_coordinates[idx + 1][1]) * edge_length
        perimeter += edge_length
    return [(centroid[0] / perimeter), (centroid[1] / perimeter)]

def process_county_attributes(svg_file_name, csv_file_name):
    """
    Given SVG file name (as string), extract county attributes (FIPS code and county boundaries)
    Then compute county centers and write a CSV file with columns corresponding to FIPS code, x-coord of centers, y-coord of centers
    """

    # Extract county attibutes from SVG file
    county_attribute_list = get_county_attributes(svg_file_name)
    print("Processed", len(county_attribute_list), "entries")

    # Ouput CSV file
    with open(csv_file_name, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for (fips, boundary) in county_attribute_list:
            boundary_coordinates = get_boundary_coordinates(boundary)
            center = compute_county_center(boundary_coordinates)
            csv_writer.writerow([fips, center[0], center[1]])
    print("Wrote csv file", csv_file_name)


# Output CSV file should have 3143 rows

#process_county_attributes("USA_Counties_with_FIPS_and_names.svg", "USA_Counties_with_FIPS_and_centers.csv")
process_county_attributes("USA_Counties_2014.svg", "USA_Counties_with_FIPS_and_centers.csv")
