from dotasnif import DotaSniffer
from pprint import pprint

def main():
  x = DotaSniffer('')
  pprint(x.getHeroes())
  

if __name__ == '__main__':
  main()