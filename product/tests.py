from django.test import TestCase
from .Calculator import Calculator
from .models import Product, Category
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
# Create your tests here.

class CalculatorTest(TestCase):
    def setUp(self):
        self.c=Calculator()
    def test_add(self):
        self.assertEqual(self.c.add(12,10),22)
        self.assertEqual(self.c.add(5,5),10)
        
    def test_sub(self):
        self.assertEqual(self.c.subtract(10,2),8)
        self.assertEqual(self.c.subtract(5,5),0)

    def test_isEven(self):
        self.assertTrue(self.c.is_even(4))
        self.assertFalse(self.c.is_even(5))
        with self.assertRaises(TypeError):
            self.c.is_even('A')

    def test_isOdd(self):
        self.assertTrue(self.c.is_odd(7))
        self.assertFalse(self.c.is_odd(6))

    def test_factorial(self):
        self.assertEqual(self.c.factorial(1),1)
        self.assertEqual(self.c.factorial(2),2)
        self.assertEqual(self.c.factorial(3),6)

        with self.assertRaises(TypeError):
            self.c.factorial('A')

        with self.assertRaises(ValueError):
            self.c.factorial(-1)

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(product_name='test_product',
                               product_description = 'test_description',
                               product_price = 12000,
                               product_brand = 'test_brand')
        
    def test_create_product(self):
        self.assertIsNotNone(self.product)
        self.assertEqual(self.product.product_name,'test_product')
        self.assertEqual(self.product.product_description,'test_description')
        self.assertEqual(self.product.product_price,12000)
        self.assertEqual(self.product.product_brand,'test_brand')

    def test_without_brand(self):
        product = Product.objects.create(product_name='test_product',
                               product_description = 'test_description',
                               product_price = 12000)
        self.assertEqual(product.product_brand,'superpet')

    def test_delete_product(self):
        count = Product.objects.count()
        self.product.delete()

        count_after = Product.objects.count()

        self.assertEqual(count_after,count-1)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    def test_update_product(self):
        self.product.product_name = 'Test Product Updated'
        self.product.save()
        self.assertEqual(Product.objects.get(id=self.product.id).product_name,'Test Product Updated')
        

    def test_get_product_by_id(self):
        product = Product.objects.get(id=self.product.id)
        self.assertEqual(product.id,self.product.id)
        self.assertEqual(product.product_name,'test_product')


class IntegrationTest(TestCase):

    def test_about(self):
        url = reverse('about')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('about.html')
        
    def test_not_found(self):
        response = self.client.get('/notfound/')
        self.assertEqual(response.status_code,404)

    def test_contact(self):
        url = reverse('contact')
        response = self.client.post(url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('contact.html')

    class ProductIntegrationTest(TestCase):
        def setUp(self):
            self.category = Category.objects.create(category_name='test_category')
            uploadedfile=SimpleUploadedFile(
                name='test_image',
                content=b'Test image for products',
                content_type='img/jpeg'
            )
            self.product = Product.objects.create(
                product_name='test product',
                product_description='test_description',
                product_price=12000,
                product_brand='superpet',
                product_image=uploadedfile,
                product_category=self.category
            )

        def test_product_list(self):
            url=reverse('products')
            response=self.client.get(url)
            self.assertEqual(response.status_code,200)
            self.assertTemplateUsed('products.html')
            self.assertContains(response,"test product")
            self.assertContains(response,"test_description")

        def test_product_detail(self):
            url=reverse('product_detail',args=[self.product.id])
            response=self.client.get(url)
            self.assertEqual(response.status_code,200)
            self.assertTemplateUsed('product_detail.html')
            self.assertContains(response,"test product")

        def test_product_not_exist(self):
            url=reverse('product_detail',args=[30])
            response=self.client.get(url)
            self.assertEqual(response.status_code,404)

        def test_logout(self):
            url=reverse('logout')
            response=self.client.get(url)
            self.assertEqual(response.status_code,302)