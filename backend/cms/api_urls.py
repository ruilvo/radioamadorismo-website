from rest_framework.routers import SimpleRouter

from .api_views import (
    FactPdfViewSet,
    FactAudioViewSet,
    FactImageViewSet,
    FactBlogPostViewSet,
)

router = SimpleRouter()
router.register("fact-pdf", FactPdfViewSet, basename="fact-pdf")
router.register("fact-audio", FactAudioViewSet, basename="fact-audio")
router.register("fact-image", FactImageViewSet, basename="fact-image")
router.register("fact-blog-post", FactBlogPostViewSet, basename="fact-blog-post")

urlpatterns = router.urls
