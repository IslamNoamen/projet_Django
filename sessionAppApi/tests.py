from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class SessionApiJwtTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="apitester",
            password="SuperSecret123!"
        )
        self.session_list_url = reverse("session-list")
        self.token_url = reverse("token_obtain_pair")
        self.refresh_url = reverse("token_refresh")
        self.verify_url = reverse("token_verify")

    def test_session_list_requires_auth(self):
        response = self.client.get(self.session_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_obtain_access_and_use_on_session_endpoint(self):
        # obtain tokens
        token_response = self.client.post(
            self.token_url,
            {"username": "apitester", "password": "SuperSecret123!"}
        )
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        access = token_response.data["access"]
        refresh = token_response.data["refresh"]

        # refresh flow
        refresh_response = self.client.post(self.refresh_url, {"refresh": refresh})
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)

        # verify flow
        verify_response = self.client.post(self.verify_url, {"token": access})
        self.assertEqual(verify_response.status_code, status.HTTP_200_OK)

        # authenticated request
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        authed_response = self.client.get(self.session_list_url)
        self.assertNotEqual(authed_response.status_code, status.HTTP_401_UNAUTHORIZED)

        # clean header
        self.client.credentials()
