m=580
g=9.81
l=1
b=0.3
h=0.03
E=206*1000000000

I=b*h*h*h/12
print(I)
Wc1=(m*g*l*l*l)/(48*E*I)
print(Wc1)
Wc2=Wc1/2
print(Wc2)
K00=(m*g)/(2*Wc2)
print(K00)

W=(m*g*l*l*l)/(48*2*E*I)
print(W)
W=0.000426

K=(m*g)/(2*W)
print(K)

K2=(4*b*h*h*h*E)/(l*l*l)
print(K2)

K3=(4*3*3*3*3*206*100)
print(K3)

sss=0.5625*30 + 5
print(sss)
print(sz)