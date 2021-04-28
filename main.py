import sys
from pseudo_code import fake_system

def main():
    for source in sys.argv[1:]:
        try:
            text = open(source).read()
            system = fake_system()
            system.compile(text)
            system.run()
        except FileNotFoundError as FNFE:
            print('Source: ', FNFE)
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()