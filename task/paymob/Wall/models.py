from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Wall(models.Model):
    author = models.ForeignKey(User , null =True ,on_delete=models.CASCADE)
    image  = models.ImageField(upload_to='image/' , null=True ,blank=True)
    title  = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(unique=True)
    timestap = models.DateTimeField(auto_now_add=True ,null=True)
    updated_data = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering =['-timestap']

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Wall.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
