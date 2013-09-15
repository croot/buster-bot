# -*- coding: utf-8 -*-

import urllib
import socket
import sys
from urllib import unwrap, toBytes, quote, splittype, splithost, splituser, unquote, addinfourl

class MyURLOpener(urllib.FancyURLopener):
    def open_http(self, url, data=None, method=None):
        data=None
        """Use HTTP protocol."""
        import httplib
        user_passwd = None
        proxy_passwd= None
        if isinstance(url, str):
            host, selector = splithost(url)
            if host:
                user_passwd, host = splituser(host)
                host = unquote(host)
            realhost = host
        else:
            host, selector = url
            # check whether the proxy contains authorization information
            proxy_passwd, host = splituser(host)
            # now we proceed with the url we want to obtain
            urltype, rest = splittype(selector)
            url = rest
            user_passwd = None
            if urltype.lower() != 'http':
                realhost = None
            else:
                realhost, rest = splithost(rest)
                if realhost:
                    user_passwd, realhost = splituser(realhost)
                if user_passwd:
                    selector = "%s://%s%s" % (urltype, realhost, rest)
                if proxy_bypass(realhost):
                    host = realhost

            #print "proxy via http:", host, selector
        if not host: raise IOError, ('http error', 'no host given')

        if proxy_passwd:
            import base64
            proxy_auth = base64.b64encode(proxy_passwd).strip()
        else:
            proxy_auth = None

        if user_passwd:
            import base64
            auth = base64.b64encode(user_passwd).strip()
        else:
            auth = None
        h = httplib.HTTP(host)

        if method is not None:
            h.putrequest(method, selector)
        else:
            h.putrequest('GET', selector)

        if data is not None:
            #h.putrequest('POST', selector)
            h.putheader('Content-Type', 'application/x-www-form-urlencoded')
            h.putheader('Content-Length', '%d' % len(data))

        if proxy_auth: h.putheader('Proxy-Authorization', 'Basic %s' % proxy_auth)
        if auth: h.putheader('Authorization', 'Basic %s' % auth)
        if realhost: h.putheader('Host', realhost)
        for args in self.addheaders: h.putheader(*args)
        h.endheaders()#delete (data) paramater, because this doesnt work on linux
        errcode, errmsg, headers = h.getreply()
        fp = h.getfile()
        if errcode == -1:
            if fp: fp.close()
            # something went wrong with the HTTP status line
            raise IOError, ('http protocol error', 0,
                            'got a bad status line', None)
        # According to RFC 2616, "2xx" code indicates that the client's
        # request was successfully received, understood, and accepted.
        if (200 <= errcode < 300):
            return addinfourl(fp, headers, "http:" + url, errcode)
        else:
            if data is None:
                return self.http_error(url, fp, errcode, errmsg, headers)
            else:
                return self.http_error(url, fp, errcode, errmsg, headers, data)

    def open(self, fullurl, data=None, method=None):
        """Use URLopener().open(file) instead of open(file, 'r')."""
        fullurl = unwrap(toBytes(fullurl))
        # percent encode url, fixing lame server errors for e.g, like space
        # within url paths.
        fullurl = quote(fullurl, safe="%/:=&?~#+!$,;'@()*[]|")
        if self.tempcache and fullurl in self.tempcache:
            filename, headers = self.tempcache[fullurl]
            fp = open(filename, 'rb')
            return addinfourl(fp, headers, fullurl)
        urltype, url = splittype(fullurl)
        if not urltype:
            urltype = 'file'
        if urltype in self.proxies:
            proxy = self.proxies[urltype]
            urltype, proxyhost = splittype(proxy)
            host, selector = splithost(proxyhost)
            url = (host, fullurl) # Signal special case to open_*()
        else:
            proxy = None
        name = 'open_' + urltype
        self.type = urltype
        name = name.replace('-', '_')
        if not hasattr(self, name):
            if proxy:
                return self.open_unknown_proxy(proxy, fullurl, data)
            else:
                return self.open_unknown(fullurl, data)
        try:
            return getattr(self, name)(url, data, method)
        except socket.error, msg:
            raise IOError, ('socket error', msg), sys.exc_info()[2]
