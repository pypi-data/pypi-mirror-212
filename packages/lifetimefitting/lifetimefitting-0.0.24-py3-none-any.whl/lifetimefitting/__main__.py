import matplotlib.pyplot as plt
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from phdimporter import TRF
from .funcs.gui import Ui_Form
from .funcs.fittingFuncs import loadAndCull, fitFL
import sys

def plotFL() -> None:
    global csv
    plt.close('all')
    for i in ui.axList:
        i.remove()
    ui.axList = []
    ui.ax1.relim()
    ui.ax1.autoscale_view()
    ui.ax2.relim()
    ui.ax2.autoscale_view()
    ui.ax3.relim()
    ui.ax3.autoscale_view()
    ui.ax4.relim()
    ui.ax4.autoscale_view()
    _, irf, loaded1 = loadAndCull(ui.irf_file, ui)
    x, y, loaded2 = loadAndCull(ui.trf_file, ui)
    if loaded1 and loaded2:
        csv = fitFL(ui, x_in=x, y_in=y, irf_in=irf)

def trf_browse() -> None:
    ui.trf_file.setText(file_dialog.getOpenFileName(directory="/Users/adrea/gdrive/Monash/PhD/Fluorophore/data/tr/AAQ", filter="PicoHarp binary of text file (*.phd *.txt)")[0])

def irf_browse() -> None:
    ui.irf_file.setText(file_dialog.getOpenFileName(directory="/Users/adrea/gdrive/Monash/PhD/Fluorophore/data/tr/AAQ", filter="PicoHarp binary of text file (*.phd *.txt)")[0])

def update_max_x() -> None:
    ui.max_x_out.setValue(ui.max_x.value())

def update_max_x_from_out() -> None:
    ui.max_x.setValue(ui.max_x_out.value())

def setupPlot() -> None:
    ui.verticalLayout_plot = QtWidgets.QVBoxLayout(ui.frame)
    ui.verticalLayout_plot.setObjectName("verticalLayout_plot")
    ui.figure, (ui.ax1, ui.ax3, ui.ax2, ui.ax4) = plt.subplots(4, 1, figsize=(8, 10), sharex=True, height_ratios=[3, 3, 1, 1])
    ui.canvas = FigureCanvas(ui.figure)
    ui.toolbar = NavigationToolbar(ui.canvas)
    ui.verticalLayout_plot.addWidget(ui.canvas)
    ui.verticalLayout_plot.addWidget(ui.toolbar)
    ui.axList = []

    # log plot
    ui.ax1.set_yscale('log')
    ui.ax1.set_ylim(1e-1, 1e5, auto=False)
    ui.ax1.axhline(0, c='k', lw=0.5)
    ui.ax1.axvline(0, c='k', lw=0.5)
    ui.ax1.set_ylabel('Counts')
    # linear plot
    ui.ax3.set_ylabel('Counts')
    ui.ax3.axvline(0, c='k', lw=0.5)
    # log residuals
    ui.ax2.set_ylabel('Residuals\n(exp)')
    ui.ax2.axvline(0, c='k', lw=0.5)
    ui.ax2.axhline(0, c='k', lw=0.5)
    # linear residuals
    ui.ax4.set_xlabel('Time (ns)')
    ui.ax4.set_ylabel('Residuals\n(lin)')
    ui.ax4.axvline(0, c='k', lw=0.5)
    ui.ax4.axhline(0, c='k', lw=0.5)

def saveCSV() -> None:
    global csv
    if 'csv' in globals():
        save_csv_dialog = QFileDialog()
        name = save_csv_dialog.getSaveFileName(filter="CSV Sheet (*.csv)")[0]
        if name != '':
            with open(name, 'w+') as f:
                f.writelines(csv)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    setupPlot()

    # file loading
    file_dialog = QFileDialog()
    ui.trf_browse.clicked.connect(trf_browse)
    ui.irf_browse.clicked.connect(irf_browse)
    ui.csv_browse.clicked.connect(saveCSV)
    ui.max_x.sliderMoved.connect(update_max_x)
    ui.max_x_out.valueChanged.connect(update_max_x_from_out)

    ui.fit_button.clicked.connect(plotFL)

    Form.show()
    sys.exit(app.exec())
