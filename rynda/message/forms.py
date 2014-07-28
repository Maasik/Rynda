# -*- coding: utf-8 -*-

from django.contrib.gis import forms as geoforms
from django.core.exceptions import ValidationError
from django.forms.util import ErrorList
from django.utils.translation import ugettext as _

import floppyforms.__future__ as forms
from leaflet.forms.widgets import LeafletWidget

from message.models import Message


class VirtualMessageFormMixin(forms.ModelForm):

    """ Виртуальные сообщения """

    def __init__(self, *args, **kwargs):
        super(VirtualMessageFormMixin, self).__init__(*args, **kwargs)
        self.fields['is_virtual'] = forms.BooleanField(default=True)

    def clean_isvirtual(self):
        return True

    def clean_location(self):
        return None


class MessageForm(forms.ModelForm):

    """ Базовая форма ввода сообщения """

    class Meta:
        model = Message
        fields = (
            'title', 'message', 'messageType',
            'category',
            'is_anonymous', 'allow_feedback', 'is_virtual',
            # 'address', 'coordinates',
        )
        widgets = {
            'category': forms.CheckboxSelectMultiple(),
        }

    def clean_messageType(self):
        test = self.cleaned_data['messageType']
        if not test:
            raise ValidationError(_("Unknown message type!"))
        return test


class UserMessageForm(forms.ModelForm):
    class Meta():
        model = Message
        fields = (
            'title', 'message', 'messageType',
            'category',
            'is_anonymous', 'allow_feedback', 'is_virtual',
        )
        widgets = {
            'messageType': forms.HiddenInput(),
            'category': forms.CheckboxSelectMultiple(),
        }

    first_name = forms.CharField(label=_('First name'), required=False)
    last_name = forms.CharField(label=_('Last name'), required=False)
    email = forms.EmailField(label=_('Contact email'), required=False)
    phone = forms.CharField(label=_('Contact phone'), required=False)
    address = forms.CharField(label=_('Address'))
    # TODO MultiPointField
    coordinates = geoforms.GeometryCollectionField(
        label=_('Coordinates'),
        widget=LeafletWidget(),)

    def save(self, force_insert=False, force_update=False, commit=True):
        msg = super(UserMessageForm, self).save(commit=False)
        msg.additional_info = {
            'first_name': self.cleaned_data['first_name'],
            'last_name': self.cleaned_data['last_name'],
            'email': self.cleaned_data['email'],
            'phone': self.cleaned_data['phone'],
        }
        if commit:
            msg.save()
        return msg

    def clean(self):
        """
        Проверка корректности формы.

        Необходимо, чтобы пользователь заполнил хотя бы одно из двух полей
        email и phone. Если это не выполнено, выдать ошибку проверки формы.
        """
        super(UserMessageForm, self).clean()
        ce = self.cleaned_data
        if ce['email'] == '' and ce['phone'] == '':
            self.errors['email'] = ErrorList([
                _("You must provide at least one from contact email or phone!"),
            ])
            self.errors['phone'] = ErrorList([
                _("You must provide at least one from contact email or phone!"),
            ])
            raise ValidationError(
                _("You must provide at least one from contact email or phone!"))
        return ce


class RequestForm(UserMessageForm):
    """ Simple request form. """

    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        self.fields['messageType'].initial = Message.REQUEST

    def clean_messageType(self):
        return Message.REQUEST


class OfferForm(UserMessageForm):
    """ Simple offer form. """

    def __init__(self, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        self.fields['messageType'].initial = Message.OFFER

    def clean_messageType(self):
        return Message.OFFER


class InformationForm(UserMessageForm):
    """ Simple information form. """

    def __init__(self, *args, **kwargs):
        super(InformationForm, self).__init__(*args, **kwargs)
        self.fields['messageType'].initial = Message.INFO

    def clean_messageType(self):
        return Message.INFO


class AdminMessageForm(MessageForm):
    class Meta(MessageForm.Meta):
        widgets = {
            'messageType': forms.Select(),
            'category': forms.CheckboxSelectMultiple(),
        }

    def clean_messageType(self):
        return self.cleaned_data['message_type']