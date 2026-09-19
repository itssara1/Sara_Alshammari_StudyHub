from django import forms

class SimpleLoginForm(forms.Form):
    display_name = forms.CharField(
        label="Display Name",
        min_length=2,
        max_length=50,
        error_messages={
            "required": "Please enter your name.",
            "min_length": (
                "Your name must contain at least 2 characters."
            ),
            "max_length": (
                "Your name cannot exceed 50 characters."
            ),
        },
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your name",
                "autocomplete": "name",
            }
        ),
    )


class ProfileImageForm(forms.Form):
    profile_image = forms.ImageField(
        label="Profile Image",
        error_messages={
            "required": "Please choose a profile image.",
            "invalid_image": (
                "Please upload a valid image file."
            ),
        },
        widget=forms.FileInput(
            attrs={
                "accept": "image/*",
            }
        ),
    )

    def clean_profile_image(self):
        image = self.cleaned_data["profile_image"]

        maximum_size = 2 * 1024 * 1024

        if image.size > maximum_size:
            raise forms.ValidationError(
                "The profile image must be smaller than 2 MB."
            )

        return image
    
class FeedbackForm(forms.Form):
    RATING_CHOICES = [
        ("", "Select a rating (optional)"),
        ("5", "5 - Excellent"),
        ("4", "4 - Very Good"),
        ("3", "3 - Good"),
        ("2", "2 - Fair"),
        ("1", "1 - Poor"),
    ]

    name = forms.CharField(
        label="Your Name",
        min_length=2,
        max_length=100,
        error_messages={
            "required": "Please enter your name.",
            "min_length": (
                "Your name must contain at least 2 characters."
            ),
            "max_length": (
                "Your name cannot exceed 100 characters."
            ),
        },
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your name",
                "autocomplete": "name",
            }
        ),
    )

    email = forms.EmailField(
        label="Email Address",
        error_messages={
            "required": "Please enter your email address.",
            "invalid": "Please enter a valid email address.",
        },
        widget=forms.EmailInput(
            attrs={
                "placeholder": "name@example.com",
                "autocomplete": "email",
            }
        ),
    )

    message = forms.CharField(
        label="Your Message",
        error_messages={
            "required": "Please enter your feedback message.",
        },
        widget=forms.Textarea(
            attrs={
                "placeholder": (
                    "Tell us about your StudyHub experience..."
                ),
                "rows": 6,
            }
        ),
    )

    rating = forms.ChoiceField(
        label="Rating",
        choices=RATING_CHOICES,
        required=False,
        widget=forms.Select(),
    )

    def clean_message(self):
        message = self.cleaned_data["message"].strip()

        if len(message) < 20:
            raise forms.ValidationError(
                "Your message must contain at least 20 characters."
            )

        return message