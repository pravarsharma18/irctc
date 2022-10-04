## bulk delete django
 t = Train.objects.all()
 t._raw_delete(t.db)