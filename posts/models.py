from django.db import models

# Create your models here.
class Post(models.Model): 
    title = models.TextField(max_length=50)
    author = models.ForeignKey(
        'auth.User', 
         on_delete=models.CASCADE,
         null=True,
         )
    text = models.TextField()
    


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
    

