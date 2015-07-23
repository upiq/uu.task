import types
import unittest2 as unittest

from plone import api
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

from uu.task.testing import (
    USER1,
    USER2,
    UUTASK_INTEGRATION_TESTING,
)


class VocabularyTest(unittest.TestCase):

    layer = UUTASK_INTEGRATION_TESTING

    def test_users(self):
        portal = self.layer['portal']
        vocab = getUtility(IVocabularyFactory, name=u"uu.task.Users")
        vocab = vocab(portal)

        user1 = api.user.get(username=USER1)
        user2 = api.user.get(username=USER2)

        self.assertTrue(isinstance(vocab._terms, types.GeneratorType))
        self.assertEqual(len(vocab), 3)

        self.assertTrue(isinstance(vocab._terms, list))
        self.assertEqual(len(vocab), 3)

        self.assertEqual(vocab.getTermByToken(USER1).value, user1)
        self.assertEqual(vocab.getTermByToken(USER2).value, user2)

        self.assertTrue(USER1 in vocab)
        self.assertTrue(user2 in vocab)

        self.assertFalse('something' in vocab)

        self.assertEqual(
            sorted([i.token for i in vocab]),
            [
                'custom-user1',
                'custom-user2',
                'test_user_1_',
            ])

        # raise Exception when creating term(str) for user that does not exists
        with self.assertRaises(Exception) as e:
            vocab.createTerm('nonexisting')
        self.assertEqual(
            e.exception.message,
            u"User with id 'nonexisting' does not exists.")

        # raise Exception when creating term from unknown object
        with self.assertRaises(Exception) as e:
            vocab.createTerm(object())
        self.assertEqual(
            e.exception.message,
            u"Term is something we can not recognize as a user.")

    def test_users_factory(self):
        portal = self.layer['portal']
        vocab = getUtility(IVocabularyFactory, name=u"uu.task.Users")
        vocab = vocab(portal, 'custom')

        self.assertEqual(len(vocab), 2)

        self.assertTrue(USER1 in vocab)
        self.assertTrue(USER2 in vocab)

    # TODO: add test that checks vocabulary can be access via json with Modify
    # content permission
