from configparser import ConfigParser

class ConfigParserSimple:
    def __init__(self, config_path):
        self.cpath = r'{}'.format(config_path)
        self.config = ConfigParser()
    
    def reread(self):
        self.config.read(self.cpath)
    
    def add_section(self, section: str):
        '''
        Добавляет секцию в файл.
        '''
        self.config.add_section(section)
    
    def set_keys(self, section: str, **pairs):
        '''
        Позволяет записать в файл сразу несколько пар ключ=значение.
        '''
        for k, v in pairs.items():
            self.config.set(section, str(k), str(v))
        
        with open(self.cpath, 'w') as config_file:
            self.config.write(config_file)
    
    def get_keys(self, section: str, keys: list):
        '''
        Позволяет получить из файла сразу несколько пар ключ=значение.
        '''
        self.reread()
        values = list()
        for key in keys:
            values.append(f'{self.config.get(section, key)}')

        return values
    
    def get_sections(self):
        '''
        Возвращает список существующих секций.
        '''
        self.reread()
        return self.config.sections()
    
    def delete_keys(self, section: str, keys: list):
        '''
        Позволяет удалить из файла сразу несколько пар ключ=значение.
        '''
        self.reread()
        for key in keys:
            self.config.remove_option(section, key)
        
        with open(self.cpath, 'w') as config_file:
            self.config.write(config_file)
    
    def delete_section(self, section: str):
        '''
        Удаляет секцию.
        '''
        self.reread()
        self.config.remove_section(section)
        
        with open(self.cpath, 'w') as config_file:
            self.config.write(config_file)