import signup
import recognize_faces

class Menu:
    def __init__(self):
        self.title = "Room Monitoring System"
        self.options = ["Register a face", "Sign in", "Start tracking"]

        self.su = signup.signup()
        self.rf = recognize_faces.recognize_faces()

    def main(self):
        border = "".join(["+" for ch in self.title])
        print (border)
        print (self.title)
        print (border + "\n")
        
        for (x, option) in enumerate (self.options, 1):
            print (str(x) + ". " + option)

        print ("\n")
        
        answer = input("Please chosoe a service: ")
        if (answer == str(1)):
            self.su.main()
        elif (answer == str(2)):
            self.rf.main()
        elif (answer == str(3)):
            print ("You chose tracking")
        else:
            print ("Invalid input")

if __name__ == '__main__':
    m = Menu()
    m.main()
