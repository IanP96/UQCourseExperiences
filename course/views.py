from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import *

# Create your views here.
# todo add favicon


def index_view(request):
    course_code = format_course_code(request.GET.get("course_code", ""))
    invalid = False
    context = {"course_code": course_code}
    if course_code:
        if valid_course_code(course_code):
            experiences = Experience.objects.filter(course_code=course_code)
            if experiences.exists():
                experience_data = {
                    experience: Comment.objects.filter(experience=experience)
                    for experience in experiences
                }
                satisfaction_rate = round(
                    sum(experiences.values_list("rating", flat=True))
                    / len(experiences) * 50
                )
                colour: str
                if satisfaction_rate > 75:
                    colour = "green"
                elif satisfaction_rate < 25:
                    colour = "red"
                else:
                    colour = "orange"
                context["num_experiences"] = len(experience_data)
                context["plural_s"] = pluralise(len(experience_data))
                context["experience_data"] = experience_data
                context["experience_data"] = experience_data
                context["satisfaction_rate"] = satisfaction_rate
                context["colour"] = colour
                return render(request, "experiences.html", context)
            else:
                return render(request, "no_experiences.html", context)
        else:
            invalid = True
    context["invalid"] = invalid
    return render(request, "index.html", context)


# todo delete this?
def experiences_view(request):
    # context = {"course_code": course_code}
    print("exp ---")
    print(request.GET)
    return render(request, "experiences.html")


def valid_course_code(course_code: str) -> bool:
    """
    Returns True if the given course code is valid (four letters followed by
    four digits), False otherwise.

    Args:
        course_code: The course code to check.
    """
    return len(course_code) == 8 and course_code[:4].isalpha() and \
        course_code[4:].isdigit()


def format_course_code(course_code: str) -> str:
    """
    Returns the given string with all letters capitalised and
    leading/trailing whitespace removed, suitable for course codes.
    Args:
        course_code: The string to format.
    """
    return course_code.strip().upper()


def pluralise(qty: int) -> str:
    return '' if qty == 1 else 's'


def add_experience_view(request):
    context = {
        "invalid_course_code": False, "invalid_description": False,
        "course_code": "", "description": ""
    }
    if request.method == "POST":
        # Form submitted
        course_code = format_course_code(request.POST["course_code"])
        description = request.POST["description"]
        rating = int(request.POST["rating"])
        invalid_course_code = not valid_course_code(course_code)
        invalid_description = len(description) < 2
        if invalid_course_code or invalid_description:
            # Invalid input
            context = {
                "invalid_course_code": invalid_course_code,
                "invalid_description": invalid_description,
                "course_code": course_code, "description": description
            }
            return render(request, "add_experience.html", context)
        else:
            # Valid input, create experience instance
            Experience(
                course_code=course_code, description=description, rating=rating
            ).save()
            return render(request, "success.html")
    else:
        return render(request, "add_experience.html")


def comment_view(request, experience_id):
    try:
        experience = Experience.objects.get(id=experience_id)
    except Experience.DoesNotExist:
        raise Http404("No experiences found that match the given id.")
    context = {
        "commented": False, "commenting": True, "experience": experience,
        "comments": Comment.objects.filter(experience=experience)
    }
    if request.method == "POST":
        # Form submitted
        description = request.POST.get("comment", "")
        if description:
            # Non-blank comment submitted
            Comment(experience=experience, description=description).save()
            context["commented"] = True
            context["commenting"] = False
    return render(request, "comment.html", context)
