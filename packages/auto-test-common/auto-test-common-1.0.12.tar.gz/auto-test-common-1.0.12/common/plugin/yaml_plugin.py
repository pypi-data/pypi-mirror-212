from common.data.data_process import DataProcess
from common.plugin.data_bus import DataBus

class YamlPlugin(object):

    @classmethod
    def load_data(self,file_name,file_path: str = TEST_DATA_PATH):
        DataBus.save_init_data()
        _path = path.join(file_path, file_name, )
        get_yaml_data(_path)

    @classmethod
    def get_dict(self,file_name, key:str=None, file_path: str = TEST_DATA_PATH):
        _data = load_data(file_name,file_path)
        if DataProcess.isNotNull(key):
            yamlData = extractor(yamlData, key)
            return yamlData
        else:
            return yamlData


if __name__ == '__main__':
    _info1 = YamlPlugin.get_dict("test.yaml")
    print(_info1)
