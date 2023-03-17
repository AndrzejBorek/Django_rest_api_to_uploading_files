from django.contrib.auth.models import User
from django.test import TestCase

from account_tier.models import AccountTier

from test import get_token, client, user_1_password, user_1_username


class UserTestCase(TestCase):
    def setUp(self):
        account_tier = AccountTier.objects.create(name="testAccountTier", thumbnail_sizes=[100], link_to_original=True,
                                                  expiring_links=True)
        user = User.objects.create_user(username=user_1_username, password=user_1_password)
        user_profile = user.user_profile
        user_profile.account_tier = account_tier
        user_profile.save()

    def test_check_if_user_has_been_created(self):
        assert User.objects.count() == 1

    def test_user_profile_associated_with_user(self):
        """Check if a user profile is associated with a user"""
        user = User.objects.first()
        user_profile = user.user_profile
        assert user_profile.account_tier
        assert user_profile.account_tier.link_to_original
        assert user_profile.account_tier.expiring_links

    def test_get_token_with_correct_credentials_should_return_ok(self):
        token = get_token(user_1_username, user_1_password)
        assert token

    def test_get_token_with_incorrect_credentials_should_return_unauthorized(self):
        token = get_token(user_1_username + "wrong", user_1_password)
        assert not token
