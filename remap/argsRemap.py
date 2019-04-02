import sys, argparse, os

def argsRemap():
    #control structure for remap functions
    #add ability to give the assenstion file which will translate the chromosome number
    ### TODO: add parameter and control structure to do create index
    parser = argparse.ArgumentParser()
    parser.add_argument("-index", "-i", help = "Set Bowtie index to be used")
    parser.add_argument("-LTRcon","-l",help = "LTR consensus sequence")
    parser.add_argument("-seqCon", "-s",help = "Complete element consensus")
    parser.add_argument("-allowance", "--a", type = int,
    help = "Number base pair variance in LTR map", nargs='?',const=1000)
    parser.add_argument("-advancedSearch","-v",
    help = "For andvanced users who wish to change bowtie search parameters directly " )
    parser.add_argument("-name", "-n", help = "Name of element family")
    parser.add_argument("-newIndex", "-b", help= "Tells program to create new bowtie index")
    parser.add_argument("-chrKeys", "-k", help = "Acts as a key to translate NCBI assention file chromosome names to numbers")
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
    if not args.chrKeys:
        print("Please provide a file of keys for chromosomes")
        sys.exit()

    return args
