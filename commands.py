#!/usr/bin/env python

from raven import Raven
import requests


def follow(parser, filepath):
    r = Raven()
    artist_ids = r.search_artist_ids(filepath)
    data = {}
    artist_ids = list(artist_ids)
    data['ids'] = [','.join(artist_ids)]
    endpoint = 'me/following'
    requests.request('PUT', r.prefix+endpoint, data=data)


def get_parser():
    """Gets parser object for commands.py"""
    import argparse
    parser = argparse.ArgumentParser(description="Commands for Raven")
    parser.add_argument("-f", "--file", dest="filepath", type=lambda x: follow(parser, x),
                        help="Specify source CSV filepath")
    return parser


if __name__ == '__main__':
    args = get_parser().parse_args()
