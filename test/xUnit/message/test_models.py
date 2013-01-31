# coding: utf-8

import unittest

from django.core.exceptions import ValidationError

from factories import MessageFactory
from message.models import Message


class TestMessage(unittest.TestCase):
    '''
    Test messages
    '''
    def setUp(self):
        self.message = MessageFactory()

    def tearDown(self):
        self.message.delete()
        self.message = None

    def test_message(self):
        self.assertIsNotNone(self.message.pk)
    
    def test_no_message_contacts(self):
        m = MessageFactory.build(contact_phone=None)
        m.contact_mail = None
        with self.assertRaises(ValidationError):
            m.save()
            m.delete()
        m = None

    def test_invalid_email(self):
        m = MessageFactory.build()
        m.contact_mail = 'notamail'
        with self.assertRaises(ValidationError):
            m.save()
            m.delete()
        m = None

    def test_phone_contact(self):
        m = MessageFactory.build()
        m.contact_mail = ''
        m.save()
        self.assertIsNotNone(m.pk)
        m.delete()

    def test_email_contact(self):
        m = MessageFactory.build(contact_phone='')
        m.save()
        self.assertIsNotNone(m.pk)
