from app import Application

app = Application()

app.run()

from chart import draw_road_charts

draw_road_charts(app.roads)
