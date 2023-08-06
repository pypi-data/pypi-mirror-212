from finbourne_lab.luminesce import make_shopper
from finbourne_lab import Convener, FileRecorder, DriveRecorder
import lumipy as lm
import argparse


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='description')
    parser.add_argument(
        '--secrets_path',
        dest='secrets_path',
        default=None,
        help='The path to your luminesce secrets json file. Optional, but if not used auth will fall back on env vars'
    )
    parser.add_argument(
        '--record_path',
        dest='record_path',
        help='The path to record data to. If prefixed with "drive:/" data will be recorded to a path in drive, '
             'otherwise it will be recorded locally'
    )
    parser.add_argument(
        '--n_parallel',
        dest='n_parallel',
        default=1,
        help='The number of parallel shoppers to run at once. Defaults to one.',
        type=int
    )
    parser.add_argument(
        '--run_time',
        dest='run_time',
        default=None,
        help='The time to run for in seconds, if None it will run forever. Defaults to None.',
        type=int
    )
    parser.add_argument(
        '--skip_ensure',
        dest='skip_ensure',
        action='store_true',
        help='Whether to skip ensure checks that check whether test scopes have the right '
             'instrument/txn/holding/portfolio content.'
    )

    args = parser.parse_args()

    print('Starting lumishopper')
    atlas = lm.get_atlas(api_secrets_filename=args.secrets_path)

    rpath = args.record_path
    print(f'Recording to {rpath}')
    if rpath.startswith('drive:'):
        recorder = DriveRecorder(atlas, rpath.replace('drive:', ''))
    else:
        recorder = FileRecorder(rpath)

    print('Creating lumishopper instance')
    shopper = make_shopper(atlas, skip_checks=args.skip_ensure)

    print(f'Running lumishopper (n_parallel = {args.n_parallel})')
    print(repr(shopper))

    c = Convener(shopper, recorder, args.n_parallel)
    t = args.run_time
    c.go(t if t is None else int(t))
