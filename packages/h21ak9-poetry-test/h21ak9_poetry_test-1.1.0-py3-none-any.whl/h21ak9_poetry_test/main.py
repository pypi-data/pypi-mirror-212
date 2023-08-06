from pypl2.pypl2api import *

def hello_world():
    """ Print hello world """
    print("Hello World!")

def read_pl2_info(filename):
    x = pl2_info(filename)
    print(x)

if __name__=="__main__":
    filename = r"C:\Users\nikhil\Documents\Sample-Data\CLH-64WB.pl2"
    read_pl2_info(filename)