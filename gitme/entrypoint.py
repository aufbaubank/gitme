import gitme
import sys
import argparse
import os
import logging

from gitme.gitlab_controller import GitlabClient
from gitme.git_controller import Git
from gitme.log import configure_logger


def create_argparser(args):
    """
    parse args
    """
    argp = argparse.ArgumentParser(description=__doc__)
    argp.add_argument(
        '-u', '--url',
        metavar='url', default='http://localhost', type=str,
        help='url of gitlab server, defaults to http://localhost'
    )
    argp.add_argument(
        '-t', '--pat',
        metavar='pat', default='', type=str,
        help='personal access token'
    )
    argp.add_argument(
        '-a', '--automerge',
        default=False, action='store_true',
        help='automerge merge requests if pipeline succeeds'
    )
    argp.add_argument(
        '-g', '--gitrepo',
        metavar='gitrepo', default=os.getcwd(), type=str,
        help='repository location, default: cwd'
    )
    argp.add_argument(
        '-b', '--branch',
        metavar='branch', default='gitme/update', type=str,
        help='branch name, default: gitme/update'
    )
    argp.add_argument(
        '-V', '--version',
        default=False, action='store_true',
        help='print version'
    )
    argp.add_argument(
        '-l', '--loglevel',
        default='critical', type=str,
        help='loglevel: critical(default), error, warning, info, debug'
    )

    argp.add_argument('-v', '--verbose', action='count', default=0)

    arguments = argp.parse_args(args)
    return arguments


def main():

    argv = sys.argv[1:]
    if len(argv) == 0:
        argv = ['--help']

    args = create_argparser(argv)
    configure_logger(args)
    logger = logging.getLogger('main')

    if args.version:
        print(gitme.__version__)
        sys.exit()

    git = Git(args)

    try:
        if not git.is_modified():
            logger.info('no files changed')
            sys.exit(0)

        if not git.create_update_branch():
            logger.info('changes already committed to update branch')
        else:
            logger.info('changes need to be pushed')
            git.push()

        glc = GitlabClient(args)
        glc.create_update_mergerequest()

    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
