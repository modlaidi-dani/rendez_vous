# projet1-part1
programme des travalleurs 
# discription:
c'est la 1er partie de projet: 
## le pojet a 2 apps : 
###### user:
- crier un compte 
- renitionalisation de mot de passe pour un utilisateur deja connecté 
- renitionaisation de mot de passe oubier a l'aide d'un code de 5 chifres envoyé a l'email
- il existe deux tipes d'utulisateurs pour le moment (chef, worker)
###### api:
- un profile sera creé pourchaque utilisateur automatiquement 
- un ulisateur peut crier une compay etautomatiqueent il sera de groupe "chef"
- un chef a un acces a tout le CRUD dela company
- un chef peut crier des services dans ca company et aussi un aces a tout le CRUD des services
- un service ades workers, chaque service a ces workers indepondament 
- un chef peut joidre les travvalers de son copany a n'import quelle service qu'il voulais , en modifiant Profile.Service  
- un servicecontien des programmes qui sont relatives aux jours de la semaine
- un worker dans un service pricis a acces a tout le CRUD  de son service
- un worker dans un service pricis n'a pas acces au CRUD  d'un autre servic
- un worker a acces au CRUD  de programme
- il peut queplusieurs services de pluseurs company prtage le meme programme
- un programme a ces heurs de repos "break time"
- un programme peut avoire plusieurs break time
- un worker a acces au CRUD de break time
- un break time peut etre partagé entre plusieurs services de plusieurs company et dans plusieurs progrmmes
  ###### pytest:
la jorité des fonctionalité son testé avec pytest   
