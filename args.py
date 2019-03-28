import sys, argparse

def args():

    parser = argparse.ArgumentParser()
    parser.add_argument("-index", "-i", help = "Set Bowtie index to be used")
    parser.add_argument("-LTRcon","-L",help = "LTR consensus sequence")
    parser.add_argument("-seqCon", "-S",help = "Element consensus without LTRs")
    parser.add_argument("-allowance", "--a", type = int,
    help = "Number base pair variance in LTR map", nargs='?',const=1000)
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

    return args
