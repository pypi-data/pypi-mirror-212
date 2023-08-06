# Upravljivost
def C_M():
    return r"""
$$
C_M = [B \ AB \ A^2 \ ... \ A^{n-1} \ B]
$$
"""

def UprSvVekt():
    return r"""
$$
  Δ_{A^T}(λ)=det(λI - A^T) \\
  A^Tv=λv \\
  v_i^TB \neq 0
$$
"""

def UprPBH():
    return r"""
$$
rang([A - \lambda I \ B]) = n, \forall \lambda
$$
"""

def UprDekomp():
    return r"""
Uzmemo prvih k lin. nezavisnih stupaca te ostatak nadopunimo do baze
$$
C_M = [q_1 \ ... \ q_k ... \ q_m] => T^{-1} = [q_1 \ ... \ q_k \ q_{k+1} \ ... \ q_n]
$$
$$
A\bar = TAT^{-1}
$$
$$
B\bar = TB
$$
$$
C\bar = CT^{-1}
$$
"""

# Osmotrivost
def O_M():
    return r"""
$$
O_M = \begin{bmatrix}
C \\
CA \\
CA^2 \\
\end{bmatrix}
$$
"""

def OsmSvVekt():
    return r"""
$$
\delta A (\lambda) = det(\lambda I - A)
$$
$$
Av = \lambda v
$$
$$
Cv_i \neq 0, \forall \lambda
$$
"""

def OsmPBH():
    return r"""
$$
rang(\begin{bmatrix}
A - \lambda I \\
c \\
\end{bmatrix}) = n, \forall \lambda
$$
"""

def OsmDekomp():
    return r"""
$$
O_MV = 0 => v \in Ker(O_m), dim(Ker(O_m)) = n - rang(O_M)
$$

$$
T^{-1} = [q_1 \ ... \ q_k v_l \ ... \ v_1]
$$
Nadopunjavamo $q_1$ do $q_2$ do baze za jezgru od $O_M$

$A \bar = TAT^{-1} \\$
$B \bar = TB \\$
$C \bar = CT^-1 \\$
"""

# Dodjeljivanje sv. vrijednosti
def Direkt():
    return r"""
$$
K = [k_{ij}], det(SI - A + BK), d(s) = (s - \lambda_1)(s - \lambda_2)
$$
"""

def Kanon():
    return r"""
$$
d(s) = (s - \lambda_1)(s - \lambda_2)
$$
$$
\Delta(s)=det(SI - A)
$$
$$
\bar{k_i} = d_i - \alpha_i, K=\bar{K} T^{-1}, T = CM \begin{bmatrix}
1 & \alpha_1 \\
0 & 1 \\
\end{bmatrix}
$$
$$
\bar{A} = T^{-1}AT, \bar{B} = T^{-1}B
$$
"""

def Akerm():
    return r"""
Ackermanova formula
$$
K = e_n^T C_M^{-1} d(A)
$$
"""

# Linearno konacni regulator

def LQR():
    return r"""
$$
A^TP + PA - PBR^{-1}B^T + C^TQC
$$
$$
K = R^{-1}B^TP
$$
$$
u^* = -Kx
$$
"""

def Imports():
    text = """
import numpy as np
from sympy import *
import control as ct
from control.matlab import *
"""
    return text

def help_otup2():
    text = """
Imports() <- importi
C_M() <- upravljivost
UprSvVekt() <- upravljivost sv. vektora
UprPBH() <- upravljivost PBH
UprDekomp() <- upravljiva dekompozicija
O_M() <- osmotrivost
OsmSvVekt() <- osmotrivost sv. vektora
OsmPBH() <- osmotrivost PBH
OsmDekomp() <- osmotriva dekompozicija
Direkt() <- direktan pristup
Kanon() <- kanonski pristup
Akerm() <- Ackermanova formula
LQR() <- Linearno konacni regulator
"""
    return text
