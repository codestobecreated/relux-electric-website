from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LocationViewSet, FranchiseViewSet,
    ZeroInvestmentViewSet, ContactViewSet,
    BlogViewSet, BlogCategoryViewSet, BlogTagViewSet,
    VideoViewSet, EventViewSet,
    HomeAboutImageViewSet, NetworkStatViewSet,
    CompanyCoreTabViewSet, FranchiseModelCardViewSet,
    ArticleViewSet, VideoHeroSlideViewSet,
    FranchiseAdminViewSet, ZeroInvestmentAdminViewSet, ContactAdminViewSet,
    admin_stats_view,
)

router = DefaultRouter()
router.register(r'locations', LocationViewSet)
router.register(r'franchise', FranchiseViewSet)
router.register(r'zero-investment', ZeroInvestmentViewSet)
router.register(r'contact', ContactViewSet)
router.register(r'blogs', BlogViewSet)
router.register(r'blog-categories', BlogCategoryViewSet, basename='blogcategory')
router.register(r'blog-tags', BlogTagViewSet, basename='blogtag')
router.register(r'videos', VideoViewSet)
router.register(r'events', EventViewSet)
router.register(r'home-about-images', HomeAboutImageViewSet, basename='homeaboutimage')
router.register(r'network-stats', NetworkStatViewSet, basename='networkstat')
router.register(r'company-core-tabs', CompanyCoreTabViewSet, basename='companycoretab')
router.register(r'franchise-model-cards', FranchiseModelCardViewSet, basename='franchisemodelcard')
router.register(r'articles', ArticleViewSet)
router.register(r'video-hero-slides', VideoHeroSlideViewSet, basename='videoheroslide')

# Admin Panel routes registered on the same router
router.register(r'admin/franchise', FranchiseAdminViewSet, basename='admin-franchise')
router.register(r'admin/zero-investment', ZeroInvestmentAdminViewSet, basename='admin-zero-investment')
router.register(r'admin/contact', ContactAdminViewSet, basename='admin-contact')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/stats/', admin_stats_view, name='admin-stats'),
]
