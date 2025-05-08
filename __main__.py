#!/usr/local/bin/python3

from argparse import ArgumentParser
from variables import ship_count
from Classes import Battleship

parser = ArgumentParser(description='Play an Amazing Battleship game against the computer.')
parser.add_argument('-d','--demo', choices=['short','apagon'], default=None)
args = parser.parse_args()

short_demo, apagon = args.demo=='short', args.demo=='apagon'
game = Battleship(short_demo, apagon, ship_count[:1 if short_demo else None])
