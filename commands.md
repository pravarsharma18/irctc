## bulk delete django
 t = Train.objects.all()
 t._raw_delete(t.db)

 ## Celery
    ###  Verify Celery Runs
        - celery -A irctc worker --beat
        - celery -A irctc beat
    ### Execute our shared_tasks
        - celery -A irctc worker -l info --beat