from django.conf.urls import include, patterns, url
from django.contrib.auth import views as auth_views
from registration.backends.default.urls import urlpatterns
from users.views import RegistrationView
from users.forms import RegistrationForm

urlpatterns = patterns('',

    # Use our local email-as-username registration form.
    url(r'^register/$',
        RegistrationView.as_view(form_class=RegistrationForm),
        name='registration_register'
        ),

    # As of Jan 2014 django-registration's auth_urls are broken
    # for 1.6 (2.5 months after the release??). Override them.
    # Also, change template names from default to avoid conflict
    # with identical names in admin's templates.
    url(r'^password/change/$',
        auth_views.password_change,
        {'template_name': "registration/user_password_change.html"},
        name='password_change'),
    url(r'^password/change/done/$',
        auth_views.password_change_done,
        {'template_name': "registration/user_password_change_done.html"},
        name='password_change_done'),
    url(r'^password/reset/$',
        auth_views.password_reset,
        {'template_name': "registration/user_password_reset.html"},
        name='password_reset'),
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        {'template_name': "registration/user_password_reset_done.html"},
        name='password_reset_done'),
    url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        {'template_name': "registration/user_password_reset_complete.html"},
        name='password_reset_complete'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'template_name': "registration/user_password_reset_confirm.html"},
        name='password_reset_confirm'),

    # Default django-registration urls. URLs not already overridden are:
    # ^activate/complete/$ [name='registration_activation_complete']
    # ^activate/(?P<activation_key>\w+)/$ [name='registration_activate']
    # ^register/complete/$ [name='registration_complete']
    # ^register/closed/$ [name='registration_disallowed']
    # ^login/$ [name='auth_login']
    # ^logout/$ [name='auth_logout']
    url(r'', include('registration.backends.default.urls')),
)
