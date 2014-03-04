#!/usr/bin/env python3
'''
blueshift-curse – Blueshift extension with IPC and an ncurses front-end
Copyright © 2014  Mattias Andrée (maandree@member.fsf.org)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


class Settings:
    '''
    Adjustment settings collections
    
    @variable  settings:list<Setting>  All settings
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.settings = []
        self.__settings = {}
    
    
    def add_setting(self, setting):
        '''
        Add a setting
        
        @param  setting:Setting  The setting to add
        '''
        self.settings.append(setting)
        self.__settings[setting.name] = setting
    
    
    def __contains__(self, key):
        '''
        Get whether or not a setting is available
        
        @param   key:str  The setting
        @return  :bool    The availability
        '''
        return key in self.__settings
    
    
    def __getitem__(self, key):
        '''
        Lookup a settings
        
        @param   key:str  The setting
        @return  :int     The value of the field
        '''
        return self.__settings[key]


class Setting:
    '''
    Adjustment setting instance
    
    @variable  name:str           The name/code of the setting
    @variable  title:str          The title of the setting
    @variable  default_value:¿V?  The default value
    @variable  current_value:¿V?  The current value
    @variable  value_type:str     The value type
    @variable  minimum:int|float  The minimum value, length if string type, `None` for unlimited
    @variable  maximum:int|float  The maximum value, length if string type, `None` for unlimited
    @variable  epsilon:int|float  The minimum (reasonable) value difference, `None` for none
    '''
    
    
    TYPE_STRING = 'str'
    '''
    Value type: string
    '''
    
    TYPE_INTEGER = 'int'
    '''
    Value type: integer
    '''
    
    TYPE_FLOAT = 'float'
    '''
    Value type: floating point
    '''
    
    
    def __init__(self, name, title, default_value, value_type, minimum = None, maximum = None, epsilon = None):
        '''
        Constructor
        
        @param  name:str           The name/code of the setting, whitespace free ASCII only
        @param  title:str          The title of the setting
        @param  default_value:¿V?  The default value
        @param  value_type:str     The value type
        @param  minimum:int|float  The minimum value, length if string type, `None` for unlimited
        @param  maximum:int|float  The maximum value, length if string type, `None` for unlimited
        @param  epsilon:int|float  The minimum (reasonable) value difference, `None` for none
        '''
        self.name = name
        self.title = title
        self.default_value = default_value
        self.current_value = default_value
        self.value_type = value_type
        self.minimum = minimum
        self.maximum = maximum
        self.epsilon = epsilon

