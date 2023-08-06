# standard imports
import os

cic_unittest_dir = os.path.dirname(os.path.realpath(__file__))
contracts_dir = os.path.join(cic_unittest_dir, 'solidity')


def bytecode(v):
    fp = os.path.join(contracts_dir, v.capitalize() + 'Test.bin')
    f = open(fp, 'r')
    r = f.read()
    f.close()
    return r
