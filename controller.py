from PyQt6.QtWidgets import QFileDialog

from gui import AppGUI
from excel_creator import ExcelCreator


class AppController:

    def __init__(self, view, exporter):
        self.view = view
        self.exporter = exporter
        self.connect_signals_and_slots()

    def select_file(self):
        #Get the button that triggered the event
        sender_button = self.view.sender()
        options = QFileDialog.Option(0)
        #Show the file dialog to select a file
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("CSV Files (*.csv)")
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                if sender_button == self.view.button1:
                    self.view.input_boxes["input1"].setText(file_path)
                elif sender_button == self.view.button2:
                    self.view.input_boxes["input3"].setText(file_path)

    def clear_data(self):
        #clear data in the input boxes
        for key in self.view.input_boxes:
            if key.find("input") != -1:
                self.view.input_boxes[key].clear()

    def cleanup_userinput(self, user_input):
        return [i.strip() for i in user_input]

    def create_excel(self):
        #get the path to a CSV file from the user
        top_csv = self.view.input_boxes["input1"].text().strip()
        bot_csv = self.view.input_boxes["input3"].text().strip()
        #get the designator lists from the user and clean them up
        designators_top = self.view.input_boxes["input2"].text().upper().split(',')
        components_top = self.cleanup_userinput(designators_top)
        designators_bot = self.view.input_boxes["input4"].text().upper().split(',')
        components_bot = self.cleanup_userinput(designators_bot)

        self.exporter.create_msa_df()

        if top_csv and components_top:
            top_data = self.exporter.csv_reader(top_csv)
            self.exporter.data_filter(top_data, components_top, "TOP")
        if bot_csv and components_bot:
            bot_data = self.exporter.csv_reader(bot_csv)
            self.exporter.data_filter(bot_data, components_bot, "BOT")

        components = components_top + components_bot
        if components:
            self.exporter.create_tolerance_df(components)
            self.exporter.export_data()

    def connect_signals_and_slots(self):
        self.view.button1.clicked.connect(self.select_file)
        self.view.button2.clicked.connect(self.select_file)
        self.view.button3.clicked.connect(self.create_excel)
        self.view.button4.clicked.connect(self.clear_data)
