from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db import models


class HomePage(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='başlıq',
        db_index=True,
        help_text="Əsas səhifə üçün başlıq"
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='mətn',
        help_text="Əsas səhifə 2-ci dərəcəli hissə")
    image = models.ImageField(
        upload_to='homepage',
        verbose_name='şəkil',
        help_text="Əsas səihfə üçün şəkil"
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name="Əsas səhifədə görünsünmü?",
        help_text="Klikləməsəniz görünməyəcək!"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Əsas səhifə'
        verbose_name_plural = 'Əsas səhifə'
        ordering = ['id']


class New(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='başlıq',
        db_index=True,
        help_text="Xəbər başlığı"
    )
    content = RichTextUploadingField(
        verbose_name='mətn',
        help_text="Xəbər detalları"
    )
    date = models.DateField(
        verbose_name='tarix',
        help_text="Xəbər tarixi"
    )
    image = models.ImageField(
        upload_to='news',
        verbose_name='şəkil',
        help_text="Xəbər üçün şəkil"
    )
    status = models.CharField(
        max_length=15,
        choices=(('published', 'Yayımlandı'), ('draft', 'Gözləmədə')),
        verbose_name="status",
        help_text="status")
    is_comment = models.BooleanField(
        default=False,
        verbose_name="Rəy üçün icazə verilsin",
        help_text="Rəy üçün icazə"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Xəbər'
        verbose_name_plural = 'Xəbərlər'
        ordering = ['-date']


class Comment(models.Model):
    news = models.ForeignKey(
        New,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Xəbər'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='İstifadəçi'
    )
    content = models.TextField(
        verbose_name='Rəy məzmunu',
        help_text="Rəy məzmunu"
    )
    date_posted = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Tarix'
    )

    def __str__(self):
        return f'{self.user} tərəfindən {self.news} xəbərə rəy'

    class Meta:
        verbose_name = 'Rəy'
        verbose_name_plural = 'Rəylər'
        ordering = ['-date_posted']


class Contact(models.Model):
    first_name = models.CharField(
        max_length=255,
        verbose_name="Adınız",
        help_text="Ad"
    )
    email = models.EmailField(
        verbose_name="Elektron poçt",
        help_text="E-poçt"
    )
    phone_number = models.CharField(
        max_length=10,
        verbose_name="Əlaqə №",
        help_text="Nümunə: 994991112233"
    )
    subject = models.CharField(
        max_length=255,
        verbose_name="Mövzu",
        help_text="Maksimum 255 simvol"
    )
    content = models.TextField(
        verbose_name="Mesajınız",
        help_text="Mesajınız"
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaradılma tarixi",
        help_text="Avtomatik yaradılır"
    )

    def __str__(self):
        return f'{self.first_name} -> {self.email} -> {self.phone_number} -> {self.subject}'

    class Meta:
        verbose_name = "Əlaqə"
        verbose_name_plural = "Əlaqə"
        ordering = ['-created_date']


class Event(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='başlıq',
        db_index=True,
        help_text="eyni başlığı 2 dəfə yaza bilməzsiniz!"
    )
    content = RichTextUploadingField(
        verbose_name='mətn',
        help_text="Tədbir mətni"
    )
    place = models.CharField(
        max_length=255,
        verbose_name='məkan',
        help_text="məkan"
    )
    date = models.DateTimeField(
        verbose_name='tarix',
        help_text="Tarix"
    )
    image = models.ImageField(
        upload_to='events',
        verbose_name='şəkil',
        help_text="Tədbir üçün şəkil"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Tədbir'
        verbose_name_plural = 'Tədbirlər'
        ordering = ['-date']


class Staff(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Adı və soyadı",
        help_text="Maksimum 255 simvol"
    )
    position = models.CharField(
        max_length=255,
        verbose_name="Tutduğu vəzifə",
        help_text="Maksimum 255 simvol"
    )
    about = RichTextUploadingField(
        verbose_name="Haqqında ümumi məlumat"
    )
    image = models.ImageField(
        upload_to="staff",
        verbose_name="Şəkil",
        help_text="Şəkil mütləq əlavə olunmalıdır!"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "İşçi heyəti"
        verbose_name_plural = "İşçi heyəti"
