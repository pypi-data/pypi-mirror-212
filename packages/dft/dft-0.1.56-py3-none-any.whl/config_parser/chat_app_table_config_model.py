from config_parser.base_config_model import BaseConfigModel
from config_parser.config_parser_enums.parameter_names import ParameterNames


class ChatAppTableConfigModel(BaseConfigModel):
    def get_required_params(self):
        return {
            ParameterNames.table_name: self.set_table_name,
        }

    def get_optional_params(self):
        return {
            ParameterNames.columns_to_ignore: self.set_columns_to_ignore,
        }

    def set_table_name(self, value):
        self.table_name = value

    def set_columns_to_ignore(self, value):
        if value is None:
            value = []

        if not isinstance(value, list):
            raise ValueError("Columns to ignore must be a list")

        self.columns_to_ignore = value
