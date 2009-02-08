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
    __value = Field(UnicodeText)
    
    vulns = ManyToMany('Vulnerability')
    
    
class Vulnerability(Entity):
    using_options(autosetup = True, tablename = 'vulnerability')
    
    description = Field(Unicode(256))
    severity = Field(Numeric)
    chance = Field(Numeric)
    
    assets = ManyToMany('Asset')
    threats = ManyToMany('Threat')
    
class Threat(Entity):
    using_options(autosetup = True, tablename = 'threat')
    
    name = Field(Unicode(64))
    description = Field(Unicode(256))
    
    vulns = ManyToMany('Vulnerability')