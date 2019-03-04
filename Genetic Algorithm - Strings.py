# -*- coding: utf-8 -*-
#The above like should fix errors involving non ascii-characters

###Initiation---------------------------------------------------------------------------------------------------------------------
#Check which version of Tk to use | My PC (Windows Python 3) runs tkinter, MACs at school require Tkinter
#This changes the importation and messageboxes (Therefore help menus, clear menu)
windowsPy3 = True
try:
  from tkinter import *
  from tkinter import messagebox
except ImportError:
  from Tkinter import *
  import tkMessageBox
  windowsPy3 = False

#Check if matplotlib graphs are installed
graphState = True
try:
  import matplotlib.pyplot as plt
except ImportError:
  graphState = False

import random

root = Tk() #Create the window that will be open
root.wm_title("Genetic Algorithm Launcher")
root.resizable(0,0) #Make window not resizeable 

##Define variables----------------------------------------------------------------------------------------------------------------
characters = [" ", "a", "b","c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p","q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "[", "]", "\\", "{", "}", "|", ";", "'", ":", '"', ",", ".", "/", "<", ">", "?"]

choice_mutateParents  = IntVar()
choice_outBasic       = IntVar()
choice_outGoal        = IntVar()
choice_outSubjects    = IntVar()
choice_graph          = IntVar()
graphStyle = [
  ("No Graph",          0, ""),
  ("Default",           1, ""),
  ("bmh",               2, "bmh"),
  ("Dark background",   3, "dark_background"),
  ("Five-thirty-eight", 4, "fivethirtyeight"),
  ("Ggplot",            5, "ggplot"),
  ("Grayscale",         6, "grayscale")
]

##Functions for during the GUI window---------------------------------------------------------------------------------------------
#Preset buttons
def pre_opReal():
  entry_mutationChance.delete(0, END)
  entry_popSize.delete(0, END)
  entry_popTarget.delete(0, END)
  entry_genLim.delete(0, END)
  
  entry_mutationChance.insert(0, "1")
  entry_popSize.insert(0, "100")
  entry_popTarget.insert(0, "5")
  entry_genLim.insert(0, "500")

  check_mutateParents.deselect()

def pre_opQuick():
  entry_mutationChance.delete(0, END)
  entry_popSize.delete(0, END)
  entry_popTarget.delete(0, END)
  entry_genLim.delete(0, END)
  
  entry_mutationChance.insert(0, "15")
  entry_popSize.insert(0, "100")
  entry_popTarget.insert(0, "5")
  entry_genLim.insert(0, "150")

  check_mutateParents.deselect()

def pre_opRough():
  entry_mutationChance.delete(0, END)
  entry_popSize.delete(0, END)
  entry_popTarget.delete(0, END)
  entry_genLim.delete(0, END)
  
  entry_mutationChance.insert(0, "30")
  entry_popSize.insert(0, "100")
  entry_popTarget.insert(0, "5")
  entry_genLim.insert(0, "250")

  check_mutateParents.select()

def pre_outSimple():
  check_outBasic.select()
  check_outGoal.select()
  check_outSubjects.deselect()
  if graphState and not choice_graph.get():  #If graphs are available and a graph is not selected, select default
    graphSelection[1].select()

def pre_outFull():
  check_outBasic.select()
  check_outGoal.select()
  check_outSubjects.select()
  if graphState and not choice_graph.get():  #If graphs are available and a graph is not selected, select default
    graphSelection[1].select()

def pre_outGraph():
  check_outBasic.deselect()
  check_outGoal.deselect()
  check_outSubjects.deselect()
  if not choice_graph.get():  #If graphs are available and a graph is not selected, select default
    graphSelection[1].select()
    
#Help message buttons
def showTextInfo(textType):
  types = {
            #Help menus
            "help_goaltext":            ["Help: Goal Text",               "These are the characters that represent the 'perfect race'.\n" +
                                                                          "The goal is to evolve subjects as close as it can to this perfect race.\n" +
                                                                          "If a subject is too far from the goal it will die off, this is to simulate natural selection."],
            
            "help_presetsOption":  	["Help: Option presets",          "Realistic [1, 100, 5, False]:\n" +
                                                                          "A realistic simulation of evolution\n\n" +
                                                                          "Real/Quick [15, 100, 5, 150, False]:\n"
                                                                          "Raises the mutation chance to speed things along.\n" +
                                                                          "Still a realistic simulation as some species can mutate at these rates.\n\n" +
                                                                          "Rough [30, 10, 5, 20, True]\n" +
                                                                          "This preset allows the parents to mutate, allowing de-evolution.\n" +
                                                                          "This is very unlikely to reach it's goal."],
            
            "help_mutationChance": 	["Help: Mutation chance (%)",     "Each character in each subject has this chance to mutate every time it is born. This will stop a population having no variety when the parents are very similar."],
            
	    "help_popSize":        	["Help: Population size",         "The amount of subjects per generation. The top 10% are bred each generation, the rest die off. Must be at least 20."],
            
            "help_popTarget": 		["Help: Target population",       "If this many subjects in a population equal perfect race the simulation will stop. Must but at least 1 and  can not be higher than the population."],
            
            "help_genLim": 		["Help: Generation limit",        "If the simulation reaches this many generations before being stopped by reaching the target population, the simulation will end. Must be at least 1."],
            
            "help_mutateParents": 	["Help: Mutate parents",          "If checked, parents will also mutate every new generation. This does not happen in real evolution and allows the population to de-evolve."],
            
            "help_presetsOut": 		["Help: Output presets",          "Simple [Default, True, True, False]:\n" +
                                                                          "Outputs basic stats with a graph if available.\n\n" +
                                                                          "Full [Default, True, True, True]:\n" +
                                                                          "All settings on. will take much longer to run and may spam the output a little.\n\n" +
                                                                          "Graph Only [Default, False, False, False]:\n" +
                                                                          "No textual output, completes the simulation the fastest and only output displayed is a graph only the simulation is complete. This is extremely fast compared to the other output presets."],
            
            "help_outBasic": 		["Help: Ouput basic statistics",  "Displays from each generation: Highest, Lowest, Median, Average."],
            
            "help_outGoal": 		["Help: Output goal",             "Displays the perfect score that the subjects can achieve. If ‘Highest” from ‘output basic stats’ is equal to the goal goal score then that subject equals the perfect race."],

            "help_outSubjects":         ["Help: Output all subjects",     "Will output every subject and its score in every generation. This will slow down the program significantly and spam the output but give exact information. "],
            
            "help_graphStyle": 		["Help: Graph style",             "Will not be available if the python module 'matplotlib' is not installed.\n\n" +
                                                                          "The different styles are simply variations of the visuals, they do not affect the format in which the information is displayed."],
            #Menu bars
            "menu_about_credits":       ["Credits",             "Developed by Bradley McInerney 2016 ©\n\n" +
                                                                "Script used: Python 3.4.3\n" +
                                                                "https://docs.python.org/3.4/copyright.html\n\n" +
                                                                "Module used: Matplotlib\n" +
                                                                "http://matplotlib.org/users/credits.html\n\n"],

            "menu_about_licence":       ["Licence & Copyright", "Developed by Bradley McInerney 2016 ©\n\n" +
                                                                "This work is licenced under a Creative Commons Attribution 4.0 International License."+
                                                                "To view a copy of this licence, visit:\n" +
                                                                "http://creativecommons.org/licenses/by/4.0\n\n" +
                                                                "Script used: Python 3.4.3\n" +
                                                                "https://docs.python.org/3.4/license.html\n\n" +
                                                                "Module used: Matplotlib\n" +
                                                                "http://matplotlib.org/users/license.html"],
            
            "menu_about_concept":       ["The Concept",         "The project I decided to complete is called a genetic algorithm. I found a project that someone else had made in which 2D cars were randomly generated, raced and then the winners were “bred” together. This process was repeated with the new generation. Using this trial and error style method the best possible outcome can be found. This concept immediately caught my attention.\n\n" +
                                                                "The program can be split into four parts:\n" +
                                                                ">Initialization: Randomize the population of the first generation\n" +
                                                                ">Evaluation: Give each individual a score based on how close it is to the perfect goal\n" +
                                                                ">Selection: Select the individuals with the highest score and remove the others\n"
                                                                ">Crossover: “Breed” the remaining individuals together and create a full population again\n" +
                                                                ">Mutation: A chance to randomise a part of each individual\n" +
                                                                ">This process will stop once a goal or a limit has been reached.\n\n" +
                                                                "Examples of genetic algorithms that inspired me:\n" +
                                                                "Car example: https://www.youtube.com/watch?v=uxourrlPlf8\n" +
                                                                "Mar1/0: https://www.youtube.com/watch?v=qv6UVOQ0F44"],
                        
            "menu_help_char":           ["Valid Characters",    "Current valid characters:\n\n" +
                                                                " ".join(characters) + "\n\n" +
                                                                "If you really want to change this list, the 'characters' array must be changed in the source code."]
  }

  #Check for which type of tk is installed (Tkinter / tkinter)
  if windowsPy3:
    messagebox.showinfo(message=types[textType][1], parent=root, title=types[textType][0])
  else:
    tkMessageBox.showinfo(message=types[textType][1], parent=root, title=types[textType][0])

#Clear and run buttons
def act_clear():
  if windowsPy3: #confirm with each messagebox version
    confirm = messagebox.askyesno(message="Are you sure you want to clear all values?", parent=root, title="Confirm?")
  else:
    confirm = tkMessageBox.askyesno(message="Are you sure you want to clear all values?", parent=root, title="Confirm?")

  if confirm:
    entry_goal.delete(0, END)
    entry_mutationChance.delete(0, END)
    entry_popSize.delete(0, END)
    entry_popTarget.delete(0, END)
    entry_genLim.delete(0, END)
    check_mutateParents.deselect()
    check_outBasic.deselect()
    check_outGoal.deselect()
    check_outSubjects.deselect()
    graphSelection[0].select()

def act_run():
  #Adds the variables for use after the window closes (I'll be honest. I couldn't find a way to return these without saving globals)
  global returned_goal, returned_mutationChance, returned_popSize, returned_popTarget, returned_genLim, returned_mutateParents, returned_outBasic, returned_outGoal, returned_outSubjects, returned_graph, runConfirm
  runConfirm = False
  returned_goal             = entry_goal.get()
  returned_mutationChance   = entry_mutationChance.get()
  returned_popSize          = entry_popSize.get()
  returned_popTarget        = entry_popTarget.get()
  returned_genLim           = entry_genLim.get()
  returned_mutateParents    = choice_mutateParents.get()
  returned_outBasic         = choice_outBasic.get()
  returned_outGoal          = choice_outGoal.get()
  returned_outSubjects      = choice_outSubjects.get()
  returned_graph            = choice_graph.get()
  ##Check for valid inputs and close window
  runError = []

  #All entriess must me filled
  if not (returned_goal and returned_mutationChance and returned_popSize and returned_popTarget and returned_genLim): runError.append("-Not all entries are filled in.")

  #Goal must only use valid characters
  missing = []
  for char in returned_goal:
    if char not in characters and char not in missing: missing.append(char)
  if missing: runError.append("-Invalid characters were used in the goal (" + ", ".join(missing) + ")")

  #popSize must be atleast 20
  try:
    if int(returned_popSize) < 20: runError.append("-Population size must be atleast 20")
  except ValueError:
    runError.append("-Population size must be a whole nuber")

  #popTarget must be atleast 1
  try:
    if int(returned_popTarget) < 1: runError.append("-Population target must be atleast 1")
  except ValueError:
    runError.append("-Target population must be a whole nuber")

  #popTartget must not be higher than popMax 
  if ("-Population size must be a whole nuber" not in runError) and ("-Target population must be a whole nuber" not in runError) and int(returned_popTarget) > int(returned_popSize):
    runError.append("-Target population must not be higher than population size")

  #Generation limit must be atleast 1
  try:
    if int(returned_genLim) < 1: runError.append("-Generation limit must be atleast 1")
  except ValueError:
    runError.append("-Generation limit must be a whole nuber")

  #Run look for and messagebox the error. If none occour, close the launcher
  if runError:
    msg = "ERROR:\n\n" + "\n\n".join(runError)
    if windowsPy3:
      messagebox.showinfo(message=msg, parent=root, title="Help")
    else:
      tkMessageBox.showinfo(message=msg, parent=root, title="Help")
  else:
    runConfirm = True
    root.destroy()


###Packing the GUI----------------------------------------------------------------------------------------------------------------
##MenuBar
menuBar = Menu(root)

menuAbout = Menu(menuBar, tearoff=0) #Create the "About" menu
menuAbout.add_command(label="Credits",          command=lambda:showTextInfo("menu_about_credits"))
menuAbout.add_command(label="Licence",          command=lambda:showTextInfo("menu_about_licence"))
menuAbout.add_command(label="The Concept",      command=lambda:showTextInfo("menu_about_concept"))
menuBar.add_cascade(label="About", menu=menuAbout)

menuHelp = Menu(menuBar, tearoff=0) #Create the "Help" menu
menuHelp.add_command(label="Valid Characters",      command=lambda:showTextInfo("menu_help_char"))
menuBar.add_cascade(label="Help", menu=menuHelp)

root.config(menu=menuBar) #Display the menubar
##Functional Options
#Heading
Label(root, text="""Genetic Algorithm""").grid(row=0, columnspan=7)

Label(root, text="""-"""*80).grid(row=1, columnspan=7)

#Goal entry
Label(root, text="""Goal text:""").grid(row=2, column=0, sticky=E)

entry_goal = Entry(root, width=36)
entry_goal.grid(row=2, column=1, sticky=W, columnspan=4, padx=(8,0))

#Option Presets
Label(root, text="""Option presets:""").grid(row=3, column=0, pady=20, stick=W, padx=(20,0))

Button(text=" Realistic ", command=pre_opReal, width=10).grid(row=3, column=1, padx=(8,0), sticky=E)
Button(text="Real/Quick", command=pre_opQuick, width=10).grid(row=3, column=2)
Button(text="  Rough  ", command=pre_opRough,  width=10).grid(row=3, column=3, padx=(0,20), sticky=W)

#Mutation chance
Label(root, text="""Mutation chance (%):""").grid(row=4, column=0, padx=8, sticky=E, columnspan=2)

entry_mutationChance = Entry(root)
entry_mutationChance.grid(row=4, column=2, padx=8, sticky=W, columnspan=3)

#Population Size
Label(root, text="""Population size:""").grid(row=5, column=0, padx=8, sticky=E, columnspan=2)

entry_popSize = Entry(root)
entry_popSize.grid(row=5, column=2, padx=8, sticky=W, columnspan=3)

#Target Population
Label(root, text="""Target population:""").grid(row=6, column=0, padx=8, sticky=E, columnspan=2)

entry_popTarget = Entry(root)
entry_popTarget.grid(row=6, column=2, padx=8, sticky=W, columnspan=3)

#Generation Limit
Label(root, text="""Generation limit:""").grid(row=7, column=0, padx=8, sticky=E, columnspan=2)

entry_genLim = Entry(root)
entry_genLim.grid(row=7, column=2, padx=8, sticky=W, columnspan=3)

#Mutate parents
check_mutateParents = Checkbutton(text="""Mutate parents""", variable=choice_mutateParents)
check_mutateParents.grid(row=8, column=2, columnspan=3, sticky=W)

##Output options
#Output Presets
Label(root, text="""Output presets:""").grid(row=10, column=0, pady=20, stick=W, padx=(20,0))

Button(               text="Simple", command=pre_outSimple,    width=10).grid(row=10, column=1, padx=(8,0), sticky=E)
Button(               text="Full", command=pre_outFull,        width=10).grid(  row=10, column=2)
graph_preset = Button(text="Graph Only", command=pre_outGraph, width=10) #The last button has to be disabled if matplotlib not installed
graph_preset.grid(row=10, column=3, padx=(0,20), sticky=W)
if not graphState: graph_preset.config(state=DISABLED)


#Output checkbox settings
check_outBasic    = Checkbutton(text="""Output basic statistics""", variable=choice_outBasic)
check_outGoal     = Checkbutton(text="""Output goal score""", variable=choice_outGoal)
check_outSubjects = Checkbutton(text="""Output all subjects""", variable=choice_outSubjects)
check_outBasic.grid(row=11, column=2, columnspan=3, sticky=W)
check_outGoal.grid(row=12, column=2, columnspan=3, sticky=W)
check_outSubjects.grid(row=13, column=2, columnspan=3, sticky=W)

#Graph Settings
Label(root, text="""Graph Style:""").grid(row=11, column=0, sticky=W, padx=(20,0))

graphSelection = [None, None, None, None, None, None, None]
for txt, val, call in graphStyle:
    graphSelection[val] = Radiobutton(root,
                text=txt,
                variable=choice_graph,
                value=val)
    graphSelection[val].grid(row=12+val, column=0, columnspan=2, sticky=W, padx=(20,0))
    if val > 0 and not graphState:  #Disable all but the first one if matplotlib not installed
      graphSelection[val].config(state=DISABLED)
      

#Help/info menus | "lambda:" stops it from running on startup
Button(text="?", command=lambda:showTextInfo("help_goaltext")      ).grid(row=2, column=6, sticky=W, padx=(0,20))
Button(text="?", command=lambda:showTextInfo("help_presetsOption") ).grid(row=3, column=6, sticky=W, padx=(0,20))
Button(text="?", command=lambda:showTextInfo("help_mutationChance")).grid(row=4, column=6, sticky=W, padx=(0,20))
Button(text="?", command=lambda:showTextInfo("help_popSize")       ).grid(row=5, column=6, sticky=W, padx=(0,20))
Button(text="?", command=lambda:showTextInfo("help_popTarget")     ).grid(row=6, column=6, sticky=W, padx=(0,20))
Button(text="?", command=lambda:showTextInfo("help_genLim")        ).grid(row=7, column=6, sticky=W, padx=(0,20))
Button(text="?", command=lambda:showTextInfo("help_mutateParents") ).grid(row=8, column=6, sticky=W, padx=(0,20))

Button(text="?", command=lambda:showTextInfo("help_presetsOut") ).grid(row=10, column=6, sticky=W, padx=(0,20))
Button(text="?", command=lambda:showTextInfo("help_outBasic")   ).grid(row=11, column=6, sticky=W, padx=(0,20))
Button(text="?", command=lambda:showTextInfo("help_outGoal")    ).grid(row=12, column=6, sticky=W, padx=(0,20))
Button(text="?", command=lambda:showTextInfo("help_outSubjects")).grid(row=13, column=6, sticky=W, padx=(0,20))
Button(text="?", command=lambda:showTextInfo("help_graphStyle") ).grid(row=11, column=1, sticky=W, padx=(40,0))

#Cancel and RUN buttons
Button(text="         Clear         ",
  command=act_clear).grid(row=16, column=3, columnspan=2, sticky=W)

Button(text="          Run          ",
  command=act_run  ).grid(row=17, column=3, columnspan=2, sticky=W)

runConfirm = False
root.mainloop()  #Run GUI window


##After the window closes---------------------------------------------------------------------------------------------------------
#Quit the program if closed not ran
if not runConfirm:
  import sys
  print("Launcher closed.")
  sys.exit("Error message")

###Set options from the launcher--------------------------------------------------------------------------------------------------
goal                = str(returned_goal)
mutationChance      = [int(returned_mutationChance), 100]   #0 in 1 chane to mutate (eg: [10, 100] would be 10%)
maxPop              = int(returned_popSize)                 #The population in each generation, min 20, rec 100
targetPop           = int(returned_popTarget)               #The population needed to be perfect for the script to complete (Use 1 for the first find)
maxGen              = int(returned_genLim)                  #Force stop the script at this point
onlyMutateChildren  = returned_mutateParents                #Will not mutate the highest/best subjects. (Stops de-evolution of whole populations, higher mutation chances have less disadvantages)

outputGenStats      = returned_outBasic                     #Will print the highest, lowest, average and median of each generation
outputGenGoal       = returned_outGoal                      #Re-prints the output each time
outputSubjects      = returned_outSubjects                  #Will print each subject and it's score
graph               = returned_graph                        #Displays a graph at the end
for txt, val, call in graphStyle:                           #Get's the data from the same list that the graph radio buttons are originally from
  if returned_graph == val: graphStyle = call               #Can be either, "bmh", "dark_background", "fivethirtyeight", "ggplot", "greyscale". Anything else will be default

##Initiation----------------------------------------------------------------------------------------------------------------------
#print("TEST 1")
population = []
while len(population) < maxPop:
  subject = ""
  while len(subject) < len(goal):             #Make all guesses the length of the goal? Or should it try to find the length?
    subject += characters[random.randint(0, len(characters)-1)]
  population.append(subject)

generation  = []
statHighest = []
statLowest  = []
statMedian  = []
statAverage = []


while len(generation) < maxGen:
  ##Evaluation--------------------------------------------------------------------------------------------------------------------
  #print("TEST 2")
  population2 = []
  for subject in population:
    fitness = 0 
    for x in range(len(goal)):                #GIVE FITNESS
      if subject[x] in goal: fitness += 1     #1 - characters in
      if subject[x] == goal[x]: fitness += 1  #1 - characters in correct positions (case sensitive)        
        
    population2.append([fitness, subject])
  population2.sort()                          #Sort it so the largest fitness first, then alphabetical
  population2.reverse()
  generation.append(population2)              #Add to gen only to stop loop (early program)

  #Output and check---------------------------------------------------------------------------------------------------------------
  statHighest.append(population2[0][0])                               #Add the stats to be used in the graph and output
  statLowest.append(population2[len(population2)-1][0])
  statMedian.append(population2[int((len(population2)-1)/2)][0])
  total = 0
  for subject in population2:
    total += subject[0]
  statAverage.append(total/len(population2))

                     
  if outputGenStats or outputSubjects: print("\nGENERATION", len(generation), " --------------------------------------------------------------") #Label the output generation

  if outputGenStats:
    if outputGenGoal: print("Goal:\t", len(goal)*2)
    print("Highest:", statHighest[len(statHighest)-1])  #Output the stats
    print("Lowest:\t", statLowest[len(statLowest)-1])
    print("Median:\t", statMedian[len(statMedian)-1])
    print("Average:", statAverage[len(statAverage)-1])
    
  if outputSubjects:
    if outputGenStats: print("")
    for subject in population2:                         #Print all population
      print(subject[1], subject[0])


  correctSubjects = 0                                   #Check if goal reached
  for subject in population2:
    if subject[1] == goal: correctSubjects += 1

  if correctSubjects >= targetPop: break                #Break the loop if target reached
  
  #Selection----------------------------------------------------------------------------------------------------------------------
  #print("TEST 3")
  population = []
  loop = 0
  while len(population) < int(maxPop/100*10):     #Only keep the top 10%
    population.append(population2[loop])
    loop += 1

  ##Breeding----------------------------------------------------------------------------------------------------------------------
  #print("TEST 4")
  population2 = []
  parents = []
  for subject in population:                      #Add the winning parents to a list
    parents.append(subject[1])
  
  while (len(population2) + len(parents)) < maxPop:
    parent1 = random.choice(population)[1]        #Get random populations that are not the same for the parents (Later make this more likely to pair beter or closer parents)
    parent2 = random.choice(population)[1]  

    child = ""                                    #Make the child from random amounts of parts from each parent 
    for x in range(len(goal)):
      if random.randint(0, 1):
        child += parent1[x]
      else:
        child += parent2[x]
    population2.append(child)                     #population2 is now a list of children and parents is a list of parents

  ##Muation-----------------------------------------------------------------------------------------------------------------------
  #print("TEST 5")
  if not onlyMutateChildren: population2 = parents + population2      #Add parents and children to the same list before mutation so all are mutated
    
  population = []
  for subject in population2:
    newSubject = ""
    for x in range(len(subject)):
      if random.randint(1, mutationChance[1]) <= mutationChance[0]:
        newSubject += random.choice(characters)
      else:
        newSubject += subject[x]
    population.append(newSubject)

  if onlyMutateChildren: population = parents + population            #Add parents and chilren together after mutation so only children are mutated


##Final output--------------------------------------------------------------------------------------------------------------------
if correctSubjects >= targetPop:    #If solved and total reached
  if targetPop == 1:
    print("\nIt took " + str(len(generation)) + " generations for a subject to evolve into '" + goal + "'.")
  else:
    print("\nIt took " + str(len(generation)) + " generations for " + str(correctSubjects) + " subjects (goal was " + str(targetPop) + ") to evolve into '" + goal + "'.")
elif correctSubjects > 0:           #If solved and total not reached  
  print("\nThe population failed to evolve " + str(targetPop) + " out of " + str(maxPop) + " population in " + str(len(generation)) + " generations, but did evolve " + str(correctSubjects) + " out of " + str(maxPop) + ".") 
else:                               #If neither solved or total reached, use a more specific score system that would not help evolve but will instead find the closest
  population = []
  for subject in population2:
    fitness = 0 
    for x in range(len(goal)):                                                      #GIVE SPECIFIC FITNESS
      if subject[x] in goal: fitness += 10                                          #10  - characters in
      if subject[x] == goal[x]: fitness += 10                                       #10  - characters in correct positions (case sensitive)
      if subject[x].lower() == "c" and goal[x].lower() == "k": fitness += 1         #1   - c's and k's
      if subject[x].lower() == "k" and goal[x].lower() == "c": fitness += 1         #1   - l's and c's
      if subject[x].lower() == goal[x].lower(): fitness += 1                        #1   - characters in correct positions(not case sensitive)
      try:                                                                          #1   - if both characters numbers
        int(subject[x])
        int(goal[x])
        fitness += 1
      except ValueError:
        pass
    population.append([fitness, subject])
  population.sort()                           #Sort it so the largest fitness first, then alphabetical
  population.reverse()

  output = []                                 #Only add the highest score, and don't add multiple
  highest = population[0][0]
  
  loop = 0
  while True:
    try:                                      #Break loop when finished all (IndexError)
      if population[loop][0] == highest:      #Break loop when finished all of the highest score
        if population[loop][1] not in output: output.append(population[loop][1])
        loop += 1
      else:
        break
    except IndexError:
      break


  print("\nThe population failed to evolve into '" + goal + "' after " + str(len(generation)) + " generations.")
  print("Closest subjects: --------------------------------------------\n" + "\n".join(output))
  
#Graph
if graph:
  if graphStyle: plt.style.use(graphStyle)            #Change style
  
  x = []
  for num in range(len(generation) + 1):              #Will get the x labels (1 all the way to max generation)
    x.append(num)

  plt.plot(x, [0] + statHighest, label="Highest")     #The 0's at the start are so that generation 0 has 0 stats
  plt.plot(x, [0] + statLowest,  label="Lowest")
  plt.plot(x, [0] + statMedian,  label="Median")
  plt.plot(x, [0] + statAverage, label="Average")

  plt.xlabel("Generation")          #Add labels
  plt.ylabel("Fitness")
  plt.title("Evolution Chart")
  
  plt.legend()
  plt.show()

input("PRESS ANY KEY TO CLOSE")     #Pause script (in cmd)
