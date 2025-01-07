from flask import Flask, request, jsonify, render_template
import geopandas as gpd
from shapely.geometry import shape

app = Flask(__name__)

# Mapping lokasi file ke nama file sebenarnya
LOCATION_FILES = {
    "malang_city.gpkg": "qgis file\Bangunan Kota Malang.gpkg",
    "batu_city.gpkg": "qgis file\Bangunan Kota Batu.gpkg",
    "pasuruan_regency.gpkg": "qgis file\Bangunan Kabupaten Pasuruan.gpkg",
    "pasuruan_city.gpkg": "qgis file\Bangunan Kota Pasuruan.gpkg"
}

@app.route("/")
def home():
    """Serve the index HTML."""
    return render_template("index2.html")

@app.route("/count", methods=["POST"])
def count_buildings():
    """Process building count request."""
    try:
        data = request.json
        drawn_polygon = data.get("drawn_polygon")
        selected_file = data.get("selected_file")

        if not drawn_polygon or not selected_file:
            return jsonify({"error": "Invalid input"}), 400

        # Load the appropriate file based on selected location
        file_path = LOCATION_FILES.get(selected_file)
        if not file_path:
            return jsonify({"error": "File not found"}), 404

        # Read the geospatial data
        gdf = gpd.read_file(file_path)

        # Convert the drawn polygon to a Shapely geometry
        user_polygon = shape(drawn_polygon)

        # Clip the GeoDataFrame to the drawn polygon
        clipped_gdf = gdf[gdf.geometry.intersects(user_polygon)]

        # Count the buildings
        building_count = len(clipped_gdf)

        return jsonify({"count": building_count})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
