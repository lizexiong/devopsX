from django.db import models

# Create your models here.



from django.contrib.auth.models import AbstractUser

from django.core.exceptions import ValidationError


class Department(models.Model):
    code = models.CharField(
        "部门编码",
        max_length=50,
        unique=True
    )

    name = models.CharField(
        "部门名称",
        max_length=100,
    )

    parent = models.ForeignKey(
        "self",
        verbose_name="上级部门",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='children',

    )

    is_active = models.BooleanField(
        "启用",
        
        default=True
    )

    sort_order = models.PositiveBigIntegerField(
        '排序',
        default=0,
    )

    create_at = models.DateTimeField(
        "创建时间",
        auto_now_add=True
    )

    update_at = models.DateTimeField(
        "更新时间",
        auto_now=True
    )

    def clean(self):
        super().clean()

        if not self.parent_id:
            return

        if self.pk and self.parent_id == self.pk:
            raise ValidationError(
                {"parent": "上级部门不能是当前部门"}
            )

        ancestor = self.parent

        visited = set()


        while ancestor is not None:
            if self.pk and ancestor.pk == self.pk:
                raise ValidationError(
                    {"parent": "上级部门不能是当前部门的后代"}
                )

            if ancestor.pk in visited:
                raise(
                    {"parnet":"部门层级中存在循环关系"}
                )

            visited.add(ancestor.pk)

            ancestor = ancestor.parent


    def __str__(self):
        return "%s - %s"%(self.code,self.name)


class User(AbstractUser):

    display_name = models.CharField(
        "姓名",
        max_length=100,
        blank=True,
    )

    employee_number = models.CharField(
        "工号",
        max_length=50,
        unique=True,
        null=True,
        blank=True
    )

    mobile = models.CharField(
        "手机号",
        max_length=20,
        blank=True
    )

    department = models.ForeignKey(
        Department,
        verbose_name="部门",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="users"
    )

    # 继承 AbstractUser.Meta，并增加业务权限。
    class Meta(AbstractUser.Meta):
        # Django migrate 后会创建这两个 Permission。
        permissions = [
            ("set_user_status", "可以启用或停用用户"),
            ("assign_user_roles", "可以分配用户角色和直接权限"),
        ]

    # 模型校验。
    def clean(self):
        # 先执行 AbstractUser 原有校验。
        super().clean()

        # 把空字符串统一改成 NULL，允许多个未填写工号的用户。
        if not self.employee_number:
            self.employee_number = None

    def __str__(self):
        # 有姓名时显示姓名；否则显示登录用户名。
        return self.display_name.strip() or self.username