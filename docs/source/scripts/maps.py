import math
import os

import pandas as pd
from bokeh.io import show
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.tile_providers import CARTODBPOSITRON, get_provider


# imported from https://towardsdatascience.com/exploring-and-visualizing-chicago-transit-data-using-pandas-and-bokeh-part-ii-intro-to-bokeh-5dca6c5ced10
def merc(lat, lon):
    """ Convert lat/lon into mercator values
    """
    r_major = 6378137.000
    x = r_major * math.radians(lon)
    scale = x / lon
    y = (
        180.0
        / math.pi
        * math.log(math.tan(math.pi / 4.0 + lat * (math.pi / 180.0) / 2.0))
        * scale
    )
    return (x, y)


tile_provider = get_provider(CARTODBPOSITRON)

# Map bounding box, roughly
lower_left = merc(49.61934607370432, -10.994519941147475)
upper_right = merc(60.931634153408915, 0.9818240754471713)

df = pd.read_csv(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "hospital_locations.csv")
)

df["coords_x"] = df.apply(lambda x: merc(x["latitude"], x["longitude"])[0], axis=1)
df["coords_y"] = df.apply(lambda x: merc(x["latitude"], x["longitude"])[1], axis=1)

source = ColumnDataSource(
    data=dict(
        x=list(df["coords_x"]), y=list(df["coords_y"]), name=list(df["Hospital Name"])
    )
)

TOOLTIPS = """
    <div class="tooltip">
        <span style="font-size: 15px; font-weight: bold; font-family: Furtiger W01,Arial,Sans-serif;">@name</span>
    </div>
"""

p = figure(
    x_range=(lower_left[0], upper_right[0]),
    y_range=(lower_left[1], upper_right[1]),
    x_axis_type="mercator",
    y_axis_type="mercator",
    toolbar_location=None,
    tooltips=TOOLTIPS,
    sizing_mode="scale_both",
)
p.add_tile(tile_provider)
p.circle(x="x", y="y", source=source, size=8, fill_color="#003087", line_color="Black")
p.axis.visible = False
p.toolbar.active_drag = None
p.toolbar.active_scroll = None
p.toolbar.active_tap = None
show(p)
