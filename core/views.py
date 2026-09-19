from django.http import Http404
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage

from .data import RESOURCES
from .forms import (
    FeedbackForm,
    ProfileImageForm,
    SimpleLoginForm,
)

VALID_THEMES = {"light", "dark"}


def get_theme(request):
    theme = request.COOKIES.get("theme", "light")

    if theme not in VALID_THEMES:
        theme = "light"

    return theme


def find_resource(resource_id):
    return next(
        (
            item
            for item in RESOURCES
            if item["id"] == resource_id
        ),
        None,
    )


def home(request):
    context = {
        "theme": get_theme(request),
    }

    return render(
        request,
        "core/home.html",
        context,
    )


def resource_list(request):
    favorite_ids = request.session.get(
        "favorites",
        [],
    )

    context = {
        "resources": RESOURCES,
        "favorite_ids": favorite_ids,
        "theme": get_theme(request),
    }

    return render(
        request,
        "core/resource_list.html",
        context,
    )


def resource_detail(request, id):
    resource = find_resource(id)

    if resource is None:
        raise Http404("Resource not found")

    selected_tab = request.GET.get(
        "tab",
        "overview",
    )

    if selected_tab not in {"overview", "details"}:
        selected_tab = "overview"

    favorite_ids = request.session.get(
        "favorites",
        [],
    )

    context = {
        "resource": resource,
        "selected_tab": selected_tab,
        "is_favorite": id in favorite_ids,
        "theme": get_theme(request),
    }

    return render(
        request,
        "core/resource_detail.html",
        context,
    )


def favorites(request):
    favorite_ids = request.session.get(
        "favorites",
        [],
    )

    favorite_resources = [
        resource
        for resource in RESOURCES
        if resource["id"] in favorite_ids
    ]

    context = {
        "favorite_resources": favorite_resources,
        "theme": get_theme(request),
    }

    return render(
        request,
        "core/favorites.html",
        context,
    )


@require_POST
def add_favorite(request, id):
    resource = find_resource(id)

    if resource is None:
        raise Http404("Resource not found")

    favorite_ids = request.session.get(
        "favorites",
        [],
    )

    if id not in favorite_ids:
        favorite_ids.append(id)
        request.session["favorites"] = favorite_ids

    return redirect(
        "core:resource_detail",
        id=id,
    )


@require_POST
def remove_favorite(request, id):
    resource = find_resource(id)

    if resource is None:
        raise Http404("Resource not found")

    favorite_ids = request.session.get(
        "favorites",
        [],
    )

    if id in favorite_ids:
        favorite_ids.remove(id)
        request.session["favorites"] = favorite_ids

    return redirect("core:favorites")


def preferences(request):
    current_theme = get_theme(request)

    if request.method == "POST":
        selected_theme = request.POST.get(
            "theme",
            "light",
        )

        if selected_theme not in VALID_THEMES:
            selected_theme = "light"

        response = redirect("core:preferences")

        response.set_cookie(
            key="theme",
            value=selected_theme,
            max_age=60 * 60 * 24 * 30,
            samesite="Lax",
        )

        return response

    context = {
        "theme": current_theme,
    }

    return render(
        request,
        "core/preferences.html",
        context,
    )

def feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data

            request.session["feedback_name"] = (
                cleaned_data["name"]
            )

            return redirect(
                "core:feedback_thanks"
            )

    else:
        form = FeedbackForm()

    context = {
        "form": form,
        "theme": get_theme(request),
    }

    return render(
        request,
        "core/feedback.html",
        context,
    )


def feedback_thanks(request):
    feedback_name = request.session.get(
        "feedback_name",
        "Learner",
    )

    context = {
        "feedback_name": feedback_name,
        "theme": get_theme(request),
    }

    return render(
        request,
        "core/feedback_thanks.html",
        context,
    )
def simple_login(request):
    if request.method == "POST":
        form = SimpleLoginForm(request.POST)

        if form.is_valid():
            request.session["user_name"] = (
                form.cleaned_data["display_name"]
            )

            return redirect("core:profile")

    else:
        form = SimpleLoginForm()

    context = {
        "form": form,
        "theme": get_theme(request),
    }

    return render(
        request,
        "core/login.html",
        context,
    )


def profile(request):
    user_name = request.session.get("user_name")

    if not user_name:
        return redirect("core:login")

    if request.method == "POST":
        form = ProfileImageForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            uploaded_image = (
                form.cleaned_data["profile_image"]
            )

            saved_path = default_storage.save(
                f"profile_images/{uploaded_image.name}",
                uploaded_image,
            )

            request.session["profile_image_path"] = (
                saved_path
            )

            return redirect("core:profile")

    else:
        form = ProfileImageForm()

    image_path = request.session.get(
        "profile_image_path"
    )

    if image_path:
        profile_image_url = default_storage.url(
            image_path
        )
    else:
        profile_image_url = None

    context = {
        "form": form,
        "user_name": user_name,
        "profile_image_url": profile_image_url,
        "theme": get_theme(request),
    }

    return render(
        request,
        "core/profile.html",
        context,
    )

def custom_404(request, exception):
    return render(request, "404.html", status=404)