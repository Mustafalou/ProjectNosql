import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import pymongo
import copy

# Connection to the database
def dbConn():
    client  = pymongo.MongoClient("mongodb+srv://dbUser:Password@mustafaloucluster.euggs.mongodb.net/MustafalouCluster?retryWrites=true&w=majority")
    db = client["Mustafalou"]

    try: db.command("ServerStatus")
    except Exception as e: print(e)
    else: print("you are connected")
    return db, client

# Creating the application
class Application(BoxLayout):
    def build(self):
          
        self.title="okok"
        self.orientation='vertical'
        self.label = Label(text = "Accueil", size_hint = (1,0.5))
        
        self.menu()

    # Main menu page
    def menu(self):
        self.add_widget(self.label)
        self.btn = Button(text = "Ajouter client", on_press = self.ajt)
        self.btn2 = Button(text = "Chercher client",on_press = self.chercher)
        self.add_widget(self.btn)
        self.add_widget(self.btn2)
        self.run = True
        self.setupForms()

    # Form page
    def setupForms(self):
        self.liste_lab = []     #List of the labels
        self.liste_input = []   #List of the inputs

        self.labelNom = Label(text = "Nom")
        self.liste_lab.append(self.labelNom)
        self.inputNom = TextInput()
        self.liste_input.append(self.inputNom)

        self.labelPrenom = Label(text = "Prenom")
        self.liste_lab.append(self.labelPrenom)
        self.inputPrenom = TextInput()
        self.liste_input.append(self.inputPrenom)

        self.labelDatedenaissance = Label(text = "Date de naissance")
        self.liste_lab.append(self.labelDatedenaissance)
        self.inputDatedenaissance= TextInput()
        self.liste_input.append(self.inputDatedenaissance)

        self.labelSexe = Label(text = "Sexe")
        self.liste_lab.append(self.labelSexe)
        self.inputSexe = TextInput()
        self.liste_input.append(self.inputSexe)

        self.labelStatussocial = Label(text = "Status social(*)")
        self.liste_lab.append(self.labelStatussocial)
        self.inputStatussocial = TextInput()
        self.liste_input.append(self.inputStatussocial)

        self.labelNum = Label(text = "Numéro de registre national(*)")
        self.liste_lab.append(self.labelNum)
        self.inputNum = TextInput()
        self.liste_input.append(self.inputNum)

        self.labelPaysdorigine = Label(text = "Pays d'origine(*)")
        self.liste_lab.append( self.labelPaysdorigine)
        self.inputPaysdorigine = TextInput()
        self.liste_input.append(self.inputPaysdorigine)

        self.labelGSM = Label(text = "GSM")
        self.liste_lab.append(self.labelGSM)
        self.inputGSM = TextInput()
        self.liste_input.append(self.inputGSM)

        self.labelFixe = Label(text = "Fixe(*)")
        self.liste_lab.append( self.labelFixe)
        self.inputFixe = TextInput()
        self.liste_input.append(self.inputFixe)

        self.labelAdresse = Label(text = "Adresse")
        self.liste_lab.append(self.labelAdresse)
        self.inputAdresse = TextInput()
        self.liste_input.append(self.inputAdresse)

        self.labelEmail = Label(text = "Email")
        self.liste_lab.append(self.labelEmail)
        self.inputEmail = TextInput()
        self.liste_input.append(self.inputEmail)
    
    
    def ajt(self,btn):
        self.clear_widgets()
        grid = GridLayout(rows=20,cols=2)
        for elem in range(len(self.liste_lab)):
            grid.add_widget(self.liste_lab[elem])
            grid.add_widget(self.liste_input[elem])
    
        self.add_widget(grid)
        grid.add_widget(Button(text = "Ajouter", on_press = self.Confirm))

    #Add to the database the client
    def Confirm(self,btn):
        self.db, self.client = dbConn()
        collection = self.db.Clients
        post = {}
        for elem in range(len(self.liste_lab)):
            if self.liste_input[elem].text != "":
                post[self.liste_lab[elem].text] = self.liste_input[elem].text
        collection.insert_one(post)
        self.client.close()
        print("Fait")
        self.clear_widgets()
        self.menu()

    #Creates the search page
    def chercher(self, btn):
        self.clear_widgets()
        self.add_widget(self.labelNom)
        self.add_widget(self.inputNom)
        self.add_widget(Button(text = "Chercher", on_press= self.Chercher))
    
    # Searches in the database    
    def Chercher(self, btn):
        self.db, self.client = dbConn()
        self.collection = self.db.Clients
        self.listeclients = self.collection.find({"Nom": {'$regex': self.inputNom.text}})
      
        self.ShowClients()

    # Shows the clients found from the search    
    def ShowClients(self):
        self.clear_widgets()
        self.liste_lab = []
        self.liste_but = []
        
        i=0
        print(i)
        for elem in self.listeclients:
            print(elem, i)
            self.liste_lab.append(Label(text = elem["Nom"]+ " "+elem["Prenom"]+" "+elem["Date de naissance"]))
            self.liste_but.append(Button(text = "confirm", on_press = self.ShowClient, id = str(i) ))
            self.add_widget(self.liste_lab[i])
            self.add_widget(self.liste_but[i])
            i+=1
        if i==0:
            self.clear_widgets()
            self.add_widget(Button(text="Personne, aller en arrière", on_press = self.chercher))

    # Shows the informations of a client found   
    def ShowClient(self,btn):
        print(btn.id)
        Nom = (self.liste_lab[int(btn.id)].text).split(" ")[0]
        Prenom = (self.liste_lab[int(btn.id)].text).split(" ")[1]
        Ddn = (self.liste_lab[int(btn.id)].text).split(" ")[2]
        self.clientdb = self.collection.find_one({"Nom" : Nom, "Prenom" : Prenom, "Date de naissance" : Ddn})
        self.clear_widgets()
        self.setupForms()
        for elem in range(len(self.liste_lab)):

            try:
                self.liste_input[elem].text = self.clientdb[self.liste_lab[elem].text]
                self.add_widget(self.liste_lab[elem])
                self.add_widget(self.liste_input[elem])
            except:
                self.add_widget(self.liste_lab[elem])
                self.add_widget(self.liste_input[elem])
        self.add_widget(Button(text = "update", on_press = self.update))

    # Updates the data in the database if new data has been introduced
    def update(self,btn):
        post= {}
        for elem in range(len(self.liste_lab)):
            if self.liste_input[elem].text != "":
                post[self.liste_lab[elem].text] = self.liste_input[elem].text
        self.collection.update_one(self.clientdb,{"$set" : post})
        self.client.close()
        self.clear_widgets()
        self.menu()

# Build and run the app        
class go(App):
    def build(self):
        gone= Application()
        gone.build()
        return gone
go().run()
