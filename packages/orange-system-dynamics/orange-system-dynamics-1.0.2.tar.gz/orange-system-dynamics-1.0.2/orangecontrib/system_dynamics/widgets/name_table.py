from Orange.widgets import widget, gui, settings
from Orange.widgets.widget import Output, Input
from Orange.data import Table
from pysd.py_backend.model import Model


class OWNameTable(widget.OWWidget):
    name = "Name Table"
    description = "Allows to rename an Orange Table"
    icon = "icons/name.svg"
    priority = 50

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

    variables_names = []

    want_main_area = False
    graph_name = "thumbnailView"
    auto_commit = settings.Setting(True)

    class Inputs:
        model = Input("Model", Model, auto_summary=False)
        data = Input("Data", Table)

    class Outputs:
        output = Output("Data", Table)

    def __init__(self):
        super().__init__()
        self.data = None
        self.model = None
        self.output = None

        self.combobox = gui.comboBox(
            self.controlArea, self, "", items=self.variables_names,
            box="Select Variable Name:",
            contentsLength=8,
        )
        self.combobox.activated.connect(self.set_table_name)

        gui.rubber(self.controlArea)
        gui.auto_commit(self.buttonsArea, self, "auto_commit", "Send",
                        box=False)

    def set_table_name(self):
        if self.data:
            table = self.data
            name = self.combobox.currentText()
            self.output = [name, table]
            self.commit.deferred()

    def get_variables(self, model):
        self.model = model
        self.variables_names = []

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
            if k not in self.stocks.union(self.flows, self.time_params,
                                          stateful)
        }
        self.variables_names = list(self.auxs)
        self.combobox.clear()
        self.combobox.addItems([name for name in self.variables_names])

    @Inputs.model
    def set_model(self, model):
        self.get_variables(model)

    @Inputs.data
    def set_data(self, data):
        self.data = data

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
    WidgetPreview(OWNameTable).run()
