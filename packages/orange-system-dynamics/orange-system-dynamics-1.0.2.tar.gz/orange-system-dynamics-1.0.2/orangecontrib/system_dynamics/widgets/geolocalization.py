from Orange.data import Table
from Orange.widgets import widget, gui, settings
from Orange.widgets.widget import Output
import shapefile


class OWGeoLocalization(widget.OWWidget):
    name = "Geo Localization"
    description = "Provides Geolocation data (latitude/longitude)"
    icon = "icons/geolocation.svg"
    priority = 40
    shape_recs = []
    nuts_available = []
    nodes = []
    want_main_area = False
    graph_name = "thumbnailView"
    auto_commit = settings.Setting(True)
    nuts_url = "https://gisco-services.ec.europa.eu/distribution/v2/nuts/" \
               "shp/NUTS_RG_20M_2021_4326.shp.zip"

    class Outputs:
        output = Output("Data", Table)

    def __init__(self):
        super().__init__()
        self.output = None

        self.combobox = gui.comboBox(
            self.controlArea, self, "", items=self.nuts_available,
            box="Select NUTS Region:",
            contentsLength=8,
        )
        self.combobox.activated.connect(self.set_coordinates)

        gui.rubber(self.controlArea)
        self.get_coordinates()
        gui.auto_commit(self.buttonsArea, self, "auto_commit", "Send",
                        box=False)

    def set_coordinates(self):
        idx_nuts = self.combobox.currentIndex()
        shp = shapefile.Reader(self.nuts_url)
        shape_rec = self.shape_recs[idx_nuts]
        polygon = shape_rec[0]

        shape = shp.shape(polygon)
        bbox = shape.bbox
        print(bbox)

        lon = bbox[0] + (bbox[2] - bbox[0])/2
        lat = bbox[1] + (bbox[3] - bbox[1])/2

        self.output = {'lon': lon,  'lat': lat}
        print(self.output)
        self.commit.deferred()

    def get_coordinates(self):
        shp = shapefile.Reader(self.nuts_url)
        self.shape_recs = [(shapeRec.record.oid,
                            f'NUTS {shapeRec.record[1]}'
                            f' - {shapeRec.record[3]}')
                           for shapeRec in
                           shp.iterShapeRecords()]
        self.nuts_available = [shapeRec[1] for shapeRec in self.shape_recs]
        self.combobox.clear()
        self.combobox.addItems(self.nuts_available)

    @gui.deferred
    def commit(self):
        """
        Commits the result the next widget in the line.
        """
        if self.output:
            self.Outputs.output.send(self.output)

        else:
            self.Outputs.output.send(None)


if __name__ == "__main__":
    from orangewidget.utils.widgetpreview import WidgetPreview
    WidgetPreview(OWGeoLocalization).run()
