
import binascii
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from graphql_relay import from_global_id


class GlobalIDToPkModelChoiceField(forms.ModelChoiceField):
  default_error_messages = {"invalid": _("Invalid ID specified.")}

  def clean(self, value):
    if not value and not self.required:
      return None

    try:
      _type, _id = from_global_id(value)
    except (TypeError, ValueError, UnicodeDecodeError, binascii.Error):
      raise ValidationError(self.error_messages["invalid"])

    try:
      forms.CharField().clean(_id)
      forms.CharField().clean(_type)
    except ValidationError:
      raise ValidationError(self.error_messages["invalid"])

    return self.queryset.get(pk=_id)


class GlobalIDToPkMultipleChoiceField(forms.ModelMultipleChoiceField):
  default_error_messages = {
    "invalid_choice": _("One of the specified IDs was invalid (%(value)s)."),
    "invalid_list": _("Enter a list of values."),
  }

  def clean(self, value):
    qs = []
    for global_id in value:
      qs.append(GlobalIDToPkModelChoiceField(queryset=self.queryset).clean(global_id))
    return qs
