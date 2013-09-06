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
        folder_name = None

        for filename in files:
            if not re.match(r'^.+\.jpg$', filename, flags=re.IGNORECASE):
                continue

            if not folder_name:
                folder_name = root.split('/')[-1]
                print 'Entering folder %s' % root

            print 'Uploading %s...' % filename

            path = '%s/%s' % (root, filename)
            client.photo.upload(path, tags=['API test', folder_name])

    print datetime.datetime.now() - starttime

if __name__ == "__main__":
    main()
