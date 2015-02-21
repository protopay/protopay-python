import os
import sys
import argparse


from .protopay import protopay


version = VERSION = __version__ = '0.0.1'


def main():

    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument('--version',  action='version', version='protopay v'+version)
    parent.add_argument('--json',     action="store_true", default=False, help="return results as json")
    parent.add_argument('--url',      default=os.getenv("PROTOPAY_URL", "https://protopay.herokuapp.com"), help="change endpoint url", type=str)
    parent.add_argument('--auth',     default=os.getenv("PROTOPAY_AUTH", None), help="your authorization token", type=str)

    parser = argparse.ArgumentParser(prog='protopay',
                                     parents=[parent],
                                     description="---\nDesciprtion\n---",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog="")

    subparsers = parser.add_subparsers(title='==== protopay Commands')

    def subparse(endpoint, ignore=[], **more):
        new_parser = subparsers.add_parser(endpoint, parents=[parent], help="# here")
        new_parser.set_defaults(func=endpoint)
        #custom
        for arg, kwargs in more.items():
            if arg[0]=='_':
                new_parser.add_argument("--%s"%arg[1:], "-%s"%arg[1], **kwargs)
            else:
                new_parser.add_argument(arg, **kwargs)

        return new_parser
    
    # general
    # =======
    subparse('charges')
    subparse('charges:complete', id=dict(nargs=1),
                                 _tip=dict(nargs="?"))
    subparse('requests')
    subparse('test', number=dict(nargs="?", default="4111111111111111"),
                     exp_month=dict(nargs="?", default="12"),
                     exp_year=dict(nargs="?", default="17"))


    if len([a for a in sys.argv if a[0]!='-']) > 1:
        args = parser.parse_args()
        if args.func == 'help':
            parser.print_help()
        else:
            # build token api object
            protopay(args)
    else:
        parser.print_help()

    sys.stdout.write("\n") # for a pretty shell


if __name__ == '__main__':
    main()
