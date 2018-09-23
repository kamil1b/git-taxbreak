""" Tool for collect artifacts for taxbreak program
@author Kamil Luczak
"""
import argparse
import os
from os.path import expanduser, expandvars
import sys
from datetime import datetime
from unicodedata import normalize
from zipfile import ZipFile
from git import Repo


def read_user(repo):
    with repo.config_reader() as reader:
        if 'user' in reader.sections():
            return next(
                (v for k, v in reader.items('user') if k == 'name'), None)
    return None


def valid_date(s):
    try:
        datetime.strptime(s, '%m/%d/%y')
        return s
    except ValueError:
        raise argparse.ArgumentTypeError(
            'Invalid date format: {}'.format(s))


def valid_output(filename):
    filename = expanduser(expandvars(filename))
    return argparse.FileType('w+')(filename)


def get_commits(repo, user, after, before):
    commits = repo.git.log(
        '--all',
        '--reverse',
        format='%H',
        author=user,
        after=after,
        before=before).split('\n')
    if '' in commits:
        commits.remove('')
    return commits


def get_diffs(repo, commits, unified):
    return '\n\n'.join(
        normalize(
            'NFKD',
            repo.git.show('-w',
                          '-p',
                          commit,
                          unified=unified)).encode(
                              'ascii',
                              'ignore') for commit in commits)


def get_files(repo, commits):
    return [{'commit_hash': commit,
             'files': [{
                 'file_name': file_name,
                 'content': repo.git.show(commit + ':' + file_name)}
                       for file_name in repo.git.diff_tree('--no-commit-id',
                                                           '--name-only',
                                                           '-r',
                                                           commit).split('\n')]
            } for commit in commits]


def write_archive(destn, commits_files):
    with ZipFile(destn, 'w') as archive:
        for commit_files in commits_files:
            for commit_file in commit_files['files']:
                if not commit_file['file_name']:
                    continue
                archive.writestr(os.path.join(commit_files['commit_hash'],
                                              commit_file['file_name']),
                                 commit_file['content'])


def main():
    today = datetime.today()
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', action='store')
    parser.add_argument(
        '-U',
        '--unified',
        type=int,
        action='store',
        default=0)
    parser.add_argument(
        '-a',
        '--after',
        te=valid_date,
        default=today.strftime('%m/1/%y'))
    parser.add_argument(
        '-b',
        '--before',
        type=valid_date,
        default=today.strftime('%m/%d/%y'))
    parser.add_argument(
        '-o',
        '--output',
        type=valid_output,
        default=sys.stdout)
    parser.add_argument(
        '-t',
        '--type',
        type=str,
        choices=['diff', 'file'],
        default='file')

    args = parser.parse_args()
    repo = Repo(os.getcwd(), search_parent_directories=True)
    user = args.user or read_user(repo)
    commits = get_commits(
        repo, user, args.after, args.before)
    if args.type == "file":
        write_archive(args.output, get_files(repo, commits))
    else:
        args.output.write(
            get_diffs(
                repo,
                commits,
                args.unified))
