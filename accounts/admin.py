from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import Group, Permission
from .models import CustomUser, AuthenticationLog, PendingUser


# Re-register Group with better display
admin.site.unregister(Group)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('permissions',)


# Register Permission model for viewing
@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'content_type', 'codename')
    list_filter = ('content_type',)
    search_fields = ('name', 'codename')


@admin.register(CustomUser)
class CustomUserAdmin(DefaultUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'national_id')
    ordering = ('-date_joined',)
    
    fieldsets = DefaultUserAdmin.fieldsets + (
        ('معلومات إضافية', {'fields': ('role', 'phone', 'national_id', 'governorate')}),
    )
    
    # Enable delete permission
    def has_delete_permission(self, request, obj=None):
        return True
    
    # Override delete to handle missing tables gracefully
    def delete_model(self, request, obj):
        try:
            obj.delete()
            self.message_user(request, f'تم حذف المستخدم {obj.username} بنجاح')
        except Exception as e:
            self.message_user(request, f'خطأ عند الحذف: {str(e)}', level='error')
    
    def delete_queryset(self, request, queryset):
        success_count = 0
        error_count = 0
        for obj in queryset:
            try:
                obj.delete()
                success_count += 1
            except Exception as e:
                error_count += 1
        
        if success_count > 0:
            self.message_user(request, f'تم حذف {success_count} مستخدم بنجاح')
        if error_count > 0:
            self.message_user(request, f'فشل حذف {error_count} مستخدم - يرجى تشغيل migrations أولاً', level='warning')
    
    # Add custom actions
    actions = ['activate_users', 'deactivate_users', 'make_staff', 'remove_staff']
    
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'تم تفعيل {updated} مستخدم بنجاح')
    activate_users.short_description = 'تفعيل المستخدمين المحددين'
    
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'تم إلغاء تفعيل {updated} مستخدم بنجاح')
    deactivate_users.short_description = 'إلغاء تفعيل المستخدمين المحددين'
    
    def make_staff(self, request, queryset):
        updated = queryset.update(is_staff=True)
        self.message_user(request, f'تم منح {updated} مستخدم صلاحيات الموظفين')
    make_staff.short_description = 'منح صلاحيات الموظفين'
    
    def remove_staff(self, request, queryset):
        updated = queryset.update(is_staff=False)
        self.message_user(request, f'تم إزالة صلاحيات الموظفين من {updated} مستخدم')
    remove_staff.short_description = 'إزالة صلاحيات الموظفين'


@admin.register(AuthenticationLog)
class AuthenticationLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'user', 'email', 'username', 'ip_address', 'success', 'created_at')
    list_filter = ('action', 'success', 'created_at')
    search_fields = ('email', 'username', 'ip_address', 'user__username', 'user__email')
    readonly_fields = ('created_at',)

    ordering = ('-created_at',)
    
    fieldsets = (
        ('معلومات العملية', {
            'fields': ('action', 'success', 'created_at')
        }),
        ('معلومات المستخدم', {
            'fields': ('user', 'email', 'username')
        }),
        ('معلومات الاتصال', {
            'fields': ('ip_address', 'user_agent')
        }),
        ('تفاصيل الخطأ', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # منع إضافة سجلات يدوياً - يتم إنشاؤها تلقائياً فقط
        return False
    
    def has_change_permission(self, request, obj=None):
        # منع تعديل السجلات - للاحتفاظ بسجل دقيق
        return False


@admin.register(PendingUser)
class PendingUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'created_at', 'expires_at', 'is_expired')
    list_filter = ('role', 'created_at')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    readonly_fields = ('id', 'verification_token', 'created_at', 'expires_at')
    ordering = ('-created_at',)
    actions = ['delete_expired_users']
    
    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True
    is_expired.short_description = 'منتهي الصلاحية'
    
    def delete_expired_users(self, request, queryset):
        expired = [user for user in queryset if user.is_expired()]
        count = len(expired)
        for user in expired:
            user.delete()
        self.message_user(request, f'تم حذف {count} مستخدم منتهي الصلاحية')
    delete_expired_users.short_description = 'حذف المستخدمين منتهي الصلاحية'

