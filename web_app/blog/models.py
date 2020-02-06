from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    highlighted = models.TextField(default="")

    def __str__(self):
        return self.title


"""
highlighted = models.TextField(default="") is the solution when an error regarding 
django.db.utils.OperationalError: no such column: blog_post.author_id is found as it assign 
defualt none value for any important text field to empty string instead of None.

https://stackoverflow.com/questions/26312219/operationalerror-no-such-column-django

As you went through the tutorial you must have come across the section on migration, as this was one of the major changes in Django 1.7

Prior to Django 1.7, the syncdb command never made any change that had a chance to destroy data currently in the database. This meant that if you did syncdb for a model, then added a new row to the model (a new column, effectively), syncdb would not affect that change in the database.

So either you dropped that table by hand and then ran syncdb again (to recreate it from scratch, losing any data), or you manually entered the correct statements at the database to add only that column.

Then a project came along called south which implemented migrations. This meant that there was a way to migrate forward (and reverse, undo) any changes to the database and preserve the integrity of data.

In Django 1.7, the functionality of south was integrated directly into Django. When working with migrations, the process is a bit different.

Make changes to models.py (as normal).
Create a migration. This generates code to go from the current state to the next state of your model. This is done with the makemigrations command. This command is smart enough to detect what has changed and will create a script to effect that change to your database.
Next, you apply that migration with migrate. This command applies all migrations in order.
So your normal syncdb is now a two-step process, python manage.py makemigrations followed by python manage.py migrate.

Now, on to your specific problem:

class Snippet(models.Model):
    owner = models.ForeignKey('auth.User', related_name='snippets')
    highlighted = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES,
                                            default='python',
                                            max_length=100)
    style = models.CharField(choices=STYLE_CHOICES,
                                     default='friendly',
                                     max_length=100)
In this model, you have two fields highlighted and code that is required (they cannot be null).

Had you added these fields from the start, there wouldn't be a problem because the table has no existing rows?

However, if the table has already been created and you add a field that cannot be null, you have to define a default value to provide for any existing rows - otherwise, the database will not accept your changes because they would violate the data integrity constraints.

This is what the command is prompting you about. You can tell Django to apply a default during migration, or you can give it a "blank" default highlighted = models.TextField(default='') in the model itself.

"""

