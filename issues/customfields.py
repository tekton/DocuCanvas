from django.utils.datastructures import MultiValueDict, MergeDict
from django.forms import widgets, fields

class MultipleTextInput(widgets.TextInput):
	def value_from_datadict(self, data, files, name):
		if isinstance(data, (MultiValueDict, MergeDict)):
			return data.getlist(name)
		return data.get(name, None)


class MultipleTextarea(widgets.Textarea):
	def value_from_datadict(self, data, files, name):
		if isinstance(data, (MultiValueDict, MergeDict)):
			return data.getlist(name)
		return data.get(name, None)


class MultipleTextField(fields.MultipleChoiceField):
	widget = MultipleTextInput

	def valid_value(self, value):
		return True