from django.db import models


# Create your models here.
class Post(models.Model): 
    CATEGORY_CHOICES = [
        ('tech', 'Technology & innovation'),
        ('fashion', 'design & fashion'),
        ('food', 'food & cooking'),
        ('creativity', 'creative corner'),
        ('inpiration', 'inspirational boards'),
        ('myspace', 'personal gist'),
        ('other', 'others'),
    ]
    title = models.CharField(max_length=50)
    author = models.ForeignKey(
        'auth.User', 
         on_delete=models.CASCADE,
         null=True,
         )
    text = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    created_at = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)    
    

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(
        'auth.User', 
         on_delete=models.CASCADE,
         null=True,
        )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.content[:20]}'
    

