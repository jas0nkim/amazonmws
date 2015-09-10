from storm.locals import *

class DiscoveredItem(object):
	__storm_table__ = 'discovered_items'
	id = Int(primary=True)
	url = Unicode()
	asin = Unicode()
	title = Unicode()
	created_at = DateTime()
	updated_at = DateTime()

__db = create_database('mysql://writeuser:123spirit@localhost/amazonmws')
StormStore = Store(__db)
