import argparse
from importlib.metadata import version, PackageNotFoundError

def main():
    parser = argparse.ArgumentParser(description='Payment Emulation')
    parser.add_argument(
        '-v',
        '--version', 
        action="version", 
        version=get_version(),
        help='Displays the current version of Payment Emulation'
    )
    
    args = parser.parse_args()

def get_version():
    try:
        return f'payment-emulation {version("payment-emulation")}'
    except PackageNotFoundError:
        return ''

if __name__ == '__main__':
    main()
