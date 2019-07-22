from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from voluntariapp.models import Event, CustomUser


class TestEventView(APITestCase):
    def setUp(self):
        self.name='elena'
        self.user_1 = CustomUser(name=self.name, surname='izquierdo')
        self.user_1.save()
        self.event_1 = Event(name='name',creator=self.user_1 )
        self.event_1.save()
        self.event_1_id = Event.objects.all().first().id

    def test_update_event_returns_ok(self):

        new_name='Gisela'
        body={'name':new_name}
        response = self.client.patch('/event/1', body, format = 'json')
        updated_event = Event.objects.filter(id=self.event_1_id).first()
        self.assertEqual(response.status, status.HTTP_200_OK)
        self.assertEqual(updated_event.name, new_name)

