from django.conf.urls import patterns

urlpatterns = patterns('announcements.views',
    (r'^criar$', 'new_announcement'),
    (r'^se-candidatar$', 'candidate_to_announcement'),
)