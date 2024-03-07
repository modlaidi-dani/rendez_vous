## Description

C'est la première partie du projet :

Le projet a 2 applications :

1. **User** :
   - Créer un compte utilisateur
   - Réinitialisation de mot de passe pour un utilisateur déjà connecté
   - Réinitialisation de mot de passe oublié à l'aide d'un code de 5 chiffres envoyé à l'email
   - Il existe deux types d'utilisateurs pour le moment (chef, travailleur)

2. **Api** :
   - Un profil sera créé pour chaque utilisateur automatiquement
   - Un utilisateur peut créer une entreprise et automatiquement il sera du groupe "chef"
   - Un chef a un accès à tout le CRUD de la compagnie
   - Un chef peut créer des services dans sa compagnie et aussi un accès à tout le CRUD des services
   - Un service a des travailleurs, chaque service a ses travailleurs indépendamment
   - Un chef peut joindre les travailleurs de sa compagnie à n'importe quel service qu'il souhaite, en modifiant Profile.Service
   - Un service contient des programmes qui sont relatifs aux jours de la semaine
   - Un travailleur dans un service précis a accès à tout le CRUD de son service
   - Un travailleur dans un service précis n'a pas accès au CRUD d'un autre service
   - Un travailleur a accès au CRUD de programme
   - Il peut que plusieurs services de plusieurs compagnies partagent le même programme
   - Un programme a ses heures de repos "break time"
   - Un programme peut avoir plusieurs break time
   - Un travailleur a accès au CRUD de break time
   - Un break time peut être partagé entre plusieurs services de plusieurs compagnies et dans plusieurs programmes

3.**Test** :
   - La majorité des fonctionnalités sont testées avec pytest
     
