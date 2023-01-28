import sys
import json
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from GetMyRenderUI import Ui_GetMyRender


class Render(QWidget, Ui_GetMyRender):
    def __init__(self):
        super(Render, self).__init__()

        self.setupUi(self)
        self.add_shot()
        self.shot_data = '{}\\config\\shot_data.json'.format(os.path.dirname(__file__))
        self.Render_Data.itemClicked.connect(self.display_shot_name)
        self.Import_Render.clicked.connect(self.get_render)
        self.ImportScript.clicked.connect(self.get_script)
        self.Render_Data.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Render_Data.customContextMenuRequested.connect(self.custom_context_menu)

    def add_shot(self):
        with open(self.shot_data, "r") as file:
            self.shot_data = json.load(file)
            for shot in self.shot_data:
                self.Render_Data.addItem(shot)

    def display_shot_name(self, shot):
        self.shot_name = shot.text()
        self.Shotinfo.setText(self.shot_name)
        self.frame_range = "{}-{}".format(self.shot_data[self.shot_name]['start_frame'],
                                          self.shot_data[self.shot_name]['end_frame'])
        self.Framerangeinfo.setText(self.frame_range)
        if self.shot_data[self.shot_name]['chanels'] == 'all':
            self.Channelinfo.setText('rgba')
        else:
            channels = self.shot_data[self.shot_name]['chanels']
            self.Channelinfo.setText(channels)
        thumbnail_path = self.shot_data[self.shot_name]['thumbnail_path']
        self.Thumbnail_label.setPixmap(thumbnail_path)
        self.render_path = ("{} {}".format(self.shot_data[self.shot_name]['path'], self.frame_range))
        self.script_path = self.shot_data[self.shot_name]['script']
        format = self.shot_data[self.shot_name]['resolution']
        self.Resolutioninfo.setText(format)
        date = self.shot_data[self.shot_name]['date']
        date = date.split('-')[0]
        self.Dateinfo.setText(date)
        extension = self.shot_data[self.shot_name]['path']
        extension = extension.split('.')[-1]
        self.Extensioninfo.setText(extension)
        time = self.shot_data[self.shot_name]['date']
        time = time.split('-')[1]
        self.Timeinfo.setText(time)

    def get_render(self):
        nukescripts.clear_selection_recursive()
        read = nuke.createNode("Read")
        read.knob("file").fromUserText(self.render_path)

    def custom_context_menu(self, pos):
        self.menu = QMenu()
        open = self.menu.addAction('Open')
        delete = self.menu.addAction('Delete')
        action = self.menu.exec_(self.Render_Data.mapToGlobal(pos))
        item_name = self.Render_Data.currentItem().text()
        print(item_name)
        if action == open:
            paths = self.shot_data[item_name]['script']
            paths = paths.split('/')
            latest_path = paths.pop()
            f_path = '/'.join(paths)
            QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(f_path))
        elif action == delete:
            print("deleted")
            del self.shot_data[item_name]
            print(self.shot_data)
            self.write_json_data(self.shot_data)

    def write_json_data(self, data):
        with open(self.shot_data, "w") as file:
            json.dump(self.shot_data, file, indent=4)

    def get_script(self):
        nukescripts.clear_selection_recursive()
        nuke.nodePaste(self.script_path)


def main():
    main.widgets = Render()
    main.widgets.show()


main()
