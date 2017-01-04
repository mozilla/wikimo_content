#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) Mozilla Corporation, 2015
#
# Contributors:
# Guillaume Destuynder (kang@mozilla.com)
#
# ABOUT:
# This is a wikimedia sync tool to ease managing files in a Git repository (for example).
# It can automatically get/push files and show diff comparisons.
#
# TODO:
# Support non *.mediawiki content such as images.
# Support exploring/listing a wiki space that doesn't yet exist on disk.

import mwclient
import hjson as json
import os, fnmatch
import hashlib
import difflib
import sys
import getopt
import subprocess

def connect(config):
    site = mwclient.Site(('https', config['site']), clients_useragent=config['useragent'])
    site.login(config['username'], config['password'])
    return site

def get_mediawiki_files_from_disk(config):
    docs = []
    for root, dirnames, filenames in os.walk(config['basedir']):
        for filename in fnmatch.filter(filenames, '*.mediawiki'):
            docs.append(os.path.join(root, filename).strip('./').rstrip('.mediawiki'))
    return docs

def blist2str(l):
    assert type(l) is list

    out = []
    for i in l:
        if type(i) is bytes:
            out.append(i.decode('utf-8'))
        else:
            out.append(i)
    return out

def check_repos_is_current(config):
    ret = subprocess.call(["git", "pull", "--ff-only", config['repos'], "master"])
    if (ret != 0):
        print ("Operation cancelled: Failed to update from upstream repository. Check you have the latest version of the wiki checked-out  before attempting to push again.")
        sys.exit(3)

def compare_site_and_disk(config, diff, site, docs, push, get):
    ''' Does both compare and push/get since it's quite similar code-wide'''
    for f in docs:
        full_path = './'+f+'.mediawiki'
        m_ondisk = hashlib.new(config['hashalg'])
        with open(full_path) as fd:
            on_disk = fd.read()
        m_ondisk.update(on_disk.encode('utf-8'))

        m_onsite = hashlib.new(config['hashalg'])
        page = site.Pages[f]
        on_site = page.text().encode('utf-8')+'\n'.encode('utf-8')
        m_onsite.update(on_site)

        if m_ondisk.digest() != m_onsite.digest():
            print("Page {} differ.".format(f))
            if (diff):
                #Just display diff in the correct order, we default to push-side-diff
                if get:
                    mydiff = difflib.unified_diff(blist2str(on_site.splitlines(1)), blist2str(on_disk.splitlines(1)))
                else:
                    mydiff = difflib.unified_diff(blist2str(on_disk.splitlines(1)), blist2str(on_site.splitlines(1)))

                sys.stdout.writelines(mydiff)

            #Now push or get whatever is needed to sync
            #But never do both push and get at once, would make no sense
            if get:
                print("Getting {} from site to disk.".format(f))
                with open(full_path, 'w') as fd:
                    fd.write(on_site.decode('utf-8'))
            elif push:
                check_repos_is_current(config)
                print("Pushing {} from disk to site.".format(f))
                page.save(on_disk, summary=u'Automated sync from {}'.format(config['repos']))

def main(opts, args):
    diff=False
    get=False
    push=False
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-d', '--diff'):
            diff=True
        elif o in ('-p', '--push'):
            if get:
                print("You can't both get and push. Choose one!")
                usage()
                sys.exit(2)
            push=True
        elif o in ('-g', '--get'):
            if push:
                print("You can't both get and push. Choose one!")
                usage()
                sys.exit(2)
            get=True
        else:
            assert False, "unhandled option {}".format(o)


    with open('sync.json') as fd:
        config = json.load(fd)
    site = connect(config)
    docs = get_mediawiki_files_from_disk(config)
    compare_site_and_disk(config, diff, site, docs, push, get)

def usage():
    print("""USAGE: {argv} [OPTIONS]

-h, --help      Shows this help text.
-d, --diff      Also shows a unified diff during comparison, upload or download.

-p, --push      Upload from disk to wiki (will overwrite wiki contents!).
-g, --get       Download from wiki to disk (you'll still want to git commit).
""".format(argv=sys.argv[0]))

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hdpg", ["help", "diff", "push", "get"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)
    main(opts, args)
