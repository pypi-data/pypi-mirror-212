from configparser import ConfigParser

class ConfigParserSimple:
    def __init__(self, config_path):
        self.cpath = config_path
        self.config = ConfigParser()
    
    def apply_changes(self):
        '''
        Записывает изменения в файл.
        '''
        with open(r'{}'.format(self.cpath), 'w') as config_file:
            self.config.write(config_file)
    
    def create_config(self, section: str, **pairs):
        '''
        Создает .ini файл.
        '''
        self.config.add_section(section)
        for k, v in pairs.items():
            self.config.set(section, k, v)
        
        self.apply_changes()
    
    def read_dict(self, settings: dict):
        '''
        Читает настройки из файла.
        '''
        self.config.read_dict(settings)
    
    def get_keys(self, section: str, keys: list):
        '''
        Возвращает список значений ключей
        '''
        values = list()
        self.config.read(self.cpath)
        for key in keys:
            values.append(f'{self.config.get(section, key)}')

        return values
    
    def get_sections(self):
        '''
        Возвращает список существующих секций.
        '''
        self.config.read(self.cpath)
        return self.config.sections()
    
    
    def set_keys(self, section: str, **pairs):
        '''
        Устанавливает значение ключам.
        '''
        self.config.read(self.cpath)
        for k, v in pairs.items():
            self.config.set(section, k, v)
        
        self.apply_changes()
    
    def delete_keys(self, section: str, keys: list):
        '''
        Удаляет ключи.
        '''
        self.config.read(self.cpath)
        for key in keys:
            self.config.remove_option(section, key)
    
    def delete_section(self, section: str):
        '''
        Удаляет секцию.
        '''
        self.config.read(self.cpath)
        self.config.remove_section(section)