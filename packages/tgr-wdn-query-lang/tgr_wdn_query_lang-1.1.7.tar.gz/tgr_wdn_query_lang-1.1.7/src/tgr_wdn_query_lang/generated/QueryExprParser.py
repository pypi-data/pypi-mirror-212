# Generated from QueryExprParser.g4 by ANTLR 4.12.0
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,16,33,2,0,7,0,2,1,7,1,1,0,5,0,6,8,0,10,0,12,0,9,9,0,1,0,1,0,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1,
        28,8,1,1,1,3,1,31,8,1,1,1,0,0,2,0,2,0,0,36,0,7,1,0,0,0,2,27,1,0,
        0,0,4,6,3,2,1,0,5,4,1,0,0,0,6,9,1,0,0,0,7,5,1,0,0,0,7,8,1,0,0,0,
        8,10,1,0,0,0,9,7,1,0,0,0,10,11,5,0,0,1,11,1,1,0,0,0,12,13,5,1,0,
        0,13,14,5,3,0,0,14,28,5,15,0,0,15,16,5,1,0,0,16,17,5,3,0,0,17,28,
        5,16,0,0,18,19,5,1,0,0,19,20,5,3,0,0,20,28,5,12,0,0,21,22,5,1,0,
        0,22,23,5,3,0,0,23,28,5,13,0,0,24,25,5,1,0,0,25,26,5,3,0,0,26,28,
        5,14,0,0,27,12,1,0,0,0,27,15,1,0,0,0,27,18,1,0,0,0,27,21,1,0,0,0,
        27,24,1,0,0,0,28,30,1,0,0,0,29,31,5,10,0,0,30,29,1,0,0,0,30,31,1,
        0,0,0,31,3,1,0,0,0,3,7,27,30
    ]

class QueryExprParser ( Parser ):

    grammarFileName = "QueryExprParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'!='", "'>'", "'>='", "'<'", "'<='", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'NULL'" ]

    symbolicNames = [ "<INVALID>", "IDENTIFIER", "WS", "OPERATOR", "EQ", 
                      "NE", "GT", "GE", "LT", "LE", "LABEL", "DELIMITER", 
                      "NUMBER", "BOOL", "NULL", "STRING", "STRING_QUOTED" ]

    RULE_exprs = 0
    RULE_expr = 1

    ruleNames =  [ "exprs", "expr" ]

    EOF = Token.EOF
    IDENTIFIER=1
    WS=2
    OPERATOR=3
    EQ=4
    NE=5
    GT=6
    GE=7
    LT=8
    LE=9
    LABEL=10
    DELIMITER=11
    NUMBER=12
    BOOL=13
    NULL=14
    STRING=15
    STRING_QUOTED=16

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.12.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ExprsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(QueryExprParser.EOF, 0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QueryExprParser.ExprContext)
            else:
                return self.getTypedRuleContext(QueryExprParser.ExprContext,i)


        def getRuleIndex(self):
            return QueryExprParser.RULE_exprs

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExprs" ):
                listener.enterExprs(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExprs" ):
                listener.exitExprs(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExprs" ):
                return visitor.visitExprs(self)
            else:
                return visitor.visitChildren(self)




    def exprs(self):

        localctx = QueryExprParser.ExprsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_exprs)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 7
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1:
                self.state = 4
                self.expr()
                self.state = 9
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 10
            self.match(QueryExprParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(QueryExprParser.IDENTIFIER, 0)

        def OPERATOR(self):
            return self.getToken(QueryExprParser.OPERATOR, 0)

        def STRING(self):
            return self.getToken(QueryExprParser.STRING, 0)

        def STRING_QUOTED(self):
            return self.getToken(QueryExprParser.STRING_QUOTED, 0)

        def NUMBER(self):
            return self.getToken(QueryExprParser.NUMBER, 0)

        def BOOL(self):
            return self.getToken(QueryExprParser.BOOL, 0)

        def NULL(self):
            return self.getToken(QueryExprParser.NULL, 0)

        def LABEL(self):
            return self.getToken(QueryExprParser.LABEL, 0)

        def getRuleIndex(self):
            return QueryExprParser.RULE_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr" ):
                listener.enterExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr" ):
                listener.exitExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr" ):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)




    def expr(self):

        localctx = QueryExprParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 27
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.state = 12
                self.match(QueryExprParser.IDENTIFIER)
                self.state = 13
                self.match(QueryExprParser.OPERATOR)
                self.state = 14
                self.match(QueryExprParser.STRING)
                pass

            elif la_ == 2:
                self.state = 15
                self.match(QueryExprParser.IDENTIFIER)
                self.state = 16
                self.match(QueryExprParser.OPERATOR)
                self.state = 17
                self.match(QueryExprParser.STRING_QUOTED)
                pass

            elif la_ == 3:
                self.state = 18
                self.match(QueryExprParser.IDENTIFIER)
                self.state = 19
                self.match(QueryExprParser.OPERATOR)
                self.state = 20
                self.match(QueryExprParser.NUMBER)
                pass

            elif la_ == 4:
                self.state = 21
                self.match(QueryExprParser.IDENTIFIER)
                self.state = 22
                self.match(QueryExprParser.OPERATOR)
                self.state = 23
                self.match(QueryExprParser.BOOL)
                pass

            elif la_ == 5:
                self.state = 24
                self.match(QueryExprParser.IDENTIFIER)
                self.state = 25
                self.match(QueryExprParser.OPERATOR)
                self.state = 26
                self.match(QueryExprParser.NULL)
                pass


            self.state = 30
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==10:
                self.state = 29
                self.match(QueryExprParser.LABEL)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





