from django.test import TestCase
from .models import CustomUser, Coordinates, Level, Pass, Image
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile

# >> TEST MODELS <<
class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass',
            fam='Фамилия',
            name='Имя',
            otc='Отчество',
            phone='1234567890'
        )

    def test_user_creation(self):
        self.assertIsInstance(self.user, CustomUser)
        self.assertEqual(self.user.email, 'testuser@example.com')

class CoordinatesModelTest(TestCase):
    def setUp(self):
        self.coordinates = Coordinates.objects.create(
            latitude=10.0,
            longitude=20.0,
            height=3000.0
        )

    def test_coordinates_creation(self):
        self.assertIsInstance(self.coordinates, Coordinates)
        self.assertEqual(self.coordinates.latitude, 10.0)

class LevelModelTest(TestCase):
    def setUp(self):
        self.level = Level.objects.create(
            winter='1A',
            summer='1A'
        )

    def test_level_creation(self):
        self.assertIsInstance(self.level, Level)
        self.assertEqual(self.level.winter, '1A')

class PassModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.coordinates = Coordinates.objects.create(
            latitude=10.0,
            longitude=20.0,
            height=3000.0
        )
        self.level = Level.objects.create(
            winter='1A',
            summer='1A'
        )
        self.pass_instance = Pass.objects.create(
            title='Перевал 1',
            beauty_title='Перевал',
            user=self.user,
            coords=self.coordinates,
            level=self.level
        )

    def test_pass_creation(self):
        self.assertIsInstance(self.pass_instance, Pass)
        self.assertEqual(self.pass_instance.title, 'Перевал 1')

class ImageModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.coordinates = Coordinates.objects.create(
            latitude=10.0,
            longitude=20.0,
            height=3000.0
        )
        self.level = Level.objects.create(
            winter='1А',
            summer='1А'
        )
        self.pass_instance = Pass.objects.create(
            title='Перевал 1',
            beauty_title='Перевал',
            user=self.user,
            coords=self.coordinates,
            level=self.level
        )
        self.image = Image.objects.create(
            data='path/to/image.jpg',
            title='Тестовое изображение',
            pass_reference=self.pass_instance
        )

    def test_image_creation(self):
        self.assertIsInstance(self.image, Image)
        self.assertEqual(self.image.title, 'Тестовое изображение')


# >> TEST API <<
image_data = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")

class PassAPITest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.coordinates = Coordinates.objects.create(
            latitude=10.0,
            longitude=20.0,
            height=3000.0
        )
        self.level = Level.objects.create(
            winter='1А',
            summer='1А'
        )
        self.pass_data = {
        'title': 'Перевал 1',
        'beauty_title': 'Перевал',
        'other_titles': 'Другое название перевала',
        'connect': 'Связанный текст',
        'user': {
            'username': 'testuser',
            'email': 'testuser4@example.com',
            'password': 'testpass',
            'fam': 'Фамилия',
            'name': 'Имя',
            'otc': 'Отчество',
            'phone': '1234567890',
        },
        'coords': { 
            'latitude': 10.0,
            'longitude': 20.0,
            'height': 3000.0
        },
        'level': { 
            'winter': 'Средний',
            'summer': 'Легкий'
        },
        'images': [{
                    'data': image_data,
                    'title': 'Тестовое изображение'
                }]
}

    def test_create_and_get_pass(self):
        # Создать перевал
        response = self.client.post(reverse('submit_data'), self.pass_data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)

        created_pass_id = response.data['id']

        # Получить перевал по ID
        response = self.client.get(reverse('get_pass_by_id', args=[created_pass_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.pass_data['title'])
        self.assertEqual(response.data['beauty_title'], self.pass_data['beauty_title'])