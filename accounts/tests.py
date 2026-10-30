from io import BytesIO
from tempfile import TemporaryDirectory

from PIL import Image

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.templatetags.static import static
from django.test import TestCase, override_settings
from django.urls import reverse


class ProfilePictureTests(TestCase):
    def setUp(self):
        media_root = self.enterContext(TemporaryDirectory())
        self.enterContext(override_settings(MEDIA_ROOT=media_root))
        self.user = get_user_model().objects.create_user(
            username="photo-test", password="test-password", role="jobseeker"
        )
        self.client.force_login(self.user)

    def picture_upload(self):
        image = BytesIO()
        Image.new("RGB", (16, 16), color="blue").save(image, format="PNG")
        return SimpleUploadedFile("portrait.png", image.getvalue(), "image/png")

    def test_upload_from_either_form_displays_on_all_profile_pages(self):
        for route, destination in (("profile", "profile"), ("edit_profile", "dashboard")):
            with self.subTest(upload_form=route):
                response = self.client.post(
                    reverse(route), {"profile_picture": self.picture_upload()}
                )
                self.assertRedirects(response, reverse(destination))

                self.user.profile.refresh_from_db()
                picture = self.user.profile.profile_picture
                self.assertTrue(picture.storage.exists(picture.name))
                with picture.open("rb") as saved_picture:
                    Image.open(saved_picture).verify()

                for page in ("profile", "edit_profile", "dashboard"):
                    with self.subTest(display_page=page):
                        self.assertContains(
                            self.client.get(reverse(page)), f'src="{picture.url}"'
                        )

    def test_saving_without_a_new_upload_preserves_existing_picture(self):
        self.user.profile.profile_picture = self.picture_upload()
        self.user.profile.save()
        original_name = self.user.profile.profile_picture.name

        for route in ("profile", "edit_profile"):
            with self.subTest(upload_form=route):
                response = self.client.post(reverse(route), {"phone": "1234567890"})
                self.assertEqual(response.status_code, 302)
                self.user.profile.refresh_from_db()
                self.assertEqual(self.user.profile.profile_picture.name, original_name)

    def test_invalid_upload_shows_an_error_on_both_forms(self):
        for route in ("profile", "edit_profile"):
            with self.subTest(upload_form=route):
                response = self.client.post(
                    reverse(route),
                    {"profile_picture": SimpleUploadedFile(
                        "invalid.png", b"not an image", "image/png"
                    )},
                )
                self.assertEqual(response.status_code, 200)
                errors = response.context["form"].errors["profile_picture"]
                self.assertContains(response, errors[0])
                self.user.profile.refresh_from_db()
                self.assertFalse(self.user.profile.profile_picture)

    def test_profile_forms_use_an_existing_default_avatar(self):
        for page in ("profile", "edit_profile"):
            with self.subTest(display_page=page):
                self.assertContains(
                    self.client.get(reverse(page)),
                    f'src="{static("img/default-user.png")}"',
                )
