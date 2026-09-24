__author__ = 'lizexiong'



from django import forms


from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
)

from django.contrib.auth.models import Group,Permission

from django.db.models import Q


from .models import Department,User


def allowed_permission_queryset():
    return(
        Permission.objects.filter(
            Q(
                content_type__app_label="accounts",
                content_type__model__in=['user','department']
            )

            | Q(
                content_type__app_label='auth',
                content_type__model="group"
            )

            | Q(
                content_type__app_label="auth",
                content_type__model="permission",
                codename="view_permission",
            )
        )

        .select_related("content_type")

        .order_by(
            "content_type__app_label",
            "content_type__model",
            "codename"
        )

    )


