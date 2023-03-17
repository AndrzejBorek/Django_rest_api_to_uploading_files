import http

from django.contrib.auth.models import User
from django.test import TestCase

from test import get_token, client, user_1_username


class ImageTestCase(TestCase):

    def test_list_user_images_should_return_empty_list(self):
        client.force_authenticate(user=User.objects.get(username=user_1_username))
        response = client.get('/image/all')
        assert response.status_code == http.HTTPStatus.OK
        assert response.get('data') is None

    # TODO Create test for uploading file.
    #  For now : {'detail': ErrorDetail(string='Missing filename. Request should include a Content-Disposition header with a filename parameter.', code='parse_error')}
    # Might require changing upload_file method.
    # Since I did not create test for uploading image, image would be uploaded manually
    # Normally after uploading image, testUser should have image associated with him in database, however since
    # image was not uploaded in "normal" way there is no image in database.
