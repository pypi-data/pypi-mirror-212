class Ordinal: #基本的にあるのはOrdinal([(0,0)])だけ。あとはカントール標準形でのみ生成する。
  def __init__(self,l):
    if l != []:
      self.l = l
    else:
      self.l = [(0,0)]
  
  def __repr__(self):
    if self.is_finit():
      return str(int(self))
    l = self.l
    s = []
    for i in l:
      if i[0] == 1:
        if i[1] == 0:
          s.append("1")
        elif i[1] == 1:
          s.append("omega")
        else:
          p = repr(i[1])
          if "+" in p or "*" in p or "**" in p:
            s.append(f"omega**({p})")
          else:
            s.append(f"omega**{p}")
      else:
        if i[1] == 0:
          s.append(f"{i[0]}")
        elif i[1] == 1:
          s.append(f"omega*{i[0]}")
        else:
          p = str(i[1])
          if "+" in p or "*" in p or "**" in p:
            s.append(f"omega**({p})*{i[0]}")
          else:
            s.append(f"omega**{p}*{i[0]}")
    return " + ".join(s)

  def __str__(self):
    if self.is_finit():
      return str(int(self))
    l = self.l
    s = []
    for i in l:
      if i[0] == 1:
        if i[1] == 0:
          s.append("1")
        elif i[1] == 1:
          s.append("ω")
        else:
          p = str(i[1])
          if "+" in p or "*" in p or "^" in p:
            s.append(f"ω^({p})")
          else:
            s.append(f"ω^{p}")
      else:
        if i[1] == 0:
          s.append(f"{i[0]}")
        elif i[1] == 1:
          s.append(f"ω*{i[0]}")
        else:
          p = str(i[1])
          if "+" in p or "*" in p or "^" in p:
            s.append(f"ω^({p})*{i[0]}")
          else:
            s.append(f"ω^{p}*{i[0]}")
    return " + ".join(s)

  def is_zero(self):
    if len(self.l) == 1 and type(self.l[0][1]) == int and self.l == [(0,0)]: #0であるか？
      return True
    return False

  def is_finit(self):
    if self.is_zero():
      return True
    if len(self.l) == 1 and type(self.l[0][1]) == Ordinal and self.l[0][1].is_zero(): #1以上の自然数か？
      return True
    return False

  def _richcmp(self,other):
    if self.is_zero():
      if other.is_zero():
        #print("premitive")
        return None
      else:
        return True
    else:
      if other.is_zero():
        return False
    for i in range(min(len(self.l),len(other.l))):
      B = self.l[i][1]._richcmp(other.l[i][1])
      #print(B)
      if B == True:
        return True
      elif B == False:
        return False
      if self.l[i][0] < other.l[i][0]:
        return True
      elif self.l[i][0] > other.l[i][0]:
        return False
    if len(self.l) == len(other.l):
      return None
    elif len(self.l) < len(other.l):
      return True
    else:
      return False

  def __eq__(self,other):
    #int型が混ざったときの処理
    if type(self) == int and type(other) == Ordinal:
      if self == 0:
        return Ordinal([(0,0)]) == other
      else:
        return Ordinal([(self,Ordinal([(0,0)]))]) == other
    if type(self) == Ordinal and type(other) == int:
      if other == 0:
        return self == Ordinal([(0,0)])
      else:
        return self == Ordinal([(other,Ordinal([(0,0)]))])
    #通常の処理
    B = self._richcmp(other)
    return B == None

  def __le__(self,other): # 'le' means 'self is less than or equal other'
    #int型が混ざったときの処理
    if type(self) == int and type(other) == Ordinal:
      if self == 0:
        return Ordinal([(0,0)]) <= other
      else:
        return Ordinal([(self,Ordinal([(0,0)]))]) <= other
    if type(self) == Ordinal and type(other) == int:
      if other == 0:
        return self <= Ordinal([(0,0)])
      else:
        return self <= Ordinal([(other,Ordinal([(0,0)]))])
    #通常の処理
    B = self._richcmp(other)
    return (B == True) or (B == None)


  def __lt__(self,other):
    #int型が混ざったときの処理
    if type(self) == int and type(other) == Ordinal:
      if self == 0:
        return Ordinal([(0,0)]) < other
      else:
        return Ordinal([(self,Ordinal([(0,0)]))]) < other
    if type(self) == Ordinal and type(other) == int:
      if other == 0:
        return self < Ordinal([(0,0)])
      else:
        return self < Ordinal([(other,Ordinal([(0,0)]))])
    #通常の処理
    B = self._richcmp(other)
    return B == True


  def __ge__(self,other):
    #int型が混ざったときの処理
    if type(self) == int and type(other) == Ordinal:
      if self == 0:
        return Ordinal([(0,0)]) >= other
      else:
        return Ordinal([(self,Ordinal([(0,0)]))]) >= other
    if type(self) == Ordinal and type(other) == int:
      if other == 0:
        return self >= Ordinal([(0,0)])
      else:
        return self >= Ordinal([(other,Ordinal([(0,0)]))])
    #通常の処理
    B = self._richcmp(other)
    return (B == False) or (B == None)

  def __gt__(self,other):
    #int型が混ざったときの処理
    if type(self) == int and type(other) == Ordinal:
      if self == 0:
        return Ordinal([(0,0)]) > other
      else:
        return Ordinal([(self,Ordinal([(0,0)]))]) > other
    if type(self) == Ordinal and type(other) == int:
      if other == 0:
        return self > Ordinal([(0,0)])
      else:
        return self > Ordinal([(other,Ordinal([(0,0)]))])
    #通常の処理
    B = self._richcmp(other)
    return B == False

  def __ne__(self,other):
    #int型が混ざったときの処理
    if type(self) == int and type(other) == Ordinal:
      if self == 0:
        return Ordinal([(0,0)]) != other
      else:
        return Ordinal([(self,Ordinal([(0,0)]))]) != other
    if type(self) == Ordinal and type(other) == int:
      if other == 0:
        return self != Ordinal([(0,0)])
      else:
        return self != Ordinal([(other,Ordinal([(0,0)]))])
    #通常の処理
    B = self._richcmp(other)
    return (B == True) or (B == False)

  def __int__(self):
    if self.is_zero():
      return 0
    elif self.is_finit():
      return self.l[0][0]
    return -1

  def normed(self):
    if self == Ordinal([(0,0)]):
      return Ordinal([(0,0)])
    l = list(self.l)
    for x in range(len(l)):
      l[x] = (l[x][0],l[x][1].normed())
    #print(l)
    i = 0
    while i < len(l):
      if i == 0:
        i += 1
        #print(i,l)
      elif l[i-1][1] < l[i][1]:
        l = self.l[:i-1] + l[i:]
        i -= 1
        #print(i,l)
      elif l[i-1][1] > l[i][1]:
        i += 1
        #print(i,l)
      else:
        l = l[:i-1] + [(l[i-1][0] + l[i][0],l[i][1])] + l[i+1:]
        i -= 1
        #print(i,l)
    return Ordinal(l)

  def __add__(self,other):
    #int型が混ざったときの処理
    if type(self) == Ordinal and type(other) == int:
      if other == 0:
        return self
      else:
        return self + Ordinal([(other,Ordinal([(0,0)]))])
    #そもそも二項とも0でないことを仮定する
    if self.is_zero():
      return other
    elif other.is_zero():
      return self
    #まず二分探索でotherの最高次の指数に対応するselfの指数の位置を調べる
    l_index = [i[1] for i in self.l] #指数の配列
    a = other.l[0][1]
    right = len(l_index)
    left = 0
    #print(left,right,None,l_index[left:right+1])
    while left < right:
      mid = (right+left)//2
      # left ~ mid の範囲にあるか？
      B = l_index[mid]._richcmp(a) # l_index[mid] < a の意
      if B == False:
        left = mid+1
      elif B == True:
        right = mid
      else:
        index = mid+1
        break
      #print(left,right,mid,l_index[left:right+1])
    if left == right:
      index = left
    #計算部分
    L = self.l[:index]
    if L == []:
      L = list(other.l)
    elif L[-1][1] == a:
      L[-1] = (L[-1][0]+other.l[0][0],a)
      L = L + other.l[1:]
    else:
      L = L + other.l
    return Ordinal(L)
    

  def __radd__(self,other):
    if type(self) == Ordinal and type(other) == int:
      if other == 0:
        return self
      else:
        return Ordinal([(other,Ordinal([(0,0)]))]) + self

  def __sub__(self,other): #a-b,,,self-other
    if type(self) == Ordinal and type(other) == int:
      if other == 0:
        return self
      else:
        return self - Ordinal([(other,Ordinal([(0,0)]))])
    #そもそも結果が負にならないことが前提
    if self < other:
      return None
    #そもそもself=otherでないことを確認する
    if self == other:
      return Ordinal([(0,0)])
    #そもそも二項とも0でないことを仮定する。other!=0なら、self >= other > 0より両方調べたことになる。
    if other.is_zero():
      return self
    #まずω^(a_r)*n_r > ω^(b_r)*m_rとなる初めてのrを探す。
    r = 0
    while r < len(other.l):
      if self.l[r][1] > other.l[r][1]:
        L = self.l[r:]
        return Ordinal(L)
      if self.l[r][1] == other.l[r][1] and self.l[r][0] > other.l[r][0]:
        L = [(self.l[r][0]-other.l[r][0],self.l[r][1])] + self.l[r+1:]
        return Ordinal(L)
      r += 1
    return Ordinal(self.l[r:])
      

  def __rsub__(self,other):
    if type(self) == Ordinal and type(other) == int:
      if other == 0:
        if self.is_zero():
          return Ordinal([(0,0)])
        return None
      else:
        return Ordinal([(other,Ordinal([(0,0)]))]) - self
  
  def __mul__(self,other):
    #int型が混ざったときの処理
    if type(self) == Ordinal and type(other) == int:
      if other == 0:
        return Ordinal([(0,0)])
      else:
        return self * Ordinal([(other,Ordinal([(0,0)]))])
    #そもそも0じゃないか？
    if self.is_zero() or other.is_zero():
      return Ordinal([(0,0)])
    #otherに定数項があるか？
    if other.l[-1][1].is_zero():
      m = other.l[-1][0]
    else:
      m = 0
    #mで場合分け
    if m > 0:
      a = self.l[0][1]
      L = [(i[0],a+i[1])for i in other.l[:-1]] + [(self.l[0][0]*m,self.l[0][1])] + self.l[1:]
    else:
      a = self.l[0][1]
      L = [(i[0],a+i[1])for i in other.l]
    return Ordinal(L)

  def __rmul__(self,other):
    if type(self) == Ordinal and type(other) == int:
      if other == 0:
        return Ordinal([(0,0)])
      else:
        return Ordinal([(other,Ordinal([(0,0)]))]) * self

  def _divmod(self,other):
    q = Ordinal([(0,0)])
    r = Ordinal(self.l)
    d = other.l[0][1]
    while r >= other:
      if r.l[0][1] != d:
        q = q + Ordinal([(r.l[0][0],r.l[0][1]-d)])
        r = r - other*Ordinal([(r.l[0][0],r.l[0][1]-d)])
      else:
        a = r.l[0][0]
        b = other.l[0][0]
        n = a//b
        if a > n*b: #引き算する余裕があるとき
          if n != 0:
            q = q + Ordinal([(n,Ordinal([(0,0)]))])
            r = r - other*Ordinal([(n,Ordinal([(0,0)]))])
        else: # a == n*b 
          if n != 0:
            q_ = q + Ordinal([(n,Ordinal([(0,0)]))])
            r_ = r - other*Ordinal([(n,Ordinal([(0,0)]))])
            if r_ is None:
              n -= 1
              if n != 0:
                q = q + Ordinal([(n,Ordinal([(0,0)]))])
                r = r - other*Ordinal([(n,Ordinal([(0,0)]))])
            else:
              q = q_
              r = r_
    if self != other*q+r:
      print("Fxxk you!!")
      exit()
    return q,r

  def __truediv__(self, other):
    if type(self) == Ordinal and type(other) == int:
      return self / Ordinal([(other,Ordinal([(0,0)]))])
    if other == 0:
      raise ZeroDivisionError("division by zero")
    res = self._divmod(other)
    if res[1] == 0:
      return res[0]
    return None

  def __rtruediv__(self, other):
    if type(self) == Ordinal and type(other) == int:
      return Ordinal([(other,Ordinal([(0,0)]))]) / self
    
  def __floordiv__(self, other):
    if type(self) == Ordinal and type(other) == int:
        return self // Ordinal([(other, Ordinal([(0, 0)]))])
    if other == 0:
        raise ZeroDivisionError("division by zero")
    res = self._divmod(other)
    return res[0]

  def __rfloordiv__(self, other):
      if type(self) == Ordinal and type(other) == int:
          return Ordinal([(other, Ordinal([(0, 0)]))]) // self

  def __mod__(self, other):
    if type(self) == Ordinal and type(other) == int:
      return self % Ordinal([(other, Ordinal([(0, 0)]))])
    if other == 0:
      raise ZeroDivisionError("division by zero")
    res = self._divmod(other)
    return res[1]

  def __rmod__(self, other):
    if type(self) == Ordinal and type(other) == int:
      return Ordinal([(other, Ordinal([(0, 0)]))]) % self

  def __pow__(self,other):
    #int型が混ざったときの処理
    if type(self) == Ordinal and type(other) == int:
      if other == 0:
        return Ordinal([(1,Ordinal([(0,0)]))])
      else:
        return self ** Ordinal([(other,Ordinal([(0,0)]))])
    #そもそも0じゃないか？
    if other.is_zero():
      return Ordinal([(1,Ordinal([(0,0)]))])
    elif self.is_zero():
      return Ordinal([(0,0)])
    #otherに定数項があるか？
    if other.l[-1][1].is_zero():
      m = other.l[-1][0]
    else:
      m = 0
    #selfが有限のときor無限のとき
    if self.is_finit():
      if other.is_finit():
        return Ordinal([(int(self)**int(other),Ordinal([(0,0)]))])
      if self == 1:
        return 1
      #有限の無限乗
      if m > 0:
        I = Ordinal([(1,Ordinal(other.l[:-1]))])
      else:
        I = Ordinal([(1,other)])
      a = Ordinal(list(self.l))
      b = m
      res = Ordinal([(1,Ordinal([(0,0)]))])
      while b:
        if b % 2 == 1:
          res *= a
        a = a*a
        b //= 2
      return I*res
    else:
      if m > 0:
        I = Ordinal([(1,self.l[0][1]*Ordinal(other.l[:-1]))])
      else:
        I = Ordinal([(1,self.l[0][1]*other)])
      a = Ordinal(list(self.l))
      b = m
      res = Ordinal([(1,Ordinal([(0,0)]))])
      while b:
        if b % 2 == 1:
          res *= a
        a = a*a
        b //= 2
      return I*res

  def __rpow__(self,other):
    if type(self) == Ordinal and type(other) == int:
      if other == 0:
        if self.is_zero():
          return Ordinal([(1,Ordinal([(0,0)]))])
        return Ordinal([(0,0)])
      else:
        return Ordinal([(other,Ordinal([(0,0)]))]) ** self

  def sqrt(self): #平方数であるか？
    if self.is_finit():
      n = int(self)
      if n == 0:
        return Ordinal([(0,0)])
      digit = (len(bin(n)[2:])+1)//2 # 2**len(bin(n)[2:]-1)  <=  n  <= 2**(len(bin(n)[2:]))
      left = 2**(digit-1)            # 1 -> 1, 2 -> 1, 3 -> 2, 4 -> 2
      right = 2**digit
      while left <= right:
          mid = (left + right) // 2
          square = mid * mid
          if square == n:
              return mid
          if square < n:
              left = mid + 1
          else:
              right = mid - 1
      return None
    a = self.l[0][1].l[0][0] #最高次の指数の係数
    if a%2 != 0:
      return None
    s = Ordinal([(self.l[0][0],Ordinal([(self.l[0][1].l[0][0]//2,self.l[0][1].l[0][1])]+self.l[0][1].l[1:]))])
    r = Ordinal(self.l) - s**2
    if r == 0:
      return s
    while True:
      p = r.l[0][1] - s.l[0][1]
      if p is None:
        break
      s = s + Ordinal([(r.l[0][0],p)])
      r = Ordinal(self.l) - s**2
      if r == 0:
        return s
    return None

  def form(self):
    if self.l[-1][1].is_zero():
      m = self.l[-1][0]
      if m == 1:
        return Ordinal(self.l[:-1])
      else:
        return Ordinal(self.l[:-1]+[(m-1,Ordinal([(0,0)]))])
    else:
      return None

OMEGA = Ordinal([(1,Ordinal([(1,Ordinal([(0,0)]))]))])
