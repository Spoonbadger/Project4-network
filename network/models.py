from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('self', blank=True, symmetrical=False, related_name="followers")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "following_count": self.following.count(),
            "followers_count": self.followers.count(),
        }
    
    def __str__(self):
        return f"User: {self.username} email:{self.email} user_id: {self.id}"


class Post(models.Model):
    sender = models.ForeignKey('User', on_delete=models.CASCADE, related_name="sender_posts")
    post_content = models.CharField(max_length=280)
    # like_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    edited_timestamp = models.DateTimeField(blank=True, null=True)

    @property
    def like_count(self):
        return self.post_likes.count()

    def serialize(self):
        return {
            "id": self.id,
            "sender": self.sender.username,
            "sender_id": self.sender.id,
            "post_content": self.post_content,
            "like_count": self.like_count,
            "timestamp": self.timestamp.strftime("%d %b, %Y at %H:%M"),
            "edited_timestamp": self.edited_timestamp.strftime("%d %b, %Y at %H:%M") if self.edited_timestamp else "Not edited",
        }
    
    def is_valid_post(self):
        if not self.post_content or not self.sender:
            return False
        return True
    
    def __str__(self):
        return f"'{self.sender.username}' posted: {self.post_content} Date Posted: {self.timestamp.strftime('%A, %b %d, %Y at %H:%M:%S')}"
    

class Like(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="user_likes")
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="post_likes")
    timestamp = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user.username} likes: "{self.post.post_content}" by {self.post.sender.username} - {self.timestamp.strftime('%A, %b %d, %Y at %H:%M:%S')}'
