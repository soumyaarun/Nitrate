.. _configuration:

Configuration Settings
======================

Asynchronous Task
-----------------

ASYNC_TASK
~~~~~~~~~~

By default, Nitrate runs registered tasks in a synchronous way. It would be
good for development, running tests, or even in a deployed server at most
cases. On the other hand, Nitrate also allows to run tasks in asynchronous way.
There are three choices for ``ASYNC_TASK``:

* ``DISABLED``: run tasks in synchronous way. This is the default.

* ``THREADING``: run tasks in a separate thread using Python ``threading``
  module. The created thread for tasks is set to run in daemon mode by setting
  ``Thread.daemon`` to True.

* ``CELERY``: Nitrate works with Celery together to run tasks. Tasks are
  scheduled in a queue and configured Celery workers will handle those
  separately.

Celery settings
---------------

Nitrate has a group of Celery settings in ``common`` settings module. Each of
them could be changed according to requirement of concrete environment. Any
other necessary Celery settings can be set in settings module as well.

* ``CELERY_BROKER_URL``
* ``CELERY_TASK_RESULT_EXPIRES``
* ``CELERY_RESULT_BACKEND``
* ``CELERYD_TIMER_PRECISION``
* ``CELERY_IGNORE_RESULT``
* ``CELERY_MAX_CACHED_RESULTS``
* ``CELERY_DEFAULT_RATE_LIMIT``
