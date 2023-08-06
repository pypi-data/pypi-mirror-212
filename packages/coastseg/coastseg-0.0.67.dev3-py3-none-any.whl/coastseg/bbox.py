# Standard library imports
import logging
from typing import Union

# Internal dependencies imports
from .exceptions import BboxTooLargeError, BboxTooSmallError
from coastseg.common import remove_z_axis, get_ids_with_invalid_area

# External dependencies imports
import geopandas as gpd
from shapely.geometry import shape
from ipyleaflet import GeoJSON


logger = logging.getLogger(__name__)

__all__ = ["Bounding_Box"]


class Bounding_Box:
    """Bounding_Box

    A Bounding Box drawn by user.
    """

    MAX_AREA = 3000000000  # UNITS = Sq. Meters
    MIN_AREA = 9000  # UNITS = Sq. Meters
    LAYER_NAME = "Bbox"

    def __init__(self, rectangle: Union[dict, gpd.GeoDataFrame], filename: str = None):
        self.gdf = None
        self.filename = "bbox.geojson"
        if isinstance(rectangle, gpd.GeoDataFrame):
            self.gdf = self._initialize_from_gdf(rectangle)
        elif isinstance(rectangle, dict):
            self.gdf = self.create_geodataframe(rectangle)
        else:
            raise Exception(
                "Invalid rectangle provided to BBox must be either a geodataframe or dict"
            )
        if filename:
            self.filename = filename

    def __str__(self):
        return f"BBox: geodataframe {self.gdf}"

    def __repr__(self):
        return f"BBox: geodataframe {self.gdf}"

    def _initialize_from_gdf(self, bbox_gdf: gpd.GeoDataFrame) -> None:
        """
        Initialize the `gdf` attribute from a GeoDataFrame containing a bounding box.

        Args:
            rois_gdf: A GeoDataFrame containing a bounding box.

        Returns:
            None.

        Raises:
            None.
        """
        # keep only the geometry and id columns
        columns = ["geometry"]
        keep_columns = [col for col in columns if col in bbox_gdf.columns]
        bbox_gdf = bbox_gdf[keep_columns]

        # remove z-axis
        bbox_gdf = remove_z_axis(bbox_gdf)
        bbox_gdf.to_crs("EPSG:4326")
        return bbox_gdf

    def create_geodataframe(
        self, rectangle: dict, crs: str = "EPSG:4326"
    ) -> gpd.GeoDataFrame:
        """Creates a geodataframe with the crs specified by crs
        Args:
            rectangle (dict): geojson dictionary
            crs (str, optional): coordinate reference system string. Defaults to 'EPSG:4326'.

        Returns:
            gpd.GeoDataFrame: geodataframe with geometry column = rectangle and given crs
        """
        geom = [shape(rectangle)]
        geojson_bbox = gpd.GeoDataFrame({"geometry": geom})
        geojson_bbox.crs = crs
        # remove z-axis
        geojson_bbox = remove_z_axis(geojson_bbox)
        return geojson_bbox

    def style_layer(self, geojson: dict, layer_name: str) -> "ipyleaflet.GeoJSON":
        """Return styled GeoJson object with layer name

        Args:
            geojson (dict): geojson dictionary to be styled
            layer_name(str): name of the GeoJSON layer
        Returns:
            "ipyleaflet.GeoJSON": shoreline as GeoJSON layer styled with yellow dashes
        """
        if geojson == {}:
            raise Exception("ERROR.\n Empty geojson cannot be drawn onto map")
        return GeoJSON(
            data=geojson,
            name=layer_name,
            style={
                "color": "#75b671",
                "fill_color": "#75b671",
                "opacity": 1,
                "fillOpacity": 0.1,
                "weight": 3,
            },
        )

    def check_bbox_size(bbox_area: float):
        """ "Raises an exception if the size of the bounding box is too large or small."""
        # Check if the size is greater than MAX_BBOX_SIZE
        if bbox_area > Bounding_Box.MAX_AREA:
            raise BboxTooLargeError()
        # Check if size smaller than MIN_BBOX_SIZE
        elif bbox_area < Bounding_Box.MIN_AREA:
            raise BboxTooSmallError()
