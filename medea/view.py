import web
import config

t_globals = dict(
  datestr=web.datestr
)

render = web.template.render('templates/', 
                             cache=config.cache, 
                             globals=t_globals)

def editor(**kw):
    """ Renders editor """
    return render.editor(**kw)
