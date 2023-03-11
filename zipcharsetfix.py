import sys
from zipfile import ZipFile

def help():
    print('Usages: zipcharsetfix.py <filename> [convert_txt=false] [from_charset=shift_jis]')
    print(' Examples:')
    print('  zipcharsetfix.py input.zip')
    print('  zipcharsetfix.py input.zip true')
    print('  zipcharsetfix.py input.zip false big5')

def converted(fn : str):
    i = fn.rfind('.')

    if i == -1:
        return fn + '.converted.zip'
    else:
        return fn[:i] + '.converted' + fn[i:]

if __name__ == '__main__':
    argc = len(sys.argv)

    if argc < 2:
        help()
    else:
        fn = sys.argv[1]
        txt = False
        encoding = 'shift_jis'

        if argc > 2:
            txt = True if sys.argv[2].lower() == 'true' else False
        
        if argc > 3:
            encoding = sys.argv[3]

        zipIn = ZipFile(fn)
        zipOut = ZipFile(converted(fn), 'w')

        zipOut.comment = zipIn.comment

        for data in zipIn.filelist:
            if not data.filename.endswith('/'):
                data.filename = data.filename.encode('cp437').decode(encoding)
                content = zipIn.open(data, 'r').read()

                if data.filename.endswith('.txt') and txt:
                    zipOut.writestr(data, content.decode(encoding))
                else:
                    zipOut.writestr(data, content)

        zipIn.close()
        zipOut.close()