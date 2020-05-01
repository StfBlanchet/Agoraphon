#! /usr/bin/env python3
# coding: utf-8

"""
Agor@aphon parsing and analytics tools lib
"""

import os
import re
import itertools
import collections as coll
import pandas as pd
from bokeh.plotting import figure
from bokeh.transform import cumsum
from app.modules.constants import TONES_, VID_, COLORS_
from math import pi
from datetime import datetime
from dateparser import parse

F_PATH = os.path.abspath(os.path.dirname(__file__))


# Regex used in parsing process
hour = re.compile(r'(\d+:\d+:\d+)')
spec_char = r"[^'%!?a-zA-Z-é-ô-à-ù-è-ï-ö,\d:\s]"
spec_char_ = r"[^a-zA-Z-0-9]"
ureg = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
html_cleaner = re.compile('<.*?>')


def clean_txt(entry):
    """
    This function removes undesired chars
    and spaces from a post.
    Returns a string.
    """

    clean = re.sub(spec_char, ' ', entry)
    clean = re.sub(r'(\s\s+)', ' ', clean)
    clean = clean.replace('\xa0', '').replace('\n', ' ')

    return clean


def clean_quote(entry):
    """
    This function removes undesired chars,
    spaces and piece of content from a quote.
    Returns a string.
    """

    quote_info = re.compile(
        r'(Le\s*\d+\s*\D+\s*\d+\s*\D\s*\d+:\d+:\d+\s*\S+\s*a\s*écrit\s*:)'
    )
    clean = re.sub(spec_char, ' ', entry)
    clean = re.sub(r'(\s\s+)', ' ', clean)
    clean = clean.replace('\xa0', '').replace('\n', ' ')
    clean = re.sub(quote_info, '', clean).strip()

    return clean


def get_tone(entry):
    """
    This function takes an image url as parameter
    from which it extracts the last item in order
    to determine its emoticon category.
    """

    entry = entry.split('/')[-1].split('.')[0]
    emoticon_tone = str()
    for key in list(TONES_.keys()):
        if entry in TONES_.get(key):
            emoticon_tone = key

    return emoticon_tone


def filter_medias(entry):
    """
    This function takes an url list as parameter,
    and splits it into category lists based on their
    content: images, vids, article, emoticons.
    Returns a dictionary.
    """

    medias = {}
    url_set = [re.findall(ureg, str(u)) for u in entry]
    url_set = list(itertools.chain.from_iterable(url_set))
    url_set = [re.sub(html_cleaner, '', u) for u in url_set]
    vid = [v for v in url_set if any(item in v for item in VID_)]
    img_set = [
        m for m in url_set
        if m.endswith(('.gif', '.png', '.jpg', '.jpeg'))
        or m.startswith('http://image')
    ]
    img = [i for i in img_set if i[:39] != os.environ.get('EMOTICON_')]
    tone_ = [e for e in img_set if e[:39] == os.environ.get('EMOTICON_')]
    tone = [get_tone(t) for t in tone_]
    source = [s for s in url_set if s not in vid and s not in img_set]
    medias.update({
        'tone': list(dict.fromkeys(tone)),
        'img': list(dict.fromkeys(img)),
        'vid': list(dict.fromkeys(vid)),
        'sources': list(dict.fromkeys(source))})

    return medias


def get_stat(entry, total, subtotal):
    """
    This function takes a list and 2 integers
    as parameters to calculate the frequency
    of a variable according to the meta (int 1)
    and the proximal (int 2) categories to
    which it belongs.
    Returns a dictionary.
    """

    statistic = {}

    if len(entry) > 0:
        list_ = list(dict.fromkeys(entry))
        rate = round((len(entry) / total) * 100, 1)
        share = round((len(entry) / len(subtotal)) * 100, 1)
    else:
        list_ = []
        rate = 0
        share = 0

    statistic.update({"list": list_, "rate": rate, "share": share})

    return statistic


def get_df(entry):
    """
    This function takes a list as parameter
    to calculate the frequency of a variable.
    Returns a dataframe.
    """

    dist = coll.Counter(entry)

    df = pd.DataFrame(data={
        "labels": list(dist.keys()),
        "counts": list(dist.values())
    })

    df['rates'] = round((df.counts / df.counts.sum()) * 100, 1)
    df = df.sort_values(by=['counts'], ascending=False).reset_index(drop=True)

    return df


def get_pie(df_entry):
    """
    This function takes a dataframe as parameter
    to configure the related pie chart.
    Returns a Bokeh figure.
    """

    data = df_entry

    data['angle'] = df_entry['counts'] / df_entry['counts'].sum() * 2 * pi
    data['color'] = COLORS_[:len(df_entry)]

    p = figure(
        plot_height=500,
        sizing_mode="scale_width",
        toolbar_location=None,
        tools="hover",
        tooltips="@labels: @rates %",
        x_range=(-0.95, 1)
    )

    p.wedge(
        x=0,
        y=1,
        radius=0.8,
        start_angle=cumsum('angle', include_zero=True),
        end_angle=cumsum('angle'),
        line_color="white",
        fill_color='color',
        source=data
    )

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None
    p.outline_line_width = 0
    p.min_border_left = 0
    p.min_border_right = 0
    p.min_border_top = 0
    p.min_border_bottom = 0

    return p


def get_datetime(date_string):
    """
    This function takes a string containing "date - time"
    as parameter, puts it in datetime format and returns
    it as slices.
    """

    date_ = str(parse(date_string)).split()
    i_date = list(map(int, date_[0].split('-')))
    i_time = list(map(int, date_[1].split(':')))
    date_time = i_date + i_time

    return date_time


def get_delay(start, end):
    """
    This function takes a start and an end datetime
    as parameters and puts the in datetime format.
    """

    s = get_datetime(start)
    e = get_datetime(end)

    start = datetime(s[0], s[1], s[2], s[3], s[4], s[5])
    end = datetime(e[0], e[1], e[2], e[3], e[4], e[5])
    hours = ((end-start).total_seconds()/60)/60
    days = hours / 24

    return hours, days
