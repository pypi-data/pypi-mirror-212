import os

import argparse
import subprocess


def deploy_monitoring():
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'deploy-oss.sh')
    subprocess.run(['bash', script_path])


def main():
    parser = argparse.ArgumentParser(description='Utility CLI to install Deepchecks components')
    subparsers = parser.add_subparsers(dest='command', help='Sub-command help')

    # install sub-command
    install_parser = subparsers.add_parser('install-monitoring', help='Install the monitoring OSS solution')
    install_parser.set_defaults(func=deploy_monitoring)

    args = parser.parse_args()

    if not hasattr(args, 'func'):
        parser.print_help()
        return

    args.func()


if __name__ == '__main__':
    main()
