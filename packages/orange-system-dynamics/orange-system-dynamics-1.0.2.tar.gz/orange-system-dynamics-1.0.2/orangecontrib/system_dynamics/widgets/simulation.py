from Orange.widgets import widget, gui, settings
from Orange.data import Table
from Orange.widgets.widget import Output, MultiInput, Input
from Orange.data.pandas_compat import table_from_frame, table_to_frame
from pysd.py_backend.model import Model
import datetime
import pandas as pd


class OWSimulation(widget.OWWidget):
    name = "Simulation"
    description = "Executes a simulation model, allows to modify parameters " \
                  "and discrete execution"
    icon = "icons/simulation.svg"
    priority = 20
    new = 0

    stocks = set()
    flows = set()
    auxs = set()

    time_params = {
        "final_time",
        "initial_time",
        "time_step",
        "saveper",
        "time",
    }

    want_main_area = False
    graph_name = "thumbnailView"
    auto_commit = settings.Setting(True)

    class Inputs:
        model = Input("Model", Model, auto_summary=False)
        data = MultiInput("Data", Table)
        location = Input("GeoLocation", Table)

    class Outputs:
        output = Output("Data", Table)

    def __init__(self):
        super().__init__()
        self.data = {}
        self.location = None
        self.output = None

        box = gui.widgetBox(self.controlArea)
        self.button = gui.button(
            box, self, "Run Simulation",
            autoDefault=False,
            callback=self.run_simulation
        )

        gui.rubber(self.controlArea)
        gui.auto_commit(self.buttonsArea, self,
                        "auto_commit", "Send", box=False)

    def run_simulation(self):

        if self.model:
            model = self.model

            dict_initial_value = {}
            for stock in self.stocks:

                if self.model[stock] != self.__getattribute__(stock):
                    dict_initial_value[stock] = self.__getattribute__(stock)

            dict_params = {}
            for aux in self.auxs:
                print(self.model[aux])

                if self.model[aux] != self.__getattribute__(aux):
                    dict_params[aux] = self.__getattribute__(aux)
                else:
                    dict_params[aux] = self.__getattribute__(
                        f'{aux}_duplicate')

            df = model.run(initial_condition=(self.time_start,
                                              dict_initial_value),
                           params=dict_params,
                           time_step=self.time_step,
                           final_time=self.time_stop
                           )

            indices = list(df.iloc[:, 0].keys())

            time = []
            for i in range(len(indices)):
                time.append((datetime.date(1999, 1, 1) + datetime.timedelta(
                    days=(indices[i])*7)).strftime('%Y-%m-%d %H:%M:%S'))
            df['Time'] = time

            # Add Geo Location:
            if self.location is not None:
                longitude = []
                latitude = []

                lon = self.location['lon']
                lat = self.location['lat']

                for i in range(len(indices)):
                    longitude.append(lon)
                    latitude.append(lat)

                df['Lon'] = longitude
                df['Lat'] = latitude

            self.output = table_from_frame(df)

            self.model.reload()
        self.commit.deferred()

    def _set_new_model(self, model):
        self.output = None
        self.model = model

        self.time_start = model["INITIAL TIME"]
        self.time_stop = model["FINAL TIME"]
        self.time_step = model["TIME STEP"]

        deps = self.model.dependencies
        stocks_integ = [k for k in deps.keys() if k.startswith("_integ")]
        stateful = [k for k in deps.keys() if k.startswith("_")]
        for s in stocks_integ:
            self.stocks.update(
                [
                    k.lower().replace(" ", "_")
                    for k in deps.keys()
                    if s in deps[k]
                ]
            )
            self.flows.update(
                [k.lower().replace(" ", "_") for k in deps[s]["step"].keys()]
            )
        self.auxs = {
            k.lower().replace(" ", "_")
            for k in deps.keys()
            if k not in self.stocks.union(self.flows,
                                          self.time_params,
                                          stateful)
        }

        if len(self.controlArea.children()) <= 3:

            self.time_box = gui.widgetBox(self.controlArea, "Time Controls:")
            gui.rubber(self.controlArea)
            self.stocks_box = gui.widgetBox(self.controlArea, "Stocks: ")
            gui.rubber(self.controlArea)
            self.auxs_box = gui.widgetBox(self.controlArea,
                                          "Auxiliary Values: ")

            gui.doubleSpin(self.time_box, self, "time_start",  0, 10**10,
                           decimals=4,
                           label="Start Time")
            gui.doubleSpin(self.time_box, self, "time_stop", 0, 10**10,
                           decimals=4,
                           label="Stop Time")
            gui.doubleSpin(self.time_box, self, "time_step", 0, 10**10,
                           decimals=4,
                           label="Step Time")

            for stock in self.stocks:
                self.__setattr__(stock, self.model[stock])
                gui.doubleSpin(self.stocks_box, self, stock, 0, 10**10,
                               decimals=2,
                               label=stock)

            for aux in self.auxs:
                self.__setattr__(aux, self.model[aux])
                self.__setattr__(f'{aux}_duplicate', self.model[aux])
                self.__setattr__(f'{aux}_state', False)

                gui.doubleSpin(self.auxs_box, self, aux, 0, 10**10,
                               decimals=2,
                               label=aux,)

    def set_variable(self, aux):

        df = table_to_frame(self.data[aux])
        print(df)

        lst = df.iloc[0].tolist()
        factor = len(lst) * [52]
        res = [x for x, n in zip(lst, factor) for _ in range(n)]

        var = pd.Series(index=range(len(res)), data=res)

        self.__setattr__(f'{aux}_duplicate', var)

    @Inputs.model
    def set_model(self, model):
        self._set_new_model(model)

    @Inputs.location
    def set_location(self, location):
        self.location = location

    @Inputs.data
    def set_data(self, _, table):
        self.data[table[0]] = table[1]
        self.set_variable(table[0])

    @Inputs.data.insert
    def insert_data(self, _, table):
        self.data[table[0]] = table[1]
        self.set_variable(table[0])

    @Inputs.data.remove
    def remove_data(self, index):
        if index == 0:
            self.data = {}

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
    WidgetPreview(OWSimulation).run()
