# test for arguments
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument('-f', '--filename', dest = 'filename', default='test.xlsm')
parser.add_argument('-n', '--number', dest = 'num', default = 100)

args = parser.parse_args()

print('filename = ', args.filename)
print('number = ', args.num)