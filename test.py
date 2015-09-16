from smitesnif import SmiteSniffer
from pprint import pprint

def main():
  x = SmiteSniffer('', '')
  #pprint(x.createSession())
  pprint(x.testSession())
  

if __name__ == '__main__':
  main()
