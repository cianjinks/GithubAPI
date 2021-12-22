import requests
import os
import math
import json

from flask import Flask, render_template

from bokeh.models import ColumnDataSource
from bokeh.resources import INLINE
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.palettes import Viridis10
from bokeh.models import WheelZoomTool
from bokeh.transform import jitter

app = Flask(__name__)

# Top Repositories (https://gitstar-ranking.com/)
repos = {
    "freeCodeCamp": "freeCodeCamp",
    "996icu": "996.ICU",
    "EbookFoundation": "free-programming-books",
    "jwasham": "coding-interview-university",
    "vuejs": "vue",
    "facebook": "react",
    #"kamranahmedse": "developer-roadmap",
    #"sindresorhus": "awesome",
    # "tensorflow": "tensorflow",
    # "twbs": "bootstrap"
}

token = os.getenv('GITHUB_TOKEN', '...')
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

@app.route('/')
def index():
    source = ColumnDataSource()

    x_data = []
    y_data = []
    color_data = []
    login_data = []
    id_data = []

    i = 0
    for owner in repos:
        url = f"https://api.github.com/repos/{owner}/{repos[owner]}/contributors"
        r = requests.get(url, headers=headers)
        repo_data = r.json()
        for contributor in repo_data:
            login = contributor["login"]
            id = contributor["id"]
            total_contributions = contributor["contributions"]
            x_data.append(repos[owner])
            y_data.append(total_contributions)
            color_data.append(Viridis10[i % 10])
            login_data.append(login)
            id_data.append(id)
        i = i + 1

    fig = figure(x_range=[repos[owner] for owner in repos], plot_height=720, plot_width=1280, tooltips=[("User", "@login"), ("User ID", "@id"), ("Contributions", "@commit_count")], tools="pan,wheel_zoom,reset", active_drag="pan", active_scroll="wheel_zoom")
    fig.circle(x=jitter("x", width=0.8, range=fig.x_range), y="y", source=source, size=5, color="color")
    fig.xaxis.axis_label = "Top Repositories"
    fig.yaxis.axis_label = "Total Contributions by User"
    # fig.xaxis.major_label_orientation = math.pi/4
    fig.xaxis.major_label_text_font_size = '10pt'
    fig.yaxis.major_label_text_font_size = '10pt'
    fig.xaxis.axis_label_text_font_size = '15pt'
    fig.yaxis.axis_label_text_font_size = '15pt'

    # fig.toolbar.active_scroll = "WheelZoomTool()"

    source.data = dict(
        x = x_data,
        y = y_data,
        color = color_data,
        login = login_data,
        id = id_data,
        commit_count = y_data
    )

    script, div = components(fig)
    return render_template(
        'index.html',
        plot_script=script,
        plot_div=div,
        js_resources=INLINE.render_js(),
        css_resources=INLINE.render_css(),
    ).encode(encoding='UTF-8')

if __name__ == "__main__":
    app.run(debug=True)