import argparse

from .plot import plot


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--sus','-s',nargs='+',default=['ETMX'],
                    help='suspension name')
parser.add_argument('--exc','-i',default='IP_TEST_L',
                    help='excitation channel')
parser.add_argument('--read','-o',default='IP_IDAMP_L',
                    help='read channel')
parser.add_argument('--refnum','-r',nargs='+',
                    default=['202202181906','202201211941'],
                    help='reference number')    
args = parser.parse_args()

# Arguments
suspensions = args.sus
ch_from = args.exc
ch_to = args.read
refnumbers = args.refnum
state = 'STANDBY' # should be given by refnumber


if __name__=='__main__':
    plot(suspensions,ch_from,ch_to,refnumbers,state)    
