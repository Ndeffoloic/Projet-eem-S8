import matplotlib.pyplot as plt
import numpy as np

# Créer des données pour l'offre et la demande
offre = np.sort(np.random.rand(100)*100)[::-1]  # offre décroissante
demande = np.sort(np.random.rand(100)*100)  # demande croissante

# Créer un graphique
plt.figure(figsize=(10, 6))

# Tracer l'offre et la demande
plt.step(range(len(offre)), offre, where='post', label='Offre')
plt.step(range(len(demande)), demande, where='post', label='Demande')

# Ajouter des titres et des étiquettes
plt.title('Courbes d\'offre et de demande')
plt.xlabel('Quantité')
plt.ylabel('Prix')
plt.legend()

# Afficher le graphique
plt.show()
