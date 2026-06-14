from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from business.models import Location, FranchiseInquiry, ZeroInvestmentPartner, ContactMessage
from content.models import Blog, Video, Event, BlogCategory, BlogTag, Article, VideoHeroSlide
from .models import HomeAboutImage, NetworkStat, CompanyCoreTab, FranchiseModelCard
from .serializers import (
    LocationSerializer, FranchiseSerializer,
    ZeroInvestmentSerializer, ContactSerializer,
    BlogSerializer, BlogCategorySerializer, BlogTagSerializer,
    VideoSerializer, EventSerializer,
    HomeAboutImageSerializer, NetworkStatSerializer,
    CompanyCoreTabSerializer, FranchiseModelCardSerializer,
    ArticleSerializer, VideoHeroSlideSerializer,
    FranchiseAdminSerializer, ZeroInvestmentAdminSerializer, ContactAdminSerializer,
)

ADMIN_TOKENS = ["relux@admin2025", "Reluxgroups@2024"]

def check_admin_token(request):
    token = request.headers.get("X-Admin-Token", "")
    return token in ADMIN_TOKENS

# Email helpers
def get_recipient_list():
    if isinstance(settings.ADMIN_TO, list):
        return settings.ADMIN_TO
    return [settings.ADMIN_TO]

def _build_html_email(title, rows, accent_color="#00b14f"):
    """Build a premium branded HTML email with Relux Electric logo and green design."""
    rows_html = ""
    for i, (label, value) in enumerate(rows):
        bg = "#fafafa" if i % 2 == 0 else "#ffffff"
        rows_html += f"""
        <tr style="background:{bg};">
          <td style="padding:13px 28px;font-family:'Segoe UI',Arial,sans-serif;font-size:13px;
                     font-weight:700;color:#1a1a1a;width:180px;vertical-align:top;
                     border-bottom:1px solid #f0f0f0;">{label}</td>
          <td style="padding:13px 28px;font-family:'Segoe UI',Arial,sans-serif;font-size:13px;
                     color:#444;vertical-align:top;border-bottom:1px solid #f0f0f0;">{value}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>{title}</title>
</head>
<body style="margin:0;padding:0;background:#f0f2f5;font-family:'Segoe UI',Arial,sans-serif;">
  <table cellpadding="0" cellspacing="0" width="100%" style="background:#f0f2f5;padding:32px 0;">
    <tr>
      <td align="center">
        <table cellpadding="0" cellspacing="0" width="620" style="max-width:620px;width:100%;">

          <!-- ── HEADER ── -->
          <tr>
            <td style="background:linear-gradient(135deg,#0a0a0a 0%,#1a1a1a 60%,#002b14 100%);
                       border-radius:16px 16px 0 0;padding:32px 36px 24px;text-align:center;">
              <!-- Logo -->
              <img src="https://reluxelectric.com/relux-electric-india-logo.svg"
                   alt="Relux Electric"
                   width="180" height="45"
                   style="display:block;margin:0 auto 20px;height:45px;width:auto;"
              />
              <!-- Green divider line -->
              <div style="height:2px;background:linear-gradient(90deg,transparent,{accent_color},transparent);
                          margin:0 auto 20px;width:80%;"></div>
              <!-- Title badge -->
              <div style="display:inline-block;background:{accent_color};
                          border-radius:30px;padding:10px 28px;">
                <span style="color:#fff;font-size:16px;font-weight:700;
                             letter-spacing:0.5px;font-family:'Segoe UI',Arial,sans-serif;">
                  {title}
                </span>
              </div>
            </td>
          </tr>

          <!-- ── BODY CARD ── -->
          <tr>
            <td style="background:#fff;padding:0;
                       box-shadow:0 8px 32px rgba(0,0,0,0.10);">
              <!-- Top green strip -->
              <div style="height:4px;background:linear-gradient(90deg,{accent_color},{accent_color}cc);"></div>
              <table cellpadding="0" cellspacing="0" width="100%">
                {rows_html}
              </table>
            </td>
          </tr>

          <!-- ── FOOTER ── -->
          <tr>
            <td style="background:#0a0a0a;border-radius:0 0 16px 16px;padding:20px 36px;text-align:center;">
              <p style="margin:0 0 6px;font-size:12px;color:#888;font-family:'Segoe UI',Arial,sans-serif;">
                This is an automated notification from
                <strong style="color:{accent_color};">Relux Electric CRM</strong>
              </p>
              <p style="margin:0;font-size:11px;color:#555;font-family:'Segoe UI',Arial,sans-serif;">
                © 2025 Relux Electric India Pvt Ltd &nbsp;|&nbsp;
                <a href="https://reluxelectric.com" style="color:{accent_color};text-decoration:none;">reluxelectric.com</a>
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

def _send_html_email(subject, plain_text, html_body):
    """Send an email with both plain-text and HTML alternatives."""
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=get_recipient_list(),
        )
        email.attach_alternative(html_body, "text/html")
        email.send(fail_silently=False)
    except Exception as e:
        print(f"Error sending email: {e}")

def send_franchise_email(instance):
    from django.utils.timezone import localtime
    submitted = localtime(instance.created_at).strftime("%B %d, %Y at %I:%M %p") if hasattr(instance, 'created_at') and instance.created_at else "N/A"
    subject = f"New Franchise Enquiry Submission"
    rows = [
        ("From:", instance.full_name),
        ("Franchise Selection:", instance.franchise_model or "N/A"),
        ("Phone:", instance.phone),
        ("State:", instance.state),
        ("City:", instance.city),
        ("Business Profile:", instance.business_profile or "N/A"),
        ("Investment Range:", instance.investment_capacity or "N/A"),
        ("Submitted:", submitted),
        ("Message:", instance.message or "N/A"),
    ]
    plain = (
        f"New Franchise Enquiry Submission\n\n"
        + "\n".join(f"{label} {value}" for label, value in rows)
    )
    html = _build_html_email("New Franchise Enquiry Submission", rows)
    _send_html_email(subject, plain, html)

def send_zero_investment_email(instance):
    from django.utils.timezone import localtime
    submitted = localtime(instance.created_at).strftime("%B %d, %Y at %I:%M %p") if hasattr(instance, 'created_at') and instance.created_at else "N/A"
    subject = f"New Zero Investment Partner Submission"
    rows = [
        ("From:", instance.full_name),
        ("Phone:", instance.phone),
        ("Location Offered:", instance.location_offered or "N/A"),
        ("Address:", instance.address or "N/A"),
        ("City:", instance.city or "N/A"),
        ("State:", instance.state or "N/A"),
        ("Land Size:", f"{instance.land_size or 'N/A'} {instance.land_unit or ''}".strip()),
        ("Electricity Connection:", instance.electricity_connection or "N/A"),
        ("Submitted:", submitted),
        ("Message:", instance.message or "N/A"),
    ]
    plain = (
        f"New Zero Investment Partner Submission\n\n"
        + "\n".join(f"{label} {value}" for label, value in rows)
    )
    html = _build_html_email("New Zero Investment Partner Submission", rows)
    _send_html_email(subject, plain, html)

def send_contact_email(instance):
    from django.utils.timezone import localtime
    submitted = localtime(instance.created_at).strftime("%B %d, %Y at %I:%M %p") if hasattr(instance, 'created_at') and instance.created_at else "N/A"
    subject = f"New Contact Message Submission"
    rows = [
        ("From:", instance.name),
        ("Phone:", instance.phone),
        ("Email:", instance.email),
        ("City:", instance.city or "N/A"),
        ("State:", instance.state or "N/A"),
        ("Subject:", instance.subject or "N/A"),
        ("Submitted:", submitted),
        ("Message:", instance.message or "N/A"),
    ]
    plain = (
        f"New Contact Message Submission\n\n"
        + "\n".join(f"{label} {value}" for label, value in rows)
    )
    html = _build_html_email("New Contact Message Submission", rows)
    _send_html_email(subject, plain, html)

# Business ViewSets
class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.filter(is_active=True)
    serializer_class = LocationSerializer

class FranchiseViewSet(viewsets.ModelViewSet):
    queryset = FranchiseInquiry.objects.all()
    serializer_class = FranchiseSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        send_franchise_email(instance)

class ZeroInvestmentViewSet(viewsets.ModelViewSet):
    queryset = ZeroInvestmentPartner.objects.all()
    serializer_class = ZeroInvestmentSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        send_zero_investment_email(instance)

class ContactViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        send_contact_email(instance)

# Content ViewSets
class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.filter(is_published=True).order_by('-created_at')
    serializer_class = BlogSerializer
    lookup_field = 'slug'

class BlogCategoryViewSet(viewsets.ModelViewSet):
    queryset = BlogCategory.objects.annotate(num_blogs=Count('blogs')).order_by('-num_blogs')
    serializer_class = BlogCategorySerializer

class BlogTagViewSet(viewsets.ModelViewSet):
    queryset = BlogTag.objects.all()
    serializer_class = BlogTagSerializer

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all().order_by('-created_at')
    serializer_class = VideoSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('date')
    serializer_class = EventSerializer

class HomeAboutImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HomeAboutImage.objects.filter(is_active=True).order_by('order')
    serializer_class = HomeAboutImageSerializer

class NetworkStatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NetworkStat.objects.all()
    serializer_class = NetworkStatSerializer

class CompanyCoreTabViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CompanyCoreTab.objects.all().order_by('order')
    serializer_class = CompanyCoreTabSerializer

class FranchiseModelCardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FranchiseModelCard.objects.filter(is_active=True).order_by('order')
    serializer_class = FranchiseModelCardSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.filter(is_published=True).order_by('-created_at')
    serializer_class = ArticleSerializer
    lookup_field = 'slug'

class VideoHeroSlideViewSet(viewsets.ModelViewSet):
    queryset = VideoHeroSlide.objects.filter(is_active=True).order_by('order')
    serializer_class = VideoHeroSlideSerializer


# ─── Sub-Admin Panel ViewSets ────────────────────────────────────────────────

class FranchiseAdminViewSet(viewsets.ModelViewSet):
    queryset = FranchiseInquiry.objects.all().order_by('-created_at')
    serializer_class = FranchiseAdminSerializer
    http_method_names = ['get', 'patch', 'head', 'options']

    def get_queryset(self):
        qs = super().get_queryset()
        status_filter = self.request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs

    def list(self, request, *args, **kwargs):
        if not check_admin_token(request):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not check_admin_token(request):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        # Auto-set responded_at when marking as responded
        if request.data.get('status') == 'responded' and not request.data.get('responded_at'):
            request.data._mutable = True if hasattr(request.data, '_mutable') else None
            data = request.data.copy()
            data['responded_at'] = timezone.now().isoformat()
            kwargs['partial'] = True
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class ZeroInvestmentAdminViewSet(viewsets.ModelViewSet):
    queryset = ZeroInvestmentPartner.objects.all().order_by('-created_at')
    serializer_class = ZeroInvestmentAdminSerializer
    http_method_names = ['get', 'patch', 'head', 'options']

    def get_queryset(self):
        qs = super().get_queryset()
        status_filter = self.request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs

    def list(self, request, *args, **kwargs):
        if not check_admin_token(request):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not check_admin_token(request):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        if request.data.get('status') == 'responded' and not request.data.get('responded_at'):
            data = request.data.copy()
            data['responded_at'] = timezone.now().isoformat()
            kwargs['partial'] = True
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class ContactAdminViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all().order_by('-created_at')
    serializer_class = ContactAdminSerializer
    http_method_names = ['get', 'patch', 'head', 'options']

    def get_queryset(self):
        qs = super().get_queryset()
        status_filter = self.request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs

    def list(self, request, *args, **kwargs):
        if not check_admin_token(request):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not check_admin_token(request):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        if request.data.get('status') == 'responded' and not request.data.get('responded_at'):
            data = request.data.copy()
            data['responded_at'] = timezone.now().isoformat()
            kwargs['partial'] = True
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


@csrf_exempt
def admin_stats_view(request):
    if not check_admin_token(request):
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    def get_counts(model):
        return {
            'total': model.objects.count(),
            'new': model.objects.filter(status='new').count(),
            'in_progress': model.objects.filter(status='in_progress').count(),
            'responded': model.objects.filter(status='responded').count(),
            'called_closed': model.objects.filter(status='called_closed').count(),
        }

    return JsonResponse({
        'franchise': get_counts(FranchiseInquiry),
        'zero_investment': get_counts(ZeroInvestmentPartner),
        'contact': get_counts(ContactMessage),
        'total': {
            'total': FranchiseInquiry.objects.count() + ZeroInvestmentPartner.objects.count() + ContactMessage.objects.count(),
            'new': FranchiseInquiry.objects.filter(status='new').count() + ZeroInvestmentPartner.objects.filter(status='new').count() + ContactMessage.objects.filter(status='new').count(),
            'in_progress': FranchiseInquiry.objects.filter(status='in_progress').count() + ZeroInvestmentPartner.objects.filter(status='in_progress').count() + ContactMessage.objects.filter(status='in_progress').count(),
            'responded': FranchiseInquiry.objects.filter(status='responded').count() + ZeroInvestmentPartner.objects.filter(status='responded').count() + ContactMessage.objects.filter(status='responded').count(),
            'called_closed': FranchiseInquiry.objects.filter(status='called_closed').count() + ZeroInvestmentPartner.objects.filter(status='called_closed').count() + ContactMessage.objects.filter(status='called_closed').count(),
        }
    })
