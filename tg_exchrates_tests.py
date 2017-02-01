# run me as "nosetests -v tg_exchrates_tests.py"
from nose.tools import *
from tg_exchrates.tg_exchrates import FUNCNAME

def setup():
    print "SETUP!"

def teardown():
    print "TEAR DOWN!"

def test_basic():
    print "I RAN!"     

def test_case1FUNCNAME(self):
    assert FUNCNAME("This is a test!", 0) == "This is a test!"

if __name__ == '__main__':
    nose.main()