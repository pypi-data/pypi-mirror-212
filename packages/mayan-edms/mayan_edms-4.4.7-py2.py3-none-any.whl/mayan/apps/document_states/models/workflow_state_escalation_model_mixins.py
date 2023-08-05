from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class WorkflowStateEscalationBusinessLogicMixin:
    def execute(self, context, workflow_instance):
        if self.evaluate_condition(workflow_instance=workflow_instance):
            try:
                self.get_class_instance().execute(context=context)
            except Exception as exception:
                self.error_log.create(
                    text='{}; {}'.format(
                        exception.__class__.__name__, exception
                    )
                )

                if settings.DEBUG or settings.TESTING:
                    raise
            else:
                self.error_log.all().delete()

    def get_comment(self):
        return self.comment or _('Workflow escalation.')
