from Orange.widgets import widget, gui, settings
from Orange.widgets.widget import Output

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QApplication, QStyle, QHBoxLayout, QComboBox, \
    QStyledItemDelegate, qApp
from PyQt5.QtWidgets import QAction, QFileDialog, QPushButton
from PyQt5.QtGui import QStandardItem, QPalette, QFontMetrics

from Orange.data import Table, Domain, TimeVariable

from pandas.core.frame import DataFrame
from drb.drivers.eurostat import DrbEurostatFactory, DrbEurostatServiceNode
from drb.drivers.discodata import DrbDiscodataServiceNode
from Orange.data.pandas_compat import table_from_frame

import xarray as xarray


from drb.utils import keyringconnection
from drb.drivers.era5.era5 import Era5ServiceNode, \
    Era5PredicateEra5SingleLevelsByHour,\
    Era5PredicateEra5SingleLevelsByMonth, Era5PredicateEra5Base


class CheckableComboBox(QComboBox):

    # Subclass Delegate to increase item height
    class Delegate(QStyledItemDelegate):
        def sizeHint(self, option, index):
            size = super().sizeHint(option, index)
            size.setHeight(20)
            return size

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setEditable(True)
        self.lineEdit().setReadOnly(True)

        palette = qApp.palette()
        palette.setBrush(QPalette.Base, palette.button())
        self.lineEdit().setPalette(palette)

        self.setItemDelegate(CheckableComboBox.Delegate())

        self.model().dataChanged.connect(self.updateText)

        self.lineEdit().installEventFilter(self)
        self.closeOnLineEditClick = False

        self.view().viewport().installEventFilter(self)

    def resizeEvent(self, event):
        self.updateText()
        super().resizeEvent(event)

    def eventFilter(self, object, event):

        if object == self.lineEdit():
            if event.type() == QEvent.MouseButtonRelease:
                if self.closeOnLineEditClick:
                    self.hidePopup()
                else:
                    self.showPopup()
                return True
            return False

        if object == self.view().viewport():
            if event.type() == QEvent.MouseButtonRelease:
                index = self.view().indexAt(event.pos())
                item = self.model().item(index.row())

                if item.checkState() == Qt.Checked:
                    item.setCheckState(Qt.Unchecked)
                else:
                    item.setCheckState(Qt.Checked)
                return True
        return False

    def showPopup(self):
        super().showPopup()
        self.closeOnLineEditClick = True

    def hidePopup(self):
        super().hidePopup()
        self.startTimer(100)
        self.updateText()

    def timerEvent(self, event):
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False

    def updateText(self):
        texts = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                texts.append(self.model().item(i).text())
        text = ", ".join(texts)

        metrics = QFontMetrics(self.lineEdit().font())
        elidedText = metrics.elidedText(text,
                                        Qt.ElideRight, self.lineEdit().width())
        self.lineEdit().setText(elidedText)

    def addItem(self, text, data=None):
        item = QStandardItem()
        item.setText(text)
        if data is None:
            item.setData(text)
        else:
            item.setData(data)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
        item.setData(Qt.Unchecked, Qt.CheckStateRole)
        self.model().appendRow(item)

    def addItems(self, texts, datalist=None):
        for i, text in enumerate(texts):
            try:
                data = datalist[i]
            except (TypeError, IndexError):
                data = None
            self.addItem(text, data)

    def currentData(self):
        # Return the list of selected items data
        res = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                res.append(self.model().item(i).data())
        return res


class OWServiceTable(widget.OWWidget):
    name = "Service Table"
    description = "Allows access services containing" \
                  " statistics and EO data table"
    icon = "icons/service.svg"
    priority = 30

    services = ["Eurostat", "ERA5", "Discodata"]
    years = ["1940", "1941", "1942", "1943", "1944", "1945", "1946", "1947",
             "1948", "1949", "1950", "1951", "1952", "1953", "1954", "1955",
             "1956", "1957", "1958", "1959", "1960", "1961", "1962", "1963",
             "1964", "1965", "1966", "1967", "1968", "1969", "1970", "1971",
             "1972", "1973", "1974", "1975", "1976", "1977", "1978", "1979",
             "1980", "1981", "1982", "1983", "1984", "1985", "1986", "1987",
             "1988", "1989", "1990", "1991", "1992", "1993", "1994", "1995",
             "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003",
             "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011",
             "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019",
             "2020", "2021", "2022", "2023"]
    months = ["January", "February", "March", "April", "Mai", "June", "July",
              "August", "September", "October", "November", "December"]
    days = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
            "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
            "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
            "31"]
    hours = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09",
             "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
             "20", "21", "22", "23"]

    db_vars = []
    tab_vars = []
    codes = []

    want_main_area = False
    graph_name = "thumbnailView"
    auto_commit = settings.Setting(True)

    class Outputs:
        output = Output("Data", Table)

    def __init__(self):
        super().__init__()
        self.service = None
        self.output = None

        self.combobox = gui.comboBox(
            self.controlArea, self, "", items=self.services,
            label="Choose Service: ",
            orientation=Qt.Horizontal,
            contentsLength=8,
        )

        self.authentication_box = gui.widgetBox(
            self.controlArea, "Authentication: ")
        gui.rubber(self.controlArea)

        self.box = gui.widgetBox(self.controlArea, " ")
        gui.rubber(self.controlArea)

        self.predicate_box = gui.widgetBox(
            self.controlArea, "Predicate: ", orientation=Qt.Horizontal)

        self.username_line = gui.lineEdit(
            self.authentication_box, self, "",
            label="Enter username:",
            orientation=Qt.Horizontal,
            controlWidth=200,
        )
        self.password_line = gui.lineEdit(
            self.authentication_box, self, "",
            label="Enter password:",
            orientation=Qt.Horizontal,
            controlWidth=200,
        )

        self.search_line = gui.lineEdit(
            self.authentication_box, self, "",
            label="Enter a keyword (ex: population):",
            orientation=Qt.Horizontal,
            controlWidth=200,
        )

        self.query_button = gui.button(
            self.authentication_box, self, "Query Service",
            autoDefault=False,
            callback=self.query_service
        )

        self.db_combobox = gui.comboBox(
            self.box, self, "", items=self.db_vars,
            label="Select Database:",
            orientation=Qt.Horizontal,
            contentsLength=8,
        )
        self.db_combobox.activated.connect(self.filter_db_variable)

        self.tab_combobox = gui.comboBox(
            self.box, self, "", items=self.tab_vars,
            label="Select Variable:",
            orientation=Qt.Horizontal,
            contentsLength=8,
        )
        self.tab_combobox.activated.connect(self.filter_tab_variable)

        self.year_combobox = CheckableComboBox()
        self.year_combobox.addItems(
            self.years, datalist=list(range(1940, 2024)))

        vbox = gui.vBox(self.predicate_box, box="Year:")
        vbox.layout().addWidget(self.year_combobox)

        self.month_combobox = CheckableComboBox()
        self.month_combobox.addItems(self.months, datalist=list(range(1, 13)))

        vbox = gui.vBox(self.predicate_box, box="Month:")
        vbox.layout().addWidget(self.month_combobox)

        self.day_combobox = CheckableComboBox()
        self.day_combobox.addItems(self.days, datalist=list(range(1, 32)))

        vbox = gui.vBox(self.predicate_box, box="Day:")
        vbox.layout().addWidget(self.day_combobox)

        self.time_combobox = CheckableComboBox()
        self.time_combobox.addItems(self.hours, datalist=list(range(0, 24)))

        vbox = gui.vBox(self.predicate_box, box="Time:")
        vbox.layout().addWidget(self.time_combobox)

        self.predicate_button = gui.button(
            self.controlArea, self, "Apply Predicate",
            autoDefault=False,
            callback=self.filter_tab_variable
        )

        gui.rubber(self.controlArea)
        gui.auto_commit(self.buttonsArea, self, "auto_commit",
                        "Send", box=False)

    def choose_service(self):
        if self.combobox.currentIndex() == 0:
            factory = DrbEurostatFactory()
            self.service = factory.create('eurostat://')

        if self.combobox.currentIndex() == 1:
            self.service = Era5ServiceNode()

        if self.combobox.currentIndex() == 2:
            self.service = DrbDiscodataServiceNode()

    def query_service(self):

        self.choose_service()
        if isinstance(self.service, DrbEurostatServiceNode):
            tables = self.service.get_attribute('tables')
            search = self.search_line.text()
            self.search_line.clear()

            self.tab_vars = []
            self.codes = []

            for table in tables:
                if search in table[0].lower():

                    self.tab_vars.append(table[0])
                    self.codes.append(table[1])

            self.db_combobox.clear()
            self.tab_combobox.clear()
            self.tab_combobox.addItems([var for var in self.tab_vars])

        if isinstance(self.service, DrbDiscodataServiceNode):

            self.db_vars = []
            self.tab_vars = []

            for db in self.service.children:

                self.db_vars.append(db.name)
                for tab in db.children:
                    self.tab_vars.append(tab.name)

            self.db_combobox.clear()
            self.db_combobox.addItems([db for db in self.db_vars])

            self.tab_combobox.clear()
            self.tab_combobox.addItems([tab for tab in self.tab_vars])

        if isinstance(self.service, Era5ServiceNode):
            # Add credential in the service
            keyringconnection.kr_add(service=self.service.path.path,
                                     username=self.username_line.text(),
                                     password=self.password_line.text())

            self.service = Era5ServiceNode()

            self.username_line.clear()
            self.password_line.clear()

            self.db_vars = []
            self.tab_vars = []

            for db in self.service.children:

                self.db_vars.append(db.name)
                for tab in db.children:
                    self.tab_vars.append(tab.name)

            self.db_combobox.clear()
            self.db_combobox.addItems([db for db in self.db_vars])

            self.tab_combobox.clear()
            self.tab_combobox.addItems([tab for tab in self.tab_vars])

    def filter_db_variable(self):
        name = self.db_combobox.currentText()
        db = self.service[name]

        self.tab_vars = []

        for tab in db.children:
            self.tab_vars.append(tab.name)

        self.tab_combobox.clear()
        self.tab_combobox.addItems([tab for tab in self.tab_vars])

    def filter_tab_variable(self):

        if isinstance(self.service, DrbEurostatServiceNode):
            idx = self.tab_combobox.currentIndex()
            code = self.codes[idx]
            table = self.service[code]
            df = table.get_impl(DataFrame)
            self.output = table_from_frame(df)

        elif isinstance(self.service, DrbDiscodataServiceNode):
            name = self.db_combobox.currentText()
            db = self.service[name]

            table_name = self.tab_combobox.currentText()
            table = db[table_name]
            df = table.get_impl(DataFrame)
            self.output = table_from_frame(df)

        elif isinstance(self.service, Era5ServiceNode):
            name = self.db_combobox.currentText()
            table_name = self.tab_combobox.currentText()

            predicate = self.apply_predicate()

            table = self.service[name][table_name][predicate]

            # for child in table[0]['root']['variables'].children:
            #     print(child.name)

            xr = table[0]['root']['variables'][-1].get_impl(xarray.DataArray)

            df = xr.to_dataframe()
            self.output = table_from_frame(df)

        self.commit.deferred()

    def apply_predicate(self):

        year = self.year_combobox.currentData()
        month = self.month_combobox.currentData()
        day = self.day_combobox.currentData()
        time = self.time_combobox.currentData()

        if len(day) == 0 or len(time) == 0:
            predicate = Era5PredicateEra5SingleLevelsByMonth(year=year,
                                                             month=month)

        else:
            predicate = Era5PredicateEra5SingleLevelsByHour(year=year,
                                                            month=month,
                                                            day=day, time=time)

        return predicate

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
    WidgetPreview(OWServiceTable).run()
