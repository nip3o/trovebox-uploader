# -*- coding: utf-8 -*-
import os
import re
import glob
import datetime
import unicodedata

from trovebox import Trovebox
from trovebox.errors import TroveboxError

def is_image(filename):
    # Trovebox supports .jpg, .gif, and .png files
    return bool(re.search(r'\.(jpg|jpeg|gif|png)$', filename, flags=re.IGNORECASE))

def main():
    try:
        client = Trovebox()
        client.configure(api_version=2)

    except IOError, e:
        print
        print '!! Could not initialize Trovebox connection.'
        print '!! Check that ~/.config/trovebox/default exists and contains proper information.'
        print
        raise e

    starttime = datetime.datetime.now()
    files_count = size_count = 0

    for root, folders, files in os.walk(u'.'):
        for filename in files:
            if not is_image(filename):
                continue

            files_count += 1
            size_count += os.path.getsize(os.path.join(root, filename))

    print 'Found %d files, total %d Mib' % (files_count, size_count / (1024 * 1024))

    for root, folders, files in os.walk(u'.'):
        folder_name = album = None

        for filename in files:
            if not is_image(filename):
                continue

            if not folder_name:
                # Convert decomposed string into a composed string.
                # Mac OS uses decomposed unicode filenames, while the Trovebox
                # album name font only supports precomposed filenames.
                folder_name = unicodedata.normalize('NFC', root.split('/')[-1])

                try:
                    client.album.create(folder_name)
                    album = client.album.create(folder_name)

                except TroveboxError, e:
                    print e.message
                    print 'Using full path as album name as fallback'
                    album = client.album.create(root)

                print 'Entering folder %s' % root

            print 'Uploading %s...' % filename

            path = '%s/%s' % (root, filename)
            client.photo.upload(path, albums=[album.id])

    print datetime.datetime.now() - starttime

if __name__ == "__main__":
    main()
