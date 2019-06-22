from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from . import views
urlpatterns=[
        url(r'^authorizations/$',obtain_jwt_token),
        url(r'^statistical/total_count/$',views.UserTotalCountView.as_view()),
        url(r'^statistical/day_increment/$',views.UserDayIncrementView.as_view()),
        url(r'^statistical/day_active/$',views.UserDayActiveView.as_view()),
        url(r'^statistical/day_orders/$',views.UserDayOrdersView.as_view()),

        ]