Bonjour, bienvenu.
Ce script a été conçus comme un outils sommaire de production pour les lead afin de rapidement check
l'arborescence windows du projet, créer des presets de dossier pour les assets, fx et shots, check les
nomenclatures, etc.

Le script se compose de deux gros layouts : Un QTreeView à gauche pour check les fichier, et une console affichant
des messages à droite.

Descriptif des fonctions : 

Menu file : 

Load path : change le path du model pour le Qtreview, et si l'utilisateur accept la warning box qui pop, change le python wrkdir 
et le workspace de maya. 

Create project tree :  Créé une arborescence pré-définis pour le projet, en accord avec notre nomenclature, dans un fichier déjà existant.

Edit menu :

Quick add asset folder : Demande à l'utilisateur un nom pour le fichier si le path selectionné dans le QTreeView est valid (soit 
/01_PREPROD/03_TechnicalDocuments/01_Assets soit /02_Prod/01_Assets/(01_CH|02_PR|03_BG). Si le nom est correct, créé une arborescece 
d'asset, sinon affiche une fenetre warning et redemande le nom jusqu'à ce qu'il soit valid ou que l'utilisateur abort l'opération.

Quick add fx folder : Comme Quick add asset folder pour un fx dans le dossier /01_PREPROD/03_TechnicalDocuments/01_Assets 
soit /02_Prod/01_Assets/04_FX).

Quick add Sequence folder : Comme Quick add asset folder pour un fx dans le dossier /01_PREPROD/03_TechnicalDocuments/02_Shots 
soit /02_Prod/02_Sequences).

Quick add Shot folder : Comme Quick add asset folder pour un fx dans le dossier /01_PREPROD/03_TechnicalDocuments/02_Shots/SQ###
soit /02_Prod/02_Sequences/SQ###).

Remove : Supprime un fichier/dossier 

Display menu : 

Expand Selection : expand les items sélectionnés

Collapse Selection : collapse les items sélectionnés

Expand All : expand tous les items (à faire, j'ai pas trouvé un moyen facile de le faire)

Collapse All : collapse tous les items (à faire, j'ai pas trouvé un moyen facile de le faire)

Naming Menu : 

Check Naming File : Prends le path de l'items sélectionné, va chercher tous les fichier en dessous et applique une boucle for pour chawue fichier. 
Dans cette boucle, je check où se trouve le fichier, si j'ai une correspondance, je teste la clef regex associée. Si elle est fause, je print 
dans la console le path, le nom du fichier et la nomenclature attendue (print du message en wip)

Check In Maya Naming (à venir) : avec mayapy, check tous les nomenclature des dag nodes de maya leur . Est ce que check les nomenclatures de tous les nods,
non dags inclus, serait une bonne idée ? Il faudrait passer tous les nodes par défaut, ça peut être long ? 

Check In Maya Cleanup (à venir) : avec mayapy, fait un check des assets et renvoie les erreurs de topology (ngons, non-manifold, ft, dh, etc.)

Rig in Maya (à venir) : avec mayapy, run le script de rig sur le fichier maya sélectionné.


QTreeView context menu :

En fonction d'où l'utilisateur clique droit, le context menu est différent

Output QTextField : 

Clear : Reset le text dans le QTextField

Close (à venir) : Cahce le layout de l'output QtextField

(J'aimerai bien trouver un moyen de gérer la taille du layout dans l'ui, de la même manière qu'on gère la taille des uis dans maya, mais je ne
sais pas comment faire)



Workflow de setup du programme :

Une fois l'ui ouverte, le programme va chercher le current workspace de maya comme path par défaut pour le model du QTreeView. Si
je veux un autre path, je load le path aved l'action File > Load path.
Une fois dans le fichier, le programme vient modifier le nom de L'ui avec le nom du dossier dans lequel il est.
Ensuite, je créé l'arbre par défaut avec File > Create project tree

Après ça, je peux créer les dossier des assets, shots ou fx, et je peux check les nomenclatures avec les fichiers existants.

 
