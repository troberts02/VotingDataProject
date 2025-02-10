Pitt County Voter Distribution Analysis
Project Overview

This project analyzes the distribution of voters in Pitt County, North Carolina, across different school districts (Elementary, Middle, and High School). The analysis is broken down by political party affiliation (DEM, REP, UNA) and includes visualizations of voter count, density, and percentage distribution within each district.
Project Structure

    Code: The main script final_project_Trey_Roberts.py contains the code for processing the voter data and generating the visualizations.

    Data: The data used in this project is stored in the Data folder, which includes:

        pitt_voters.gpkg: Geopackage file containing voter data.

        GIS_DATA: Folder containing shapefiles for Elementary, Middle, and High School districts.

    Output: The output visualizations are saved in the Output folder as JPEG images.

Dependencies

To run this project, you will need the following Python libraries:

    geopandas

    numpy

    matplotlib

    shapely

You can install these dependencies using pip:
bash
Copy

pip install geopandas numpy matplotlib shapely

How to Run the Project

    Clone the repository or download the project files.

    Ensure that all dependencies are installed.

    Navigate to the project directory.

    Run the main script:
    bash
    Copy

    python final_project_Trey_Roberts.py

    The output visualizations will be saved in the Output folder.

Modifying the Loaded Data

If you want to change the loaded data (e.g., use a different voter dataset or school district boundaries), follow these steps:

    Voter Data:

        Replace the pitt_voters.gpkg file in the Data folder with your new voter data file.

        Ensure the new file has a geometry column for spatial data and a party_cd column for party affiliation.

        Update the voter_data_file variable in the main() function to point to your new file:
        python
        Copy

        voter_data_file = data_folder / 'your_new_voter_file.gpkg'

    School District Data:

        Replace the shapefiles in the GIS_DATA folder with your new district boundary files.

        Update the district_files_dict variable in the main() function to point to your new files:
        python
        Copy

        district_files_dict = {
            "Elementary School Districts": [gis_data_folder / 'your_elementary_districts.shp'],
            "Middle School Districts": [gis_data_folder / 'your_middle_districts.shp'],
            "High School Districts": [gis_data_folder / 'your_high_districts.shp']
        }

Output Files

The script generates three JPEG files, one for each type of school district:

    elementary_school_districts_distribution_TreyRoberts.jpg

    middle_school_districts_distribution_TreyRoberts.jpg

    high_school_districts_distribution_TreyRoberts.jpg

Each file contains visualizations for voter count, density, and percentage distribution for DEM, REP, and UNA voters.
Author

    Trey Roberts

    Email: robertstrey9@gmail.com

Acknowledgments

    Data provided by Pitt County GIS.

    Special thanks to the instructors and peers for their support and feedback.
