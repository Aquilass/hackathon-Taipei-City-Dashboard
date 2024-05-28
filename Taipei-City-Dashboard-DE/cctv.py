import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# step one : download the csv file from https://data.taipei/dataset/detail?id=50a5c4ec-9515-4c30-b83f-30b66e37053d and save it to the same directory as this script


# step two : create a function that reads the csv file and appends the first three digits of the camera ID to the URL
def original_to_modify():
    # Load the CSV file into a DataFrame
    df = pd.read_csv("cctv.csv")

    # Define the function to append the first three digits to the URL
    def append_to_url(camera_id):
        return "https://cctv.bote.gov.taipei:8502/jpg/" + camera_id[:3]

    # Apply the function to the '攝影機編號' column and store the result in a new column
    df["攝影機區域"] = df["攝影機編號"].apply(lambda x: x[:3])
    df["攝影機路徑"] = df["攝影機編號"].apply(append_to_url)
    df["攝影機數字編號"] = df["攝影機編號"].str.extract(r"(\d+)")
    # Save the DataFrame back to the CSV file
    df.to_csv("cctv_modify.csv", index=False)


def csv_to_geojson():
    # Load the CSV file into a DataFrame
    df = pd.read_csv("cctv_modify.csv")

    # Create a GeoDataFrame from the DataFrame
    geometry = [Point(xy) for xy in zip(df["WGSX"], df["WGSY"])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry)

    # Convert the GeoDataFrame to GeoJSON format
    gdf.to_file("cctv.geojson", driver="GeoJSON")


original_to_modify()
csv_to_geojson()
