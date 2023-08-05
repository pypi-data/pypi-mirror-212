from celery import Celery
from django.conf import settings
from msb.dataclasses.notification import (NotificationData, EmailNotificationData, YammerNotificationData)
from msb.env import NameConst

from .exceptions import NotificationServiceExceptions
from .msb_service import MsbService


class CeleryService(MsbService):

	def __init__(self, **kwargs):
		super().__init__()
		self.celery = Celery()


class NotificationService(CeleryService):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.queue_name = kwargs.get('queue', settings.MSB_NOTIFICATION_QUEUE_NAME)
		self.service_name = kwargs.get('service', settings.MSB_SERVICE_NAME)

	def send(self, data: NotificationData = None, task_name: str = NameConst.ASYNC_TASK_NAME):
		try:
			if not isinstance(data, NotificationData):
				raise NotificationServiceExceptions.InvalidNotificationData

			self.celery.send_task(name=task_name, args=[self.service_name], kwargs=data.__dict__, queue=self.queue_name)
		except Exception as e:
			self.raise_exceptions(e, NotificationServiceExceptions.NotificationSendFailed)

	def send_email_notification(self, data: EmailNotificationData = None, task: str = None):
		_task = (task or getattr(settings, 'MSB_EMAIL_NOTIFICATION_TASK_NAME', NameConst.EMAIL_NOTIFICATION_TASK_NAME))
		return self.send(data, _task)

	def send_yammer_notification(self, data: YammerNotificationData = None, task: str = None):
		_task = (task or getattr(settings, 'MSB_YAMMER_NOTIFICATION_TASK_NAME', NameConst.YAMMER_NOTIFICATION_TASK_NAME))
		return self.send(data, _task)


__all__ = ['NotificationService', 'NotificationData', 'EmailNotificationData', 'YammerNotificationData']
