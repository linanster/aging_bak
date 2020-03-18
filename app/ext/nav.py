from flask_nav import Nav
from flask_nav.elements import Navbar, View

nav = Nav()
nav.register_element('top', Navbar(u'老化测试工具',
                                    View(u'测试', 'blue_nav.index'),
                                    View(u'管理', 'blue_nav.manage'),
                                    View(u'关于', 'blue_nav.about'),
                                    ))


