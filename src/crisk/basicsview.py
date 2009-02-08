#!/usr/bin/env python

from kiwi.ui.delegates import ProxySlaveDelegate

from model import *

class BasicsView(ProxySlaveDelegate):
    def __init__(self):        
        widget_list = ['name', 'location', 'initial_date', 'scope']
        try:
            basics_model = Basic.get(1)
        except:
            basics_model = None
            
        ProxySlaveDelegate.__init__(self, basics_model, widget_list, 
                                    gladefile = 'ui', 
                                    toplevel_name = 'BasicsWindow')
    def proxy_updated(self, *args):
#        print args
#        session.commit()
        pass