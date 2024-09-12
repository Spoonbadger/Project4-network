from django.test import TestCase, Client

# Create your tests here.
from .models import Post, Like, User

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import pathlib
# import os

# def file_uri(filename):
#    return pathlib.Path(os.path.abspath(filename)).as_uri()

# driver = webdriver.Chrome()


# Check each view, check each webpage loads, check webpages if logged in or logged out...
# all from default: import unitest

# Could improve testing with: 
# Add More Edge Cases: 
# Consider testing scenarios like trying to create a post without being logged in, or handling invalid data.
# And Test Post Limits: 
# Check if there are limits on the number of posts that can be retrieved or displayed.


#class WebPageTests(TestCase):

 #   def test_like(self):
  #      driver.get(file_uri('/'))
   #     page_title = driver.find_element(By.ID, 'all-posts-title')
    #    self.assertEqual(page_title.text, 'Squeeker')


class PostTestCase(TestCase):

    def setUp(self):
        # Set up users, tweets, and a logged in user
        self.user1 = User.objects.create(username="Darcy")
        self.user1.set_password('hello')
        self.user1.save()
        self.user2 = User.objects.create(username="Bingley")
        self.user2.set_password('hello')
        self.user2.save()
        self.user3 = User.objects.create(username="Wickham")
        self.user3.set_password('hello')
        self.user3.save()

        self.post1 = Post.objects.create(post_content="The Pride or the Prejudice", sender=self.user1)
        self.post2 = Post.objects.create(post_content="A skip and a hop and here we go", sender=self.user2)
        self.post3 = Post.objects.create(post_content="No thanks, Lizzy", sender=self.user3)

        self.client = Client()


    def test_user_created(self):
        self.assertEqual(self.user1.username, 'Darcy')

    
    def test_post_create(self):
        post_obj = Post.objects.create(post_content="The distinction of rank presevered.", sender=self.user1)
        self.assertTrue(post_obj.is_valid_post())
        self.assertEqual(post_obj.id, 4)
        self.assertEqual(post_obj.sender, self.user1)


    def test_user_login(self):
        login = self.client.login(username='Darcy', password='hello')
        self.assertTrue(login)

    
    def test_all_posts(self):
        self.client.login(username='Darcy', password='hello')
        response = self.client.get('/all_posts/')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        posts = response_data.get('posts', [])
        self.assertEqual(len(posts), 3)


    def test_delete_account(self):
        self.assertEqual(len(User.objects.all()), 3)
        test_user = User.objects.create(username='test1')
        test_user.set_password('hello')
        test_user.save()
        self.assertEqual(len(User.objects.all()), 4)
        test_user.delete()
        self.assertFalse(User.objects.filter(username='test1').exists())
        self.assertEqual(len(User.objects.all()), 3)

    
    def test_delete_squeek(self):
        test_squeek = Post.objects.create(post_content="THIS IS A TEST, OK?", sender=self.user1)
        test_squeek.save()
        self.assertEqual(len(Post.objects.filter(sender=self.user1)), 2)
        test_squeek.delete()
        self.assertEqual(len(Post.objects.filter(sender=self.user1)), 1)


    def test_following_posts_data(self):
        self.client.login(username='Darcy', password='hello')
        self.user1.following.add(self.user2)

        response = self.client.get('/api/following_posts/')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        posts = response_data.get('posts', [])
        
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]['post_content'], 'A skip and a hop and here we go')


    def test_follow_unfollow(self):
        self.user1.following.add(self.user2)
        self.user1.following.add(self.user3)
        self.assertEqual(self.user1.following.count(), 2)

        self.user1.following.remove(self.user3)
        self.assertEqual(self.user1.following.count(), 1)


    def test_like_unlike(self):
        Like.objects.create(user=self.user1, post=self.post1)
        self.assertEqual(len(Like.objects.all()), 1)
        Like.objects.create(user=self.user2, post=self.post1)
        Like.objects.create(user=self.user3, post=self.post2)
        self.assertEqual(len(Like.objects.filter(post=self.post1)), 2)

        do_not_like_anymore = Like.objects.filter(user=self.user1)
        do_not_like_anymore.delete()
        self.assertEqual(len(Like.objects.filter(post=self.post1)), 1)



    def test_new_post(self):
        self.client.login(username='Darcy', password='hello')
        Post.objects.create(post_content="Everyone is rubbish", sender=self.user1)
        self.assertEqual(len(Post.objects.all()), 4)

    def test_invalid_new_post(self):
        invalid_post = Post.objects.create(post_content="", sender=self.user3)
        self.assertFalse(invalid_post.is_valid_post())
        invalid_post = Post.objects.create(post_content="Hiya", sender=self.user1)
        self.assertTrue(invalid_post.is_valid_post())


    def test_edit_post(self):
        post_to_edit = Post.objects.get(id=1)
        post_to_edit.post_content = "Pride and Prejudice"
        post_to_edit.save()

        post_to_edit.refresh_from_db()
        self.assertEqual(post_to_edit.post_content, "Pride and Prejudice")


    def test_profile_data(self):
        self.client.login(username='Darcy', password='hello')
        id = self.user1.id

        response = self.client.get(f'/api/profile/{id}/')
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertEqual(response_data.get('profile_username'), 'Darcy')


    def test_index_not_logged_in(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

    
    




