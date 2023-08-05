from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mayan.apps.databases.model_mixins import ExtraDataModelMixin
from mayan.apps.events.classes import EventManagerSave
from mayan.apps.events.decorators import method_event

from .classes import GPGBackend
from .events import event_key_created
from .literals import KEY_TYPE_CHOICES

from .managers import KeyManager
from .model_mixins import KeyBusinessLogicMixin


class Key(ExtraDataModelMixin, KeyBusinessLogicMixin, models.Model):
    """
    Fields:
    * key_type - Will show private or public, the only two types of keys in
    a public key infrastructure, the kind used in Mayan.
    """
    key_data = models.TextField(
        help_text=_('ASCII armored version of the key.'),
        verbose_name=_('Key data')
    )
    creation_date = models.DateTimeField(
        editable=False, verbose_name=_('Creation date')
    )
    expiration_date = models.DateTimeField(
        blank=True, editable=False, null=True,
        verbose_name=_('Expiration date')
    )
    fingerprint = models.CharField(
        editable=False, max_length=40, unique=True,
        verbose_name=_('Fingerprint')
    )
    length = models.PositiveIntegerField(
        editable=False, verbose_name=_('Length')
    )
    algorithm = models.PositiveIntegerField(
        editable=False, verbose_name=_('Algorithm')
    )
    user_id = models.TextField(
        editable=False, verbose_name=_('User ID')
    )
    key_type = models.CharField(
        choices=KEY_TYPE_CHOICES, editable=False, max_length=3,
        verbose_name=_('Type')
    )

    objects = KeyManager()

    class Meta:
        verbose_name = _('Key')
        verbose_name_plural = _('Keys')

    def __str__(self):
        return '{} - {}'.format(self.key_id, self.user_id)

    def clean(self):
        """
        Validate the key before saving.
        """
        import_results = GPGBackend.get_instance().import_key(
            key_data=self.key_data
        )

        if not import_results.count:
            raise ValidationError(
                message=_('Invalid key data')
            )

        if Key.objects.filter(fingerprint=import_results.fingerprints[0]).exists():
            raise ValidationError(
                message=_('Key already exists.')
            )

    def get_absolute_url(self):
        return reverse(
            viewname='django_gpg:key_detail', kwargs={'key_id': self.pk}
        )

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'event': event_key_created,
            'target': 'self'
        }
    )
    def save(self, *args, **kwargs):
        self.introspect_key_data()
        super().save(*args, **kwargs)
