#!/usr/bin/python
import requests
import subprocess
import sys


DEBUG = True

REPO_API_URL = 'https://api.github.com/repos/{owner}/{repo}'


class CommadnException(Exception):
    pass


def call(cmd):
    print "$", cmd
    if subprocess.Popen(cmd, shell=True).wait() != 0:
        raise CommadnException('Command "{cmd}" fail'.format(cmd=cmd))


def parse_url(git_url):
    # git@github.com:ad-m/github-clone.git
    # https://github.com/ad-m/github-clone.git
    if git_url.startswith('git@github.com'):
        return tuple(git_url.split('.')[1].split(':')[1].split('/'))
    if git_url.startswith('https://github.com/'):
        return tuple(git_url.split('.')[1].split('/')[1:])
    raise ValueError("Mailform URL")


def get_parent_git_url(user, repo):
    url = REPO_API_URL.format(owner=user, repo=repo)
    return (lambda x: x['parent']['ssh_url'] if 'parent' in x else None)(requests.get(url).json())


def git_add(git_url, directory):
    call('git clone {url} {directory}'.format(url=git_url, directory=directory))
    parent_git_url = get_parent_git_url(*parse_url(git_url))
    if parent_git_url:
        call('cd {directory}; git remote add upstream {url}'.format(url=parent_git_url,
                                                                    directory=directory))
        call('cd {directory}; git fetch upstream; git fetch origin'.format(directory=directory))


def main():
    try:
        if len(sys.argv) == 3:
            if 'github' not in sys.argv[1]:
                print("Incorrect git_url")
                return
            git_add(sys.argv[1], sys.argv[2])
        else:
            print "Usage: {sh} [git_url] [output_dir]".format(sh=sys.argv[0])
    except CommadnException as e:
        print str(e)

if '__main__' == __name__:
    main()
