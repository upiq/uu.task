import types
import unittest2 as unittest

from plone import api
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

from uu.task.testing import (
    UUTASK_INTEGRATION_TESTING, USER1, USER2, GROUP1, GROUP2
)


class VocabularyTest(unittest.TestCase):

    layer = UUTASK_INTEGRATION_TESTING

    def test_user_and_groups_vocabulary(self):
        portal = self.layer['portal']
        vocab = getUtility(IVocabularyFactory, name=u"uu.task.UsersAndGroups")
        vocab = vocab(portal)

        user1 = api.user.get(username=USER1)
        user2 = api.user.get(username=USER2)
        group1 = api.group.get(groupname=GROUP1)
        group2 = api.group.get(groupname=GROUP2)

        self.assertTrue(isinstance(vocab._terms, types.GeneratorType))
        self.assertEqual(len(vocab), 9)

        self.assertTrue(isinstance(vocab._terms, list))
        self.assertEqual(len(vocab), 9)

        self.assertEqual(vocab.getTermByToken('user-' + USER1).value, user1)
        self.assertEqual(vocab.getTermByToken(user2).value, user2)
        self.assertEqual(vocab.getTermByToken('group-' + GROUP1).value, group1)
        self.assertEqual(vocab.getTermByToken(group2).value, group2)

        self.assertTrue('user-' + USER1 in vocab)
        self.assertTrue(user2 in vocab)
        self.assertTrue('group-' + GROUP1 in vocab)
        self.assertTrue(group2 in vocab)

        self.assertFalse('something' in vocab)

        self.assertEqual(
            sorted([i.token for i in vocab]),
            [
                'group-Administrators',
                'group-AuthenticatedUsers',
                'group-Reviewers',
                'group-Site Administrators',
                'group-group1',
                'group-group2',
                'user-test-user',
                'user-user1',
                'user-user2',
            ])

        # raise Exception when creating term(str) for user that does not exists
        with self.assertRaises(Exception) as e:
            vocab.createTerm('user-nonexisting')
        self.assertEqual(
            e.exception.message,
            u"User with username 'nonexisting' does not exists.")

        # raise Exception when creating term(str) for group that does not exists
        with self.assertRaises(Exception) as e:
            vocab.createTerm('group-nonexisting')
        self.assertEqual(
            e.exception.message,
            u"Group with groupname 'nonexisting' does not exists.")

        # raise Exception when creating term(str) that does not start
        # with 'user-' or 'group-'
        with self.assertRaises(Exception) as e:
            vocab.createTerm('something')
        self.assertEqual(
            e.exception.message,
            u"Term should start with `user-` or `group-` instead is "
            u"'something'.")

        # raise Exception when creating term from unknown object
        with self.assertRaises(Exception) as e:
            vocab.createTerm(object())
        self.assertEqual(
            e.exception.message,
            u"Term is something we can not recognize as a user or group.")

    def test_user_and_groups_vocabulary_factory(self):
        portal = self.layer['portal']
        vocab = getUtility(IVocabularyFactory, name=u"uu.task.UsersAndGroups")
        vocab = vocab(portal, '1')

        user1 = api.user.get(username=USER1)
        group1 = api.group.get(groupname=GROUP1)

        self.assertEqual(len(vocab), 2)

        self.assertEqual(vocab.getTermByToken('user-' + USER1).value, user1)
        self.assertEqual(vocab.getTermByToken('group-' + GROUP1).value, group1)


# TODO: add test
# check that vocabulary can be access via json with Modify content permission
