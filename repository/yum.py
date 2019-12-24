# coding=utf-8
import os, os.path
import shutil
import subprocess
import xml.dom.minidom
import requests
import time
import gzip
import calendar



class Yum:
    def __init__(self, dir_path, address_server):
        self.log = ""
        self.dir_path = "/" + dir_path
        self.address_server = address_server

    def download(self, path, if_modified_since = True, stream = False):
        url      = self.address_server + "/" + path;
        filepath = self.dir_path       + "/" + path;

        headers = { }

        if if_modified_since:
            try:
                mod_time = os.path.getmtime(filepath);
                headers["If-Modified-Since"] = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(mod_time));
            except OSError as e:
                pass

        r = requests.get(url, headers=headers, stream=stream)

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        if r.status_code == 200:
            mod_time = None;
            if 'Last-Modified' in r.headers:
                mod_time = calendar.timegm(time.strptime(r.headers['Last-Modified'], "%a, %d %b %Y %H:%M:%S %Z"))

            if stream:
                with open(filepath, 'wb') as fd:
                    for chunk in r.iter_content(chunk_size=10*1024*1024):
                        fd.write(chunk)

                if mod_time:
                    os.utime(filepath, (mod_time, mod_time))

                return (r.status_code, None)
            else:
                with open(filepath, 'wb') as fd:
                    fd.write(r.content)

                if mod_time:
                    os.utime(filepath, (mod_time, mod_time))

                return (r.status_code, r.content)
        else:
            return (r.status_code, None)

        # --------

    def update(self):
        # ----

        tree_before = []
        for i in os.walk(self.dir_path):
            tree_before.append(i)

        downloaded_set = set()

        # ----

        (http_code, repomd_content)  = self.download( 'repodata/repomd.xml' );

        if http_code == 304:
            return (0, "ok")
        elif http_code != 200:
            return (1, "Error on download repodata/repomd.xml: " + http_code)

        downloaded_set.add('repodata/repomd.xml');

        # ----

        ( http_code, IGNORE ) = self.download( 'repodata/repomd.xml.asc', False, True);
        if http_code == 200:
            downloaded_set.add('repodata/repomd.xml.asc');

        # ----

        rpms = set();

        dom = xml.dom.minidom.parseString(repomd_content)
        dom.normalize()
        nodes = dom.getElementsByTagName("location")
        for location in nodes:
            metafile = location.getAttribute('href')
            is_primary = metafile.endswith("primary.xml") or metafile.endswith("primary.xml.gz")

            if is_primary:
                (http_code, primary_content) = self.download(metafile, False);
                if http_code != 200:
                    return (1, "Error on download " + metafile + ": " + http_code)

                if metafile.endswith("primary.xml.gz"):
                    primary_content = gzip.decompress(primary_content)

                primary = xml.dom.minidom.parseString(primary_content)
                primary.normalize()
                for rpm_location in primary.getElementsByTagName("location"):
                    rpms.add(rpm_location.getAttribute('href'))
            else:
                (http_code, IGNORE) = self.download(metafile, False, True);
                if http_code != 200:
                    return (1, "Error on download " + metafile + ": " + http_code)


            downloaded_set.add(metafile)

        # ----

        for rpm in rpms:
            (http_code, IGNORE) = self.download(rpm, True, True);
            if http_code != 200 and http_code != 304:
                return (1, "Error on download " + rpm + ": " + http_code)

            downloaded_set.add(rpm)

        # ----

        for address, dirs, files in tree_before:
            for file in files:
                path = address + '/' + file;
                rel_path = os.path.relpath(path, self.dir_path);
                if not (rel_path in downloaded_set):
                    os.remove(path);

        # ----

        return (0, "Ok")