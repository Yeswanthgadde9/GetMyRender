import nuke
import Get_My_Render_Export_Data
menubar = nuke.menu("Nuke")
mymenu = menubar.addMenu("Yesh")
render_menu = menubar.addMenu("Dispatcher")
mymenu.addCommand("GetMyRender", "import GetMyRender;GetMyRender.main()")
render_menu.addCommand("DispatchRender", "import Render;Render.ThumbnailMaker()")
nuke.knobDefault("Write.afterRender", "Get_My_Render_Export_Data.GetMyData()")
