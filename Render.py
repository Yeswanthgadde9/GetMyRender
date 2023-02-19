import os 
import nuke
import nukescripts


class ThumbnailMaker:
    def __init__(self):
        self.render()

    def render(self):
        node = nuke.selectedNode()
        if node.Class() != 'Write':
            nuke.message("Please select a write node")
        else:
            try:
                self.file = node['file'].getValue()
                self.shot_name = os.path.basename(self.file).title()
                self.shot_name = self.shot_name.split('.')[0]
                render = nuke.getFramesAndViews('Render', '1-2')
                range = render[0]
                first_frame = int(range.split('-')[0])
                last_frame = int(range.split('-')[1])
                nuke.execute(node, first_frame, last_frame)
                self.make_thumbnail()
            except:
                TypeError

    def make_thumbnail(self):
        nukescripts.clear_selection_recursive()
        del_nodes = []
        frame_path = self.file.split('.')[0]
        frame_path = self.file.split('/')[:-1]
        frame_path = ('/').join(frame_path)
        print(frame_path)
        for folder, subfolder, files in os.walk(frame_path):
            frames = [files[frame] for frame in (0,-1)]
        tb_frame = frames[0].split('.')[1]
        read_path = r"{}".format(self.file).replace('%04d', str(tb_frame))
        read = nuke.createNode('Read')
        read['file'].setValue(read_path)
        del_nodes.append(read)
        reformat = nuke.nodes.Reformat(format='square_512', pbb=True, resize='fill', black_outside=True)
        reformat.setInput(0, read)
        del_nodes.append(reformat)
        thumbnail_path = r'{}\\thumbnails\\{}_{}.png'.format(os.path.dirname(__file__), self.shot_name, str(tb_frame)).replace("\\", "/")
        write = nuke.nodes.Write(file=thumbnail_path)
        write['file_type'].setValue('png')
        write.setInput(0, reformat)
        del_nodes.append(write)
        nuke.execute(write, 1, 1)
        for node in del_nodes:
            nuke.delete(node)
