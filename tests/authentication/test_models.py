import pytest

from authentication.models import User

pytestmark = pytest.mark.django_db


def test_normal_user(normal_user: User) -> None:
    assert normal_user.is_staff is False
    assert str(normal_user) == "Jane Doe"
    assert normal_user.get_full_name() == "Jane Doe"
    assert normal_user.get_short_name() == "Jane"


def test_admin(admin: User) -> None:
    assert admin.is_staff is True


def test_create_admin_is_superuser_false(user_default_fields) -> None:
    user_default_fields["is_superuser"] = False
    with pytest.raises(ValueError, match="Superuser must have is_superuser=True."):
        User.objects.create_superuser(
            "user@example.com", "some-password", **user_default_fields
        )
