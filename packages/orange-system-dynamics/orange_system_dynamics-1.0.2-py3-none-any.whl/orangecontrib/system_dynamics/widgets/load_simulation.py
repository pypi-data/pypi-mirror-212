from AnyQt.QtWidgets import QAction, QFileDialog, QPushButton
from Orange.widgets import widget, gui, settings
from Orange.widgets.widget import Output
from pathlib import Path
from pysd.py_backend.model import Model
import pysd


class OWLoadSimulation(widget.OWWidget):
    name = "Load Simulation"
    description = "Loads a simulation workflow from the " \
                  "directory structure, supports Vensim and Xmile"
    icon = "icons/load_simulation.svg"
    priority = 10

    current_path = None
    want_main_area = False
    graph_name = "thumbnailView"
    auto_commit = settings.Setting(True)

    class Outputs:
        output = Output("Model", Model, auto_summary=False)

    def __init__(self):
        super().__init__()
        self.output = None

        browse_action = QAction(
            self,
            text="\N{HORIZONTAL ELLIPSIS}",
        )

        browse_action.triggered.connect(self.__show_open_dialog_file)
        browse_button = QPushButton(
            browse_action.iconText(),
            clicked=browse_action.trigger
        )

        vbox = gui.vBox(self.controlArea, box="Select Simulation File:")
        hbox = gui.hBox(vbox)
        hbox.layout().addWidget(browse_button)

        gui.rubber(self.controlArea)
        gui.auto_commit(self.buttonsArea, self, "auto_commit", "Send",
                        box=False)

    @gui.deferred
    def commit(self):
        """
        Commits the result the next widget in the line.
        """
        if self.current_path:
            model = _load_model(self.current_path)
            self.Outputs.output.send(model)

        else:
            self.Outputs.output.send(None)

    def __show_open_dialog_file(self):
        self.current_path, f = QFileDialog.getOpenFileName(
            self, 'Select directory/file', 'some/default/path/',
            'Product files(*.mdl *.xmile)')
        if self.current_path:
            self.commit.deferred()


def _load_model(file):

    path = Path(file)

    if path.suffix == ".mdl":
        model = pysd.read_vensim(file)

    elif path.suffix == ".xmile":
        model = pysd.read_xmile(file)

    else:
        raise ValueError("File format not supported")

    return model


if __name__ == "__main__":
    from orangewidget.utils.widgetpreview import WidgetPreview
    WidgetPreview(OWLoadSimulation).run()
