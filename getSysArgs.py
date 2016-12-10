import sys

## Checks that the proper number of arguments are provided for running a
#  python file
#
#  @param args list
#   list of strings that include (in order) python file name and all arguments
#   to be used in file
#
#  @return list of sys arguments
def usage(args):
    if len(sys.argv) != len(args):
        print 'Usage:\npython ' + ' '.join(args)
        sys.exit(1)

    return sys.argv
