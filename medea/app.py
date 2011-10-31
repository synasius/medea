import web, os
import config

from view import render

urls = (
        '/', 'editor',
)

app = web.application(urls, globals())


class editor(object):
    def GET(self):
        lib = parse_library(config.LIBRARY_PATH)
        config.LOG.debug(lib)
        return render.editor(lib)


def parse_library(lib):
    import fnmatch
    files = fnmatch.filter(os.listdir(lib), "*.x3d")
    
    # prepend the path to the x3d filename
    inlines = [[os.path.join(lib, file)] for file in files]
    
    for file in inlines:
        thumb = os.path.splitext(file[0])[0] + '.png'
        file.append(os.path.exists(thumb) and thumb or config.LIBRARY_NO_THUMB)
    
    return inlines


if __name__ == '__main__':
    app.run()
