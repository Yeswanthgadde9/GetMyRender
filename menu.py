import nuke
import Get_My_Render_Export_Data
menubar = nuke.menu("Nuke")
m = menubar.addMenu("Yesh")
m.addCommand("GetMyRender", "import GetMyRender;GetMyRender.main()")
nuke.knobDefault("Write.afterRender", "Get_My_Render_Export_Data.GetMyData()")
