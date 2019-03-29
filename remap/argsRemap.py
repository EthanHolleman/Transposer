import sys, argparse, os

def argsRemap():
    #control structure for remap functions

    parser = argparse.ArgumentParser()
    parser.add_argument("-index", "-i", help = "Set Bowtie index to be used")
    parser.add_argument("-LTRcon","-l",help = "LTR consensus sequence")
    parser.add_argument("-seqCon", "-s",help = "Element consensus without LTRs")
    parser.add_argument("-allowance", "--a", type = int,
    help = "Number base pair variance in LTR map", nargs='?',const=1000)
    parser.add_argument("-advancedSearch","-v",
    help = "For andvanced users who wish to change bowtie search parameters directly " )
    args = parser.parse_args()

    if not args.index:
        print("Need index")
        sys.exit()
    if not args.LTRcon:
        print("Please supply LTR consensus sequence")
        sys.exit()
    if not args.seqCon:
        print("Please provide an element consensus sequence")
        sys.exit()
    if args.advancedSearch == "t":
        os.system("nano tier.py")

    return args
