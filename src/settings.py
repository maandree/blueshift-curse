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
    @variable  script:str?             Script client's should source
    '''
    
    def __init__(self, script = None):
        '''
        Constructor
        
        @param  script:str?  Script client's should source
        '''
        self.settings = []
        self.__settings = {}
        self.script = script
    
    
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
    
    
    def __repr__(self):
        '''
        Convert to human- and machine-readable representation
        
        @return  :str  Human- and machine-readable representation
        '''
        return repr((self.script, self.settings))
    
    
    @staticmethod
    def from_repr(representation):
        '''
        Convert from human- and machine-readable representation
        
        @param   representation:str  The representation
        @return  :Settings           The setting
        '''
        (script, settings_) = eval(representation)
        settings = Settings(script)
        for setting in settings_:
            settings.add_setting(Setting.from_dict(setting))
        return settings


class Setting:
    '''
    Adjustment setting instance
    
    @variable  name:str                    The name/code of the setting
    @variable  title:str                   The title of the setting
    @variable  default_value:¿V??          The default value
    @variable  current_value:¿V??          The current value
    @variable  value_type:str              The value type
    @variable  minimum:int|float           The minimum value, length if string or list type, `None` for none
    @variable  maximum:int|float           The maximum value, length if string or list type, `None` for none
    @variable  epsilon:int|float           The minimum (reasonable) value difference, `None` for none
    @variable  possible_values:list<¿V?>?  List of possible values, `None` if not applicable
    '''
    
    
    TYPE_STRING = 'str'
    '''
    Value type: string
    '''
    
    TYPE_LIST = 'list'
    '''
    Value type: string list
    '''
    
    TYPE_INTEGER = 'int'
    '''
    Value type: integer
    '''
    
    TYPE_FLOAT = 'float'
    '''
    Value type: floating point
    '''
    
    
    def __init__(self, name, title, default_value, value_type, minimum = None, maximum = None, epsilon = None, possible_values = None):
        '''
        Constructor
        
        @param  name:str                    The name/code of the setting, whitespace free ASCII only
        @param  title:str                   The title of the setting
        @param  default_value:¿V??          The default value
        @param  value_type:str              The value type
        @param  minimum:int|float           The minimum value, length if string or list type, `None` for none
        @param  maximum:int|float           The maximum value, length if string or list type, `None` for none
        @param  epsilon:int|float           The minimum (reasonable) value difference, `None` for none
        @param  possible_values:list<¿V?>?  List of possible values, `None` if not applicable
        '''
        self.name            = name
        self.title           = title
        self.default_value   = default_value
        self.current_value   = default_value
        self.value_type      = value_type
        self.minimum         = minimum
        self.maximum         = maximum
        self.epsilon         = epsilon
        self.possible_values = possible_values
    
    
    def __repr__(self):
        '''
        Convert to human- and machine-readable representation
        
        @return  :str  Human- and machine-readable representation
        '''
        as_dict = { 'name'            : name
                  , 'title'           : title
                  , 'default_value'   : default_value
                  , 'current_value'   : current_value
                  , 'value_type'      : value_type
                  , 'minimum'         : minimum
                  , 'maximum'         : maximum
                  , 'epsilon'         : epsilon
                  , 'possible_values' : possible_values
                  }
        return repr(as_dict)
    
    
    @staticmethod
    def from_dict(dictionary):
        '''
        Convert from a dictionary
        
        @param   dictionary:dict<str, str|int|float|¿V??>  The dictionary
        @return  :Setting                                  The setting
        '''
        values = 'name, title, default_value, value_type, minimum, maximum, epsilon, possible_values'
        setting = Setting(*[dictionary[value] for value in values.split(', ')])
        setting.current_value = dictionary['current_value']
        return setting
    
    
    @staticmethod
    def from_repr(representation):
        '''
        Convert from human- and machine-readable representation
        
        @param   representation:str  The representation
        @return  :Setting            The setting
        '''
        return Setting.from_dict(eval(representation))

