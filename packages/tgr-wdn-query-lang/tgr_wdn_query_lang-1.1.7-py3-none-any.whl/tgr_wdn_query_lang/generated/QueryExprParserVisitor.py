# Generated from QueryExprParser.g4 by ANTLR 4.12.0
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .QueryExprParser import QueryExprParser
else:
    from QueryExprParser import QueryExprParser

# This class defines a complete generic visitor for a parse tree produced by QueryExprParser.

class QueryExprParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by QueryExprParser#exprs.
    def visitExprs(self, ctx:QueryExprParser.ExprsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QueryExprParser#expr.
    def visitExpr(self, ctx:QueryExprParser.ExprContext):
        return self.visitChildren(ctx)



del QueryExprParser