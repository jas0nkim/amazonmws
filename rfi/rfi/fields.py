from django.db.models import ForeignKey, OneToOneField

class RfiForeignKey(ForeignKey):

    def get_attname(self):
        return self.db_column if self.db_column else '%s_id' % self.name

class RfiOneToOneField(OneToOneField):

    def get_attname(self):
        return self.db_column if self.db_column else '%s_id' % self.name
