#!/usr/bin/env python
import zarafa
import mailbox

from zarafa import Folder

ignored_folders = [ 'Suggested Contacts',
                    'Quick Step Settings',
                    'Conversation Action Settings',
                    'RSS Feeds',
                    'Junk E-mail',
                    'Tasks',
                    'Notes',
                    'Journal',
                    'Calendar',
                    'Contacts',
                    'Deleted Items',
                    'Outbox' ]

def mymbox(self, location):
    maildir = location.add_folder(self.name)
    maildir.lock()
    for item in self.items():
        maildir.add(item.eml())
    maildir.unlock()

Folder.mbox = mymbox

def main():
    s = zarafa.Server()
    for user in s.users(remote=False):
        print 'user:', user.name
        if user.store:
            maildir = mailbox.Maildir(user.name)
            for folder in user.store.folders(recurse=True, parse=True):
                if folder.name in ignored_folders:
                    continue
                print '  folder: count=%s size=%s %s%s' % (str(folder.count).ljust(8), str(folder.size).ljust(10), folder.depth*'    ', folder.name)
                folder.mbox(maildir)

if __name__ == '__main__':
    main()
