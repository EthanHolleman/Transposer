import sys, argparse

def argsCon():
    parser = argparse.ArgumentParser()

    parser.add_argument("-Pagan", "-P", help =
    "Use pagan software, requires fasta file to create consensus")
    parser.add_argument("-conFiles", "-c",
    help = "Collection sequences used for consensus")
    args = parser.parse_args()
    

    if args.Pagan and not args.conFiles:
        print("Arguement -P requires -c")
        sys.exit()
    elif not args.Pagan and args.conFiles:
        print("Argument -c requires -P")
        sys.exit()
        #needs to run the pagan search and send con to useful location
