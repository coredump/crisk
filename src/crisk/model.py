#!/usr/bin/env python
# coding: utf-8 

import datetime
from elixir import *

class Basic(Entity):
    using_options(autosetup = True, tablename = 'basic')
    
    name = Field(Unicode(64))
    location = Field(Unicode(64))
    initial_date = Field(DateTime, default = datetime.datetime.now)
    scope = Field(UnicodeText)
    
class Asset(Entity):
    using_options(autosetup = True, tablename = 'asset')
    
    
    name = Field(Unicode(64))
    description = Field(UnicodeText)
    __value = Field(Numeric)
    
    vulns = ManyToMany('Vulnerability', ondelete = 'cascade')
    
    def set_value(self, value):
        self.__value = int(value)

    def get_value(self):
        return self.__value
    
    value = property(get_value, set_value)
    
    
class Vulnerability(Entity):
    using_options(autosetup = True, tablename = 'vulnerability')
    
    description = Field(Unicode(256))
    severity = Field(Numeric)
    chance = Field(Numeric)
    
    assets = ManyToMany('Asset', ondelete = 'cascade')
    threats = ManyToMany('Threat', ondelete = 'cascade')
    
class Threat(Entity):
    using_options(autosetup = True, tablename = 'threat')
    
    name = Field(Unicode(64))
    description = Field(Unicode(256))
    
    vulns = ManyToMany('Vulnerability', ondelete = 'cascade')