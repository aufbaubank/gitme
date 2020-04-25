# gitme

[![Build Status](https://travis-ci.com/aufbaubank/gitme.svg?branch=master)](https://travis-ci.com/aufbaubank/gitme)
[![codecov](https://codecov.io/gh/aufbaubank/gitme/branch/master/graph/badge.svg)](https://codecov.io/gh/aufbaubank/gitme)

Can be used to create a merge request on gitlab for a changed repostory.

Desired Workflow:
1. periodically run some tasks in a git repository that may change some files
2. run `gitme` to create a merge request, if files have changed

## options

```
usage: gitme [-h] [-u url] [-t pat] [-a] [-g gitrepo] [-b branch] [-V]
             [-l LOGLEVEL] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -u url, --url url     url of gitlab server, defaults to http://localhost
  -t pat, --pat pat     personal access token
  -a, --automerge       automerge merge requests if pipeline succeeds
  -g gitrepo, --gitrepo gitrepo
                        repository location
  -b branch, --branch branch
                        branch name, default: gitme/update
  -V, --version         print version
  -l LOGLEVEL, --loglevel LOGLEVEL
                        loglevel: critical, error, warning, info, debug
  -v, --verbose
```
