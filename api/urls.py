from django.urls import path, include

from api.views import CourseCreateAPIView, ReviewCreateAPIView, CourseApiViewSet

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'courses', CourseApiViewSet)

urlpatterns = [
    path('courses/create/', CourseCreateAPIView.as_view()),
    path('courses/<int:course_pk>/reviews/create/', ReviewCreateAPIView.as_view()),
    path('', include(router.urls))
]