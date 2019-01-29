#Importando bibliotecas necessárias
import matplotlib.pyplot as plt
import numpy as np

#Criando vetores para serem plotados
t = np.arange(-4, 4, 0.01)
s = np.arctan(t)

print s
    
#Plotando valores
plt.plot(t, s)
plt.title('ARCTANGENT')
plt.xlabel('Tangent')
plt.ylabel('Arctangent')
plt.grid(True)
plt.show()