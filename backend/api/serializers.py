from rest_framework import serializers
from business.models import Location, FranchiseInquiry, ZeroInvestmentPartner, ContactMessage, LocationReview
from content.models import Blog, Video, Event, BlogCategory, BlogTag, EventImage, Article, VideoHeroSlide
from .models import HomeAboutImage, NetworkStat, CompanyCoreTab, FranchiseModelCard

# Business Serializers
class LocationReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationReview
        fields = ['id', 'name', 'rating', 'date_str', 'comment', 'created_at']

class LocationSerializer(serializers.ModelSerializer):
    facilities = serializers.SerializerMethodField()
    reviews = LocationReviewSerializer(many=True, read_only=True)
    avg_rating = serializers.ReadOnlyField()
    total_reviews = serializers.ReadOnlyField()

    class Meta:
        model = Location
        fields = '__all__'

    def get_facilities(self, obj):
        if obj.facilities:
            return [f.strip() for f in obj.facilities.split(',') if f.strip()]
        return []

class FranchiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FranchiseInquiry
        fields = '__all__'

class ZeroInvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZeroInvestmentPartner
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'

# Admin serializers (expose tracking fields, allow PATCH)
class FranchiseAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = FranchiseInquiry
        fields = [
            'id', 'full_name', 'email', 'phone', 'city', 'state',
            'investment_capacity', 'franchise_model', 'business_profile',
            'message', 'created_at',
            'status', 'assigned_to', 'response_note', 'responded_at',
        ]
        read_only_fields = [
            'id', 'full_name', 'email', 'phone', 'city', 'state',
            'investment_capacity', 'franchise_model', 'business_profile',
            'message', 'created_at',
        ]

class ZeroInvestmentAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZeroInvestmentPartner
        fields = [
            'id', 'full_name', 'email', 'phone', 'city', 'state',
            'land_size', 'land_unit', 'electricity_connection', 'address',
            'message', 'created_at',
            'status', 'assigned_to', 'response_note', 'responded_at',
        ]
        read_only_fields = [
            'id', 'full_name', 'email', 'phone', 'city', 'state',
            'land_size', 'land_unit', 'electricity_connection', 'address',
            'message', 'created_at',
        ]

class ContactAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = [
            'id', 'name', 'email', 'phone', 'city', 'state',
            'subject', 'message', 'created_at',
            'status', 'assigned_to', 'response_note', 'responded_at',
        ]
        read_only_fields = [
            'id', 'name', 'email', 'phone', 'city', 'state',
            'subject', 'message', 'created_at',
        ]

# Content Serializers
class BlogSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=BlogCategory.objects.all(),
        allow_null=True,
        required=False
    )

    class Meta:
        model = Blog
        fields = '__all__'

class BlogCategorySerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(read_only=True)

    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'count']

class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields = ['id', 'image']

class EventSerializer(serializers.ModelSerializer):
    images = EventImageSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'date', 'time', 'location', 'description', 'image', 'images', 'created_at']

class HomeAboutImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeAboutImage
        fields = '__all__'

class NetworkStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkStat
        fields = '__all__'

class CompanyCoreTabSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyCoreTab
        fields = ['id', 'tab_id', 'label', 'content', 'order']

class FranchiseModelCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = FranchiseModelCard
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class VideoHeroSlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoHeroSlide
        fields = '__all__'

