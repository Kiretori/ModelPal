import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QListWidget, QHBoxLayout, QFileDialog, QInputDialog, QMessageBox
)
from PyQt6.QtCore import Qt
import ml_utils
import os 

class ProfileForm(QWidget):
    def __init__(self):
        super().__init__()

        # Layout for the form
        layout = QVBoxLayout()

        # Profile name input
        layout.addWidget(QLabel('Profile Name:'))
        self.profile_name_input = QLineEdit()
        layout.addWidget(self.profile_name_input)

        # Model files list
        layout.addWidget(QLabel('Model Files:'))
        self.model_files_list = QListWidget()
        layout.addWidget(self.model_files_list)

        # Buttons to upload and delete model files
        model_files_buttons_layout = QHBoxLayout()
        self.upload_button = QPushButton('Upload Model Files')
        self.upload_button.clicked.connect(self.upload_models)
        model_files_buttons_layout.addWidget(self.upload_button)

        self.delete_model_file_button = QPushButton('Delete Model File')
        self.delete_model_file_button.clicked.connect(self.delete_model_file)
        model_files_buttons_layout.addWidget(self.delete_model_file_button)
        layout.addLayout(model_files_buttons_layout)

        # Input features list
        layout.addWidget(QLabel('Input Features:'))
        self.input_features_list = QListWidget()
        self.input_features_list.itemSelectionChanged.connect(self.update_buttons)
        layout.addWidget(self.input_features_list)

        # Buttons to add and delete input features
        input_feature_buttons_layout = QHBoxLayout()
        self.add_input_feature_button = QPushButton('Add Input Feature')
        self.add_input_feature_button.clicked.connect(self.add_input_feature)
        input_feature_buttons_layout.addWidget(self.add_input_feature_button)

        self.delete_input_feature_button = QPushButton('Delete Input Feature')
        self.delete_input_feature_button.clicked.connect(self.delete_input_feature)
        input_feature_buttons_layout.addWidget(self.delete_input_feature_button)
        layout.addLayout(input_feature_buttons_layout)

        # Target variables list
        layout.addWidget(QLabel('Target Variables:'))
        self.target_variables_list = QListWidget()
        self.target_variables_list.itemSelectionChanged.connect(self.update_buttons)
        layout.addWidget(self.target_variables_list)

        # Buttons to add and delete target variables
        target_variable_buttons_layout = QHBoxLayout()
        self.add_target_variable_button = QPushButton('Add Target Variable')
        self.add_target_variable_button.clicked.connect(self.add_target_variable)
        target_variable_buttons_layout.addWidget(self.add_target_variable_button)

        self.delete_target_variable_button = QPushButton('Delete Target Variable')
        self.delete_target_variable_button.clicked.connect(self.delete_target_variable)
        target_variable_buttons_layout.addWidget(self.delete_target_variable_button)
        layout.addLayout(target_variable_buttons_layout)

        # Save profile button
        self.save_button = QPushButton('Save Profile')
        layout.addWidget(self.save_button)

        # Set layout to the main window
        self.setLayout(layout)

        # Initialize the button states
        self.update_buttons()

    def warning_box(self, window_title, text, additional_text):
        warning_box = QMessageBox(self)
        warning_box.setIcon(QMessageBox.Icon.Warning)
        warning_box.setWindowTitle(window_title)
        warning_box.setText(text)
        warning_box.setInformativeText(additional_text)
        warning_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        warning_box.exec()


    def upload_models(self):
        # Function to upload model files
        files, _ = QFileDialog.getOpenFileNames(self, 'Select Model Files', '', 'All Files (*)')
        if files:

            file_names = [os.path.basename(file) for file in files]

            input_features = ml_utils.get_input_features_from_file(files[0])
            
            # TODO: implement the input feature validation fully (different shapes case, different labels case etc...)
            if len(files) > 1:
                features_for_validation = ml_utils.get_input_features_from_file(files[1])
                if sorted(input_features) == sorted(features_for_validation):
                    self.warning_box("Warning", "Input features mismatch", "Models have different input feature labels this might cause errors later!")



            self.input_features_list.addItems(input_features)
            self.model_files_list.addItems(file_names)
            self.update_buttons()

    def delete_model_file(self):
        # Function to delete the selected model file
        selected_item  = self.model_files_list.currentItem()
        if selected_item:
            self.model_files_list.takeItem(self.model_files_list.row(selected_item))
            self.update_buttons()

    def add_input_feature(self):
        # Function to add an input feature
        feature, ok = QInputDialog.getText(self, 'Add Input Feature', 'Feature:')
        if ok and feature:
            self.input_features_list.addItem(feature)
            self.update_buttons()

    def delete_input_feature(self):
        # Function to delete the selected input feature
        selected_item = self.input_features_list.currentItem()
        if selected_item:
            self.input_features_list.takeItem(self.input_features_list.row(selected_item))
            self.update_buttons()

    def add_target_variable(self):
        # Function to add a target variable
        variable, ok = QInputDialog.getText(self, 'Add Target Variable', 'Variable:')
        if ok and variable:
            self.target_variables_list.addItem(variable)
            self.update_buttons()

    def delete_target_variable(self):
        # Function to delete the selected target variable
        selected_item = self.target_variables_list.currentItem()
        if selected_item:
            self.target_variables_list.takeItem(self.target_variables_list.row(selected_item))
            self.update_buttons()

    def update_buttons(self):
        # Enable/disable the delete buttons based on list content
        self.delete_input_feature_button.setEnabled(self.input_features_list.count() > 0)
        self.delete_target_variable_button.setEnabled(self.target_variables_list.count() > 0)
        self.delete_model_file_button.setEnabled(self.model_files_list.count() > 0)


   

def main():
    app = QApplication(sys.argv)
    window = ProfileForm()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
