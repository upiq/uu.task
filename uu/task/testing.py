from plone import api
from plone.app.testing import (
    PLONE_FIXTURE,
    PloneSandboxLayer,
    IntegrationTesting,
    FunctionalTesting,
)


USER1 = 'custom-user1'
USER2 = 'custom-user2'


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


UUTASK_FIXTURE = UUTaskFixture()
UUTASK_INTEGRATION_TESTING = IntegrationTesting(
    bases=(UUTASK_FIXTURE,), name="UUTaskFixture:Integration")
UUTASK_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(UUTASK_FIXTURE,), name="UUTaskFixture:Functional")
