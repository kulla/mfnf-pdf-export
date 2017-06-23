"""Module for downloading all articles in a sitemap into a tree-like directory
structure.

Copyright 2017 Stephan Kulla
"""

import json
import os
import functools
import gevent
import config

from api import MediaWikiAPI

gevent.monkey.patch_all()

def remove_special_characters(word):
    """Clear a word from special characters."""
    return functools.reduce(lambda w, sc: w.replace(sc, ''),
                            "()!?:\'",
                            word.replace(' ', '_'))

def download(node, storage_path, wikibook_api):
    """Download the article of a sitemap node and all of its children.

    Arguments:
        node -- sitemap node (dict with name, link and children)
        storage_path -- directory for download (string)
        wikibook_api -- MediaWikiAPI object to perform the download
    """
    name = remove_special_characters(node["name"])
    link = node["link"]
    children = node["children"]
    target_path = os.path.join(storage_path, name)
    if children:
        os.makedirs(target_path, exist_ok=True)
        jobs = [gevent.spawn(download, child, target_path, wikibook_api)
                for child in children]
        gevent.joinall(jobs)
    if link and not children:
        contents = wikibook_api.get_content(link)
        with open(target_path + ".txt", 'w') as output_file:
            output_file.write(contents)

def run_script(sitemap_file_name):
    """Recursively download a sitemap.

    Arguments:
        sitemap_file_name -- name of the sitemap file (string)
    """
    wikibooks = MediaWikiAPI()

    with open(sitemap_file_name, 'r') as sitemap_file:
        sitemap = json.loads(sitemap_file.read())

    books = sitemap["children"]
    jobs = [gevent.spawn(download, book, "raw", wikibooks) for book in books]
    gevent.joinall(jobs)

if __name__ == "__main__":
    run_script(config.SITEMAP_FILE_NAME)
