from config_parser.base_config_model import BaseConfigModel
from config_parser.config_parser_enums.parameter_names import ParameterNames


class TrainingDataConfigModel(BaseConfigModel):

    def get_optional_params(self):
        return {
            ParameterNames.parameter_values: self.set_parameter_values,
            ParameterNames.author: self.set_author,
            ParameterNames.application_name: self.set_application_name,
            ParameterNames.template: self.set_template,
        }

    def get_required_params(self):
        return {
            ParameterNames.prompt: self.set_prompt,
            ParameterNames.reference: self.set_reference,
            ParameterNames.answer_type: self.set_answer_type
        }

    def set_parameter_values(self, value):
        if value is None:
            value = {}
        if not isinstance(value, dict):
            raise ValueError("Parameter Values in training data must be a map of parameter_name to value")

        self.parameter_values = value

    def set_prompt(self, value):
        if not isinstance(value, str):
            raise ValueError("Prompt must be of type string")

        self.prompt = value

    def set_reference(self, value):
        if not isinstance(value, str):
            raise ValueError("Reference must be a string")

        self.reference = value

    def set_answer_type(self, value):
        if not isinstance(value, str):
            raise ValueError("Answer Type must be a string")

        available_types = ["Action", "Python", "Sql"]

        if value not in available_types:
            raise ValueError(f"Answer Types must be in {str(available_types)}")

        self.answer_type = value

    def set_author(self, value):
        self.author = value

    def set_application_name(self, value):
        self.application_name = value

    def set_template(self, value):
        self.template = value
