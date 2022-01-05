from rest_framework.routers import SimpleRouter

from .api_views import FactExamQuestionViewSet

router = SimpleRouter()
router.register(
    "fact-exam-question", FactExamQuestionViewSet, basename="fact-exam-question"
)

urlpatterns = router.urls
