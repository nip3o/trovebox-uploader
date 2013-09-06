import os
import re
import datetime

from trovebox import Trovebox
from trovebox.errors import TroveboxError

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

    for root, folders, files in os.walk(os.getcwd()):
        folder_name = album = None

        for filename in files:
            # Trovebox supports .jpg, .gif, and .png files
            if not re.search(r'\.(jpg|jpeg|gif|png)$', filename, flags=re.IGNORECASE):
                continue

            if not folder_name:
                folder_name = root.split('/')[-1]

                try:
                    album = client.album.create(folder_name)
                except TroveboxError, e:
                    print e.message
                    print 'Using full path as album name as fallback'

                print 'Entering folder %s' % root

            print 'Uploading %s...' % filename

            path = '%s/%s' % (root, filename)
            client.photo.upload(path, albums=[album.id])

    print datetime.datetime.now() - starttime

if __name__ == "__main__":
    main()
