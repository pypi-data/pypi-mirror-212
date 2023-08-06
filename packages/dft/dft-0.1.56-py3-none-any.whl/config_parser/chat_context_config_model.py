from config_parser.base_config_model import BaseConfigModel
from config_parser.chat_app_table_config_model import ChatAppTableConfigModel
from config_parser.config_parser_enums.parameter_names import ParameterNames


class ChatContextConfigModel(BaseConfigModel):

    def get_optional_params(self):
        return {
            ParameterNames.table_config: self.set_table_config,
            ParameterNames.behaviour: self.set_behaviour,
            ParameterNames.created_by: self.set_created_by,
        }

    def get_required_params(self):
        return {
            ParameterNames.keywords: self.set_keywords,
        }

    def set_keywords(self, value):
        if not isinstance(value, list):
            raise ValueError("Keywords must be a list")

        self.keywords = value

    def set_table_config(self, value):
        if value is None:
            value = []

        if not isinstance(value, list):
            raise ValueError("Table config for chat context must be a list")

        table_configs = []

        for table_config in value:
            table_config_model = ChatAppTableConfigModel(table_config)
            table_configs.append(table_config_model)

        self.table_config = table_configs

    def set_behaviour(self, value):
        self.behaviour = value

    def set_created_by(self, value):
        self.created_by = value
