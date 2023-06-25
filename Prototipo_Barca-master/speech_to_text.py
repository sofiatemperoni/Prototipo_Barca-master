
import speech_recognition as sr
import pyttsx3
import langid
import langdetect
import threading
import sys
from PIL import Image
import pygame


#interfaccia
import tkinter as tk
from PIL import ImageTk
from tkinter import Tk, Button, Label
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename

pause_event = threading.Event()
stop_event = threading.Event()
task_thread = None

button_style = {
    'font': ('Arial', 8),
    'bg': 'grey',
    'fg': 'white',
    'activebackground': 'blue',
    'activeforeground': 'white',
    'relief': 'raised',
    'borderwidth': 2,
    'width': 10,
    'height': 2,
}

            
#funzione per aprire un immagine
def open_image(pathname):
                    image = Image.open(pathname)
                    #image = image.resize((1530, 807))  # Ridimensiona l'immagine
                    photo = ImageTk.PhotoImage(image)
                    return photo       
 
def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


#funzione audio recognizer
def recognizer(window):
    r = sr.Recognizer()

    while not stop_event.is_set():

        while  pause_event.is_set():
            # Wait when the pause event is set
            pass   

        with sr.Microphone() as source2: #si sceglie qua il microfono come input

            print("I'm listening")   
            window.title("Listening")
 
            r.adjust_for_ambient_noise(source2, duration=0.2) #sensibilita microfono
                
            audio2 = r.listen(source2) 
        
        try: #per gestire gli errori se qualcosa va storto

            #MyText=r.recognize_google(audio2) #prende audio e lo converte in testo, presupponendo sia italiano
            MyText=r.recognize_google(audio2, language='it-IT') #prende audio e lo converte in testo, presupponendo sia italiano

            MyText = MyText.lower() #mette testo minuscolo
            print("You said: " + MyText) #appare sul terminale il testo
            
            language= langid.classify(MyText)[0] #identifica la lingua
            
            language2= langdetect.detect(MyText) #altra funzione di un altra libreria per la lingua

            # Stampa detected language
            print("Detected languages:", language )
            print("Detected languages numero 2:", language )

            #inserire qui le varie immagini associate alla lingua
            if language == "it" or language == "mg":
                image_path = "./Prototipo_Barca-master/Immagini_sfondo/1.jpg"
                image = Image.open(image_path)
                photo = ImageTk.PhotoImage(image)
                label1.configure(image=photo)
                label1.image = photo
            elif language == "es" or language == "eo":
                image_path = "./Prototipo_Barca-master/Immagini_sfondo/2.jpg"
                image = Image.open(image_path)
                photo = ImageTk.PhotoImage(image)
                label1.configure(image=photo)
                label1.image = photo
            elif language == "sq":
                image_path = "./Prototipo_Barca-master/Immagini_sfondo/3.jpg"
                image = Image.open(image_path)
                photo = ImageTk.PhotoImage(image)
                label1.configure(image=photo)
                label1.image = photo
            else:
                print("lingua non riconosciuta")
            #    image_path = "./test2.jpg"

          

        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said, the language is not in my dictionary")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
                                        

#################------------FUNCTIONS--------#################################

def start_listening():
    global task_thread
    pause_event.clear()
    stop_event.clear()
    task_thread = threading.Thread(target=recognizer, args=(window,))
    task_thread.start()
   
def pause_listening():
    window.title("Paused")
    pygame.mixer.music.stop()
    pause_event.set()

def resume_listening():
    pause_event.clear()

def stop_listening():
    global task_thread
    if task_thread and task_thread.is_alive():
        stop_event.set()
        task_thread.join()
        stop_event.clear()
        sys.exit()  

# Function to play the audio1
def play_audio(filename):
   pygame.mixer.music.load(filename)  # Replace "audio.mp3" with your MP3 file path
   pygame.mixer.music.play()

#Funzione che gestisce il click sullo schermo per far partire la voce
def handle_click(event):
    x = event.x
    y = event.y
    
    print(x)
    print(y)

    pygame.init()

    #finestra di pixel nella quale deve avvenire il click 
    if 0 <= x <= 150 and 300 <= y <= 600:
        print("Clicked on the specified portion of the screen!")
        play_audio("Prototipo_Barca-master/Colline_cioccolato.mp3") #PRIMOMP3
        #SpeakText("Le Colline del Cioccolato sono una famosa attrazione turistica di Bohol.") #qui leggo la storia
    elif 300 <= x <= 500 and 130 <= y <= 300: #CELLA DEL SECONDO MP3
        print("Clicked on the specified portion of the screen!")
        play_audio("Prototipo_Barca-master/Dragone.mp3") #SECONDO MP3

    elif 0 <= x <= 1000 and 0 <= y <= 2000: #POSIZIONE IN CUI CLICCARE PER FAR APPARIRE LA TERZA IMMAGINE
        image_path = "./Prototipo_Barca-master/Immagini_sfondo/3.jpg"
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        label1.configure(image=photo)
        label1.image = photo

    elif 0 <= x <= 1000 and 0 <= y <= 2000: #POSIZIONE IN CUI CLICCARE PER FAR APPARIRE LA SECONDA IMMAGINE
        image_path = "./Prototipo_Barca-master/Immagini_sfondo/2.jpg"
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        label1.configure(image=photo)
        label1.image = photo

#################------------MAIN--------#################################

if __name__ =="__main__":
        # Crea una finestra
        window = tk.Tk()
        window.geometry("1920x1080") #formato finestra
        window.resizable(True, True)
        window.state('zoomed')
        window.title("Title for my program") #Inserire il titolo del progetto !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                
        photo_image = open_image("./Prototipo_Barca-master/Immagini_sfondo/0.jpg")  # Immagine predefinita di sfondo
        label1 = tk.Label(window)
        label1.configure(image=photo_image)
        label1.place(x=545, y=0) #coordinate pixel per immagine di sfondo

        # Create buttons for control
        start_button = tk.Button(window, text="Start", command=start_listening, **button_style)
        start_button.pack
        start_button.place(x=670, y=750) #coordinate button start (precedenti 600,750)

        pause_button = tk.Button(window, text="Pause", command=pause_listening, **button_style)
        pause_button.pack
        pause_button.place(x=770, y=750) #coordinate button pause (precedenti 700,750)

        resume_button = tk.Button(window, text="Resume", command=resume_listening, **button_style)
        resume_button.pack
        #resume_button.place(x=800, y=750)

        window.bind("<Button-1>", handle_click)

        #stop_button = tk.Button(window, text="Stop", command=stop_listening)
       # stop_button.place(x=400, y=450)

        # Start the Tkinter event loop
        window.mainloop()




