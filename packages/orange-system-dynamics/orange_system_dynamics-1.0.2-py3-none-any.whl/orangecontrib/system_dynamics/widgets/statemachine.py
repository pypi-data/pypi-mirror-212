from Orange.widgets import widget, gui, settings
from Orange.widgets.widget import Output
from AnyQt.QtWidgets import QAction, QFileDialog, QPushButton
import sismic.io
from sismic.io import import_from_yaml
from sismic.model import Statechart
from Orange.data import Table
from Orange.data.pandas_compat import table_from_frame


class OWStateMachine(widget.OWWidget):
    name = "State Machine"
    description = "Reads a YAML file containing a State Machine"
    icon = "icons/statemachine.svg"
    priority = 60
    statemachine = None
    current_path = None
    want_main_area = False
    graph_name = "thumbnailView"
    auto_commit = settings.Setting(True)

    class Outputs:
        output = Output("StateMachine", Statechart, auto_summary=False)

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

        vbox = gui.vBox(self.controlArea,
                        box="Select Simulation File:")
        hbox = gui.hBox(vbox)
        hbox.layout().addWidget(browse_button)

        gui.rubber(self.controlArea)
        gui.auto_commit(self.buttonsArea, self,
                        "auto_commit", "Send", box=False)

    @gui.deferred
    def commit(self):
        """
        Commits the result the next widget in the line.
        """

        if self.current_path:
            statemachine = _load_statemachine(self.current_path)
            self.Outputs.output.send(statemachine)

        else:
            self.Outputs.output.send(None)

    def __show_open_dialog_file(self):
        self.current_path, f = QFileDialog.getOpenFileName(
            self, 'Select directory/file',
            'some/default/path/', 'Product files'
            '(*.yaml *.scxml)')
        if self.current_path:
            self.commit.deferred()


def _load_statemachine(file):

    statemachine = import_from_yaml(filepath=file)
    return statemachine


if __name__ == "__main__":
    from orangewidget.utils.widgetpreview import WidgetPreview
    WidgetPreview(OWStateMachine).run()
