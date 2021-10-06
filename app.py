import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import pymongo




def dbConn():
    client  = pymongo.MongoClient("mongodb+srv://dbUser:Password@mustafaloucluster.euggs.mongodb.net/MustafalouCluster?retryWrites=true&w=majority")
    db = client["Mustafalou"]

    try: db.command("ServerStatus")
    except Exception as e: print(e)
    else: print("you are connected")
    return db
class Application(BoxLayout):
    def build(self):
          
        self.title="okok"
        self.orientation='vertical'
        self.jeu=0
        self.ancien_jeu = -1
        self.label = Label(text = "Mastermind", size_hint = (1,0.5))
        self.add_widget(self.label)
        self.colors =  {"red" : [1,0,0,1], "green" : [0,1,0,1],"yellow":[1,1,0,1],"blue":[0,0,1,1],"pink" : [1,0.412,0.706,1] ,"dark" : [0,0,0,1]}
        self.db = dbConn()
        self.menu()
    def menu(self):
        self.btn = Button(text = "Ajouter client", on_press = self.ajt)
        self.btn2 = Button(text = "Chercher client")
        self.jeu+=1 
        self.add_widget(self.btn)
        self.add_widget(self.btn2)
        self.run = True
    def ajt(self,btn):
        self.clear_widgets()
        grid = GridLayout(rows=20,cols=2)
        
        liste_lab = []
        liste_input = []
        labelNom = Label(text = "Nom")
        liste_lab.append(labelNom)
        inputNom = TextInput()
        liste_input.append(inputNom)
        labelPrenom = Label(text = "Prenom")
        liste_lab.append(labelPrenom)
        inputPrenom = TextInput()
        liste_input.append(inputPrenom)
        labelDatedenaissance = Label(text = "Date de naissance")
        liste_lab.append(labelDatedenaissance)
        inputDatedenaissance= TextInput()
        liste_input.append(inputDatedenaissance)
        labelSexe = Label(text = "Sexe")
        liste_lab.append(labelSexe)
        inputSexe = TextInput()
        liste_input.append(inputSexe)
        labelStatussocial = Label(text = "Status social(*)")
        liste_lab.append(labelStatussocial)
        inputStatussocial = TextInput()
        liste_input.append(inputStatussocial)
        labelNum = Label(text = "Numéro de registre national(*)")
        liste_lab.append(labelNum)
        inputNum = TextInput()
        liste_input.append(inputNum)
        labelPaysdorigine = Label(text = "Pays d'origine(*)")
        liste_lab.append( labelPaysdorigine)
        inputPaysdorigine = TextInput()
        liste_input.append(inputPaysdorigine)
        labelGSM = Label(text = "GSM")
        liste_lab.append(labelGSM)
        inputGSM = TextInput()
        liste_input.append(inputGSM)
        labelFixe = Label(text = "Fixe(*)")
        liste_lab.append( labelFixe)
        inputFixe = TextInput()
        liste_input.append(inputFixe)
        labelAdresse = Label(text = "Adresse")
        liste_lab.append(labelAdresse)
        inputAdresse = TextInput()
        liste_input.append(inputAdresse)
        labelEmail = Label(text = "Email")
        liste_lab.append(labelEmail)
        inputEmail = TextInput()
        liste_input.append(inputEmail)
        for elem in range(len(liste_lab)):
            grid.add_widget(liste_lab[elem])
            grid.add_widget(liste_input[elem])
    
        self.add_widget(grid)
        grid.add_widget(Button(text = "Ajouter", on_press = self.Confirm))
    def Confirm(self,btn):
        print(inputNom.text)
        """
        post1 = {
                "Nom" : inputNom.Text,
                "Prenom": "Antoine",
                "Date de Naissance": "06/10/2021"
            }
        
        collection = self.db.Guns
        collection.insert_one(post1)
        """
      
        print(0)
        pass
         
class go(App):
    def build(self):
        gone= Application()
        gone.build()
        return gone
go().run()
