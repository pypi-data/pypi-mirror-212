from config_parser.base_config_model import BaseConfigModel
from config_parser.chat_app_table_config_model import ChatAppTableConfigModel
from config_parser.chat_context_config_model import ChatContextConfigModel
from config_parser.config_parser_enums.parameter_names import ParameterNames


class ChatAppConfigModel(BaseConfigModel):
    def get_required_params(self):
        return {
            ParameterNames.unique_name: self.set_name,
        }

    def get_optional_params(self):
        return {
            ParameterNames.description: self.set_description,
            ParameterNames.created_by: self.set_created_by,
            ParameterNames.default_langauge: self.set_default_langauge,
            ParameterNames.icon_color_code: self.set_icon_color_code,
            ParameterNames.icon_code: self.set_icon_code,
            ParameterNames.cover_photo_id: self.set_cover_photo_id,
            ParameterNames.allowed_user_emails: self.set_allowed_user_emails,
            ParameterNames.editor_user_emails: self.set_editor_user_emails,
            ParameterNames.table_config: self.set_table_config,
            ParameterNames.default_chat_context: self.set_default_chat_context,
            ParameterNames.chat_contexts: self.set_chat_contexts,
            ParameterNames.training_data: self.set_training_data,
        }

    def set_name(self, value):
        self.unique_name = value

    def set_description(self, value):
        self.description = value

    def set_created_by(self, value):
        self.created_by = value

    def set_default_langauge(self, value):
        self.default_langauge = value

    def set_icon_color_code(self, value):
        self.icon_color_code = value

    def set_icon_code(self, value):
        self.icon_code = value

    def set_cover_photo_id(self, value):
        self.cover_photo_id = value

    def set_allowed_user_emails(self, value):
        self.allowed_user_emails = value

    def set_editor_user_emails(self, value):
        self.editor_user_emails = value

    def set_table_config(self, value):
        if value is None:
            value = []

        table_configs = []

        for table_config in value:
            table_configs.append(ChatAppTableConfigModel(table_config))

        if not isinstance(value, list):
            raise ValueError("Table Config must be a list")

        self.table_config = table_configs

    def set_default_chat_context(self, value):
        self.default_chat_context = value

    def set_chat_contexts(self, value):
        if value is None:
            value = []

        if not isinstance(value, list):
            raise ValueError("Chat Contexts must be a list")

        chat_contexts = []
        for chat_context in value:
            chat_contexts.append(ChatContextConfigModel(chat_context))

        self.chat_contexts = chat_contexts

    def set_training_data(self, value):
        if value is None:
            value = []

        if not isinstance(value, list):
            raise ValueError("Training Data must be a list")

        self.training_data = value


