from contextlib import contextmanager
from os.path import expanduser, dirname
import os
import json
import xerox
import tempfile
from subprocess import Popen, PIPE
#file format not stable!
hfile = expanduser("~/histfile_test")
nhistory = 30

selections = {
    '*': 'primary',
    '+': 'clipboard'
}

modemap = {
    'v': 'c',
    'V': 'L',
}

#TODO: config interface?
stickychoice = True

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

# pure documentative for now
rpcHandler = lambda f: f

class NvimYanklist(object):
    def __init__(self, vim):
        self.provides = ['clipboard']
        self.choice = None

        vim.command("let g:yanklist_channel = {}".format(vim.channel_id)) #FIXME

    def sel_name(self, reg):
        return 'clipboard' if reg == '+' else 'primary'
        

    def clipboard_get(self, reg):
        if reg in selections:
            txt = Popen(['xclip', '-selection', selections[reg], '-o'], stdout=PIPE).communicate()[0]
            # emulate vim behavior
            if txt.endswith('\n'):
                txt = txt[:-1]
                regtype = 'V'
            else:
                regtype = 'v'
            return txt.split('\n'), regtype
        else:
            if self.choice is not None:
                c = self.choice
                self.choice = None
                return c
            with HistoryFile(hfile) as hlist:
                if len(hlist) == 0:
                    return ''
                return hlist[0]

    def clipboard_set(self, lines, regtype, reg):
        if reg in selections:
            txt = '\n'.join([line for line in lines])
            if regtype == 'V':
                txt = txt + '\n'
            _cmd = ['xclip', '-selection', selections[reg]]
            Popen(_cmd, stdin=PIPE).communicate(txt)
            if reg == '*': return

        with HistoryFile(hfile,'w') as hlist:
            for i,val in enumerate(list(hlist)):
                if val[0] == lines:
                    del hlist[i]
                    break
            hlist.insert(0, [lines, regtype])
            if len(hlist) > nhistory:
                del hlist[nhistory+1:]

    @rpcHandler
    def yanklist_choose(self, c):
        if stickychoice:
            # push pasted to front
            self.clipboard_set(c[0],c[1], '"')
        else:
            self.choice = c

    @rpcHandler
    def yanklist_candidates(self):
        c = []
        try:
            with HistoryFile(hfile) as hlist:
                for i,t in enumerate(hlist):
                    m = modemap.get(t[1],t[1])
                    txt = '\n'.join(t[0])
                    c.append({'action__value': t,
                        'word': '{} {} {!r}'.format(i+1, m, '\n'.join(t[0]))})
            return c
        except:
            import traceback
            traceback.print_exc()
            return []

