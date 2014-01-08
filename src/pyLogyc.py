#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pyLogyc
#############################################################################
#############################################################################
##                                                                         ##
##                                  pyLogyc                                ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2012-2013 Cédrick FAURY

#    pyLogyc is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
    
#    pyLogyc is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with pyLogyc; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
pyLogyc.py
Copyright (C) 2011-2012  
@author: Cedrick FAURY

"""
__appname__= "pyLogyc"
__author__ = u"Cédrick FAURY"
__version__ = "0.3"

#
# Import des modules nécessaires
#

# GUI
import wx

from math import ceil
# Calcul scientifique
#import scipy

#########################################################################################################
#########################################################################################################
#
#  Variable
#
#########################################################################################################
#########################################################################################################  
class Variable:
    def __init__(self, nom, val = 0, nomNorm = "", 
                 bornes = [None,None], modeLog = True,
                 expression = None, multiple = False):
        self.n = nom
        self.nn = nomNorm
        self.v = val
  
        self.bornes = bornes
        self.modeLog = modeLog
        self.multiple = multiple
        
        # Si la variable fait partie d'une expression
        self.expression = expression
        
    def __repr__(self):
        return self.n+" = "+str(self.v)+"("+str(self.t)+")"
    
    def Augmenter(self, coef = 1):
        if self.EstValide(self.v + coef):
            self.v += coef

       
            
    def Diminuer(self, coef = 1):
        if self.EstValide(self.v - coef):
            self.v += -coef
       

    def ChangerSigne(self):
        self.v = -self.v
            
    def EstValideStr(self, val):
#        print "validStr?",val, type(val), eval(val)
        
        try:
            if len(val) > 1:
                val = val.lstrip('0')
            v = eval(val)
            return self.EstValide(v), v
        except NameError:
            return False, None
        except SyntaxError:
            return False, None
        except:
            return False, None    
        
    #########################################################################################################
    def EstValide(self, val):
#        print "valid?",val, type(val), self.t
        v = val
        
        if type(v) == int:
            return self.EstDansBornes(v)

        
        return False
    
    #########################################################################################################
    def EstDansBornes(self, v):
        return      (self.bornes[0] == None or v >= self.bornes[0]) \
                and (self.bornes[1] == None or v <= self.bornes[1])

#########################################################################################################
#########################################################################################################
#
#  Variable booléenne
#
#########################################################################################################
#########################################################################################################  


FONT_SIZE = 16
FONT_EQ_HD = 300
FONT_EQ = int(100/9*16)


class VariableBin:
    def __init__(self, nom, val = 0, nomNorm = "", 
                 expression = None, bornes = [None,None]):
        self.n = nom
        self.nn = nomNorm
        self.v = val
        self.bornes = bornes
        
        # Si la variable fait partie d'une expression
        self.expression = expression
        
    def __repr__(self):
        return self.n+" = "+str(self.v)
    
    
    def Augmenter(self):
        if self.v == 0:
            self.v = 1
            
    def Diminuer(self):
        if self.v == 1:
            self.v = 0
            



myEVT_VAR_CTRL = wx.NewEventType()
EVT_VAR_CTRL = wx.PyEventBinder(myEVT_VAR_CTRL, 1)

#----------------------------------------------------------------------

class VarEvent(wx.PyCommandEvent):
    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)
        self.var = None

    def SetVar(self, var):
        self.var = var

    def GetVar(self):
        return self.var
    
    
class VariableCtrl(wx.Panel):
    def __init__(self, parent, variable, signeEgal = True, 
                 slider = False, fct = None, help = "", sizeh = -1):
        wx.Panel.__init__(self, parent, -1)
        
#        if coef == None:
#            self.coef = 1
#        else:
#            self.coef = coef
        
        # Une fonction d'activation/désactivation du zoomauto à l'utilisation du slider
        self.fct = fct
        self.etatInit = None
        
        
        #
        # Nom de la variable (titre)
        #
        self.variable = variable
        txt = self.variable.n
        if signeEgal:
            txt += " ="
        txtnom = wx.StaticText(self, -1, txt)
            
        if len(help) > 0:
            txtnom.SetToolTipString(help)
            
        #
        # Valeur de la variable
        #
        self.text = wx.TextCtrl(self, -1, self.lstToText(self.variable.v), size = (sizeh, -1))#,
        if self.variable.nn == "":
            txtn = u"de la variable "+self.variable.n
        else:
            txtn = self.variable.nn
        self.text.SetToolTipString(u"Saisir la valeur "+txtn)
        
        self.Bind(wx.EVT_TEXT, self.OnChar, self.text)
#        self.Bind(wx.EVT_CHAR, self.OnChar, self.text)
        
        # Contrôle de la variable
        self.spin = wx.SpinButton(self, -1, size = (15,25), style = wx.SP_VERTICAL | wx.SP_ARROW_KEYS)
        
        self.spin.SetRange(-100, 100)
        self.spin.SetValue(0)
        self.spin.SetToolTipString(u"Agir ici pour augmenter/diminuer la valeur "+txtn)

        self.Bind(wx.EVT_SPIN_UP, self.OnSpinUp, self.spin)
        self.Bind(wx.EVT_SPIN_DOWN, self.OnSpinDown, self.spin)
        
        vs = wx.BoxSizer( wx.HORIZONTAL)
        vs.Add( txtnom, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALIGN_RIGHT|wx.LEFT, 4 )
        vs.Add(self.text, 1, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT, 5 )
        vs.Add(self.spin, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT, 5 )
        
        sizer = wx.BoxSizer( wx.VERTICAL)
        sizer.Add(vs)
        
        if slider:
            self.sli = wx.Slider(self, -1, 0, -100, 100, 
                                 size = (self.text.GetSize()[0] + self.spin.GetSize()[0] + 20, 20),
                                 style = wx.SL_TOP)
            self.sli.SetToolTipString(u"Agir ici pour augmenter/diminuer la valeur "+txtn)

#            self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
            self.Bind(wx.EVT_SCROLL_CHANGED, self.OnScroll, self.sli)
            self.Bind(wx.EVT_SCROLL_THUMBTRACK, self.OnScroll, self.sli)
            self.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.OnScrollRelease, self.sli)
            sizer.Add(self.sli, flag = wx.ALIGN_RIGHT|wx.BOTTOM, border = 4)
            self.lastPos = 0
        
        self.SetSizerAndFit(sizer)
    
    
    #########################################################################################################
    def sendEvent(self):
        # Pour contourner un bug de scipy ...
        self.variable.v = self.variable.v
#        print "Variable :",self.variable.n, self.variable.v[0]
        evt = VarEvent(myEVT_VAR_CTRL, self.GetId())
        evt.SetVar(self.variable)
        self.GetEventHandler().ProcessEvent(evt)
    
    
#    #########################################################################################################
#    def OnLeave( self, event ):    
#        print "Leave"
#        self.Parent.SetFocus()
        
    #########################################################################################################
    def OnScroll( self, event ):
#        if self.release: 
#            self.release = False
#            return
#        
#        print "OnScroll", event.GetPosition()
        
        pos = event.GetPosition()
        if pos != self.lastPos:
            
            # Quand on commence le Scroll, on "désactive"
            if self.etatInit == None:
                self.etatInit = self.fct() # Etat d'activation initial
                self.fct(False) # Désactivation
            
            # Effet du Scroll ...
            coef = 10.0 **((pos-self.lastPos) / 100.0)
            self.variable.Augmenter(coef)
        
            self.mofifierValeurs()
            self.lastPos = pos
        
            # On remet dans l'état d'activation initial (avant Scroll)
            self.fct(self.etatInit) # Etat d'activation initial
            self.etatInit = None
        
        
    #########################################################################################################
    def OnScrollRelease( self, event ):
#        print "ScrollRelease"
        # On remet le slider au milieu
#        self.release = True
        self.sli.SetValue(0)
        self.lastPos = 0
        
#        # On remet dans l'état d'activation initial (avant Scroll)
#        self.fct(self.etatInit) # Etat d'activation initial
#        self.etatInit = None
        
        
        
        
    #########################################################################################################
    def OnSpinUp( self, event ):
#        print "SpinUp", self.coef
        self.variable.Augmenter()
        self.mofifierValeurs()
        
        
    #########################################################################################################
    def OnSpinDown( self, event ):
#        print "SpinDown", self.coef
        self.variable.Diminuer()
        self.mofifierValeurs()
       
        
    #########################################################################################################
    def mofifierValeurs(self):
        self.text.ChangeValue(self.lstToText(self.variable.v))
        
        # On teste si la variable permet une valeur d'expression valide
        valid = True
        if self.variable.expression != None:
            try:
                e = self.variable.expression.evaluer()
            except:
                valid = False
            if e == None:
                valid = False
        if valid:
            self.sendEvent()
            self.marquerValid(True)
        else:
            self.marquerValid(False)
        
    
    #########################################################################################################
    def mofifierValeursSsEvt(self):
        self.text.ChangeValue(self.lstToText(self.variable.v))


    #########################################################################################################
    def lstToText(self, v):
        return str(v)
        
        
        
    #########################################################################################################
    def getLstValeurs(self, text):
        valid = True
        lst = text.split()
        lstValeurs = []
        for t in lst:
            try:
                v = eval(t)
            except:
                v = t
                
            if type(v) == int or type(v) == float:
                lstValeurs.append(v)
            else:
                valid = False
                continue
            
        return valid, lstValeurs


    #########################################################################################################
    def OnChar(self, event):
        val = event.GetString()
        v = eval(val)
        valid = self.variable.EstValide(v)
            
        if not valid :
            self.marquerValid(False)
        else:
            self.variable.v = v
            self.marquerValid(True)
            self.sendEvent()
        event.Skip()
        
        return
    
    
    
    def marquerValid(self, etat):
        if etat:
            self.text.SetBackgroundColour(
                 wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            
        else:
            self.text.SetBackgroundColour("pink")
            self.text.SetFocus()
        
        self.Refresh()
        
        
#########################################################################################################
#########################################################################################################
#
#  Expression mathématique Dec-Hex-Bin
#
#########################################################################################################
#########################################################################################################  
class ExpressionDHB():
    def __init__(self, parent):
        self.parent = parent
        
        self.dec = u""
        self.hex = u""
        self.bin = u""
        
        self.typeNeg = 2
        self.long = 8
        self.longAuto = True
    
    
    ########################################################################################################
    def SetLongAuto(self, a):
        self.longAuto = a
#        self.SetDec(self.dec)
        
    ########################################################################################################
    def SetLong(self, l):
        self.long = l
        
    ########################################################################################################
    def SetTypeNeg(self, t):
        self.typeNeg = t
        
    ########################################################################################################
    def SetDec(self, s):
        self.dec = s
        self.hex = self.GetHex()
        if self.hex == False:
            return False
        self.bin = self.GetBin()
        return True
        
    ########################################################################################################
    def SetBin(self, s):
        self.bin = s
        self.dec = self.GetDec('bin')
        if self.dec == False:
            return False
        self.hex = self.GetHex()
        
        
    ########################################################################################################
    def SetHex(self, s):
        self.hex = s
        self.dec = self.GetDec('hex')
        if self.dec == False:
            return False
        self.bin = self.GetBin()
        
        
    ######################################################################################################
    def GetDec(self, base):
        lh = self.getConstantes(base)
        if base == 'bin':
            s = self.bin
            b = 2
        elif base == 'hex':
            s = self.hex
            b = 16
        expr = ""
        dd=0
        for d,f in lh:
            expr += s[dd:d]
#            print s[d:f]
#            print eval(s[d:f])
            try:
                expr += str(int(s[d:f], b))
            except ValueError:
                return False
            dd = f
        expr += s[f:]
        return expr
    
    ######################################################################################################
    def GetBin(self):
        ld = self.getConstantes()
#        lh = self.getConstantes('hex')
        s = self.dec
        expr = ""
        dd = 0
        f = 0
        for d,f in ld:
            expr += s[dd:d]
#            print s[d:f]
#            print eval(s[d:f])
            try:
                expr += bin(eval(s[d:f]))[2:]
            except:
                return False
            dd = f
        expr += s[f:]
        return expr
    
    ######################################################################################################
    def GetHex(self):
        ld = self.getConstantes()
        s = self.dec
        expr = ""
        dd = 0
        f = 0
        for d,f in ld:
            expr += s[dd:d]
#            print s[d:f]
#            print eval(s[d:f])
            try:
                expr += hex(eval(s[d:f]))[2:].upper()
            except:
                return False
            dd = f
        expr += s[f:]
        return expr
    
    
    ######################################################################################################
    def GetLongMax(self):
        l = 0
        s = self.dec
        for d,f in self.getConstantes():
            try:
                l = max(l, len(bin(eval(s[d:f]))[2:]))
            except:
                return False
        return l
        
        
    ######################################################################################################
    def GetNeg(self):
        """ Renvoie la valeur "négative" du nombre
        """
        
        if self.typeNeg == 0: # Bit de signe
            l = self.GetLongMax()
            if l >= self.long:
                self.long = l+1
                self.MiseAJourCtrlLong()
            f = "{0:0"+str(self.long)+"b}"
            return int("1"+f.format(abs(self.rdec))[1:], 2)
        
        elif self.typeNeg == 1: # Complément à 1
            t = int("1"*self.long, 2)
            return t^abs(self.rdec)
        
        elif self.typeNeg == 2: # Complément à 2
            t = int("1"*self.long, 2)
            n = (t^abs(self.rdec)) + 1
            return (t^abs(self.rdec)) + 1
        
        
        
    ######################################################################################################
    def GetNegBin(self):
        f = "{0:0"+str(self.long)+"b}"
        if self.typeNeg == 0: # Bit de signe
            return "1"+f.format(self.rdec)
        
        elif self.typeNeg == 1: # Complément à 1
            
            s = f.format(self.rdec)

            t = int("1"*self.long, 2)
            
            return f.format(t^abs(self.rdec))
#            return "".join(str(1 & int(n) >> i) for i in range(64)[::-1])
#            return "".join(str(1-eval(c)) for c in s)
        
        elif self.typeNeg == 2: # Complément à 2
            t = int("1"*self.long, 2)
            n = (t^abs(self.rdec)) + 1
#            s = f.format(self.rdec)
#            n = int("".join([str(1-eval(c)) for c in s]), 2) +1
            return f.format(n)
        
    
    ######################################################################################################
    def GetNegHex(self):
        return hex(int(self.GetNeg(), 2))[2:].upper()
        
    ######################################################################################################
    def GetEvalDec(self):
        r = self.evaluer()
        if r != None:
            self.rdec = r
            return str(r)
        else:
            self.rdec = None
            return ""
        
    ######################################################################################################
    def GetEvalHex(self):
        if self.rdec == None:
            return ""
        
        l = self.GetLongMax()
        if l > self.long:
            self.long = l
            self.MiseAJourCtrlLong()
            
        if self.rdec < 0:
            n = self.GetNeg()
        else:
            n = self.rdec
        
        return hex(n)[2:].upper()
    
    ######################################################################################################
    def GetEvalBin(self, frmt = 0):
        if self.rdec == None:
            return ""
        
        l = self.GetLongMax()
        if l > self.long:
            self.long = l
            self.MiseAJourCtrlLong()
            
        if self.rdec < 0:
            n = self.GetNeg()
        else:
            n = self.rdec
        
        if frmt == 0: # Format Brut
            return "{0:b}".format(n)
        
        elif frmt == 1: # Nombre de bit fixe
            f = "{0:0"+str(self.long)+"b}"
            return f.format(n)
        
        elif frmt == 2: # Nombre de bit fixe + écart 4x4
            f = "{0:0"+str(self.long)+"b}"
            t = f.format(n).zfill(int(4*ceil(float(self.long)/4)))
            return " ".join(t[i*4:(i+1)*4] for i in range(self.long/4+1))
        
    ######################################################################################################
    def MiseAJourCtrlLong(self):
        self.parent.MiseAJourCtrlLong(self.long)
        
    ######################################################################################################
    def evaluer(self):
        """ Renvoie une valeur numérique de l'expression
        """
        dic = {}
        # On fait l'évaluation
        try:
            v = int(eval(self.dec, {"__builtins__": None}, dic))
        except:
#            print "erreur", self.py_expr
            return None
#        print type (v)
        return v
    
    
    #########################################################################################################
    def getConstantes(self, base = 'dec'):
        """ Analyse de la chaine
        """
        lh = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
        if base == 'dec':
            expr = self.dec
            lc = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        elif base == 'hex':
            expr = self.hex
            lc = lh
        elif base == 'bin':
            expr = self.bin
            lc = ['0', '1']
        
        l = []
        d = -1
        f = -1
        for i, c in enumerate(expr):
            if c.upper() in lh:
                if d >= 0:
                    f = i
                else:
                    d = i
                    f = i
            else:
                if d >= 0:
                    l.append([d, f+1])
                d = -1
                f = -1
        if d >= 0:
            l.append([d, f+1])        

        return l    
        
    
#########################################################################################################
#########################################################################################################
#
#  Expression mathématique avec variables
#
#########################################################################################################
#########################################################################################################  
GREEK = ['alpha', 'beta', 'chi', 'delta', 'epsilon', 'gamma', 'lambda', 'mu', 'nu', 'omega',\
         'phi', 'psi', 'rho', 'sigma', 'tau', 'theta', 'xi', 'Delta', 'Gamma', 'Lambda', 'Omega', \
         'Phi', 'Psi', 'Sigma', 'Theta', 'Xi', 'Nabla', 'pi']

# liste des fonctions "sûres"
safe_list = ['not', 'and', 'or']

# Utilisation de la liste des fonctions "sûres" pour filtrer l'espace de nom local 
safe_dict = dict([ (k, locals().get(k, None)) for k in safe_list ])

# liste des fonctions et opérateurs "sûre"
math_list = safe_list + ['*', '/', '+', '^', '-', '(', ')']

class Expression():
    """ Expression mathématique
        Attributs :
         - smp_expr : chaine = forme simple de l'expression (/ + . ^)
         - py_expr : forme évaluable par python (not or and ^)
         - math : chaine au format LaTeX 
    """
    def __init__(self, expr = '', nom = 'S'):
        self.nom = nom
        self.MiseAJour(expr)
        
        
    ######################################################################################################
    def MiseAJour(self, expr = ''):
        # Une chaine apte à subir un 'eval'
        #    (une expression évaluable par python)
        self.py_expr = expr
        
        # Création d'un dictionnaire de Variables : {'nom' : Variable}
        vari = self.getVariables()
#        print "vari =",vari
        self.vari = {}
        for n, v in vari.items():
            if n in GREEK:
                nn = r""+"\\"+n
            else:
                nn = n
            self.vari[n] = VariableBin(nn, val = v, expression = self)

        # Une expression "simple"
        self.MiseAJourPy2Smp(self.py_expr)
        
        # Une chaine mathText
        self.math = self.getMplText()
        
        
        
    ######################################################################################################
    def MiseAJourSmp2Py(self, expr = ''):
        for p, n in [["not ", "/"], [" or ", "+"], [" and ", "."]]:
            expr = expr.replace(n,p)
        self.MiseAJour(expr)

    ######################################################################################################
    def MiseAJourPy2Smp(self, expr = ''):
        for p, n in [["not", "/"], ["or", "+"], ["and", "."]]:
            expr = expr.replace(p,n)
        expr = expr.replace(" ", "")
        self.smp_expr = expr
        
    ######################################################################################################
    def IsConstante(self):
        return len(self.vari) == 0
    

    ######################################################################################################
    def evaluer(self, **args):
        """ Renvoie une valeur numérique de l'expression
        """
        if len(args) != 0:
            self.setVariables(args)
            
        # On crée un dictionnaire de variables : {'nom' : valeur}
        #    (nécessaire pour "eval")

        dic = {}
        for n, v in self.vari.items():
#            print " ", n, v
            dic[n] = v.v
#        print "dic", dic
        global safe_dict
        dic.update(safe_dict)
        
        # On fait l'évaluation
        try:
            v = int(eval(self.py_expr, {"__builtins__": None}, dic))
        except:
#            print "erreur", self.py_expr
            return None
#        print type (v)
        
        return v
    
    
    ######################################################################################################
    def parentheses(self):
        """ Renvoie l'expression mise entre parenthèses
            si cela se doit !!
        """
        if '+' in self.math or '-' in self.math or '/' in self.math:
            return r"\left({"+self.math+r"}\right)"
        else:
            return self.math
     
     
    ######################################################################################################
    def getMplText(self):
        """ Renvoie une chaine compatible mathtext de Matplotlib
        """
        expr = self.smp_expr
        
        def getMath(expr):
#            print ": ",expr
            continuer = True
            i = 0
            p = 0
            while continuer:
                if i >= len(expr) - 1:
                    continuer = False
                    return expr
                
                # Séparation des principaux termes de l'expression
                elif expr[i] == '+' or expr[i] == '^':
                    continuer = False
                    a, b, c = expr.partition(expr[i])
#                    print "   ", a, b, c
                    return '{'+a+'}'+expr[i]+getMath(c)
                
                
                # Traitement des sous-expressions entre parenthèses
                elif expr[i] == '(':
                    p = 1
                    j = i+1
                    continuer2 = True
                    while continuer2:
                        if j > len(expr) - 1:
                            continuer2 = False
                            ssex = '#'
                        elif expr[j] == '(':
                            p += 1
                        elif expr[j] == ')':
                            p += -1
                        if p == 0:
                            continuer2 = False
                            ssex = getMath(expr[i+1:j])
                        j += 1
                    continuer2 = False
                    
                    # On fait un paquet entre crochets {}
                    expr = expr[0:i] + '({' + ssex + '})' + expr[j:]
                    i = i+3+len(ssex)
#                    print "   (   ", expr, i
        
                # Traitement des not
                elif expr[i] == '/':
                    p = 0
                    j = i+1
                    continuer2 = True
                    while continuer2:
                        if j > len(expr) - 1:
                            continuer2 = False
                            ssex = getMath(expr[i+1:j])
                        elif expr[j] == '(':
                            p += 1
                        elif expr[j] == ')':
                            p += -1
                        elif p <= 0 and (expr[j] == '.' or expr[j] == '+'):
                            continuer2 = False
                            ssex = getMath(expr[i+1:j])
                        j += 1
                    continuer2 = False
                    
                    # On enlève les paranthèses éventuelles autour de la sous expression
                    if ssex[0] == '(' and ssex[-1] == ')':
                        ssex = ssex[1:-1]
#                        print " >>", ssex
                                
                    # On fait un paquet entre crochets {}
                    expr = expr[0:i] + '\overline{' + ssex + '}' + expr[j-1:]
                    i = i+10+len(ssex)
#                    print "   /   ", expr, i
                        
                # Séparation des produits
                elif expr[i] == '.':
                    continuer = False
                    a, b, c = expr.partition(expr[i])
#                    print "   ", a, b, c
                    return '{'+a+'}'+expr[i]+getMath(c)
 
                i += 1
        
        ex1 = getMath(expr)
        
        # Traitement global de l'expression pour la rendre compatible avec mathtext
        ex1 = ex1.replace('(', r"\left(")
        ex1 = ex1.replace(')', r"\right)")
        ex1 = ex1.replace('^', r"\oplus ")
            
        # Traitement des lettres grecques
        for g in GREEK:
            ex1 = ex1.replace(g, r""+"\\"+g)
        
        return self.nom+'='+ex1
        
        
    #########################################################################################################
    def getVariables(self):
        """ Analyse de la chaine (prétendue expression mathématique)
            et renvoie un dictionnaire {nom : valeur}
        """
#        print "getVariables", self.py_expr
        expr = self.py_expr

        # Découpage le la chaine autour des opérateurs
        for i in math_list:
            expr = expr.replace(i,'#')
        expr = expr.split('#')
        
        # Création du dictionnaire de variables
        b={}
        for i in expr:
            try:
                int(i)      # C'est une constante
            except:         # C'est une variable
                if i.strip()!='':
                    b[i.strip()] = 0 # On lui affecte la valeur 0
#        print " -->", b
        return b
    
    #########################################################################################################
    def setVariables(self, **args):
        for n, v in args.items():
            self.vari[n].v = v
    
    #########################################################################################################
    def getTableVerite(self, **args):
        """ Renvoie la table de vérité de l'expression sous la forme :
             - E : Entrées = [[valeurs possibles 1ère variable], ... [valeurs possibles nième variable]] (0 ou 1)
             - S : Sortie =  [valeurs de sortie]
            Les variables sont classées par ordre alphabétique.
        """ 
        E = [[eval(l) for l in int2bin(n, len(self.vari))] for n in range(2**len(self.vari))]
#        print "entrées", E
        S = []
        l = self.vari.keys()
        l.sort()
#        print "nvari", l
        for i, e in enumerate(E):
            for i, n in enumerate(l):
                self.vari[n].v = e[i]
            v = self.evaluer()
#            print "valeur", v
            if v == None:
                return False, False
            else:
                S.append(v)
#        print "sortie", S
        return E,S
        
            
    #########################################################################################################        
    def GetBmpHD(self):
        """ Renvoie une image (wx) en "haute définition"
        """
        return mathtext_to_wxbitmap(self.math, FONT_EQ_HD)

    #########################################################################################################
    def GetTeX(self):
        """ Renvoie l'expression sous forme de chaine LaTeX
        """
        return self.math
    

def int2bin(n, count=24):
    """returns the binary of integer n, using count number of digits"""
    return "".join([str((n >> y) & 1) for y in range(count-1, -1, -1)])


#########################################################################################################
#########################################################################################################
#
#  Image MPL de l'expression
#
#########################################################################################################
######################################################################################################### 
class ScrolledBitmap(wx.ScrolledWindow):
    def __init__(self, parent, idd, lstBmp = []):
        self.tip = u""
        self.num = 0
        
        wx.ScrolledWindow.__init__(self, parent, idd)#, style = wx.BORDER_SIMPLE)
        self.SetScrollRate(1,0)
        
        self.sb = wx.StaticBitmap(self, -1, wx.NullBitmap)
        psizer = wx.BoxSizer(wx.HORIZONTAL)
        psizer.Add(self.sb, flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)# | wx.EXPAND)
        self.SetSizer(psizer)
        
        if type(lstBmp) != list:
            lstBmp = [lstBmp]
            
        if lstBmp != []:
            self.SetBitmap(lstBmp[0])
        
        self.lstBmp = lstBmp
        
        self.mouseInfo = None

        self.sb.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.sb.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.sb.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.sb.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.sb.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
        self.SetToolTipString()
       
    def __repr__(self):
        return str(self.GetId())
    
        
    #########################################################################################################
    def sendEvent(self):
        pass

        
    ######################################################################################################    
    def OnRightClick(self, event = None):
#        print "OnRightClick"
        
        def copierImg(event):
            if self.GetBmpHD == None:
                bmp = self.sb.GetBitmap()
            else:
                bmp = self.GetBmpHD()
            CopierBitmap(bmp)
            
        def copierTeX(event):
            if self.GetTeX == None:
                tex = ""
            else:
                tex = self.GetTeX()
            CopierTeX(tex)
            
        menu = wx.Menu()
        itemImg = wx.MenuItem(menu, 0,u"Copier comme une image")
        menu.AppendItem(itemImg)
        self.Bind(wx.EVT_MENU, copierImg, id=0)
        itemTeX = wx.MenuItem(menu, 1,u"Copier comme une equation LaTeX")
        menu.AppendItem(itemTeX)
        self.Bind(wx.EVT_MENU, copierTeX, id=1)
        
        self.PopupMenu(menu)
        menu.Destroy()
        
        
    ######################################################################################################    
    def OnSize(self, event = None):
        
#        print "OnSize ScrolledBitmap"
        w, h = self.sb.GetSize()
        wx.CallAfter(self.SetVirtualSize, (w,h))
#        wx.CallAfter(self.SetVirtualSizeHints, w, h)#, w, h)

        if self.GetScrollThumb(wx.HORIZONTAL) > 0:
            self.sb.SetCursor(wx.StockCursor(wx.CURSOR_SIZEWE))
        else:
            self.sb.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
            
        self.SetToolTipStringComplet()
#        self.Refresh()
#        wx.CallAfter(self.Parent.Layout)
        self.Parent.Refresh()
#        self.Layout()
#        self.Refresh()
        
    ######################################################################################################    
    def SetToolTipString(self, s = ""):
        self.tip = s
        self.SetToolTipStringComplet()
        
    ######################################################################################################    
    def SetToolTipStringComplet(self):
        if self.GetScrollThumb(wx.HORIZONTAL) > 0:
            t = u"Faire glisser pour visualiser"+u"\n"
        else:
            t = u""
            
        t += u"Click droit pour copier dans le presse-papier"
        
        if len(self.lstBmp) > 1:
            t += "\n" + u"Click gauche pour choisir une autre fonction"
        
        if self.tip != "":
            t = self.tip + "\n\n("+ t + u")"

        self.sb.SetToolTipString(t)
        
    
    ######################################################################################################    
    def OnMouseDown(self, event):
        x0, y0 = self.GetViewStart()
        x, y = event.GetX(), event.GetY()
        self.mouseInfo = (x,y, x0, y0)
        
    
    ######################################################################################################    
    def OnMouseUp(self, event):
        return
        x0, y0 = self.GetViewStart()
        x, y = event.GetX(), event.GetY()
        mouseInfo = (x,y, x0, y0)
        if self.mouseInfo == None or self.mouseInfo[0] == mouseInfo[0]:
            self.AugmenterNum()
        self.mouseInfo = None
        
    
    ######################################################################################################    
    def OnMouseMove(self, event):
        if self.mouseInfo == None: 
            return
        x = event.GetX()
        
        dx = -x+self.mouseInfo[0]
        xu = self.GetScrollPixelsPerUnit()[0]
        
        x0 = self.mouseInfo[2]
        
        self.Scroll(x0+dx/xu,0)
     
     
    ######################################################################################################    
    def OnLeave(self, event):
        self.mouseInfo = None
    
    ######################################################################################################    
    def AugmenterNum(self, sendEvent = True):
        self.num += 1
        self.num = self.num % len(self.lstBmp)
        self.AffBitmap(self.num, sendEvent = sendEvent)
        
    ######################################################################################################    
    def SetBitmap(self, lstBmp, GetBmpHD = None, GetTeX = None, num = None):
#        print "SetBitmap"
        if type(lstBmp) != list:
            lstBmp = [lstBmp]
            
        #
        # Fonction pour obtenir l'image en HD
        #
        self.GetBmpHD = GetBmpHD
        
        self.GetTeX = GetTeX
        
        #
        # On modifie l'image
        #
        self.lstBmp = lstBmp
        
        if num != None:
            self.num = num
            
        if self.num+1 > len(self.lstBmp):
            self.num = 0

        self.AffBitmap(self.num, sendEvent = False)
        
        
    ######################################################################################################    
    def AffBitmap(self, num, sendEvent = True):
        if self.num+1 > len(self.lstBmp):
            return
        
        self.Freeze()
#        print num, self.lstBmp
        bmp = self.lstBmp[num]
        self.sb.SetBitmap(bmp)
        
        #
        # On règle la taille viruelle
        #
        if bmp == wx.NullBitmap:
            w, h = 1,1
        else:
            w, h = bmp.GetWidth(), bmp.GetHeight()
        print w,h
        self.SetVirtualSize((w, h))
#        self.SetVirtualSizeHints(w, h, w, h)
        
        #
        # On fixe la hauteur
        #
        self.SetClientSize((self.GetClientSize()[0], h))
        self.SetMinSize((-1, self.GetSize()[1]))
        self.SetMaxSize((-1, self.GetSize()[1]))
        
        self.OnSize()

        self.Thaw()
        
        if sendEvent:
            self.sendEvent()
        


#############################################################################################################
#
#    Fonction de génération de bitmap (wx) à partir d'une expression Matplotlib (LaTeX)
#
#############################################################################################################

from matplotlib.mathtext import MathTextParser
mathtext_parser = MathTextParser("Bitmap")
def mathtext_to_wxbitmap(s, taille = 100, color =  None):
    global mathtext_parser
    if s == "":
        return wx.NullBitmap
    
    if s[0] <> r"$":
        s = mathText(s)
    
    try:
        ftimage, depth = mathtext_parser.parse(s, taille)
    except:     # La syntaxe de l'expression n'est pas correcte
        return


    # Partie enlevée (provisoire ??) pour éviter de charger le module Scipy
#    # Coloration de l'image
#    if color != None:
#        if type(color) == str or type(color) == unicode :
#            color = wx.NamedColour(color)
#        
#        x = ftimage.as_array()
#        
#        # Create an RGBA array for the destination, w x h x 4
#        rgba = scipy.zeros((x.shape[0], x.shape[1], 4), dtype=scipy.uint8)
#        rgba[:,:,0:3] = color
#        rgba[:,:,3] = x
#       
#        # Convertion en Bitmap
#        bmp = wx.BitmapFromBufferRGBA(
#            ftimage.get_width(), ftimage.get_height(),
#            rgba.tostring())
#        
#    else:
    # Convertion en Bitmap
    bmp = wx.BitmapFromBufferRGBA(
        ftimage.get_width(), ftimage.get_height(),
        ftimage.as_rgba_str())
    
    return bmp


def mathText(s):
    return r'$'+s+'$'

##########################################################################################################
##########################################################################################################
##
##  Table de vérité
##
##########################################################################################################
########################################################################################################## 
#class TableVerite():
#    """ Table de vérité
#    """
#    def __init__(self, lstExpressions):
#        self.lstExp = lstExpressions
#        self.e={}
#        self.s={}
#        
#    def evaluer(self):
#        """
#        Evaluation des sorties en fonction des entrées selon les expressions
#        """
#        pass
#
#    def getVariables(self):
#        lst = []
#        for e in self.lstExp:
#            lst.extend(e.getVariables())
#        lst = str.split()
#        lst = list(set(lst))
#        lst.sort()
#        return lst
#            
#        
#        
#    def remplirEntrees(self):
#        v = self.getVariables()
#        self.e = [[l for l in bin(n)] for n in range(2**len(v))]
#        
#    
#    def remplirSorties(self, entrees):
#        for e in self.e:
#            for i, v in enumerate(self.getVariables()):
#                self.s[v] = self.lstExp[i].eval(e)
#        return


#########################################################################################################
#########################################################################################################
#
#  Fenêtre principale
#
#########################################################################################################
######################################################################################################### 
class LogycFrame(wx.Frame):
    def __init__(self, parent, ID, title, pos=wx.DefaultPosition,
            size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE
            ):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        self.SetIcon(wx.Icon('pyLogyc_logo.ico'))
        self.SetFont()
        
        self.Freeze()
        
        self.nb = wx.Notebook(self, -1)
        
        self.pageTable = LogycTable(self.nb) 
        
        self.pageConvers = LogycConversion(self.nb)
        self.nb.AddPage(self.pageTable, u"Table de vérité")
        self.nb.AddPage(self.pageConvers, u"Conversion")
        
        self.sizer = wx.BoxSizer()
        self.sizer.Add(self.nb, 1, flag = wx.EXPAND)
        self.SetSizerAndFit(self.sizer)
        
        self.Layout()
        self.Thaw()
        self.Refresh()
        
#        self.Bind(wx.EVT_SIZE, self.OnReSize)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        
    
    ########################################################################################################
    def OnReSize(self, event):
        self.sizer.FitInside(self)
#        self.Fit()
        
        
    ########################################################################################################
    def OnCloseWindow(self, event):
        """ Interception de l'évenement de fermeture de fenêtre
        """
        self.Destroy()
 
    ########################################################################################################
    def SetFont(self):
        self.font = wx.Font(FONT_SIZE, wx.FONTFAMILY_DEFAULT , wx.NORMAL, wx.NORMAL)
        
#########################################################################################################
#########################################################################################################
#
#  Fenêtre table de vérité
#
#########################################################################################################
#########################################################################################################    
class LogycTable(wx.Panel):
    def __init__(self, parent):

        wx.Panel.__init__(self, parent, -1)
        
        #
        #    Table de vérité
        #
        self.table = wx.ListCtrl(self, -1, style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES)
        self.table.Bind(wx.EVT_SIZE, self.OnResize)
        
        #
        #    Le panel pour les saisies d'expression
        #
        panelSaisie = PanelSaisie(self)
        
        #
        #    Mise en place des éléments
        #
        sizerG = wx.BoxSizer(wx.VERTICAL)
        sizerG.Add(panelSaisie, flag = wx.EXPAND|wx.ALL, border = 2)
#        sizerG.Add(button, flag = wx.ALL, border = 2)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(sizerG, 1,flag = wx.EXPAND|wx.ALL, border = 2)
        sizer.Add(self.table, flag = wx.GROW|wx.ALL, border = 2)
        
        self.SetSizerAndFit(sizer)
        self.Layout()
        self.Refresh()
        
#        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
#        self.sizer.Add(panel, 1 , flag = wx.EXPAND)
#        self.SetSizerAndFit(self.sizer)
        
    ########################################################################################################
    def GetFont(self):
        return self.Parent.Parent.font
    
    ########################################################################################################
    def MiseAJourTable(self, nomE, nomS, E, S):
        self.table.ClearAll()
        
        self.table.SetFont(self.GetFont())
        
        for i, n in enumerate(nomE):
            self.table.InsertColumn(i, n)
            self.table.SetColumnWidth(i, wx.LIST_AUTOSIZE)
        self.table.InsertColumn(len(nomE), nomS)
        self.table.SetColumnWidth(len(nomE), wx.LIST_AUTOSIZE)
        
#        font = wx.Font(FONT_SIZE, wx.FONTFAMILY_DEFAULT , wx.NORMAL, wx.BOLD)
        for i, e in enumerate(E):
            pos = self.table.InsertStringItem(i, str(e[0]))
            for j in range(len(e)-1):
                self.table.SetStringItem(pos, j+1, str(e[j+1]))
            self.table.SetStringItem(pos, len(e), str(S[i]))
            
#            self.table.SetItemFont(pos, font)
        
        
        self.table.Layout()
        self.OnResize()
        self.Fit()

    ########################################################################################################
    def OnResize(self, event=None):
        height = int(2*FONT_SIZE)
        for indx in xrange(self.table.GetItemCount()):
            height += self.table.GetItemRect(indx).height
        self.table.SetMinSize((-1, height))
        
        

#########################################################################################################
#########################################################################################################
#
#  Fenêtre conversion
#
#########################################################################################################
#########################################################################################################    
class LogycConversion(wx.Panel):
    def __init__(self, parent):

        wx.Panel.__init__(self, parent, -1)
                 
        
        #
        #    Zones de saisie d'expressions
        #
        l1 = wx.StaticText(self, -1, u"dec")
        l1.SetFont(self.GetFont())
        t1 = wx.TextCtrl(self, -1, u"")
        t1.SetFont(self.GetFont())
        t1.SetToolTipString(u"Expression sous forme décimale")
        self.dec = t1
        self.Bind(wx.EVT_TEXT, self.EvtTextDec, t1)
        r1 = wx.TextCtrl(self, -1, u"", style = wx.TE_READONLY)
        r1.SetFont(self.GetFont())
        r1.SetToolTipString(u"Résultat sous forme décimale")
        self.rdec = r1
        
        l2 = wx.StaticText(self, -1, u"hex")
        l2.SetFont(self.GetFont())
        t2 = wx.TextCtrl(self, -1, u"")
        t2.SetFont(self.GetFont())
        t2.SetMinSize((200, -1))
        t2.SetToolTipString(u"Expression sous forme héxadécimale")
        self.hex = t2
        self.Bind(wx.EVT_TEXT, self.EvtTextHex, t2)
        r2 = wx.TextCtrl(self, -1, u"", style = wx.TE_READONLY)
        r2.SetFont(self.GetFont())
        r2.SetToolTipString(u"Résultat sous forme héxadécimale")
        self.rhex = r2
        
        l3 = wx.StaticText(self, -1, u"bin")
        l3.SetFont(self.GetFont())
        t3 = wx.TextCtrl(self, -1, u"")
        t3.SetFont(self.GetFont())
        t3.SetMinSize((200, -1))
        t3.SetToolTipString(u"Expression sous forme binaire")
        self.bin = t3
        self.Bind(wx.EVT_TEXT, self.EvtTextBin, t3)
        r3 = wx.TextCtrl(self, -1, u"", style = wx.TE_READONLY)
        r3.SetFont(self.GetFont())
        r3.SetToolTipString(u"Résultat sous forme binaire")
        self.rbin = r3
        
        
        
        sb = wx.StaticBox(self, -1, u"Représentation des nombres négatifs")
        sbs = wx.StaticBoxSizer(sb, wx.VERTICAL)
        
        rb = wx.RadioBox(
                         self, -1, u"Code", wx.DefaultPosition, wx.DefaultSize,
                         [u"Bit de signe",
                          u"Complément à 1",
                          u"Complément à 2"], 
                         1, wx.RA_SPECIFY_COLS
                         )
        
        rb.SetToolTipString(u"Type de codage pour les nombres négatifs\n" \
                            u" * Bit de signe : MSB = 0 -> positif\n" \
                            u"                  MSB = 1 -> négatif\n" \
                            u" * Complément à 1 :\n"\
                            u" * Complément à 2 :\n")
        
        self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, rb)
        sbs.Add(rb, flag = wx.EXPAND|wx.ALL, border = 2)
        
        self.longMot = Variable(u"Longeur du mot", 8, bornes = [2, None])
        lm = VariableCtrl(self, self.longMot, help = u"Nombre de bits des nombres binaires", sizeh = 30)
        self.Bind(EVT_VAR_CTRL, self.OnVariableModified)
        sbs.Add(lm, flag = wx.EXPAND|wx.ALL, border = 2)
        self.lm = lm
        
#        cb = wx.CheckBox(self, -1, u"Automatique", style=wx.ALIGN_RIGHT)
#        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb)
#        sbs.Add(cb, flag = wx.EXPAND|wx.ALL, border = 2)
        
        
        rbb = wx.RadioBox(
                         self, -1, u"Affichage binaire", wx.DefaultPosition, wx.DefaultSize,
                         [u"Brut",
                          u"Longueur fixe",
                          u"Avec séparateur"], 
                         1, wx.RA_SPECIFY_COLS
                         )
        rbb.SetToolTipString(u"Type d'affichage des nombres binaires")
        self.rbb = rbb
        self.rbb.SetSelection(2)
        self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBoxAff, rbb)
        
        #
        #    Mise en place des éléments
        #
        sizer = wx.GridBagSizer()
        sizer.Add(l1, (0,0), flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        sizer.Add(t1, (0,1), flag = wx.EXPAND|wx.ALL, border = 2)
        sizer.Add(r1, (0,2), flag = wx.EXPAND|wx.ALL, border = 2)
        sizer.Add(l2, (1,0), flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        sizer.Add(t2, (1,1), flag = wx.EXPAND|wx.ALL|wx.ALIGN_CENTER, border = 2)
        sizer.Add(r2, (1,2), flag = wx.EXPAND|wx.ALL, border = 2)
        sizer.Add(l3, (2,0), flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        sizer.Add(t3, (2,1), flag = wx.EXPAND|wx.ALL|wx.ALIGN_CENTER, border = 2)
        sizer.Add(r3, (2,2), flag = wx.EXPAND|wx.ALL, border = 2)
        sizer.Add(sbs, (3,0), (1,2), flag = wx.EXPAND|wx.ALL, border = 2)
        sizer.Add(rbb, (3,2), flag = wx.EXPAND|wx.ALL, border = 2)
        
        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(3)
        
        self.SetSizerAndFit(sizer)
        self.Bind(wx.EVT_SIZE, self.OnResize)
        self.Layout()
        self.Refresh()
        
        
        #
        # Initialisation
        #
        self.expr = ExpressionDHB(self)
#        cb.SetValue(self.expr.longAuto)
        rb.SetSelection(self.expr.typeNeg)
        self.longMot.v = self.expr.long
        lm.mofifierValeursSsEvt()
        
        
        
    ########################################################################################################
    def GetFont(self):
        return self.Parent.Parent.font
    
    ########################################################################################################
    def EvtCheckBox(self, event):
        self.expr.SetLongAuto(event.IsChecked())
        self.MiseAJour()
        
    ########################################################################################################
    def EvtRadioBox(self, event):
        self.expr.SetTypeNeg(event.GetInt())
        self.MiseAJour()
    
    ########################################################################################################
    def EvtRadioBoxAff(self, event):
        self.MiseAJour()    
    
    ########################################################################################################
    def MiseAJour(self):
        self.dec.ChangeValue(self.expr.dec)
        self.hex.ChangeValue(self.expr.hex)
        self.bin.ChangeValue(self.expr.bin)
        self.rdec.ChangeValue(self.expr.GetEvalDec())
        self.rhex.ChangeValue(self.expr.GetEvalHex())
        self.rbin.ChangeValue(self.expr.GetEvalBin(self.rbb.GetSelection()))
        self.OnResize()
        
    ########################################################################################################
    def Verifier(self, base, v = True):
        if self.expr.rdec == None or v == False:
            self.marquerValid(base, False)
        else:
            self.marquerValid(base, True)
    
    ########################################################################################################
    def EvtTextDec(self, event):
        s = event.GetString()
        v = self.expr.SetDec(s)
        if v:
            self.MiseAJour()
        self.Verifier('dec', v)
        
    ########################################################################################################
    def EvtTextHex(self, event):
        s = event.GetString()
        self.expr.SetHex(s)
        self.MiseAJour()
        self.Verifier('hex')
        
    ########################################################################################################
    def EvtTextBin(self, event):
        s = event.GetString()
        v = self.expr.SetBin(s)
        if v:
            self.MiseAJour()
        self.Verifier('bin', v)

    ########################################################################################################
    def OnVariableModified(self, event):
        self.expr.SetLong(event.GetVar().v)
        self.MiseAJour()

    ########################################################################################################
    def marquerValid(self, base, valid):
        """ Gestion de la couleur de fond des TextCtrl
            en fonction de la validité ou non de l'expression
        """
        if valid:
            col = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
        else:
            col = "pink"
        
        if base == 'dec':
            self.dec.SetBackgroundColour(col)
        elif base == 'hex':
            self.hex.SetBackgroundColour(col)
        else:
            self.bin.SetBackgroundColour(col)
        
        self.Refresh()
        
    ########################################################################################################
    def OnResize(self, event=None):
        dc = wx.WindowDC(self)
        font = wx.Font(FONT_SIZE, wx.FONTFAMILY_DEFAULT , wx.NORMAL, wx.NORMAL)
        dc.SetFont(font)
        width, height = dc.GetTextExtent(self.rbin.GetValue())

        self.rbb.SetMinSize((width+8, -1))
        self.Layout()
        
        
    ######################################################################################################
    def MiseAJourCtrlLong(self, l):
        self.longMot.v = l
        self.lm.mofifierValeursSsEvt()
        
        
        
        
        
#########################################################################################################
#########################################################################################################
#
#  Panel pour les saisies d'expression
#
#########################################################################################################
#########################################################################################################
class PanelSaisie(wx.Panel):
    def __init__(self, parent, expr = '(not a or b) and (b ^ c)', nom = "S"):
        wx.Panel.__init__(self, parent, -1)
        
        self.nom = nom
        self.parent = parent
        
        
        #
        #    Zones de saisie d'expressions
        #
        l1 = wx.StaticText(self, -1, nom+u" =")
        l1.SetFont(self.GetFont())
        t1 = wx.TextCtrl(self, -1, u"")
        t1.SetFont(self.GetFont())
        t1.SetToolTipString(u"Expression sous forme simple :\n" \
                            u"  not a   --> /a\n" \
                            u"  a and b --> a.b\n"\
                            u"  a or b  --> a+b\n"\
                            u"  a xor b --> a^b")
        self.ts = t1
        self.Bind(wx.EVT_TEXT, self.EvtTextSmp, t1)
        
        l2 = wx.StaticText(self, -1, nom+u" =")
        l2.SetFont(self.GetFont())
        t2 = wx.TextCtrl(self, -1, u"")
        t2.SetFont(self.GetFont())
        t2.SetMinSize((200, -1))
        t2.SetToolTipString(u"Expression sous forme interprétable par python :\n" \
                            u" (ou exclusif = '^')")
        self.tp = t2
        self.Bind(wx.EVT_TEXT, self.EvtTextPy, t2)
        
        #
        #    Image laTex de l'expression 
        #
        self.bmp = ScrolledBitmap(self, -1)
        
        
        #
        #    Mise en place des éléments dans panelSaisie
        #
        sizer = wx.GridBagSizer()
        sizer.Add(l1, (0,0), flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        sizer.Add(t1, (0,1), flag = wx.EXPAND|wx.ALL, border = 2)
        sizer.Add(l2, (1,0), flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        sizer.Add(t2, (1,1), flag = wx.EXPAND|wx.ALL|wx.ALIGN_CENTER, border = 2)
        sizer.Add(self.bmp, (2,0), (1,2), flag = wx.EXPAND|wx.ALL, border = 2)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(2)
        
        #
        # Initialisation
        #
        self.expr = Expression(expr, nom)
        self.tp.ChangeValue(self.expr.py_expr)
        self.ts.ChangeValue(self.expr.smp_expr)
        self.MiseAJourBmp()
        self.MiseAJourTable()
        
        
        self.SetSizerAndFit(sizer)
        
    
    ########################################################################################################
    def GetFont(self):
        return self.parent.GetFont()

    ########################################################################################################
    def EvtTextSmp(self, event):
        s = event.GetString()
        self.expr.MiseAJourSmp2Py(s)
        self.tp.ChangeValue(self.expr.py_expr)
        self.MiseAJourBmp()
        self.MiseAJourTable()
        
    ########################################################################################################
    def EvtTextPy(self, event):
        s = event.GetString()
        self.expr.MiseAJourPy2Smp(s)
        self.ts.ChangeValue(self.expr.smp_expr)
        self.MiseAJourBmp()
        self.MiseAJourTable()
        
    ########################################################################################################
    def MiseAJourBmp(self):
        bmp = mathtext_to_wxbitmap(self.expr.math, FONT_EQ)
        if bmp == None: # L'expression n'est pas correcte !!!
            self.marquerValid(False)
        else:
            self.marquerValid(True)
            self.bmp.SetBitmap(bmp, GetBmpHD = self.expr.GetBmpHD, GetTeX = self.expr.GetTeX)
            
        self.Layout()
        
    ########################################################################################################
    def marquerValid(self, valid):
        """ Gestion de la couleur de fond des TextCtrl
            en fonction de la validité ou non de l'expression
        """
        if valid:
            col = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
            self.ts.SetBackgroundColour(col)
            self.tp.SetBackgroundColour(col)
        else:
            self.ts.SetBackgroundColour("pink")
            self.tp.SetBackgroundColour("pink")
        self.Refresh()
        
    ########################################################################################################
    def MiseAJourTable(self):
        E, S = self.expr.getTableVerite()
        if E == False:
            self.marquerValid(False)
            return
        else:
            self.marquerValid(True)
            
        l = self.expr.vari.keys()
        l.sort()
        
        if len(E) > 0 and len(E[0]) > 0:
            self.parent.MiseAJourTable(l, self.nom, E, S)
            self.marquerValid(True)
        else:
            self.marquerValid(False)
            
        
#########################################################################################################
#
#  Fonctions de copie vers le presse-papier
#
#########################################################################################################
def CopierTeX(TeX):
    obj = wx.TextDataObject(TeX)
    wx.TheClipboard.Open()
    wx.TheClipboard.SetData(obj)
    wx.TheClipboard.Close()    
      
def CopierBitmap(bmp):
    bmp2 = wx.EmptyBitmap(bmp.GetWidth(), bmp.GetHeight())
    mdc = wx.MemoryDC()
    mdc.SelectObject(bmp2)
    mdc.SetBackgroundMode(wx.SOLID)
    mdc.SetBackground(wx.WHITE_BRUSH)
    mdc.Clear()
    mdc.DrawBitmap(bmp, 0,0)
    mdc.SelectObject(wx.NullBitmap)
        
    obj = wx.BitmapDataObject()
    obj.SetBitmap(bmp2)
    wx.TheClipboard.Open()
    wx.TheClipboard.SetData(obj)
    wx.TheClipboard.Close()    
    
    
#########################################################################################################
#########################################################################################################
#
#  Application principale
#
#########################################################################################################
#########################################################################################################    
class LogycApp(wx.App):
    def OnInit(self):
        frame = LogycFrame(None, -1, u"pyLogyc")
        frame.Show()
        self.SetTopWindow(frame)
        return True


if __name__ == '__main__':
    app = LogycApp(False)
    app.MainLoop()

    