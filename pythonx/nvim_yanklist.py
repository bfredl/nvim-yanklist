from contextlib import contextmanager
from os.path import expanduser, dirname
import os
import json
import xerox
import tempfile

#file format not stable!
hfile = expanduser("~/histfile_test")
@contextmanager
def HistoryFile(fn, mode='r'):
    try:
        with open(fn,'r') as f:
            contents = f.read()
            hlist = json.loads(contents)
    except IOError:
        hlist = []
    yield hlist
    if mode == 'w':
        js = json.dumps(hlist)
        with tempfile.NamedTemporaryFile(
                'w', dir=dirname(fn), delete=False) as tf:
            tf.write(js)
            tempname = tf.name
        os.rename(tempname, fn)

class NvimYanklist(object):
    def __init__(self, vim):
        print "xx"
        self.provides = ['clipboard_get', 'clipboard_set', 'yanklist_candidates']

        vim.command("let g:yanklist_channel = {}".format(vim.channel_id)) #FIXME

    def clipboard_get(self):
        return xerox.paste().split('\n')

    def clipboard_set(self, lines):
        txt = '\n'.join(lines)
        xerox.copy(txt)
        with HistoryFile(hfile,'w') as hlist:
            try:
                hlist.remove(txt)
            except ValueError:
                pass
            hlist.insert(0,txt)

    def yanklist_candidates(self):
        c = []
        try:
            with HistoryFile(hfile) as hlist:
                for i,t in enumerate(hlist):
                    c.append({'action__text': t,
                        'action__regtype': ('V' if ('\n' in t) else 'v'),
                        'word': '{} {!r}'.format(i+1, t)})
            return c
        except:
            import traceback
            traceback.print_exc()
            return []

