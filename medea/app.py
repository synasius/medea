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
    # list in lib directory and prepend the path
    files = map(lambda x: os.path.join(lib,x), os.listdir(lib)) 
    config.LOG.debug(files)
    
    inlines = sorted(fnmatch.filter(files, "*.x3d"))
    thumbs = sorted(fnmatch.filter(files, "*.png"))

    return zip(inlines, thumbs)


if __name__ == '__main__':
    app.run()
