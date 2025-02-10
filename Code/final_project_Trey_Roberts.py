import geopandas as gpd
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt
from shapely.strtree import STRtree

def count_voter_by_polygon(point_series: gpd.GeoSeries, polygons_series: gpd.GeoSeries):
    data = np.zeros((len(polygons_series), 2))  # Count and Density
    result_gdf = gpd.GeoDataFrame(data=data, columns=("Count", "Density"), geometry=polygons_series)
    point_2264 = point_series.to_crs("EPSG:2264")
    points_tree = STRtree(point_2264.geometry)
    points_df = point_2264.reset_index(drop=True)

    for i, polygon in enumerate(polygons_series):
        print(f"Processing {i+1} of {len(polygons_series)} polygons")
        possible_matches = points_tree.query(polygon)
        if possible_matches.size:
            possible_matches_indices = [points_df.index.get_loc(index) for index in possible_matches]
            within_polygon = points_df.iloc[possible_matches_indices]
            within_polygon = within_polygon[within_polygon.within(polygon)]
            count = len(within_polygon)
        else:
            count = 0

        area_in_sqmi = polygon.area * 3.86102e-7
        density = count / area_in_sqmi if area_in_sqmi > 0 else 0

        result_gdf.loc[i, "Count"] = count
        result_gdf.loc[i, "Density"] = density

    return result_gdf

def calculate_percentage(gdf, total_count):
    gdf["Percent"] = (gdf["Count"] / total_count) * 100
    return gdf

def plot_voter_distribution(district_files, voters_gdfs, school_type, output_prefix, output_folder):
    num_parties = 3
    num_plots_per_party = 3  # Count, Density, Percentage
    num_districts = len(district_files)
    fig, axes = plt.subplots(nrows=num_parties, ncols=num_plots_per_party * num_districts,
                             figsize=(16 * num_districts, 6 * num_parties),
                             gridspec_kw={'hspace': 0.5, 'wspace': 0.3})

    party_labels = ["DEM", "REP", "UNA"]
    for idx, (party, voters_gdf) in enumerate(voters_gdfs.items()):
        for col_idx, district_file in enumerate(district_files):
            district_gdf = gpd.read_file(district_file, engine="pyogrio")
            voter_district_gdf = count_voter_by_polygon(voters_gdf["geometry"], district_gdf["geometry"])
            voter_district_gdf.insert(0, column="district", value=district_gdf["NAME"])

            total_count = len(voters_gdf)
            voter_district_gdf = calculate_percentage(voter_district_gdf, total_count)

            ax_count = axes[idx, 3 * col_idx]
            ax_density = axes[idx, 3 * col_idx + 1]
            ax_percent = axes[idx, 3 * col_idx + 2]

            voter_district_gdf.plot(ax=ax_count, column="Count", cmap="jet", legend=True)
            ax_count.set_title(f"{party} Voter Count")

            voter_district_gdf.plot(ax=ax_density, column="Density", cmap="jet", legend=True)
            ax_density.set_title(f"{party} Voter Density")

            voter_district_gdf.plot(ax=ax_percent, column="Percent", cmap="viridis", legend=True, vmin=2, vmax=12)
            ax_percent.set_title(f"{party} Percentage")

    plt.suptitle(f"Pitt County Voter Distribution by {school_type}, by Trey Roberts (robertsda20@students.ecu.edu)", fontsize=16)
    plt.savefig(output_folder / f"{output_prefix}_distribution_TreyRoberts.jpg")

def main():
    base_dir = Path(__file__).resolve().parent.parent
    data_folder = base_dir / 'Data'
    gis_data_folder = data_folder / 'GIS_DATA'
    output_folder = base_dir / 'Output'
    output_folder.mkdir(parents=True, exist_ok=True)

    voter_data_file = data_folder / 'pitt_voters.gpkg'
    voter_gdf = gpd.read_file(voter_data_file, engine="pyogrio")
    
    voters_gdfs = {
        "DEM": voter_gdf[voter_gdf["party_cd"] == "DEM"],
        "REP": voter_gdf[voter_gdf["party_cd"] == "REP"],
        "UNA": voter_gdf[voter_gdf["party_cd"] == "UNA"]
    }

    district_files_dict = {
        "Elementary School Districts": [gis_data_folder / 'Pitt_County_Elementary_School_Attendance_Districts' / 'Pitt_County_Elementary_School_Attendance_Districts.shp'],
        "Middle School Districts": [gis_data_folder / 'Pitt_County_Middle_School_Attendance_Districts' / 'Pitt_County_Middle_School_Attendance_Districts.shp'],
        "High School Districts": [gis_data_folder / 'Pitt_County_High_School_Attendance_Districts' / 'Pitt_County_High_School_Attendance_Districts.shp']
    }

    for school_type, district_files in district_files_dict.items():
        output_prefix = school_type.replace(" ", "_").lower()
        plot_voter_distribution(district_files, voters_gdfs, school_type, output_prefix, output_folder)

if __name__ == "__main__":
    main()
