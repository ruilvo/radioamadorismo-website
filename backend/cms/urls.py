from rest_framework.routers import SimpleRouter

from .views import FactImageViewSet, FactBlogPostViewSet

router = SimpleRouter()
router.register("fact-image", FactImageViewSet, basename="fact-image")
router.register("fact-blog-post", FactBlogPostViewSet, basename="fact-blog-post")

urlpatterns = router.urls
