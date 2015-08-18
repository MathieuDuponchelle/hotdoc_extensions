import os

from better_doc_tool.core.base_extension import BaseExtension
from better_doc_tool.core.doc_tool import doc_tool
from better_doc_tool.core.symbols import FunctionSymbol

class SourceCodeLinker(BaseExtension):
    EXTENSION_NAME="scl-extension"

    def __init__(self, args):
        BaseExtension.__init__(self, args)
        self.__link_pattern = args.scl_pattern
        self.__local_prefix = os.path.abspath(args.scl_prefix)

    @staticmethod
    def add_arguments (parser):
        parser.add_argument ("--scl-pattern", action="store", required=True,
                dest="scl_pattern", help="Pattern to use to create the link")
        parser.add_argument ("--scl-prefix", action="store", required=True,
                dest="scl_prefix", help="Prefix to remove from the absolute path")

    def __symbol_formatted (self, symbol):
        if not symbol.comment:
            return
        filelink = os.path.relpath (symbol.comment.filename, self.__local_prefix)
        link = self.__link_pattern % (filelink, symbol.comment.lineno)
        symbol.comment.description += "\n[Visit source code](%s)" % link

    def setup(self):
        doc_tool.formatter.formatting_symbol_signals[FunctionSymbol].connect(
                self.__symbol_formatted)
