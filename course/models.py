from django.db import models
from django.db.models import Model, TextField, CharField, IntegerField, \
    ForeignKey, CASCADE, DateField
from datetime import date
from humanize import naturalday

# Create your models here.


class Experience(Model):

    course_code = CharField(max_length=8)
    description = TextField()
    RATING_CHOICES = [
        (0, "Did not like the course"), (1, "Neutral"), (2, "Liked the course")
    ]
    rating = IntegerField(
        choices=RATING_CHOICES,
        help_text="2 if the student liked the course, 1 if the student "
                  "didn't like the course, 0 if they were neutral.",
        default=1
    )
    creation_date = DateField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.course_code} ({self.id}): {trim(self.description, 20)}"

    def readable_creation_date(self) -> str:
        return naturalday(self.creation_date).capitalize()


class Comment(Model):

    experience = ForeignKey(Experience, CASCADE)
    description = TextField()
    creation_date = DateField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.experience.course_code} ({self.id}): " \
               f"{trim(self.description, 20)}"

    def readable_creation_date(self) -> str:
        return naturalday(self.creation_date).capitalize()


def trim(text: str, num_chars: int) -> str:
    """
    Trims a string to the given length and adds an ellipsis if part of the
    string was cut off.

    Examples:
        >>> trim("Lorem ipsum", 8)
        "Lorem..."
        >>> trim("Hello", 8)
        "Hello"
    """
    if len(text) <= num_chars:
        return text
    else:
        return f"{text[:num_chars - 3]}..."
