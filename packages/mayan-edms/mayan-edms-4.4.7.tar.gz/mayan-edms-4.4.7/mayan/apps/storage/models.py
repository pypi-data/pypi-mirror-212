from pathlib import Path

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mayan.apps.databases.model_mixins import ExtraDataModelMixin
from mayan.apps.events.classes import (
    EventManagerMethodAfter, EventManagerSave
)
from mayan.apps.events.decorators import method_event

from .classes import DefinedStorageLazy
from .events import (
    event_download_file_created, event_download_file_deleted
)
from .literals import (
    STORAGE_NAME_DOWNLOAD_FILE, STORAGE_NAME_SHARED_UPLOADED_FILE
)
from .managers import DownloadFileManager, SharedUploadedFileManager
from .model_mixins import (
    DatabaseFileModelMixin, DownloadFileBusinessLogicMixin
)
from .utils import download_file_upload_to, shared_uploaded_file_upload_to


class DownloadFile(
    DatabaseFileModelMixin, DownloadFileBusinessLogicMixin,
    ExtraDataModelMixin, models.Model
):
    """
    Keep a database link to a stored file. Used for generated files meant
    to be downloaded at a later time.
    """

    file = models.FileField(
        storage=DefinedStorageLazy(
            name=STORAGE_NAME_DOWNLOAD_FILE
        ), upload_to=download_file_upload_to, verbose_name=_('File')
    )
    label = models.CharField(
        db_index=True, max_length=192, verbose_name=_('Label')
    )
    user = models.ForeignKey(
        editable=False, on_delete=models.CASCADE,
        related_name='download_files', to=settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
    )

    objects = DownloadFileManager()

    class Meta:
        ordering = ('-datetime',)
        verbose_name = _('Download file')
        verbose_name_plural = _('Download files')

    def __str__(self):
        return self.filename or self.label

    @method_event(
        event_manager_class=EventManagerMethodAfter,
        event=event_download_file_deleted
    )
    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(viewname='storage:download_file_list')

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'event': event_download_file_created,
            'target': 'self'
        }
    )
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class SharedUploadedFile(DatabaseFileModelMixin, models.Model):
    """
    Keep a database link to a stored file. Used to share files between code
    that runs out of process.
    """

    file = models.FileField(
        storage=DefinedStorageLazy(
            name=STORAGE_NAME_SHARED_UPLOADED_FILE
        ), upload_to=shared_uploaded_file_upload_to, verbose_name=_('File')
    )
    filename = models.CharField(
        blank=True, max_length=255, verbose_name=_('Filename')
    )

    objects = SharedUploadedFileManager()

    class Meta:
        verbose_name = _('Shared uploaded file')
        verbose_name_plural = _('Shared uploaded files')

    def __str__(self):
        return self.filename

    def save(self, *args, **kwargs):
        self.filename = self.filename or Path(path=self.file.name).name
        super().save(*args, **kwargs)
        self.file.close()
