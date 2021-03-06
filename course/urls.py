from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from .views import GetAllCourseView, CreateCourseView, DeleteCourseView, DetailCourseView, UpdateCourseView, CreateFeelingStudentModelView, GetCourseForLecturerAndAdminView, UploadVideosView, CheckDiscountView, activateCourseView, GetAllCourseTemporaryView, ChangeCourseTemporaryView

urlpatterns = [
    path('list-owner', GetCourseForLecturerAndAdminView.as_view(),
         name='list-course-for-admin'),
    path('upload-videos', UploadVideosView.as_view()),
    path('list', GetAllCourseView.as_view(), name='list-course'),
    path('create-feeling', CreateFeelingStudentModelView.as_view(),
         name='create-feeling'),
    url(r'^list/(?P<id>\d+)$',
        DetailCourseView.as_view(), name='detail-course'),
    path('create', CreateCourseView.as_view(), name='create-course'),
    url(r'^update/(?P<id>\d+)$', UpdateCourseView.as_view(), name='update-course'),
    url(r'^delete/(?P<id>\d+)$', DeleteCourseView.as_view(), name='delete-course'),
    path('check-discount', CheckDiscountView.as_view(), name='check-discount'),
    path('activate', activateCourseView.as_view(), name='check-activate-course'),
    path('list-temporary', GetAllCourseTemporaryView.as_view(),
         name='list-course-temporary'),
    # path('change-course-temporary', ChangeCourseTemporaryView.as_view(), name='list-course-temporary'),
    url(r'^update-temporary/(?P<id>\d+)$',
        ChangeCourseTemporaryView.as_view(), name='update-temporary-course'),
]
#  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
