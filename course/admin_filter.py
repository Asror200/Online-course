from django.contrib import admin
import datetime


class JoinedDateFilter(admin.SimpleListFilter):
    """ This function is used to filter objects by joined date """
    title = 'joined'
    parameter_name = 'joined_date'

    def lookups(self, request, model_admin):
        return [
            ('this_year', 'This Year'),
            ('last_year', 'Last Year'),
            ('last_30_days', 'Last 30 Days'),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'this_year':
            return queryset.filter(created_at__year=datetime.date.today().year)
        if value == 'last_year':
            return queryset.filter(created_at__year=datetime.date.today().year - 1)
        if value == 'last_30_days':
            return queryset.filter(created_at__gte=datetime.date.today() - datetime.timedelta(days=30))
        return queryset
