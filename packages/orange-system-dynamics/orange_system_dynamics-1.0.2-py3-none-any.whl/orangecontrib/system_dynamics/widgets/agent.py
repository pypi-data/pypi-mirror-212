from Orange.widgets import widget, gui, settings
from Orange.widgets.widget import Output, Input
from AnyQt.QtGui import QPixmap
from AnyQt.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsView
import sismic.io
from sismic.io import import_from_yaml, export_to_plantuml
from sismic.interpreter import Interpreter
from sismic.model import Statechart
import os
import io
import sys
import plantuml
from Orange.data import Table
from Orange.data.pandas_compat import table_from_frame
import agentpy as ap
import networkx as nx
from matplotlib import pyplot as plt


class Agent(ap.Agent):

    def setup(self):
        """ Initialize a new variable at agent creation. """
        self._statemachine = self.model.statemachine
        self.states = self._statemachine.states
        self.transitions = self._statemachine.transitions
        self.events = self._statemachine.events_for()

        interpreter = Interpreter(self._statemachine)
        interpreter.execute_once()

        # State 0 is a root state
        self.actual_state = interpreter.configuration[1]
        self.event = self._statemachine.preamble

    @property
    def statemachine(self) -> Statechart:
        """
        Embedded statechart
        """
        return self._statemachine

    def update_state(self):
        for transition in self.transitions:
            if transition.source == self.actual_state and \
                    self.event == transition.event:
                self.actual_state = transition.target


class Model(ap.Model):

    def add_statemachine(self, statemachine):
        self._statemachine = statemachine

    @property
    def statemachine(self) -> Statechart:
        """
        Embedded statechart
        """
        return self._statemachine

    def setup(self):
        """ Initialize the agents and network of the model. """

        # Prepare a small-world network
        self.graph = nx.watts_strogatz_graph(
            self.p.population,
            self.p.number_of_neighbors,
            self.p.network_randomness)

        # Create agents and network
        self.agents = ap.AgentList(self, self.p.population, Agent)
        self.network = self.agents.network = ap.Network(self, self.graph)
        self.network.add_agents(self.agents, self.network.nodes)

        for i, agent in enumerate(self.agents):
            self.graph.add_node(i, agent=agent)

        # Add edges between nodes in the graph
        for i in range(self.p.population):
            for j in self.graph.neighbors(i):
                self.graph.add_edge(i, j)

        # Infect a random share of the population
        io = int(self.p.initial_infection_share * self.p.population)
        self.agents.random(io).actual_state = "infectious"
        for agent in self.agents:
            if agent.actual_state == 'infectious':
                agent.color = (0, 0, 1)
                agent.timer = 3
            if agent.actual_state == 'susceptible':
                agent.color = (0, 0.6, 1)
                agent.timer = 0

    def update(self):
        """ Record variables after setup and each step. """

        # Record share of agents with each condition
        for i, c in enumerate(('susceptible', 'infectious',
                               'recovered', 'dead')):
            n_agents = len(self.agents.select(
                self.agents.actual_state == c))
            self[c] = n_agents
            self.record(c)

        # Stop simulation if disease is gone
        if self.infectious == 0:
            self.stop()

    def step(self):
        """ Define the models' events per simulation step. """

        for agent in self.agents:
            rng = self.model.random

            for n in agent.network.neighbors(agent):
                if n.actual_state == 'infectious' and \
                        agent.actual_state == 'susceptible':
                    if self.p.infection_chance > rng.random():
                        agent.event = 'infection = True'
                        agent.timer = 3
                        agent.color = (0, 0, 1)

            if agent.actual_state == 'infectious':
                agent.timer -= 1
                if agent.timer == 0:
                    if self.p.recovery_chance > rng.random():
                        agent.event = 'recovery = True'
                        agent.color = (0.2, 1, 0)
                    else:
                        agent.event = 'recovery = False'
                        agent.color = (0, 0, 0)

        # Call 'update_state' for all agents
        self.agents.update_state()

    def end(self):
        """ Record evaluation measures at the end of the simulation. """

    def visualize(self):
        # Create a layout for the graph
        pos = nx.circular_layout(self.graph)

        # Create a new figure
        figure = plt.figure()

        # Draw the graph nodes and edges
        nx.draw_networkx_nodes(self.graph, pos,
                               node_color=[agent.color
                                           for agent in self.agents])
        nx.draw_networkx_edges(self.graph, pos)

        # Add a legend for the agent colors
        color_labels = {'susceptible': (0, 0.6, 1),
                        'infectious': (0, 0, 1), 'recovered': (0.2, 1, 0),
                        'dead': (0, 0, 0)}
        patches = [plt.plot([], [], marker="o", ms=10, ls="",
                            mec=None, color=color_labels[key],
                            label=key)[0] for key in color_labels]
        plt.legend(handles=patches, ncol=4, frameon=False)

        return figure


class OWAgent(widget.OWWidget):
    name = "Agent"
    description = "Creates an agent from State Machine"
    icon = "icons/agent.svg"
    priority = 70
    want_main_area = True
    graph_name = "thumbnailView"
    auto_commit = settings.Setting(True)

    class Inputs:
        statemachine = Input("StateMachine", Statechart, auto_summary=False)

    class Outputs:
        output = Output("Model", Model, auto_summary=False)

    def __init__(self):
        super().__init__()
        self.output = None

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

    def _create_agent_from_machine(self, statemachine):
        self.model = Model()
        self.model.add_statemachine(statemachine)
        self.agent = Agent(self.model)
        self._show_agent()

    def _show_agent(self):

        graph = sismic.io.export_to_plantuml(self.agent.statemachine)
        img = plantuml.PlantUML(
            'http://www.plantuml.com/plantuml/img/').processes(graph)

        # show a PNG thumbnail of the original image
        pixmap = QPixmap()
        pixmap.loadFromData(img)

        pic = QGraphicsPixmapItem()
        pic.setPixmap(pixmap)
        self.main_box_scene.clear()
        self.main_box_scene.addItem(pic)

    @Inputs.statemachine
    def set_statemachine(self, statemachine):
        self._create_agent_from_machine(statemachine)
        self.commit.deferred()

    @gui.deferred
    def commit(self):
        """
        Commits the result the next widget in the line.
        """
        if self.agent:
            self.Outputs.output.send(self.model)

        else:
            self.Outputs.output.send(None)


if __name__ == "__main__":
    from orangewidget.utils.widgetpreview import WidgetPreview
    WidgetPreview(OWAgent).run()
