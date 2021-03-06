#!/usr/bin/python3
# Run the tests from the test dir with "python3 -m unittest test_*"

import unittest
import os
import sys

sys.path.insert(0, os.path.abspath('..'))  # hacks ;-)
from torrent_extractor.torrent import TorrentFactory, TvEpisode, Film


class TorrentTest(unittest.TestCase):
    """Contains test cases for module torrent.py"""

    def setUp(self):
        self.torrentFactory = TorrentFactory()

        self.errors = []  # collects errors

        # These are just dummy names, the files does not exist, the format is (file name, tv series name, season number)
        self.tvepisodesdummies = []
        self.tvepisodesdummies.append(
            ('True.Blood.Season.7.Complete.1080p.WEB-DL.DD5.1.H.264-YFN',
             'True Blood', 'Season 7'))
        self.tvepisodesdummies.append(
            ('Family Guy S08E01 Road to the Multiverse PDTV XviD-FQM [eztv]',
             'Family Guy', 'Season 8'))
        self.tvepisodesdummies.append((
            '90210 S02E07 Unmasked HDTV XviD-FQM [eztv]', '90210', 'Season 2'))
        self.tvepisodesdummies.append(
            ('Family Guy S08E03 PDTV XviD-2HD [eztv]', 'Family Guy',
             'Season 8'))
        self.tvepisodesdummies.append(
            ('Family.Guy.S08E08.Dog.Gone.PDTV.XviD-FQM', 'Family Guy',
             'Season 8'))
        self.tvepisodesdummies.append(
            ('Extant S01E09E10 720p HDTV X264-DIMENSION (NEW)', 'Extant',
             'Season 1'))
        self.tvepisodesdummies.append(
            ('Fargo.S01.Complete.720p.HDTV.H264.DD5.1.AC3-HDWTV', 'Fargo',
             'Season 1'))
        self.tvepisodesdummies.append(
            ('Masters.of.Sex.S02E07.720p.HDTV.x264-IMMERSE', 'Masters of Sex',
             'Season 2'))
        self.tvepisodesdummies.append(
            ('Weissensee - S01E01.avi', 'Weissensee', 'Season 1'))
        self.tvepisodesdummies.append(
            ('House.of.Cards.2013.S02.1080p.NF.WEBRip.DD5.1.x264-NTb',
             'House of Cards 2013', 'Season 2'))
        self.tvepisodesdummies.append(('Downton_Abbey.5x01.720p_HDTV_x264-FoV',
                                       'Downton Abbey', 'Season 5'))
        self.tvepisodesdummies.append(
            ('Brooklyn.Nine-Nine.S02E06.720p.HDTV.x264-KILLERS',
             'Brooklyn Nine-Nine', 'Season 2'))
        self.tvepisodesdummies.append(
            ('Top.Gear.UK.S22E02.1080p.HDTV.x264-FaiLED.mkv', 'Top Gear UK',
             'Season 22'))
        self.tvepisodesdummies.append(
            ('Top.Gear.S22E03.720p.HDTV.x264-ORGANiC.mkv', 'Top Gear',
             'Season 22'))
        self.tvepisodesdummies.append(
            ('Top_Gear.22x01.720p_HDTV_x264-FoV', 'Top Gear', 'Season 22'))

        # These are also just dummy names, the files does not actually exist, the format is (file name, film title)
        self.filmdummies = []
        self.filmdummies.append((
            'Godzilla 2014 1080p BluRay DTS x264-HDMaNiAcS (NEW)', 'Godzilla'))
        self.filmdummies.append((
            'X-Men Days of Future Past 2014 720p KORSUB HDRip x264 5 1ch AC3-MiLLENiUM',
            'X-Men Days of Future Past'))
        self.filmdummies.append(
            ('Catch Me If You Can 2002 1080p x264 DTS mkvrg',
             'Catch Me If You Can'))
        self.filmdummies.append(
            ('Divergent.2014.720p.BluRay.DD5.1.x264-HiDt', 'Divergent'))
        self.filmdummies.append((
            'James.Bond.007.The.World.Is.Not.Enough.1999.1080p.BluRay.x264-CiNEFiLE',
            'James Bond 007 The World Is Not Enough'))
        self.filmdummies.append((
            'Two.Days.One.Night.(Deux.Jours.une.Nuit).2014.Bluray.1080p.DTS-HD.x264-Grym',
            'Two Days One Night (Deux Jours une Nuit)'))
        self.filmdummies.append(
            ('Horns.2013.1080p.BluRay.AVC.DTS-HD.MA.5.1-HDAccess', 'Horns'))

    def tearDown(self):
        self.assertEqual([], self.errors)  # test that we have no errors

    # Tests that sending in args pointing to nonexistent files raises exceptions
    def test_make_nonexisting_files(self):
        for nonce in self.tvepisodesdummies:
            self.assertRaises(Exception,
                              lambda: self.torrentFactory.make(nonce))
            for nonce in self.filmdummies:
                self.assertRaises(Exception,
                                  lambda: self.torrentFactory.make(nonce))

    def test_has_ok_extension(self):
        try:
            self.assertTrue(
                self.torrentFactory._TorrentFactory__has_ok_extension(
                    "Masters.of.Sex.mkv"))
            self.assertFalse(
                self.torrentFactory._TorrentFactory__has_ok_extension(
                    "Masters.of.Sex.flac"))
        except AssertionError as e:
            self.errors.append(str(e))

    def test_match_tv_series(self):
        for tv_series in self.tvepisodesdummies:
            try:
                self.assertEqual(
                    self.torrentFactory._TorrentFactory__match_tv_series(
                        tv_series[0]), tv_series[-2:])
            except AssertionError as e:
                self.errors.append(str(e))

    def test_tv_title_normalisation(self):
        def to_file_name(title):
            return '.'.join(title.split(' ')) +  '.S07E01.Episode.Title.1080p.Source.Release-Group.mkv'

        def assert_destination(file_name, expected):
            title_season = self.torrentFactory._TorrentFactory__match_tv_series(file_name)
            torrent = TvEpisode(title_season, file_name)
            self.assertEqual(torrent.destination.split('/')[0], expected)

        assert_destination(to_file_name('Game of Thrones'), 'Game of Thrones')
        assert_destination(to_file_name('Game Of Thrones'), 'Game of Thrones')
        assert_destination(to_file_name('The Night Of 2016'), 'The Night Of 2016')
        assert_destination(to_file_name('The Night of 2016'), 'The Night Of 2016')
        assert_destination(to_file_name('The night of'), 'The Night Of')
        assert_destination(to_file_name('iZombie'), 'iZombie')
        assert_destination(to_file_name('FireFly'), 'FireFly')
        assert_destination(to_file_name('parks and recreation'), 'Parks and Recreation')
        assert_destination(to_file_name('this is us'), 'This Is Us')
        assert_destination(to_file_name('taboo UK'), 'Taboo UK')

    def test_match_film(self):
        for film in self.filmdummies:
            try:
                self.assertEqual(
                    self.torrentFactory._TorrentFactory__match_film(film[0]),
                    film[1])
            except AssertionError as e:
                self.errors.append(str(e))


if __name__ == '__main__':
    unittest.main()
