# coding: utf-8

import unittest

from django.core.exceptions import ValidationError

from message.factories import MessageFactory
from test.factories import UserFactory


class TestMessage(unittest.TestCase):
    '''
    Test messages
    '''
    def setUp(self):
        self.user = UserFactory()
        self.message = MessageFactory.build()

    def tearDown(self):
        self.user.delete()
        self.message = None

    def test_message_unicode(self):
        self.assertEqual(self.message.title, "%s" % self.message)

    def test_message_save(self):
        self.message.save()
        self.assertIsNotNone(self.message.pk)

    def test_message_remove(self):
        self.message.remove()
        self.assertTrue(self.message.is_removed())

    def test_message_restore(self):
        self.message.remove()
        self.assertTrue(self.message.is_removed())
        self.message.restore()
        self.assertFalse(self.message.is_removed())


class TestMessageCleanData(unittest.TestCase):
    '''
    Test message cleaf functionality.
    '''
    def setUp(self):
        self.user = UserFactory()
        self.message = MessageFactory.build()

    def tearDown(self):
        self.message = None
        self.user.delete()

    def catch_wrong_data(self):
        ''' Common test missed data'''
        with self.assertRaises(ValidationError):
            self.message.save()
            self.message.delete()

    def test_no_message_contacts(self):
        self.message.contact_phone = None
        self.message.contact_mail = None
        self.catch_wrong_data()

    def test_invalid_email(self):
        self.message.contact_mail = 'notamail'
        self.catch_wrong_data()

    def test_phone_contact(self):
        self.message.contact_mail = ''
        self.message.save()
        self.assertIsNotNone(self.message.pk)
        self.message.delete()

    def test_email_contact(self):
        self.message.contact_phone = ''
        self.message.save()
        self.assertIsNotNone(self.message.pk)
        self.message.delete()


class TestUserMessage(unittest.TestCase):
    def setUp(self):
        self.user = UserFactory()

    def tearDown(self):
        self.user.delete()
        self.user = None

    def test_user_message(self):
        msg = MessageFactory(user=self.user)
        self.assertIsNotNone(msg)
        self.assertEqual(self.user, msg.user)