import sys
import requests
from json import dumps
from urllib import urlencode


version = VERSION = __version__ = '0.0.1'


class protopay(object):
    def __init__(self, args):
        self.args = dict(auth=args.auth, url=args.url,
                         func=None, json=args.json)

        res = getattr(self, args.func.replace(':','_'))(**dict([(k,v) for k,v in args._get_kwargs() if k not in self.args]))
        if res:
            if self.json:
                return dumps(res.json(), indent=2, sort_keys=True)
            else:
                sys.stdout.write(res.text)
        self.result = res

    def __getattr__(self, index):
        return self.args[index]

    def _fetch(self, method, endpoint, query={}, body=None):
        ext = ".json" if self.json else ".txt"
        body = dumps(body)
        query = ("?%s"%urlencode(query)) if query else ""

        res = getattr(requests, method)("/".join([self.url]+map(str,endpoint)) + ext + query,
                                        headers={"User-Agent": "protopay v%s"%version, "Authorization": "token %s"%self.auth},
                                        data=body)
        return res

    def write(self, message):
        sys.stdout.write(message+"\n")

    # Starting Endpoints
    # ==================
    def charges(self):
        return self._fetch('get', ('charges', ))

    def charges_complete(self, id, tip=None):
        return self._fetch('put', ('charges', id[0]), body=dict(tip=tip))

    def requests(self):
        return self._fetch('get', ('requests', ))

    def help(self):
        sys.stdout.write(protopay.__doc__)

    def test(self, number, exp_month, exp_year):
        """run tests on an account
        """
        self.write('=========== Pre Auth ===========')
        res = self._fetch('post', ('charges', ), body=dict(number=number, exp_month=exp_month, exp_year=exp_year, amount=1, preauth=True))
        data = res.json()
        self.write('HTTP %d' % res.status_code)
        self.write(dumps(data, indent=2))
        assert data['charges'][0]['status'] == 'approved'

        self.write('=========== Pre Auth Complete w/ 100% tip ===========')
        res = self._fetch('put', ('charges', data['charges'][0]['id']), body=dict(tip=1))
        data = res.json()
        self.write('HTTP %d' % res.status_code)
        self.write(dumps(data, indent=2))
        assert data['charges'][0]['status'] == 'approved'

        self.write('=========== Delete ===========')
        res = self._fetch('delete', ('charges', data['charges'][0]['id']))
        data = res.json()
        self.write('HTTP %d' % res.status_code)
        self.write(dumps(data, indent=2))
        assert data['charges'][0]['status'] in ('voided', 'refunded')
