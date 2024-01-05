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
    creation_date = DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.course_code} ({self.id}): {trim(self.description, 20)}"

    def readable_creation_date(self) -> str:
        return pretty_date(self.creation_date)


class Comment(Model):

    experience = ForeignKey(Experience, CASCADE)
    description = TextField()
    creation_date = DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.experience.course_code} ({self.id}): " \
               f"{trim(self.description, 20)}"

    def readable_creation_date(self) -> str:
        return pretty_date(self.creation_date)


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


def pretty_date(date_to_format: date):
    """
    Get a date object and return a pretty string like 'yesterday',
    '3 months ago', 'today', etc.

    Source: https://stackoverflow.com/questions/1551382/user-friendly-time-format-in-python
    (slightly modified)
    """
    diff = date.today() - date_to_format
    day_diff = diff.days

    if day_diff <= 0:
        return "today"
    elif day_diff == 1:
        return "yesterday"
    elif day_diff < 7:
        return f"{str(day_diff)} days ago"
    elif day_diff < 31:
        return f"{str(round(day_diff / 7))} weeks ago"
    if day_diff < 365:
        return f"{str(round(day_diff / 30))} months ago"
    return f"{str(round(day_diff / 365))} years ago"
