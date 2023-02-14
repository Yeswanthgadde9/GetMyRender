import json
import os
from datetime import datetime
import nuke
import nukescripts


class GetMyData:
    def __init__(self):
        data = self.get_details()
        self.make_thumbnail()
        self.write_json(data)

    def get_details(self):
        details = {}
        self.node = nuke.thisNode()
        self.path = self.node['file'].getValue()
        script = nuke.root()
        format = self.node.format().name()
        script = script['name'].value()
        self.c_time = datetime.now()
        self.channels = self.node['channels'].value()
        frame_path = self.path.split('/')[:-1]
        frame_path = ('/').join(frame_path)
        for folder, subfolder, files in os.walk(frame_path):
            self.frames = [files[frame] for frame in (0,-1)]
        self.start_frame = self.frames[0].split('.')[1]
        self.end_frame = self.frames[1].split('.')[1]
        self.shot_name = os.path.basename(self.path).title()
        self.shot_name = self.shot_name.split('.')[0]
        self.thumbnail_path = '{}\\thumbnails\\{}_{}.png'.format(os.path.dirname(__file__), self.shot_name, str(self.start_frame))
        self.thumbnail_path = self.thumbnail_path.replace('\\', '/')
        details[self.shot_name] = {"path": self.path, "script": script, "start_frame": self.start_frame,
                                   "end_frame": self.end_frame, "thumbnail_path": self.thumbnail_path,
                                   "chanels": self.channels, "date": datetime.now().strftime('%d/%m/%Y-%H:%M:%S'),
                                   "resolution": format}
        return details

    def make_thumbnail(self):
        nukescripts.clear_selection_recursive()
        del_nodes = []
        read_path = self.path.replace('%04d', str(self.start_frame))
        read = nuke.createNode('Read')
        read['file'].setValue(read_path)
        read.setSelected(True)
        del_nodes.append(read)
        reformat = nuke.nodes.Reformat(format='square_512', pbb=True, resize='fill', black_outside=True)
        reformat.setInput(0, read)
        reformat.setSelected(True)
        del_nodes.append(reformat)
        write = nuke.createNode("Write")
        write['file'].setValue(self.thumbnail_path)
        write['file_type'].setValue('png')
        write.setInput(0, reformat)
        write.setSelected(True)
        del_nodes.append(write)
        nuke.execute(write, 1, 1)
        for nodes in del_nodes:
            nuke.delete(nodes)

    def write_json(self, new_data):
        file_name ='{}\\config\\shot_data.json'.format(os.path.dirname(__file__))
        file_data = {}
        try:
            with open(file_name, 'r') as data_file:
                file_data = json.load(data_file)
        except:
            pass
        shot_count = file_data.keys()
        if len(shot_count) > 10:
            time_val = dict()
            for key, val in file_data.items():
                time = val['Date']
                time_val[key] = time
                l_time = min(time_val.values())
                l_val = time_val.keys()[time_val.values().index(l_time)]
                l_thumb = file_data[l_val]['thumbnail_path']
            del file_data[l_val]
            os.remove(l_thumb)
            file_data.update(new_data)
            with open(file_name, 'w') as file_data:
                json.dump(file_data, file_data, indent=4)
        else:
            file_data.update(new_data)
            with open(file_name, 'w') as write_file:
                json.dump(file_data, write_file, indent=4)
