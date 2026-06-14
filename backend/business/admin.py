from django.contrib import admin
from .models import Location, FranchiseInquiry, ZeroInvestmentPartner, ContactMessage, LocationReview

from django.utils.translation import gettext_lazy as _

class StateRegionFilter(admin.SimpleListFilter):
    title = _('State')
    parameter_name = 'state_filter'
    template = 'admin/dropdown_filter.html'

    def lookups(self, request, model_admin):
        states = set(model_admin.model.objects.exclude(state__isnull=True).exclude(state='').values_list('state', flat=True))
        lookups = [
            ('south', _('South India & Others')),
            ('north', _('North India ')),
        ]
        for state in sorted(states):
            lookups.append((state, state))
        return lookups

    def queryset(self, request, queryset):
        SOUTH_STATES = ['tamil nadu', 'tamilnadu', 'kerala', 'karnataka', 'andhra', 'telangana', 'pondicherry', 'puducherry']
        val = self.value()
        
        if val == 'north':
            from django.db.models import Q
            q = Q()
            for s in SOUTH_STATES:
                q |= Q(state__icontains=s)
            return queryset.exclude(q)
        elif val == 'south':
            from django.db.models import Q
            q = Q()
            for s in SOUTH_STATES:
                q |= Q(state__icontains=s)
            return queryset.filter(q)
        elif val:
            return queryset.filter(state=val)
        return queryset

class CityFilter(admin.SimpleListFilter):
    title = _('City')
    parameter_name = 'city_filter'
    template = 'admin/dropdown_filter.html'

    def lookups(self, request, model_admin):
        cities = set(model_admin.model.objects.exclude(city__isnull=True).exclude(city='').values_list('city', flat=True))
        return sorted([(city, city) for city in cities if city])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(city=self.value())
        return queryset

class FranchiseModelFilter(admin.SimpleListFilter):
    title = _('Franchise Model')
    parameter_name = 'franchise_model_filter'
    template = 'admin/dropdown_filter.html'

    def lookups(self, request, model_admin):
        models = set(model_admin.model.objects.exclude(franchise_model__isnull=True).exclude(franchise_model='').values_list('franchise_model', flat=True))
        return sorted([(m, m) for m in models if m])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(franchise_model=self.value())
        return queryset

class BusinessProfileFilter(admin.SimpleListFilter):
    title = _('Business Profile')
    parameter_name = 'business_profile_filter'
    template = 'admin/dropdown_filter.html'

    def lookups(self, request, model_admin):
        profiles = set(model_admin.model.objects.exclude(business_profile__isnull=True).exclude(business_profile='').values_list('business_profile', flat=True))
        return sorted([(p, p) for p in profiles if p])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(business_profile=self.value())
        return queryset

class InvestmentCapacityFilter(admin.SimpleListFilter):
    title = _('Investment Range')
    parameter_name = 'investment_capacity_filter'
    template = 'admin/dropdown_filter.html'

    def lookups(self, request, model_admin):
        ranges = set(model_admin.model.objects.exclude(investment_capacity__isnull=True).exclude(investment_capacity='').values_list('investment_capacity', flat=True))
        return sorted([(r, r) for r in ranges if r])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(investment_capacity=self.value())
        return queryset

class CreatedAtFilter(admin.SimpleListFilter):
    title = _('Date')
    parameter_name = 'created_at_filter'
    template = 'admin/date_range_filter.html'

    def lookups(self, request, model_admin):
        return (
            ('today', _('Today')),
            ('past_7_days', _('Past 7 days')),
            ('this_month', _('This month')),
            ('this_year', _('This year')),
        )

    def queryset(self, request, queryset):
        import datetime
        from django.utils import timezone
        from django.utils.dateparse import parse_date
        
        today = timezone.now().date()
        val = self.value()
        
        # 1. Check quick range values
        if val == 'today':
            queryset = queryset.filter(created_at__date=today)
        elif val == 'past_7_days':
            start_date = today - datetime.timedelta(days=7)
            queryset = queryset.filter(created_at__date__gte=start_date)
        elif val == 'this_month':
            queryset = queryset.filter(created_at__year=today.year, created_at__month=today.month)
        elif val == 'this_year':
            queryset = queryset.filter(created_at__year=today.year)
            
        # 2. Check custom date range query parameters
        from_date_str = request.GET.get('created_at_from')
        to_date_str = request.GET.get('created_at_to')
        
        if from_date_str:
            from_date = parse_date(from_date_str)
            if from_date:
                queryset = queryset.filter(created_at__date__gte=from_date)
                
        if to_date_str:
            to_date = parse_date(to_date_str)
            if to_date:
                queryset = queryset.filter(created_at__date__lte=to_date)
                
        return queryset

@admin.register(FranchiseInquiry)
class FranchiseInquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'state', 'city', 'franchise_model', 'business_profile', 'investment_capacity', 'created_at')
    search_fields = ('full_name', 'email', 'city', 'state', 'franchise_model', 'business_profile', 'investment_capacity')
    list_filter = (
        FranchiseModelFilter,
        StateRegionFilter,
        CityFilter,
        BusinessProfileFilter,
        InvestmentCapacityFilter,
        CreatedAtFilter,
    )
    actions = ['export_selected_to_csv']

    @admin.action(description=_('Export selected inquiries to CSV'))
    def export_selected_to_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="franchise_inquiries_selected.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Full Name', 'Email', 'Phone', 'State', 'City', 
            'Franchise Model', 'Current Business Profile', 
            'Investment Capacity', 'Created At'
        ])
        
        for obj in queryset:
            writer.writerow([
                obj.full_name,
                obj.email,
                obj.phone,
                obj.state,
                obj.city,
                obj.franchise_model,
                obj.business_profile,
                obj.investment_capacity,
                obj.created_at.strftime('%Y-%m-%d %H:%M:%S') if obj.created_at else ''
            ])
            
        return response

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('export-csv/', self.admin_site.admin_view(self.export_csv_view), name='business_franchiseinquiry_export_csv'),
        ]
        return custom_urls + urls

    def export_csv_view(self, request):
        import csv
        from django.http import HttpResponse
        
        # Get the changelist instance with the current active filters!
        cl = self.get_changelist_instance(request)
        queryset = cl.get_queryset(request)
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="franchise_inquiries.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Full Name', 'Email', 'Phone', 'State', 'City', 
            'Franchise Model', 'Current Business Profile', 
            'Investment Capacity', 'Created At'
        ])
        
        for obj in queryset:
            writer.writerow([
                obj.full_name,
                obj.email,
                obj.phone,
                obj.state,
                obj.city,
                obj.franchise_model,
                obj.business_profile,
                obj.investment_capacity,
                obj.created_at.strftime('%Y-%m-%d %H:%M:%S') if obj.created_at else ''
            ])
            
        return response

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        from django.contrib.admin.models import LogEntry
        from django.contrib.contenttypes.models import ContentType
        
        # Get ContentType for FranchiseInquiry
        ct = ContentType.objects.get_for_model(self.model)
        
        # Get 10 recent actions
        recent_actions = LogEntry.objects.filter(content_type=ct).order_by('-action_time')[:10]
        extra_context['recent_actions'] = recent_actions
        
        return super().changelist_view(request, extra_context=extra_context)

class ZeroStateRegionFilter(admin.SimpleListFilter):
    title = _('State')
    parameter_name = 'state_filter'
    template = 'admin/dropdown_filter.html'

    def lookups(self, request, model_admin):
        return (
            ('south', _('South India & Others')),
            ('north', _('North India ')),
            ('tamil_nadu', _('Tamil Nadu')),
            ('kerala', _('Kerala')),
            ('karnataka', _('Karnataka')),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'south':
            return queryset.filter(state__iexact='Tamil Nadu') | queryset.filter(state__iexact='Kerala') | queryset.filter(state__iexact='Karnataka') | queryset.exclude(state__iexact='North India')
        elif val == 'north':
            return queryset.filter(state__iexact='North India')
        elif val:
            state_mapping = {
                'tamil_nadu': 'Tamil Nadu',
                'kerala': 'Kerala',
                'karnataka': 'Karnataka',
            }
            db_val = state_mapping.get(val, val)
            return queryset.filter(state__iexact=db_val)
        return queryset

class ZeroCityFilter(admin.SimpleListFilter):
    title = _('City')
    parameter_name = 'city_filter'
    template = 'admin/dropdown_filter.html'

    def lookups(self, request, model_admin):
        cities = ZeroInvestmentPartner.objects.exclude(city__isnull=True).exclude(city='').values_list('city', flat=True).distinct()
        return [(c.lower().replace(' ', '_'), c) for c in cities]

    def queryset(self, request, queryset):
        val = self.value()
        if val:
            cities = ZeroInvestmentPartner.objects.exclude(city__isnull=True).exclude(city='').values_list('city', flat=True).distinct()
            city_mapping = {c.lower().replace(' ', '_'): c for c in cities}
            db_val = city_mapping.get(val, val)
            return queryset.filter(city__iexact=db_val)
        return queryset

class LandUnitFilter(admin.SimpleListFilter):
    title = _('Land Unit')
    parameter_name = 'land_unit'
    template = 'admin/dropdown_filter.html'

    def lookups(self, request, model_admin):
        return (
            ('sqft', _('SQ.FT')),
            ('acres', _('ACRES')),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'sqft':
            return queryset.filter(land_unit__iexact='SQ.FT')
        elif val == 'acres':
            return queryset.filter(land_unit__iexact='ACRES')
        return queryset

class ElectricityConnectionFilter(admin.SimpleListFilter):
    title = _('Electricity')
    parameter_name = 'electricity_connection'
    template = 'admin/dropdown_filter.html'

    def lookups(self, request, model_admin):
        return (
            ('yes', _('Yes')),
            ('no', _('No')),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'yes':
            return queryset.filter(electricity_connection__iexact='YES')
        elif val == 'no':
            return queryset.filter(electricity_connection__iexact='NO')
        return queryset

@admin.register(ZeroInvestmentPartner)
class ZeroInvestmentPartnerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'state', 'city', 'land_size', 'land_unit', 'electricity_connection', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'city', 'state', 'land_size')
    list_filter = (
        ZeroStateRegionFilter,
        ZeroCityFilter,
        LandUnitFilter,
        ElectricityConnectionFilter,
        CreatedAtFilter,
    )
    actions = ['export_selected_to_csv']

    @admin.action(description=_('Export selected partners to CSV'))
    def export_selected_to_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="zero_investment_partners_selected.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Full Name', 'Email', 'Phone', 'Address', 'State', 'City', 
            'Land Size', 'Land Unit', 'Electricity Connection', 'Message', 'Created At'
        ])
        
        for obj in queryset:
            writer.writerow([
                obj.full_name,
                obj.email,
                obj.phone,
                obj.address,
                obj.state,
                obj.city,
                obj.land_size,
                obj.land_unit,
                obj.electricity_connection,
                obj.message,
                obj.created_at.strftime('%Y-%m-%d %H:%M:%S') if obj.created_at else ''
            ])
            
        return response

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('export-csv/', self.admin_site.admin_view(self.export_csv_view), name='business_zeroinvestmentpartner_export_csv'),
        ]
        return custom_urls + urls

    def export_csv_view(self, request):
        import csv
        from django.http import HttpResponse
        
        # Get the changelist instance with the current active filters!
        cl = self.get_changelist_instance(request)
        queryset = cl.get_queryset(request)
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="zero_investment_partners.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Full Name', 'Email', 'Phone', 'Address', 'State', 'City', 
            'Land Size', 'Land Unit', 'Electricity Connection', 'Message', 'Created At'
        ])
        
        for obj in queryset:
            writer.writerow([
                obj.full_name,
                obj.email,
                obj.phone,
                obj.address,
                obj.state,
                obj.city,
                obj.land_size,
                obj.land_unit,
                obj.electricity_connection,
                obj.message,
                obj.created_at.strftime('%Y-%m-%d %H:%M:%S') if obj.created_at else ''
            ])
            
        return response

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        from django.contrib.admin.models import LogEntry
        from django.contrib.contenttypes.models import ContentType
        
        # Get ContentType for ZeroInvestmentPartner
        ct = ContentType.objects.get_for_model(self.model)
        
        # Get 10 recent actions
        recent_actions = LogEntry.objects.filter(content_type=ct).order_by('-action_time')[:10]
        extra_context['recent_actions'] = recent_actions
        
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'state', 'city', 'subject', 'created_at')
    search_fields = ('name', 'email', 'phone', 'state', 'city', 'subject')
    list_filter = (
        StateRegionFilter,
        CityFilter,
        CreatedAtFilter,
    )
    actions = ['export_selected_to_csv']

    @admin.action(description=_('Export selected messages to CSV'))
    def export_selected_to_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="contact_messages_selected.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Name', 'Email', 'Phone', 'State', 'City', 'Subject', 'Message', 'Created At'
        ])
        
        for obj in queryset:
            writer.writerow([
                obj.name,
                obj.email,
                obj.phone,
                obj.state,
                obj.city,
                obj.subject,
                obj.message,
                obj.created_at.strftime('%Y-%m-%d %H:%M:%S') if obj.created_at else ''
            ])
            
        return response

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('export-csv/', self.admin_site.admin_view(self.export_csv_view), name='business_contactmessage_export_csv'),
        ]
        return custom_urls + urls

    def export_csv_view(self, request):
        import csv
        from django.http import HttpResponse
        
        cl = self.get_changelist_instance(request)
        queryset = cl.get_queryset(request)
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="contact_messages.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Name', 'Email', 'Phone', 'State', 'City', 'Subject', 'Message', 'Created At'
        ])
        
        for obj in queryset:
            writer.writerow([
                obj.name,
                obj.email,
                obj.phone,
                obj.state,
                obj.city,
                obj.subject,
                obj.message,
                obj.created_at.strftime('%Y-%m-%d %H:%M:%S') if obj.created_at else ''
            ])
            
        return response

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        from django.contrib.admin.models import LogEntry
        from django.contrib.contenttypes.models import ContentType
        
        ct = ContentType.objects.get_for_model(self.model)
        recent_actions = LogEntry.objects.filter(content_type=ct).order_by('-action_time')[:10]
        extra_context['recent_actions'] = recent_actions
        
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'city', 'state', 'country', 'status', 
        'charger_connector', 'charger_power', 'charger_count', 
        'is_active', 'created_at'
    )
    search_fields = ('name', 'city', 'state', 'country', 'facilities', 'charger_connector')
    list_filter = (
        StateRegionFilter,
        CityFilter,
        CreatedAtFilter,
        'status',
        'is_active',
    )
    actions = ['export_selected_to_csv']

    @admin.action(description=_('Export selected locations to CSV'))
    def export_selected_to_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="locations_selected.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Name', 'Address', 'City', 'State', 'Country', 'Zip Code', 
            'Latitude', 'Longitude', 'Status', 'Facilities', 
            'Charger Connector', 'Charger Power', 'Charger Count', 'Is Active', 'Created At'
        ])
        
        for obj in queryset:
            writer.writerow([
                obj.name,
                obj.address or '',
                obj.city,
                obj.state or '',
                obj.country,
                obj.zip_code or '',
                str(obj.latitude) if obj.latitude else '',
                str(obj.longitude) if obj.longitude else '',
                obj.status,
                obj.facilities or '',
                obj.charger_connector or '',
                obj.charger_power or '',
                obj.charger_count,
                'Yes' if obj.is_active else 'No',
                obj.created_at.strftime('%Y-%m-%d %H:%M:%S') if obj.created_at else ''
            ])
            
        return response

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('export-csv/', self.admin_site.admin_view(self.export_csv_view), name='business_location_export_csv'),
        ]
        return custom_urls + urls

    def export_csv_view(self, request):
        import csv
        from django.http import HttpResponse
        
        cl = self.get_changelist_instance(request)
        queryset = cl.get_queryset(request)
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="locations.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Name', 'Address', 'City', 'State', 'Country', 'Zip Code', 
            'Latitude', 'Longitude', 'Status', 'Facilities', 
            'Charger Connector', 'Charger Power', 'Charger Count', 'Is Active', 'Created At'
        ])
        
        for obj in queryset:
            writer.writerow([
                obj.name,
                obj.address or '',
                obj.city,
                obj.state or '',
                obj.country,
                obj.zip_code or '',
                str(obj.latitude) if obj.latitude else '',
                str(obj.longitude) if obj.longitude else '',
                obj.status,
                obj.facilities or '',
                obj.charger_connector or '',
                obj.charger_power or '',
                obj.charger_count,
                'Yes' if obj.is_active else 'No',
                obj.created_at.strftime('%Y-%m-%d %H:%M:%S') if obj.created_at else ''
            ])
            
        return response

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        from django.contrib.admin.models import LogEntry
        from django.contrib.contenttypes.models import ContentType
        
        ct = ContentType.objects.get_for_model(self.model)
        recent_actions = LogEntry.objects.filter(content_type=ct).order_by('-action_time')[:10]
        extra_context['recent_actions'] = recent_actions
        
        return super().changelist_view(request, extra_context=extra_context)
        return super().changelist_view(request, extra_context=extra_context)

class LocationReviewInline(admin.TabularInline):
    model = LocationReview
    extra = 1

# Update LocationAdmin to show reviews inline
LocationAdmin.inlines = [LocationReviewInline]
