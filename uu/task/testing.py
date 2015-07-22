from plone import api
from plone.app.testing import (
    PLONE_FIXTURE,
    PloneSandboxLayer,
    IntegrationTesting,
    FunctionalTesting,
)


USER1 = 'user1'
USER2 = 'user2'
GROUP1 = 'group1'
GROUP2 = 'group2'


class UUTaskFixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import uu.task
        self.loadZCML(package=uu.task)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'uu.task:default')

        for username in [USER1, USER2]:
            api.user.create(
                username=username,
                email="test@example.com",
                properties=dict(fullname=username),
            )

        for groupname, username in [(GROUP1, USER1), (GROUP2, USER2)]:
            api.group.create(groupname=groupname, title=groupname)
            api.group.add_user(groupname=groupname, username=username)


UUTASK_FIXTURE = UUTaskFixture()
UUTASK_INTEGRATION_TESTING = IntegrationTesting(
    bases=(UUTASK_FIXTURE,), name="UUTaskFixture:Integration")
UUTASK_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(UUTASK_FIXTURE,), name="UUTaskFixture:Functional")
