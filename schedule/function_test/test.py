# for obtaining arguments
from argparse import ArgumentParser
parser = ArgumentParser(prog='Duty arrange',
                        description='Arranging on-call duties for residents',
                        epilog='please contact 4437 if any suggestions')

parser.add_argument('-f', dest = 'filename', default='duty.xlsm', type=str) # to contain system arguments from jupyter
parser.add_argument('-file', dest = 'filename', default='duty.xlsm', type=str)
parser.add_argument('-num', dest = 'num', default = 100, type=int)

args = parser.parse_args()

# take argument of how many nunmbers to run
# take argument of the file name, append xlsm if not
NUM_TO_RUN = args.num
FILE_NAME = args.filename
FILE_NAME = 'duty.xlsm' if FILE_NAME.endswith('json') else FILE_NAME
FILE_NAME = FILE_NAME if FILE_NAME.endswith('.xlsm') else FILE_NAME + '.xlsm'
# if FILE_NAME.endswith('json') == True:
#     FILE_NAME = 'duty.xlsm'
# if FILE_NAME.endswith('.xlsm') == False:
#     FILE_NAME = FILE_NAME + '.xlsm'


