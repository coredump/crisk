#!/usr/bin/env python
# coding: utf-8 

import datetime
from elixir import *

class Basic(Entity):
    
    using_options(autosetup = True)
    
    name = Field(Unicode(64))
    location = Field(Unicode(64))
    initial_date = Field(DateTime, default = datetime.datetime.now)
    scope = Field(UnicodeText)
    
class Asset(Entity):
    
    name = Field(Unicode(64))
    description = Field(UnicodeText)
    value = Field(UnicodeText)
    
    vulns = ManyToMany('Vulnerabilities')
    
class Vulnerabilities(Entity):
    
    description = Field(Unicode(256))
    severity = Field(Numeric)
    chance = Field(Numeric)
    
    assets = ManyToMany('Asset')
    threats = ManyToMany('Threat')
    
class Threat(Entity):
    
    name = Field(Unicode(64))
    description = Field(Unicode(256))
    
    vulns = ManyToMany('Vulnerabilities')