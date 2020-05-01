#! /usr/bin/env python3
# coding: utf-8

"""
Agor@aphon views
"""

import os
from flask import render_template, request, send_file
from app import app
from .modules.search import TopicSeeker
from .modules.scrap import PostSeeker
from .modules.analytics import Analyzer
from .modules.nlp import NlProcess
from .modules.process import get_pie, F_PATH
from bokeh.resources import INLINE
from bokeh.embed import components


@app.route('/')
def home():
    return render_template(
        "home.html",
        title='Agoraphon. La voix des forums.'
    )


@app.route('/topics', methods=['GET', 'POST'])
def topics():
    """
    This view launches the scraping, parsing and
    indexing jobs and / or the search jobs for a
    targeted topic depending on whether it is a
    thematic or an open search.
    """
    target = request.args['q']
    if len(target) > 0:
        t = TopicSeeker(target)
        t.switch()

        return render_template(
            "topic_menu.html",
            title='Agor@phon. Topics Dashboard',
            message=t.info,
            dataset=t.targeted_topic,
            ref=target
        )

    else:

        return render_template(
            "transit.html",
            title='Erreur',
            subtitle='Oups !',
            message='Veuillez entrer un terme de recherche.',
            redirect='/',
            button='retour'
        )


@app.route('/analytics', methods=['GET', 'POST'])
def analytics():
    """
    This view launches the analytics jobs
    of the whole posts contained in a topic,
    and returns the data in the form of a dashboard.
    """
    target = request.args['ref']
    a = Analyzer(target)
    a.gather_data()
    p1 = get_pie(a.df_tone)
    p2 = get_pie(a.df_dom)
    script1, div1 = components(p1)
    script2, div2 = components(p2)

    return render_template(
        "dashboard.html",
        title='Agor@phon. Topic analysis',
        topic=a.title,
        sample=a.sample,
        stat=a.stat,
        dom=a.df_dom,
        tone=a.df_tone,
        ref=target,
        plot_script1=script1,
        plot_div1=div1,
        plot_script2=script2,
        plot_div2=div2,
        js_resources=INLINE.render_js(),
        css_resources=INLINE.render_css()
    )


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    """
    This view launches the scraping, parsing
    and indexing jobs in case the content of
    a targeted topic is not already indexed.
    """
    target = request.args['ref']
    p = PostSeeker(target)
    p.check_sources()

    if p.status == 'success':
        return render_template(
            "transit.html",
            title='Agor@phon. Topic analysis',
            subtitle='Fini !',
            message="Merci d'avoir patienté.",
            redirect='/analytics?ref={}'.format(target),
            button='analyser',
        )
    else:
        return render_template(
            "transit.html",
            title='Agor@phon. Topic analysis',
            subtitle='Oups !',
            message="Ce topic n'existe plus.",
            redirect='/',
            button='retour',
        )


@app.route('/nlp', methods=['GET', 'POST'])
def nlp():
    """
    This view launches the natural
    language processing jobs that
    allow to extract named entities
    and nouns from the post corpus.
    """
    target = request.args['data']
    n = NlProcess(target)
    n.get_corpus()

    return render_template(
        "nlp_dashboard.html",
        title='Agor@phon. NLP',
        ner=n.ner,
        nouns=n.nouns,
        topic=n.title,
        ref=target
    )


@app.route('/download')
def download_file():
    """
    This view allows the user to download
    the text corpus via a csv file.
    """
    target = request.args['data']
    file = '-'.join(target.split())
    path = os.path.join(F_PATH, 'data/{}.csv'.format(file))

    return send_file(path, as_attachment=True)


@app.errorhandler(404)
def page_not_found(e):

    return render_template(
        "transit.html",
        title='Erreur',
        subtitle='404',
        message="Cette page n'existe pas / plus.",
        redirect='/',
        button='retour'
    ), 404
