from Orange.widgets import widget, gui, settings
from Orange.widgets.widget import Output, Input
from AnyQt.QtGui import QPixmap, QImage
from AnyQt.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsView
import sismic.io
from sismic.io import import_from_yaml
from sismic.interpreter import Interpreter
from Orange.data import Table
from Orange.data.pandas_compat import table_from_frame
from .agent import Model, Agent


class OWEnvironment(widget.OWWidget):
    name = "Multi Agent Environment"
    description = "Defines interactions between agents " \
                  "in a multi-agent system configuration"
    icon = "icons/environment.svg"
    priority = 80
    statemachine = None
    population = 1000
    number_of_neighbors = 2
    network_randomness = 0.5
    initial_infection_share = 0.2
    infection_chance = 0.4
    recovery_chance = 0.2
    step = 0
    time = 0
    current_path = None
    want_main_area = True
    graph_name = "thumbnailView"
    auto_commit = settings.Setting(True)

    class Inputs:
        model = Input("Model", Model, auto_summary=False)

    class Outputs:
        output = Output("Data", Table)

    def __init__(self):
        super().__init__()
        self.output = None

        parameters_box = gui.widgetBox(self.controlArea, "Parameters:")

        gui.spin(parameters_box, self, "population", 0, 10 ** 8,
                 label="Number of agents:"
                 )

        gui.spin(parameters_box, self, "number_of_neighbors", 0, 100,
                 label="Number of neighbors per agent:"
                 )

        gui.doubleSpin(parameters_box, self,
                       "network_randomness", 0, 1,
                       decimals=2,
                       label="Network randomness:"
                       )

        gui.doubleSpin(parameters_box, self,
                       "initial_infection_share", 0, 1,
                       decimals=2,
                       label="Initial infection rate:"
                       )

        gui.doubleSpin(parameters_box, self,
                       "infection_chance", 0, 1,
                       decimals=2,
                       label="Infection chance:"
                       )

        gui.doubleSpin(parameters_box, self,
                       "recovery_chance", 0, 1,
                       decimals=2,
                       label="Recovery chance:"
                       )

        gui.rubber(self.controlArea)
        step_execute_box = gui.widgetBox(
            self.controlArea, "Step by step execution:")
        self.button = gui.button(
            step_execute_box, self, "Step execute",
            autoDefault=False,
            callback=self.step_execute
        )
        self.button = gui.button(
            step_execute_box, self, "Reset simulation",
            autoDefault=False,
            callback=self.reset_simulation
        )

        gui.rubber(self.controlArea)
        simulation_box = gui.widgetBox(self.controlArea)

        self.button = gui.button(
            simulation_box, self, "Run Simulation",
            autoDefault=False,
            callback=self.run_simulation
        )

        # Main area box
        gui.vBox(self.mainArea)
        self.main_box_scene = QGraphicsScene(self)
        self.main_box_view = QGraphicsView(self.main_box_scene)

        self.main_layout = self.mainArea.layout()
        self.main_layout.addWidget(self.main_box_view)

        self.mainArea.setMinimumWidth(100)

        gui.rubber(self.controlArea)
        gui.auto_commit(self.buttonsArea, self,
                        "auto_commit", "Send", box=False)

    def reset_simulation(self):
        self.step = 0
        self.model.sim_reset()
        self.main_box_scene.clear()
        self.output = None
        self.commit.deferred()

    def _update_sim_parameters(self):
        parameters = {'population': self.population,
                      'network_randomness':
                          self.network_randomness,
                      'number_of_neighbors':
                          self.number_of_neighbors,
                      'initial_infection_share':
                          self.initial_infection_share,
                      'recovery_chance': self.recovery_chance,
                      'infection_chance': self.infection_chance}

        return parameters

    def step_execute(self):
        if self.step == 0:
            self.model.set_parameters(self._update_sim_parameters())
            self.model.sim_setup()

        self.model.t = self.step
        self.model.sim_step()
        self.model.stop()
        self.step = self.step + 1

        self.model.create_output()
        results = self.model.output
        df = results.variables.Model

        # Visualize the graph
        self._show_graph()

        self.output = table_from_frame(df)
        self.commit.deferred()

    def run_simulation(self):

        self.model.set_parameters(self._update_sim_parameters())
        self.model.sim_reset()
        results = self.model.run(steps=100)
        self.step = self.model.t
        df = results.variables.Model

        # Visualize the graph
        self._show_graph()

        self.output = table_from_frame(df)
        self.commit.deferred()

    def _show_graph(self):

        figure = self.model.visualize()

        # Convert the Matplotlib figure to a QPixmap
        canvas = figure.canvas
        canvas.draw()
        buffer = canvas.buffer_rgba()
        qimage = QImage(buffer, canvas.get_width_height()[0],
                        canvas.get_width_height()[1],
                        QImage.Format_ARGB32)

        # Create a QGraphicsPixmapItem to display the graph
        pic = QGraphicsPixmapItem(QPixmap.fromImage(qimage))

        # Create a QGraphicsScene to hold the pixmap item
        self.main_box_scene.clear()
        self.main_box_scene.addItem(pic)

    def _set_new_environment(self, model):
        self.model = model

    @Inputs.model
    def set_model(self, model):
        self._set_new_environment(model)

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
    WidgetPreview(OWEnvironment).run()
