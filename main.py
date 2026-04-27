import sys
from PyQt6.QtWidgets import QApplication

from gui import AppGUI
from controller import AppController
from excel_creator import ExcelCreator


def main():
    app = QApplication([])

    view = AppGUI()
    view.show()

    model = ExcelCreator()

    controller = AppController(
        view=view,
        exporter=model
    )

    sys.exit(app.exec())


if __name__ == "__main__":
    main()