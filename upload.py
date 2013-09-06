import os
import re
import datetime

from trovebox import Trovebox

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
            if not re.match(r'^.+\.jpg$', filename, flags=re.IGNORECASE):
                continue

            if not folder_name:
                folder_name = root.split('/')[-1]
                album = client.album.create(folder_name)
                print 'Entering folder %s' % root

            print 'Uploading %s...' % filename

            path = '%s/%s' % (root, filename)
            client.photo.upload(path, albums=[album.id])

    print datetime.datetime.now() - starttime

if __name__ == "__main__":
    main()
