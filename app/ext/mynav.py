from flask_nav import Nav
from flask_nav.elements import Navbar, View

nav = Nav()
nav.register_element('top', Navbar(u'老化测试工具',
                                    View(u'测试', 'blue_index.index'),
                                    View(u'管理', 'blue_index.manage'),
                                    View(u'关于', 'blue_index.about'),
                                    ))

def init_nav(app):
    nav.init_app(app)

