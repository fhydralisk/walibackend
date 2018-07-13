

class AbstractPusher(object):

    def send_push_to(self, content, extra, all_devices, raise_exception, **kwargs):
        raise NotImplementedError

    def send_push_to_phones(self, content, extra, pns, raise_exception, **kwargs):
        def to_md5(pn):
            import hashlib
            h1 = hashlib.md5()
            h1.update(pn)
            return h1.hexdigest()

        pns_md5 = map(to_md5, pns)
        self.send_push_to(content, extra, alias=pns_md5, raise_exception=raise_exception, all_devices=False)
