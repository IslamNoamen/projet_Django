from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from datetime import date
import random, string

class Conference(models.Model):
    conference_id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255,
        validators=[RegexValidator(regex=r'^[a-zA-Z\s,]+$', message="Name can only contain letters, spaces, and commas.")]
    )
    description = models.TextField(
        validators=[MinLengthValidator(30, "Description must be at least 30 characters long.")]
    )
    location = models.CharField(max_length=255)

    THEME = [
        ('CS&IA', 'Computer Science & Artificial Intelligence'),
        ('SE', 'Science & Engineering'),
        ('CS', 'Social Sciences & Education'),
        ('IT', 'Interdisciplinary Themes'),
    ]
    theme = models.CharField(max_length=255, choices=THEME)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError("End date must be after start date.")

    def __str__(self):
        return f"{self.name} ({self.theme})"


class Submission(models.Model):
    submission_id = models.CharField(max_length=20, primary_key=True, editable=False)
    user_id = models.ForeignKey('UserApp.User', on_delete=models.CASCADE, related_name='submissions')
    conference_id = models.ForeignKey('ConferenceApp.Conference', on_delete=models.CASCADE, related_name='submissions')

    title = models.CharField(max_length=255)
    abstract = models.TextField()
    keywords = models.TextField()

    papier = models.FileField(
        upload_to='submissions/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )

    STATUS = [
        ('submitted', 'Submitted'),
        ('under review', 'Under Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=50, choices=STATUS)
    payed = models.BooleanField(default=False)

    submission_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.submission_id:
            random_id = ''.join(random.choices(string.ascii_uppercase, k=8))
            self.submission_id = f"SUB-{random_id}"
        super().save(*args, **kwargs)

    def clean(self):
        
        errors = {}
        if self.conference_id and self.conference_id.start_date < date.today():
            # Change 'conference_id' to 'conference_id' or use __all__ for non-field errors
            errors['conference_id'] = ["La soumission ne peut être faite que pour des conférences à venir."]

        if self.keywords:
            keyword_list = [kw.strip() for kw in self.keywords.split(',') if kw.strip()]
            if len(keyword_list) > 10:
                errors['keywords'] = [f"Vous avez saisi {len(keyword_list)} mots-clés. Le maximum autorisé est 10."]

        if self.user_id:
            from django.utils import timezone
            today = timezone.now().date()
            today_submissions = Submission.objects.filter(
                user_id=self.user_id,
                submission_date__date=today
            ).count()
            if not self.pk and today_submissions >= 3:
                errors['user_id'] = ["Vous avez déjà soumis 3 conférences aujourd'hui. Limite journalière atteinte."]

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.submission_id} - {self.title}"