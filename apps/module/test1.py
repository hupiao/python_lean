import argparse


def run(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--hp', type=str, choices=['a', 'b'], help='hdhdhhd')
    parser.add_argument('--id', type=str, choices=['1', '2'], help='hdhdhhd')
    args = parser.parse_args(args)
    print args.hp
    print args.id




