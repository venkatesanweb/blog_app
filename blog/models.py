from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType



#category

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)  
    content = models.TextField()  
    image_url = models.ImageField(null=True,upload_to="posts/image")
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=255, blank=True, db_index=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    is_published = models.BooleanField(default=False)

 


    def save(self, *args, **kwargs):
        if not self.slug:  # Generate slug only if it's not set
            self.slug = slugify(self.title)
            count = 1
            original_slug = self.slug
            while Post.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{count}"
                count += 1
        super().save(*args, **kwargs)
    @property
    def formatted_img_url(self):
        url = self.image_url if self.image_url.__str__().startswith(('http','https')) else self.image_url.url
        return url

    def __str__(self):
        return self.title
    

class aboutus(models.Model):
    content = models.TextField()
    



    

    

