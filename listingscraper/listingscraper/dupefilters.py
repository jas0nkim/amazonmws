from scrapy.dupefilters import RFPDupeFilter

class DisabledDupeFilter(RFPDupeFilter):

	# commented out duplication check
    def request_seen(self, request):
        fp = self.request_fingerprint(request)
        # if fp in self.fingerprints:
        #     return True
        self.fingerprints.add(fp)
        if self.file:
            self.file.write(fp + os.linesep)
