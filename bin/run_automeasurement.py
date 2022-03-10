
import argparse
import ezca

ezca = ezca.Ezca()
grdsts_fmt = 'GRD-VIS_%s_STATE_S'


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sus',nargs='+')
    parser.add_argument('--stg',nargs='+')
    args = parser.parse_args()
    suslist = args.sus
    stglist = args.stg

    stslist = [ezca[grdsts_fmt%(sus)] for sus in suslist]
    print(stslist)
