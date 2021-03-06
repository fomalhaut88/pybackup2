from models.base_command import BaseCommand
from models.source import SourceList


class SourceShow(BaseCommand):
    title = 'source-show'
    args = ()
    doc = "Shows added sources."

    def execute(self):
        source_list = SourceList()

        if source_list:
            print("%-40s%-50s%s" % ("=*= HASH =*=", "=*= SOURCE =*=", "=*= TARGET =*="))
            for source in source_list:
                print("%-40s%-50s%s" % (source.hash, source.src, source.trg))
        else:
            print("no sources")
