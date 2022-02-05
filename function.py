import math
import re
import copy

class TokenDisc:

	"""
	tokenを解析するためのクラス
	"""
	def __init__( self ):
		self.DEC = 1
		self.INT = 2
		self.FNC = 3
		self.CON = 4
		self.VAR = 5
		self.OPN = 6
		self.CLO = 7
		self.PWR = 8
		self.OP1 = 9
		self.OP2 = 10
		
		self.regs = [
			( self.DEC, re.compile( r'(0|[-]*[1-9][0-9]*|[-])*[.][0-9]+' ) ),
			( self.INT, re.compile( r'(0|[-]*[1-9][0-9]*)' ) ),
			( self.FNC, re.compile( r'(sin|cos|tan|log)' ) ),
			( self.CON, re.compile( r'(pi|e)' ) ),
			( self.VAR, re.compile( r'[a-z][a-z0-9]*' ) ),
			( self.OPN, re.compile( r'[(]' ) ),
			( self.CLO, re.compile( r'[)]' ) ),
			( self.PWR, re.compile( r'\^' ) ),
			( self.OP1, re.compile( r'(\*|/)' ) ),
			( self.OP2, re.compile( r'(\+|\-)' ) ) ]

	def check( self, f ):
		for reg in self.regs:
			p = reg[ 1 ]
			matchObj = p.match( f )
			if matchObj is not None:
				return ( reg[ 0 ], matchObj.group(), matchObj.end() )
		return None

class ExprsDisc:

	"""
	数式を解析するためのクラス
	"""
	def __init__( self ):
		self.tokenDisc = TokenDisc()
		self.tokenes = []

	def analyze( self, text ):
		st = 0
		text = text.replace( " ", "" )
		while( True ):
			res = self.tokenDisc.check( text[ st: ] )
			if res is None:
				break
			# print( res[ 1 ] )
			st += res[ 2 ]

	def check( self, f ):
		text = f.replace( " ", "" )
		self.tokenes = []
		res = self._isFormula( text )
		# print( res )
		return res

	def _isFormula( self, text ):
		"""
		exprs_formulaとして妥当か否かのチェック処理

		Parameters
		----------
		arg1 : self
		arg2 : text
			チェック対象の文字列(空白を含まないこと)

		Returns
		-------
		False
			exprs_formulaとして妥当ではない
		{ result, text, size }
			exprs_formulaとして妥当
			result : True
			text : exprs_formula部分の文字列
			size : 文字列サイズ
		"""

		# exprs_additiveの評価
		res = self._isAdditive( text )
		if res == False:
			return False
		obj = MyFormula( res[ 'obj' ] )
		return {
			'result':True,
			'text':res[ 'text' ],
			'size':res[ 'size' ],
			'obj':obj }

	def _isAdditive( self, text ):
		"""
		exprs_additiveとして妥当か否かのチェック処理

		Parameters
		----------
		arg1 : self
		arg2 : text
			チェック対象の文字列(空白を含まないこと)

		Returns
		-------
		False
			exprs_additiveとして妥当ではない
		{ result, text, size }
			exprs_additiveとして妥当
			result : True
			text : exprs_additive部分の文字列
			size : 文字列サイズ
		"""

		st = 0

		# exprs_multiplicativeの評価

		res_mul = self._isMultiplicative( text[ st: ] )
		if res_mul == False:
			return False
		st += res_mul[ 'size' ]

		# "+"または"-"の評価

		res = self._isPlusMinus( text[ st: ] )
		if res == False:
			obj = MyAdditive( res_mul[ 'obj' ] )
			return {
				'result':True,
				'text':text[ 0:st ],
				'size':st,
				'obj':obj }
		st += res[ 'size' ]

		# exprs_additiveの評価

		res_add = self._isAdditive( text[ st: ] )
		if res_add[ 'result' ] == False:
			return False
		st += res_add[ 'size' ]

		obj = MyAdditive( res_mul[ 'obj' ], res[ 'text' ], res_add[ 'obj' ] )
		return {
			'result':True,
			'text':text[ 0:st ],
			'size':st,
			'obj':obj }

	def _isMultiplicative( self, text ):
		st = 0

		# exprs_powerの評価

		res_pow = self._isPower( text[ st: ] )
		if res_pow == False:
			return False
		st += res_pow[ 'size' ]

		# "*"または"/"の評価

		res = self._isMultiplyDivide( text[ st: ] )
		if res == False:
			obj = MyMultiplicative( res_pow[ 'obj' ] )
			return {
				'result':True,
				'text':text[ 0:st ],
				'size':st,
				'obj':obj }
		st += res[ 'size' ]

		# exprs_multiplicativeの評価

		res_mul = self._isMultiplicative( text[ st: ] )
		if res_mul == False:
			return False
		st += res_mul[ 'size' ]

		obj = MyMultiplicative( res_pow[ 'obj' ], res[ 'text' ], res_mul[ 'obj' ] )
		return {
			'result':True,
			'text':text[ 0:st ],
			'size':st,
			'obj':obj }

	def _isPower( self, text ):
		st = 0

		# exprs_primaryの評価

		res_pri = self._isPrimary( text[ st: ] )
		if res_pri == False:
			return False
		st += res_pri[ 'size' ]

		# "^"の評価

		res = self._isMultiply( text[ st: ] )
		if res == False:
			obj = MyPower( res_pri[ 'obj' ] )
			return {
				'result':True,
				'text':text[ 0:st ],
				'size':st,
				'obj':obj }
		st += res[ 'size' ]

		# exprs_powerの評価

		res_pow = self._isPower( text[ st: ] )
		if res_pow[ 'result' ] == False:
			return False
		st += res_pow[ 'size' ]

		obj = MyPower( res_pri[ 'obj' ], res_pow[ 'obj' ] )
		return {
			'result':True,
			'text':text[ 0:st ],
			'size':st,
			'obj':obj }

	def _isPrimary( self, text ):

		st = 0
		res = self.tokenDisc.check( text[ st: ] )
		if res is None:
			return False
		if res[ 0 ] == self.tokenDisc.CON:
			#------
			# 定数
			#------
			obj = MyPrimary( "constant", res[ 1 ] )
			return {
				'result':True,
				'text':res[ 1 ],
				'size':res[ 2 ],
				'obj':obj }

		if res[ 0 ] == self.tokenDisc.INT:
			#------
			# 整数
			#------
			obj = MyPrimary( "integer", res[ 1 ] )
			return {
				'result':True,
				'text':res[ 1 ],
				'size':res[ 2 ],
				'obj':obj }

		if res[ 0 ] == self.tokenDisc.DEC:
			#------
			# 小数
			#------
			obj = MyPrimary( "decimal", res[ 1 ] )
			return {
				'result':True,
				'text':res[ 1 ],
				'size':res[ 2 ],
				'obj':obj }

		if res[ 0 ] == self.tokenDisc.VAR:
			#------
			# 変数
			#------
			obj = MyPrimary( "variable", res[ 1 ] )
			return {
				'result':True,
				'text':res[ 1 ],
				'size':res[ 2 ],
				'obj':obj }

		if res[ 0 ] == self.tokenDisc.FNC:
			#------
			# 関数
			#------
			st += res[ 2 ]

			res_fnc = res

			res = self.tokenDisc.check( text[ st: ] )
			if res is None:
				return False
			if res[ 0 ] != self.tokenDisc.OPN:
				return False
			st += res[ 2 ]

			res_add = self._isAdditive( text[ st: ] )
			if res_add == False:
				return False
			st += res_add[ 'size' ]

			res = self.tokenDisc.check( text[ st: ] )
			if res is None:
				return False
			if res[ 0 ] != self.tokenDisc.CLO:
				return False
			st += res[ 2 ]

			obj = MyFunction( res_fnc[ 1 ], res_add[ 'obj' ] )

			return {
				'result':True,
				'text':text[ 0:st ],
				'size':st,
				'obj':obj }

		elif res[ 0 ] == self.tokenDisc.OPN:
			#------------------
			# 括弧付きの加算式
			#------------------
			st += res[ 2 ]

			res_add = self._isAdditive( text[ st: ] )
			if res_add == False:
				return False
			st += res_add[ 'size' ]

			res = self.tokenDisc.check( text[ st: ] )
			if res is None:
				return False
			if res[ 0 ] != self.tokenDisc.CLO:
				return False
			st += res[ 2 ]

			return {
				'result':True,
				'text':text[ 0:st ],
				'size':st,
				'obj':res_add[ 'obj' ] }

		return False

	def _isPlusMinus( self, text ):
		res = self.tokenDisc.check( text )
		if res is None:
			return False
		if res[ 0 ] != self.tokenDisc.OP2:
			return False
		return { 'result':True, 'text':res[ 1 ], 'size':res[ 2 ] }

	def _isMultiplyDivide( self, text ):
		res = self.tokenDisc.check( text )
		if res is None:
			return False
		if res[ 0 ] != self.tokenDisc.OP1:
			return False
		return { 'result':True, 'text':res[ 1 ], 'size':res[ 2 ] }

	def _isMultiply( self, text ):
		res = self.tokenDisc.check( text )
		if res is None:
			return False
		if res[ 0 ] != self.tokenDisc.PWR:
			return False
		return { 'result':True, 'text':res[ 1 ], 'size':res[ 2 ] }


class MyFormula:

	def __init__( self, obj ):

		self.value = obj

	def print( self ):

		self.value.print()
		print( "" )

	def getValue( self, varName=None, varVal=None ):
		v = self.value.getValue( varName, varVal )
		return v

	def diff( self, varName ):
		tmp_v = self.value.diff( varName )
		v = MyFormula( tmp_v )
		return v

	def normalization( self ):
		while True:
			res = self.value.normalization( False )
			if res == True:
				continue
			break


class MyFunction:

	def __init__( self, type, obj ):
		"""
		Parameters
		----------
		arg1 : str
			sin, cos, tan, log
		arg2 : class
			MyAdditiveクラス
		"""
		self.type = type
		self.value = obj

	def print( self ):

		print( self.type, end="" )
		print( "(", end="" )
		self.value.print()
		print( ")", end="" )

	def getValue( self, varName=None, varVal=None ):
		v2 = self.value.getValue( varName, varVal )
		if type( v2 ) is not int and type( v2 ) is not float:
			return self.type + "(" + str( v2 ) + ")"

		if self.type == "sin":
			v = math.sin( v2 )
			return v
		elif self.type == "cos":
			v = math.cos( v2 )
			return v
		elif self.type == "tan":
			v = math.tan( v2 )
			return v
		elif self.type == "log":
			v = math.log( v2 )
			return v
			
		return "error"

	def diff( self, varName ):
		if self.type == "sin":
			vp = self.value.diff( varName )
			v = MyFunction( "cos", vp )
			return v
		elif self.type == "cos":
			vp = self.value.diff( varName )
			mo = MyPrimary( "integer", -1 )
			mvp = MyMultiplicative( mo, "*", vp )
			s = MyFunction( "sin", vp )
			v = MyMultiplicative( mvp, "*", s )
			return v
		elif self.type == "tan":
			vp = self.value.diff( varName )
			c = MyFunction( "cos", vp )
			two = MyPrimary( "integer", 2 )
			c2 = MyPower( c, two )
			v = MyMultiplicative( vp, "/", c2 )
			return v
		elif self.type == "log":
			vp = self.value.diff( varName )
			v = MyMultiplicative( vp, "/", self.value )
			return v

class MyAdditive:

	def __init__( self, p1, op=None, p2=None ):

		self.value1 = p1
		self.value2 = p2
		self.operator = op

	def print( self ):

		self.value1.print()
		if self.operator is not None:
			print( self.operator, end="" )
			self.value2.print()

	def getValue( self, varName=None, varVal=None ):
		v1 = self.value1.getValue( varName, varVal )
		if self.operator is None:
			return v1

		v2 = self.value2.getValue( varName, varVal )
		if ( type( v2 ) is int or type( v2 ) is float ) \
			and ( type( v1 ) is int or type( v1 ) is float ):
			if self.operator == "+":
				v = v1 + v2
			else:
				v = v1 - v2
			return v

		return str( v1 ) + self.operator + str( v2 )

	def diff( self, varName ):

		if self.operator is None:
			v = self.value1.diff( varName )
			return v

		p1p = self.value1.diff( varName )
		p2p = self.value2.diff( varName )

		v = MyAdditive( p1p, "+", p2p )

		return v

	def normalization( self, acc ):

		if self.operator is None:
			res = self.value1.normalization( acc )
			return res

		if self.value2.getValue() == 0.0:
			self.operator = None
			self.value2 = None
			return True

		return acc

class MyMultiplicative:

	def __init__( self, p1, op=None, p2=None ):

		self.value1 = p1
		self.value2 = p2
		self.operator = op

	def print( self ):

		self.value1.print()
		if self.operator is not None:
			print( self.operator, end="" )
			self.value2.print()

	def getValue( self, varName=None, varVal=None ):
		v1 = self.value1.getValue( varName, varVal )
		if self.operator is None:
			return v1

		v2 = self.value2.getValue( varName, varVal )
		if ( type( v2 ) is int or type( v2 ) is float ) \
			and ( type( v1 ) is int or type( v1 ) is float ):
			if self.operator == "*":
				v = v1 * v2
			else:
				v = v1 / v2
			return v

		return str( v1 ) + self.operator + str( v2 )

	def diff( self, varName ):
		if self.operator is None:
			v = self.value1.diff( varName )
			return v

		p1p = self.value1.diff( varName )
		p2p = self.value2.diff( varName )

		v1 = MyMultiplicative( p1p, "*", self.value2 )
		v2 = MyMultiplicative( self.value1, "*", p2p )

		v = MyAdditive( v1, "+", v2 )

		return v


class MyPower:

	def __init__( self, p1, p2=None ):

		self.value1 = p1
		self.value2 = p2

	def print( self ):

		self.value1.print()
		if self.value2 is not None:
			print( "^", end="" )
			self.value2.print()

	def getValue( self, varName=None, varVal=None ):
		v1 = self.value1.getValue( varName, varVal )
		if self.value2 is None:
			return v1

		v2 = self.value2.getValue( varName, varVal )
		if ( type( v2 ) is int or type( v2 ) is float ) \
			and ( type( v1 ) is int or type( v1 ) is float ):
			v = v1 ** v2
			return v

		return str( v1 ) + "^" + str( v2 )

	def diff( self, varName ):
		if self.value2 is None:
			v = self.value1.diff( varName )
			return v

		f = copy.deepcopy( self.value1 )
		g = copy.deepcopy( self.value2 )
		fg = MyPower( f, g )

		logf = MyFunction( "log", f )
		gp = g.diff( varName )
		logf_gp = MyMultiplicative( logf, "*", gp )

		one = MyPrimary( "integer", 1 )
		one_f = MyMultiplicative( one, "/", f )
		one_f_g = MyMultiplicative( one_f, "*", g )
		fp = f.diff( varName )
		one_f_g_fp = MyMultiplicative( one_f_g, "*", fp )

		tmp_v = MyAdditive( logf_gp, "+", one_f_g_fp )
		tmp_v2 = MyPrimary( "addition", tmp_v )

		v = MyMultiplicative( fg, "*", tmp_v2 )

		return v

class MyPrimary:

	def __init__( self, type, obj ):
		"""
		Parameters
		----------
		arg1 : str
			integer 整数値
			decimal 小数値
			constant 定数値
			addition 加算式
			function 関数
			variable 変数
		arg2 : class
			integer, decimal
				整数値、小数値を表す文字列
			constant
				定数値を表す文字列(piまたはe)
			variable
				変数を表す文字列
			addition
				MyAdditiveクラス
			function
				MyFunctionクラス
		"""
		self.INTEGER = 1
		self.DECIMAL = 2
		self.CONSTANT = 3
		self.ADDITION = 4
		self.FUNCTION = 5
		self.VARIABLE = 6
		self.ERROR = 99

		if type == "integer":
			self.type = self.INTEGER
			self.value = int( obj )
		elif type == "decimal":
			self.type = self.DECIMAL
			self.value = float( obj )
		elif type == "constant":
			self.type = self.CONSTANT
			self.value = obj
		elif type == "variable":
			self.type = self.VARIABLE
			self.value = obj
		elif type == "addition":
			self.type = self.ADDITION
			self.value = obj
		elif type == "function":
			self.type = self.FUNCTION
			self.value = obj
		else:
			self.type = self.ERROR

	def print( self ):

		if self.type == self.INTEGER or self.type == self.DECIMAL:
			print( self.value, end="" )
		elif self.type == self.CONSTANT:
			print( self.value, end="" )
		elif self.type == self.VARIABLE:
			print( self.value, end="" )
		elif self.type == self.FUNCTION:
			self.value.print()
		elif self.type == self.ADDITION:
			print( "(", end="" )
			self.value.print()
			print( ")", end="" )
		else:
			print( "error!!!", end="" )

	def getValue( self, varName=None, varVal=None ):

		if self.type == self.INTEGER:
			return self.value
		elif self.type == self.DECIMAL:
			return self.value
		elif self.type == self.CONSTANT:
			if self.value == "pi":
				return 3.14159265
			elif self.value == "e":
				return 2.71828183
		elif self.type == self.VARIABLE:
			if varName is not None and self.value == varName:
				return varVal
			else:
				return self.value
		elif self.type == self.FUNCTION:
			return self.value.getValue()
		elif self.type == self.ADDITION:
			v = self.value.getValue()
			if type( v ) is int or type( v ) is float:
				return v
			return "(" + v + ")"

		return "error"

	def diff( self, varName ):

		#------
		# 数値
		#------
		if self.type == self.INTEGER \
			or self.type == self.DECIMAL \
			or self.type == self.CONSTANT:

			v = MyPrimary( "integer", 0 )
			return v

		#------
		# 変数
		#------
		if self.type == self.VARIABLE:
			if self.value == varName:
				v = MyPrimary( "integer", 1 )
				return v
			else:
				v = MyPrimary( "integer", 0 )
				return v

		#------
		# 関数
		#------
		if self.type == self.FUNCTION:
			v = self.value.diff( varName )
			return v

		#--------
		# 加算式
		#--------
		if self.type == self.ADDITION:
			v = self.value.diff( varName )
			return v

		return None

	def normalization( self ):
		if self.type == self.FUNCTION:
			res = self.value.normalization()
			return res
		if self.type == self.ADDITION:
			res = self.value.normalization()
			return res
		return None


class function:

	def __init__( self, text ):
		"""
		関数を定義する

		Parameters
		----------
		args1 : self
		args2 : text
			関数を表す文字列

		Returns
		-------
		なし
		"""

		self.object = ( ExprsDisc().check( text ) )[ 'obj' ]
		return

	def print( self ):
		"""
		関数を表示する

		Parameters
		----------
		args1 : self

		Returns
		-------
		なし
		"""

		self.object.print()
		return

	def diff( self, variable ):
		"""
		微分する

		Parameters
		----------
		args1 : self
		args2 : variable
			微分対象の変数の文字列

		Returns
		-------
		function
			微分後の関数
		"""

		return self.object.diff( variable )

	def getValue( self, variable, value ):
		"""
		値の取得

		Parameters
		----------
		args1 : self
		args2 : variable
			変数の文字列
		args3 : value
			値（数値）

		Returns
		-------
		値
		"""

		return self.object.getValue( variable, value )


# import function
# f = function.function( "x^2" )
# f.print()
# v = f.getValue( "x", 1 )
# g = f.diff( "x" )
# g.print()

# text = "x^2"
# disc = ExprsDisc()
# o = disc.check( text )
# 
# t = type( o[ 'obj' ] )
# print( t )
# o[ 'obj' ].print()
# v = o[ 'obj' ].getValue( "x", 4 )
# print( v )
# 
# vp = o[ 'obj' ].diff( "x" )
# vp.print()
# 
# a = vp.getValue( "x", 0 )
# print( "value is ", end="" )
# print( a )


		

