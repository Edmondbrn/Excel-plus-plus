## Projet excel ++

L'idée serait de faire une appli avec interface utilisateur pour charger des données csv / excel et pouvoir faire des graphiques et des test statistiques associées.

### Features

1. Afficher les données dans un tableau comme excel, donc possibilité de choisir le fichier
-> charger avec pandas et afficher avec tkinter (voir widget si tableau existe)
2. Pouvoir calculer la moyenne / médianne etc... des colonnes numériques en fonction d'une ou plusieurs colonnes catégoriques
-> méthodes de base de pandas
3. Proposer une panoplie de graphiques pour les données sélectionnées
-> plotnine (graphique R ggplot pour la facilité de modification)
4. Proposer une série de test statistiques de base (t-test, chi2...) avec le output complet + tester la normalité des graphiques
-> pingouin / scipy
5. Ajouter les résultats stats sur les graphiques (ns, *, ** ...)
6. Permettre la modification du graphique en temps réel avec les options de menu (couleur, taille texte etc...)

### Comment faire

- Graphiques
Une classe qui crée un objet contenant toutes les caractéristiques du graphique peut être pas mal (taille, type de graphique etc...)
Plus facile de mettre à jour les données avec les mutateurs (set_X)
Faire une méthode pour sauvegarder le fichier dans un dossier tmp pour ensuite charger l'image dans une fenêtre (je ne pense pas pouvoir directement récupérer le graphique sans le sauvegarder avant, mais A VOIR)

- test stats
Fonctions basées sur pingouin au maximum et scipy si pas d'autres alternatives (test de fischer /!\\)

- GUI
Classe tkinter pour gérer l'actualisation et les actions de l'utilisateurs
1 page principale avec le tableau et les actions en barre de tâche + possibilité de sélectionner les données en temps réel ? Ou juste cocher les colonnes ?
Constructeur avec tous les widgets
Méthode pour lancer l'appli
Méthode pour générer les graphiques (fait appel à la classe graphique)
Méthode pour les erreurs ?
