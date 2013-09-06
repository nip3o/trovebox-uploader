# -*- coding: utf-8 -*-
import os
import re
import logging
import unicodedata

from trovebox import Trovebox
from trovebox.errors import TroveboxError, TroveboxDuplicateError

from progressbar import ProgressBar, Percentage, Bar, ETA, FileTransferSpeed

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

    files_count = size_count = uploaded_count = 0

    for root, _, files in os.walk(u'.'):
        for filename in files:
            if not is_image(filename):
                continue

            files_count += 1
            size_count += os.path.getsize(os.path.join(root, filename))

    print 'Found %d files, total %d Mib' % (files_count, size_count / (1024 * 1024))

    widgets = [Percentage(), Bar(), ETA(), ' ', FileTransferSpeed()]
    size = ProgressBar(maxval=size_count, widgets=widgets).start()

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
                logging.info('Entering folder %s' % root)

                try:
                    album = client.album.create(folder_name)

                except TroveboxError, e:
                    logging.warning('Album "%s" already exists, falling back on path' % folder_name)
                    album = client.album.create(unicodedata.normalize('NFC', root))

            path = os.path.join(root, filename)

            try:
                logging.info('Uploading %s' % filename)
                client.photo.upload(path, albums=[album.id])
            except TroveboxDuplicateError:
                logging.warning('File %s was already uploaded' % path)
                pass

            uploaded_count += os.path.getsize(path)
            size.update(uploaded_count)
    size.finish()

if __name__ == "__main__":
    main()
