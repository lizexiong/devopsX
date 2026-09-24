# devopsX/accounts/admin.py
# 导入 Django Admin 模块。
from django.contrib import admin

# 复用 Django 成熟的用户和角色 Admin 基类。
from django.contrib.auth.admin import GroupAdmin, UserAdmin

# Group 在本模块中作为角色使用。
from django.contrib.auth.models import Group

# 导入本 App 的模型。
from .models import Department, User


# 把自定义 User 注册到 Admin。
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # 用户编辑页的字段分组。
    fieldsets = (
        # 第一组显示用户名和只读格式的密码摘要。
        (None, {"fields": ("username", "password")}),

        # 第二组显示 devopsX 业务资料。
        (
            "业务信息",
            {
                "fields": (
                    "display_name",
                    "employee_number",
                    "email",
                    "mobile",
                    "department",
                )
            },
        ),

        # 第三组显示状态和权限。
        (
            "权限与状态",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),

        # 第四组显示登录和创建时间。
        (
            "重要日期",
            {"fields": ("last_login", "date_joined")},
        ),
    )

    # Admin 新建用户页的字段。
    add_fieldsets = (
        (
            None,
            {
                # 使用较宽的 Admin 表单样式。
                "classes": ("wide",),

                # password1 和 password2 来自 UserCreationForm。
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "display_name",
                    "employee_number",
                    "email",
                    "mobile",
                    "department",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    # 用户列表显示的列。
    list_display = (
        "username",
        "display_name",
        "employee_number",
        "department",
        "is_active",
        "is_staff",
    )

    # 用户列表右侧筛选器。
    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "department",
        "groups",
    )

    # 用户列表搜索字段。
    search_fields = (
        "username",
        "display_name",
        "employee_number",
        "email",
        "mobile",
    )

    # 默认按用户名排序。
    ordering = ("username",)

    # 多对多权限使用左右选择框。
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    # 只有激活的超级用户可以在侧边栏看到用户 Admin。
    def has_module_permission(self, request):
        return (
            request.user.is_active
            and request.user.is_superuser
        )

    # 只有激活的超级用户可以查看用户 Admin 页面。
    def has_view_permission(self, request, obj=None):
        return (
            request.user.is_active
            and request.user.is_superuser
        )

    # 只有激活的超级用户可以通过 Admin 新建用户。
    def has_add_permission(self, request):
        return (
            request.user.is_active
            and request.user.is_superuser
        )

    # 只有激活的超级用户可以进入用户编辑页。
    def has_change_permission(self, request, obj=None):
        return (
            request.user.is_active
            and request.user.is_superuser
        )

    # 禁止从 Admin 删除用户，删除必须走受控业务页面。
    def has_delete_permission(self, request, obj=None):
        return False

    # 编辑既有用户时锁定会绕过业务保护的敏感字段。
    def get_readonly_fields(self, request, obj=None):
        # 保留 UserAdmin 原有只读字段。
        readonly_fields = super().get_readonly_fields(
            request,
            obj,
        )

        # 新建用户页仍使用 add_fieldsets 中的完整初始设置。
        if obj is None:
            return readonly_fields

        # 既有用户的启停、超级用户标记和授权必须走业务页面。
        return (
            *readonly_fields,
            "is_active",
            "is_superuser",
            "groups",
            "user_permissions",
        )


# Django 已自动注册 Group，先取消原有可写注册。
admin.site.unregister(Group)


# 重新注册只读的角色 Admin。
@admin.register(Group)
class CustomGroupAdmin(GroupAdmin):
    # 只有激活的超级用户能看到角色 Admin。
    def has_module_permission(self, request):
        return (
            request.user.is_active
            and request.user.is_superuser
        )

    # 只有激活的超级用户能查看角色。
    def has_view_permission(self, request, obj=None):
        return (
            request.user.is_active
            and request.user.is_superuser
        )

    # 角色新增必须经过 RoleForm 的权限白名单。
    def has_add_permission(self, request):
        return False

    # 角色修改必须经过 RoleForm 的权限白名单。
    def has_change_permission(self, request, obj=None):
        return False

    # 角色删除必须经过业务页面的占用检查。
    def has_delete_permission(self, request, obj=None):
        return False


# 把 Department 注册到 Admin。
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    # 部门列表显示的列。
    list_display = (
        "code",
        "name",
        "parent",
        "is_active",
        "sort_order",
    )

    # 按启用状态筛选。
    list_filter = ("is_active",)

    # 按编码或名称搜索。
    search_fields = ("code", "name")

    # 与模型默认排序保持一致。
    ordering = ("sort_order", "code")