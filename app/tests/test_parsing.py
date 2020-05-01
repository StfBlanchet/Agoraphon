#! /usr/bin/env python3
# coding: utf-8

"""
Agor@aphon Parser unit tests
"""

from app.modules.process import clean_txt, clean_quote, get_tone, filter_medias
import unittest


class TestParserProcessing(unittest.TestCase):

    def setUp(self):
        # Fixture
        self.raw_text = \
            "Tkt c'est ok   lol >@< \xa0: \nregarde ici   "
        self.raw_quote = \
            "Le 21 avril 2020 à 22:00:46 KiloP@_ a écrit: " \
            "Ptain  j'hallucine \nlisez ça \xa0!"
        self.emoticon = \
            "http://image.lol.com/smileys_img/14.gif"
        self.raw_content = [
            'Le bureau national demande son exclusion '
            '<img src="http://image.lol.com/pol39"> viré de son propre '
            'parti ce pervers',
            '<a href="https://www.lefigaro.fr/politique/20200421" '
            'title="https://www.lefigaro.fr/politique/20200421" '
            'target="_blank" class="h ">'
            'https://www.lefigaro.fr/p<i></i>'
            '<span>olitique/</span>20200421</a>',
            '<img src="http://image.lol.com/mplo18.gif" '
            'alt="jy" data-code="jy" title="jy" '
            'width="16" height="16" />ils auraient voulu le '
            'd&eacute;gager des raisons politiques et '
            'strat&eacute;giques ils ne feraient pas autrement',
            'la pétition ici : <span class="rty" target="_blank" '
            'title='
            '"http://www.youscribe.com/BookReader/Index/1431/?documentId=7082"'
            '>http://www.youscribe.com<i></i><'
            'span>/BookReader/Ind</span>ex/1431/?documentId=7082</span></p>',
            'Encore une fois Soral avait raison '
            '<a href="https://image.lol.com/3487432.png" '
            'target="_blank" class="u "><img class="img" '
            'src="https://image.lol.com/3487432.png" '
            'alt="https://image.lol.com/3487432.png" '
            'width="68" height="51"></a> Ha ! '
            '<a href="https://www.youtube.com/watch?v=hyp0XaT" '
            'target="_blank" class="ghj">'
            'https://www.youtube.com/watch?v=hyp0XaT</a>']

    def test_clean_txt(self):
        # Check point 1:
        # Is the returned string
        # cleaned of undesired chars and spaces?
        t = clean_txt(self.raw_text)
        self.assertEqual(t, "Tkt c'est ok lol : regarde ici ")

    def test_clean_quote(self):
        # Check point 2:
        # Is the returned string
        # cleaned of undesired chars, spaces and phrases?
        q = clean_quote(self.raw_quote)
        self.assertEqual(q, "Ptain j'hallucine lisez ça !")

    def test_get_tone(self):
        # Check point 3:
        # Is the returned value the accurate tone,
        # given the last url element?
        tone = get_tone(self.emoticon)
        self.assertEqual(tone, 'déception')

    def test_filter_medias(self):
        # Check point 4:
        # Are the returned categories filled with
        # the right urls?
        medias = filter_medias(self.raw_content)
        self.assertEqual(medias['tone'], [])
        self.assertEqual(
            medias['img'],
            ['http://image.lol.com/pol39',
             'http://image.lol.com/mplo18.gif',
             'https://image.lol.com/3487432.png']
        )
        self.assertEqual(
            medias['vid'],
            ['https://www.youtube.com/watch?v=hyp0XaT']
        )
        self.assertEqual(
            medias['sources'],
            ['https://www.lefigaro.fr/politique/20200421',
             'http://www.youscribe.com/BookReader/Index/1431/?documentId=7082']
        )
