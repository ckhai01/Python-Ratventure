#Chua Che Khai P05 (S10203107E)

import random

#all comments describe the code underneath it
#example:
#I'm explaining the code underneath me!
#I am the code that is being explained!

#note for teachers checking code: on the town menu, you can type 10 to force a leaderboard update. The current day
#will be forced into the leaderboard and sorted.


#(mostly) empty variables for loading the game
pos=[]
orb=[]
world_map=[]
stats={}
day=0
inventory={}
alert=False
has_orb=False

print("Welcome to Ratventure!")
print("----------------------")

# Code your main program here

def view_char():
    for n in stats:
        #skipping mindmg and maxdmg, only Damage is required to be displayed
        if n=="mindmg" or n=="maxdmg":
            continue
        print("{:>7}: {}". format(n, stats[n]))
    if has_orb==True:
        print("You are holding the Orb of Power!")
        
def view_inventory():
    num=0
    description=["Restores 10 HP.", "Deals 5 damage, ignores defence.",\
                 "Decreases enemy defence by 1",\
                 "Instantly kills rats. Severely damages Rat King."]    
    for n in inventory:
        print("{:15}: {:5} {}".format(n, str(inventory[n]), description[num]))
        num+=1
    print("You have {} Gold".format(stats["Gold"]))

def map_generator():
    add=False
    town=[]
    #this nested list will store all coordinates of towns
    townpos=[[0,0]]
    
    world_map = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
                 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
                 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
                 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
                 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
                 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
                 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
                 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' K ']] 
    num=0
    while num<4:
        #generates 2 random variables
        x=random.randint(0,7)
        y=random.randint(0,7)
        town=[x,y]
        
        #checking the coordinates in townpos
        for i in townpos:
            #abs() makes the result positive so I don't have to type additional if statements
            #if the generated values of x and y are too close to any towns, it makes the variable 'add' false
            #and breaks the loop, allowing the program to generate a new set of variables to check.
            if abs(x-i[0])<3 and abs(y-i[1])<3:
                add=False
                break
            #sometimes the town may be at the rat king spot, so this checks for that rare occasion.
            elif x==7 and y==7:
                add=False
                break
            #the town is very likely to be too close to rat king, so loop breaks if it is too close
            elif abs(x-7)<3 and abs(y-7)<3:
                add=False
                break
            
            #very important: no break line here as the generated set of coordinates must pass the check
            #for every coordinate in the townpos list. If I added break here, once the town has satisfied the
            #requirements with one other town, it breaks and doesn't check the others.            
            else:
                add=True
                
        #this is outside of the list loop. If the set of coordinates passes all the checks, 
        #add will become True and the coordinates will be added to the list. Num increases by one to ensure there
        #will not be more than 5 towns.                
        if add==True: 
            townpos.append(town)
            num+=1
            
    #adds to the world map list. This is outside of the original while loop.  
    for i in townpos:
        sublist=world_map.pop(i[0])
        sublist.pop(i[1])
        sublist.insert(i[1]," T ")
        world_map.insert(i[0], sublist) 
        
    return world_map
        
def generate_orb():
    while True:
        orb=[]
        #generates 4 random coordinates. x goes together with y, and x1 goes together with y2.
        #ensures that orb is not close to the start.
        x=random.randint(0,3)
        y=random.randint(4,7)
        x2=random.randint(4,7)
        y2=random.randint(0,7)
        coin=random.randint(1,2)

        if coin==1:
            orb.append(x)
            orb.append(y)
        elif coin==2:
            orb.append(x2)
            orb.append(y2)  
            
        #loops if the space already hsa a town or the king.    
        if world_map[orb[0]][orb[1]]==" T " or world_map[orb[0]][orb[1]]==" K ":
            continue
        else:
            return orb
    
        
def main_menu():
    main_text = ["New Game",\
                 "Resume Game",\
                 "View Leaderboard",\
                 "Exit Game"]    
    #this chunk of code appears a lot
    #it prints the menu from the list
    while True:
        num=1
        for i in main_text:
            print("{}) {}".format(num,i))
            num+=1        
        try:
            choice=int(input("\nEnter choice: "))
        except:
            print("Invalid Choice.")
            continue
        if choice==1:
            #create default stats, need to be global to be accessed later
            global world_map
            global has_orb
            global pos
            global day
            global orb
            global alert        
            global stats
            global inventory
            world_map = map_generator()
            pos=[0,0]
            orb=generate_orb()
            alert=False
            day=1
            has_orb=False
            num=1
            name=input("Enter your hero's name: ")
            
            stats={"Name": "The Hero", "Damage": "2-4", "Defence": 1, "HP": 20, "Gold": 0, "mindmg": 2, "maxdmg": 4}
            inventory={"Potion": 0, "Bomb": 0, "Corrosive Acid":0, "Anti Rat Bomb": 0}
            stats["Name"]=name
            map_updater()
            break
            
        elif choice==2:
            if load_game()==False:
                print("Error! No save data found.\n")
                continue
            map_updater()
            #read text file, initialize stats from file
            break
        elif choice==3:
            try:
                view_leaderboard()
            except:
                file=open("leaderboard.txt", "w+")
                file.close()
                view_leaderboard()
            continue
        
        elif choice==4:
            quit()    
        
def map_updater():
    x=0
    for i in world_map:
        y=0
        for j in i:
            #clearing all previously present instances of H
            if world_map[x][y]==" H ":
                world_map[x][y]=" "
            elif world_map[x][y]=="H/T":
                world_map[x][y]=" T "
            elif world_map[x][y]=="H/K":
                world_map[x][y]=" K "            
            y+=1
        x+=1
    
    row=world_map[pos[0]]
    world_map.pop(pos[0])
    #removing row
    if row[pos[1]]==" T ":
        #changing letter at player position
        row.pop(pos[1])
        row.insert(pos[1], "H/T")
    elif row[pos[1]]==" K ":
        row.pop(pos[1])
        row.insert(pos[1], "H/K")    
    else:
        row.pop(pos[1])
        row.insert(pos[1], " H ")    
    
    world_map.insert(pos[0], row)    
def view_map():
    x=-1
    for i in range(17):
        #printing +---+ once every 2 lines
        if i%2==0:
            print("+---+---+---+---+---+---+---+---+")
            x+=1
        else:
            for j in range(8):
                print("|", end='')
                #printing out object if present in world map list
                if world_map[x][j]!=' ':
                    print("{}".format(world_map[x][j]), end='')
                    #adding a line at index 7
                    if j==7:
                        print("|", end='')
                #adding spaces and line at index 7
                elif j==7:
                    print("   |", end='')
                #printing out spaces for formatting purposes
                else:
                    print("   ", end='')
            print()    

def help():
    #a small help section for the player.
    help_text=["Ask about history of the world.",\
               "Ask about towns.",\
               "Ask about combat.",\
               "Ask about negotiation.",\
               "Ask about the Orb of Power.",\
               "Exit"]
    print("Town Elder: Welcome, my hero. What assistance do you require?")
    while True:
        num=1
        print()
        for i in help_text:
            print("{}) {}".format(num,i))
            num+=1            
        try:
            choice=int(input("\nEnter choice: "))
        except:
            print("Invalid Choice.")
            continue
        if choice==1:
            print("""Long ago, we lived in peace with the Rat Kingdom. However, 
all that changed when a tyrannical king inherited the throne.
The new king could harness the energy from the Orb of Power,
making him far more powerful than any king before him.
He has since been waging war against us, and I fear that our forces
are unable to hold on for much longer. Please help us, Hero.""")
            
        elif choice==2:
            print("""There are 5 towns in this region. You can choose to rest at
these towns to fully restore your health, purchase items for your journey
and save your progress. Be sure to make full use of what we offer here.""")
            
        elif choice==3:
            print("""You are lucky to have been blessed with immense power. The open plains of this
region are infested with rats. These rats will grow stronger every 10 days.
You can choose to strike them down with your blade, use items to carefully defeat them, 
or retreat if the situation looks dire. I entrust the decision to you, Hero.""")
        elif choice==4:
            print("""I understand that you have also been blessed with the ability
to communicate with the rats. When the enemy is weak, you may choose to
strike up a conversation with them. Pay special attention to what their
personality might be and be sure to answer them according to their
personality. I believe you will receive extraordinary rewards should you
succeed, but failure will surely enrage the enemy and result in a fiercer
fight. The choice is yours.""")
        elif choice==5:
            print("""I have heard that you are able to sense the whereabouts of
the orb of power. A fragment of it lies in this region. I recommend
finding it as soon as possible to make your journey much easier. In
any case, you will need it for your fight against the King, as his
prior exposure to the Orb has made him immune to those without it.""")
        elif choice==6:
            print("I wish you luck in your journey.")
            break
            

def town_menu():
    town_text = ["View Character",\
                 "View Map",\
                 "View Inventory",
                 "Talk to Town Elder (Help)",\
                 "Move",\
                 "Rest",\
                 "Shop",\
                 "Save Game",\
                 "Exit Game"]    
   #stops game from crashing when player makes a typo.
   #all of my inputs will have this while True try and except loop.
    while True:
        print("\nDay {}. You are in a town.".format(day))
        num=1
        print()
        for i in town_text:
            print("{}) {}".format(num,i))
            num+=1            
        try:
            choice=int(input("\nEnter choice: "))
        except:
            print("Invalid Choice.")
            continue
        if choice==1:
            view_char()
        elif choice==2:
            view_map()
        elif choice==3:
            view_inventory()
        elif choice==4:
            help()
        elif choice==5:
            move()
            break
        elif choice==6:
            rest()
            break
        elif choice==7:
            shop()
        elif choice==8:
            save_game()
        elif choice==9:
            quit()
        elif choice==10:
            leaderboard_updater()
            print("Leaderboard updated! This is a secret option!")


def move():
    global alert
    global day
    view_map()
    print("W = up; A = left; S = down; D = right")
    alert=False
    while True:
        choice=input("\nYour move: ")
        choice=choice.lower()
        day+=1
        #each if statement will check if player is about to move outside the map.
        #loops if movement isnt possible, otherwise will modify pos list
        if choice=="w" and pos[0]!=0:
            pos[0]-=1
            map_updater()
            break
        elif choice=="s" and pos[0]!=7:
            pos[0]+=1
            map_updater()
            break
        elif choice=="a" and pos[1]!=0:
            pos[1]-=1 
            map_updater()
            break
        elif choice=="d" and pos[1]!=7:
            pos[1]+=1
            map_updater()
            break
        elif choice!="w" and choice!="a" and choice!="s" and choice!="d":
            print("Invalid input!")
        else:
            print("You cannot move outside the map!")
        
            
def rest():
    #probably didn't need to be a function here
    stats["HP"]=20
    print("You are fully healed.\n")
    global day
    day+=1
    
def outdoor_menu():
    open_text = ["View Character",\
                 "View Map",\
                 "View Inventory",\
                 "Move",\
                 "Sense Orb",\
                 "Exit Game"]    
    while True:
        print()
        num=1
        for i in open_text:
            print("{}) {}".format(num,i))
            num+=1        
        try:
            choice=int(input("\nEnter choice: "))
        except:
            print("Invalid Choice.")
            continue
        #this if statement sends player back to battle if player had just ran away
        if alert==True and choice!=4 and choice!=6:
            combat()
        elif choice==1:
            view_char()
        elif choice==2:
            view_map()
        elif choice==3:
            view_inventory()
        elif choice==4:
            move()
            break
        elif choice==5:
            sense_orb()
            break
        elif choice==6:
            quit()
      
def combat():
    fight_text = ["Attack",\
                  "Use Item",\
                  "Negotiate",
                  "Run"]    
    global enemystats
    global alert
    negotiated=False
    
    #made this a function to include more enemies later
    if alert==False:
        enemystats=generate_enemy()
    else:
        #restores enemy HP to max, but keeps enemy type the same if player ran away.
        enemystats["HP"]=enemystats["maxhp"]
        
    while True:  
        print()
        print("Encounter! - {}".format(enemystats["Name"]))
        #doesn't print certain stats like mindmg as they are mainly for program's use only
        for n in enemystats:
            if n=="Name" or n=="mindmg" or n=="maxdmg" or n=="maxhp":
                continue
            print("{:<7}: {}". format(n, enemystats[n])) 
        num=1
        for i in fight_text:
            print("{}) {}".format(num,i))
            num+=1             
        try:
            choice=int(input("\nEnter choice: "))  
        except:
            print("Invalid Choice.")
            continue
        
        if choice==1: 
            #1 in 20 chance for player to deal double damage
            herodmg=(random.randint(stats["mindmg"], stats["maxdmg"])) - enemystats["Defence"]
            critical=random.randint(0,20)
            
            #this if statement fixes the bug that occurs when defence is too high.
            #When damage goes to negative, it heals the target. Should set it to 0 instead.
            if herodmg<0:
                herodmg=0  
                
            if critical==20:
                herodmg=herodmg * 2
                print("Critical Hit!")   
                
            enemystats["HP"]-=herodmg 
           
            
            print("You deal {} damage to the {}!".format(herodmg, enemystats["Name"]))
            
            #always checks if enemy is dead first before they make their move. 
            if enemystats["HP"]<=0:
                print("The {} is dead. Congratulations!!".format(enemystats["Name"])) 
                gold=random.randint(2,5)
                stats["Gold"]+=gold
                print("The {} dropped {} Gold!".format(enemystats["Name"], gold))
                alert=False
                break   
            
            enemydmg=(random.randint(enemystats["mindmg"], enemystats["maxdmg"])) - stats["Defence"]
            
            if enemydmg<0:
                enemydmg=0
            stats["HP"]-=enemydmg
            print("Ouch! The {} hit you for {} damage!".format(enemystats["Name"], enemydmg))
            if stats["HP"]<=0:
                print("The {} has slain the hero. Game over!".format(enemystats["Name"]))
                quit()                 
            print("You have {} HP left.".format(stats["HP"]))            
                   
                         
        elif choice==2:
            use_item()
            if enemystats["HP"]<=0:
                print("The {} is dead. Congratulations!!".format(enemystats["Name"])) 
                gold=random.randint(1,4)
                stats["Gold"]+=gold
                print("The {} dropped {} Gold!".format(enemystats["Name"], gold))
                alert=False
                break                       
            enemydmg=(random.randint(enemystats["mindmg"], enemystats["maxdmg"])) - stats["Defence"]
            if enemydmg<0:
                enemydmg=0
            stats["HP"]-=enemydmg
            print("Ouch! The {} hit you for {} damage!".format(enemystats["Name"], enemydmg))
            if stats["HP"]<=0:
                print("The {} has slain the hero. Game over!".format(enemystats["Name"]))
                quit()                  
            print("You have {} HP left.".format(stats["HP"]))                       
            continue

        elif choice==3:
            #the variable 'check' determines whether the player failed negotiation or not.
            #a failed negotiation would result in 'check' becoming False and sending the player back
            #to battle. Otherwise, it ends the battle.
            check="neutral"
            if enemystats["HP"]>=5:
                print("Enemy HP must be below 5 to negotiate!")
                continue
            elif negotiated==True:
                print("The enemy is unwilling to negotiate.")
                continue
            
            elif enemystats["HP"]<5:
                check=negotiation()
                
            if check==True:
                print("The {} retreats!".format(enemystats["Name"]))
                break
            elif check==False:
                negotiated=True
                print("The {} continues to fight!".format(enemystats["Name"]))
            
        elif choice==4:
            print("You run and hide.")
            alert=True
            break    
            

def sense_orb():
    global has_orb
    #prevents player from picking up orb if player already has orb
    if pos==orb and has_orb==False:
        stats["mindmg"]+=5
        stats["maxdmg"]+=5
        dmgrange=''
        dmgrange=dmgrange+str(stats["mindmg"]) + "-" + str(stats["maxdmg"])
        stats["Damage"]=dmgrange
        stats["Defence"]+=5
        print("You found the Orb of Power!")
        print("Your attack increases by 5!")
        print("Your defence increases by 5!")
        has_orb=True
    elif has_orb==True:
        print("You already have the Orb of Power!")    
        
    #a lot of if statements here, but I cannot see any way of simplifying it.
    #taking the x and y coordinates of both points, the difference between them can determine the direction
    elif pos[0]==orb[0] and pos[1]-orb[1]>0:
        print("You sense that the orb of power is to the West.")
    elif pos[0]==orb[0] and pos[1]-orb[1]<0:
        print("You sense that the orb of power is to the East.")   
    elif pos[1]==orb[1] and pos[0]-orb[0]>0:
        print("You sense that the orb of power is to the North.")
    elif pos[1]==orb[1] and pos[0]-orb[0]<0:
        print("You sense that the orb of power is to the South.")
    elif pos[0]-orb[0]>0 and pos[1]-orb[1]<0:
        print("You sense that the orb of power is to the North-East.")
    elif pos[0]-orb[0]>0 and pos[1]-orb[1]>0:
        print("You sense that the orb of power is to the North-West.")    
    elif pos[0]-orb[0]<0 and pos[1]-orb[1]<0:
        print("You sense that the orb of power is to the South-East.")       
    elif pos[0]-orb[0]<0 and pos[1]-orb[1]>0:
        print("You sense that the orb of power is to the South-West.") 
    else:
        #this shouldn't trigger but i'm keeping it for bug fixing purposes
        print("That's weird. You can't sense the orb. Perhaps a bug is blocking you?")
        
       
    global day    
    day+=1    
    print("Day {}. You are out in the open.".format(day))
    outdoor_menu()    
    
    

def boss_fight():
    bossfight_text = ["Attack",\
                  "Use Item",\
                  "Run"]    
    global enemystats
    enemystats={"Name": "Rat King", "Damage": "6-10", "Defence": 5, "HP": 40, "mindmg": 6, "maxdmg": 10, "maxhp":40}
    modifier=day//10
    enemystats["mindmg"]+=modifier
    enemystats["maxdmg"]+=modifier
    enemystats["Damage"]=str(enemystats["mindmg"])+"-"+str(enemystats["maxdmg"])
    
    #standalone function due to the orb of power requirement
    #otherwise, it is identical to regular combat but the stats are fixed
    while True: 
        print("Encounter! - {}".format(enemystats["Name"]))
        for n in enemystats:
            if n=="Name" or n=="mindmg" or n=="maxdmg" or n=="maxhp":
                continue
            print("{}: {}". format(n, enemystats[n])) 
            num=1
        for i in bossfight_text:
            print("{}) {}".format(num,i))
            num+=1                     
        choice=int(input("\nEnter choice: "))  
        if choice==1: 
            if has_orb==False:
                print("You do not have the Orb of Power - The Rat King is immune!")
                herodmg=0
            elif has_orb==True:
                herodmg=(random.randint(stats["mindmg"], stats["maxdmg"])) - enemystats["Defence"]
                if herodmg<0:
                    herodmg=0
                
            enemystats["HP"]-=herodmg 
            print("You deal {} damage to the {}!".format(herodmg, enemystats["Name"]))
            if enemystats["HP"]<=0:
                print("The {} is dead. You are victorious!!".format(enemystats["Name"]))
                print("Congratulations, you have defeated the Rat King!")
                print("The world is saved! You win!")
                print("Days taken: {}".format(day))
                leaderboard_updater()
                quit()        
            
            enemydmg=(random.randint(enemystats["mindmg"], enemystats["maxdmg"])) - stats["Defence"]
            if enemydmg<0:
                enemydmg=0            
            stats["HP"]-=enemydmg
            print("Ouch! The {} hit you for {} damage!".format(enemystats["Name"], enemydmg))
            print("You have {} HP left.".format(stats["HP"]))            
            if stats["HP"]<=0:
                print("The {} has slain the hero. Game over!".format(enemystats["Name"]))
                quit()            
                    
            
        elif choice==2:
            if has_orb==False:
                print("You do not have the Orb of Power - The Rat King stuns you!")
                herodmg=0
                continue
            use_item()
            if enemystats["HP"]<=0:
                print("The {} is dead. You are victorious!!".format(enemystats["Name"]))
                print("Congratulations, you have defeated the Rat King!")
                print("The world is saved! You win!")
                print("Days taken: {}".format(day))
                leaderboard_updater()
                quit()
            enemydmg=(random.randint(enemystats["mindmg"], enemystats["maxdmg"])) - stats["Defence"]
            if enemydmg<0:
                enemydmg=0
            stats["HP"]-=enemydmg
            print("Ouch! The {} hit you for {} damage!".format(enemystats["Name"], enemydmg))
            print("You have {} HP left.".format(stats["HP"]))            
            if stats["HP"]<=0:
                print("The {} has slain the hero. Game over!".format(enemystats["Name"]))
                quit()                        
            continue            
        elif choice==3:
            print("You run and hide.")
            global alert
            alert=True
            break        


def generate_enemy():
    #enemy types are stored and generated here
    enemy=random.randint(1,4)
    if enemy==1:
        enemystats={"Name": "Common Rat", "Damage": "1-3", "Defence": 1, "HP": 10, "mindmg": 1, "maxdmg": 3, "maxhp":10}
    elif enemy==2:
        enemystats={"Name": "Armoured Rat", "Damage": "1-2", "Defence": 2, "HP": 15, "mindmg": 1, "maxdmg": 2, "maxhp":15}
    elif enemy==3:
        enemystats={"Name": "Assassin Rat", "Damage": "2-4", "Defence": 0, "HP": 8, "mindmg": 2, "maxdmg": 4, "maxhp":8}
    elif enemy==4:
        enemystats={"Name": "Elite Rat", "Damage": "2-4", "Defence": 1, "HP": 12, "mindmg": 2, "maxdmg": 4, "maxhp":12}
    
    #scales enemy difficulty every ten days.
    modifier=day//10
    enemystats["mindmg"]+=modifier
    enemystats["maxdmg"]+=modifier
    enemystats["Damage"]=str(enemystats["mindmg"])+"-"+str(enemystats["maxdmg"])
    enemystats["Defence"]+=modifier
    return enemystats
    


def save_game():
    file=open("savedata.txt", "w+")
    #saves stats in this format:
    #statname:statnumber
    for i in stats:
        file.write(i)
        file.write(":")
        file.write(str(stats[i]))
        file.write("\n")
    for n in inventory:
        file.write(n)
        file.write("-")
        file.write(str(inventory[n]))    
        file.write("\n")
    #adds 'wm' to allow next line to detect when the world map starts
    file.write("wm")
    
    #since world_map is a nested list, a nested loop is used here
    #i is a list of 8 elements, while j is the elements within that list
    #Since my list stores the letters with spaces("space T space"), I manually detect which letter the variable j is
    #and adds the letter to the text file without spaces
    
    #if j is H/T or H/K, I replace it with X and Y. Length of the world map string in the file is important
    #and has to be exactly 64
    
    #changed empty elements to 0 instead as it makes reading the line simpler later
    #sample map code: wmX0000000000T000000000T000T00000000000000000000000000T0000000000K
    
    for i in world_map:
        for j in i:
            if j==" ":
                file.write("0")
            elif j==" T ":   
                file.write("T")
            elif j==" K ":
                file.write("K")
            elif j=="H/T":
                file.write("X")  
            elif j=="H/K":
                file.write("Y")
            else:
                #this statement should not trigger under normal circumstances
                file.write(j)
                
    #this chunk saves the global variables. Used '=' instead of ":" as my load function detects ":" for stats 
    #added the word "end" to signify when the world map section ends
    file.write("\nend")
    file.write("\npos="+str(pos[0])+","+str(pos[1]))
    file.write("\norb="+str(orb[0])+","+str(orb[1]))
    file.write("\nday="+str(day))
    file.write("\nalert="+str(alert))
    file.write("\nhasorb="+str(has_orb))
    file.write("\n\nDo not tamper with the save file (other than the numerical values)\nor the file will not load!")
    print("Your progress has been saved!")

def load_game():
    global world_map
    global has_orb
    global pos
    global orb
    global day
    global alert
    global inventory
    
    name="savedata.txt"
    #only reading the file, no need to overwrite it.
    try:
        file=open(name, "r")
    except:
        #returns false to allow main menu to check if save data is not present.
        #Realistically this error should only trigger once.
        return False
    #since I'm creating a nested list, I created a sublist to add to the world_map list.
    sublist=[]
    for line in file:
        if (":" in line)==True:
            #split function creates a list, and I remove the "\n" at the end since it interferes with
            #integer handling.
            line=line.split(":")
            line[1]=line[1][:-1]
            
            #if the stat can be converted to an integer, it will do so. However, some of the stats
            #like "name" are not integers. They will just be stored as a string.
            try:
                stats[line[0]]=int(line[1])
            except ValueError:
                stats[line[0]]=line[1]  
                
        elif ("-" in line)==True:
            line=line.split("-")
            line[1]=line[1][:-1]
            inventory[line[0]]=int(line[1])
                
            
                          
                
        #detects when the world map line starts        
        elif ("wm" in line)==True:
            for i in line:
                #ignores the wm part of the world map line
                if i=="w" or i=="m":
                    continue
                
                #reverses the conversion done in the saving function. On hindsight, making the elements in the
                #list have spaces wasn't very efficient, but changing it would alter a lot of other functions
                #dealing with the map. 
                elif i=="T":
                    sublist.append(" T ")
                elif i=="K":
                    sublist.append(" K ")
                elif i=="0":
                    sublist.append(' ')
                elif i=="X":
                    sublist.append("H/T")
                elif i=="Y":
                    sublist.append("H/K")
                 
                #This is a seperate if statement as it needs to be checked every loop. It will add the sublist in
                #and reset the sublist so that the nested lists dont exceed the length of 8. 
                if len(sublist)==8:
                    world_map.append(sublist)
                    sublist=[]            
        #everything under this comment initializes the global variables. Depending on what the line is, it will
        #define the variables accordingly. 
        elif line=="hasorb=True\n":
            has_orb=True
        elif line=="hasorb=False\n":
            has_orb=False     
        
        elif ("pos" in line)==True:
            for i in line:
                #tries to append the integer to the list. Otherwise it skips the current iteration of i. 
                try:
                    pos.append(int(i))
                except:
                    continue
        elif ("orb" in line)==True:
            for i in line:
                try:
                    orb.append(int(i))
                except:
                    continue   
                
        #I could not use the same method as the previous 2 variables as "days" could potentially be 2 or 3 digits.
        #hence, I locate where "=" is at and pull the integer that comes after the "=", but ends before the second last
        #index.
        elif ("day" in line)==True:
            index=line.find("=")+1
            day=int(line[index:-1])
            
        elif line=="alert=True\n":
            alert=True
        elif line=="alert=False\n":
            alert=False     
    print("Save file '{}' has been loaded!\n".format(stats["Name"]))

 
def leaderboard_updater():
    num=1
    #attempts to open file, otherwise creates one.
    try:
        file=open("leaderboard.txt", "r")
    except:
        file=open("leaderboard.txt", "w+")
        
    #empty dictionary for me to work with. 
    leaderboard={}
    
    #the format for my leaderboard file is
    #1. Name: x days

    for line in file: 
        #finding the index of the ":" and "days" allows me to isolate the number of days, regardless of how long it is.
        index1=line.find(":")
        index2=line.find("days")
        
        #the name always starts at index 3 and ends at the ":"
        #thus, I can create a dictionary with the name and integer value of the days taken.        
        leaderboard[line[3:index1]]=int(line[index1+2:index2])
        
    file.close()
    #adds the new name and score when the player beats the rat king.
    leaderboard[stats["Name"]]=day
    #sorts the dictionary in ascending order of values.
    sorted_leaderboard=sorted(leaderboard.items(), key=lambda x:x[1])
    
    #opens the file again to re-insert the sorted leaderboard.
    file=open("leaderboard.txt", "w")
    
    for i in range(len(sorted_leaderboard)):
        #readded back in the same format as before.
        file.write(str(num)+". "+sorted_leaderboard[i][0]+": "+str(sorted_leaderboard[i][1])+" days"+"\n")
        num+=1
        #stops adding once 5 entries have been reached. Since the dictionary has been sorted,
        #the worst score will always be ignored.
        if i==4:
            break    
def view_leaderboard():
    #straightforward function to print out the leaderboard. The variable num here is used to check if
    #the text file is empty and prints something instead of nothing at all.
    num=1
    file=open("leaderboard.txt", "r")
    for line in file:
        print(line)
        num+=1
    if num==1:
        print("\nLeaderboard is empty!\n")
    
def shop():
    #defining local variables so that I can easily edit them if I wish
    price=[3, 4, 5, 10, 10]
    items=["Potion", "Bomb", "Corrosive Acid", "Blacksmith", "Armoursmith"]
    description=["Restores 10 HP.", "Deals 5 damage, ignores defence.",\
                 "Decreases enemy defence by 1",\
                 "Increases your damage by 1 permanently.",\
                 "Increases your defences by 1 permanently."]
    
    print("Welcome to the shop! How may I help you?")
        
    while True:
        #prints out items available and their prices
        #also prints out two additional options not in the list above.
        num=1
        print("You have {} Gold.".format(stats["Gold"]))
        for i in items:
            print("{}) {:20}: {:2} Gold      {}".format(num, i, price[num-1], description[num-1]))
            num+=1
            
        print("{}) Check Inventory".format(num))
        num+=1
        print("{}) Exit".format(num))  
        
        try:
            choice=int(input("\nEnter choice: "))
        except:
            print("Invalid Choice.")
            continue
        selection=choice-1
        
        if choice==7:
            print("Thanks for coming!")
            break
        elif choice==6:
            for i in inventory:
                print("{}: {}".format(i, inventory[i]))
                
        elif price[selection]>stats["Gold"]:
            print("You don't have enough gold for that!")
            continue
        
        elif items[selection]=="Blacksmith":
            stats["mindmg"]+=1
            stats["maxdmg"]+=1
            stats["Damage"]=str(stats["mindmg"])+"-"+str(stats["maxdmg"])
            stats["Gold"]-=price[selection]
            print("Your damage went up by 1!")
            
        elif items[selection]=="Armoursmith":
            stats["Defence"]+=1
            stats["Gold"]-=price[selection]
            print("Your defence went up by 1!")        
                
            
        else:
            inventory[items[selection]]+=1
            stats["Gold"]-=price[selection]
            print("{} purchased!".format(items[selection]))
            continue
                                            
def use_item():
    num=1
    for n in inventory:
        print("{}) {}: {}".format(num, n, inventory[n]))  
        num+=1
    print("{}) Back".format(num))
    
    while True:
        try:
            item=int(input("\nEnter item: "))
        except:
            print("Invalid choice.")
            
        if item==1 and inventory["Potion"]>0:
            stats["HP"]+=10
            print("{} used a potion. 10 HP Restored!".format(stats["Name"]))
            inventory["Potion"]-=1
            
            if stats["HP"]>20:
                print("HP cannot go above 20!")
                stats["HP"]=20
            break
            
        elif item==2 and inventory["Bomb"]>0:
            herodmg=5          
            enemystats["HP"]-=herodmg 
            print("You used the bomb to deal {} damage to the {}!".format(herodmg, enemystats["Name"]))
            inventory["Bomb"]-=1
            break
        elif item==3:
            if enemystats["Defence"]>0:
                enemystats["Defence"]-=1
                print("The corrosive acid melted the enemy's armour!")
                
            else:
                print("The enemy has no armour to melt!")
                print("The acid corrodes the enemy directly!")
                herodmg=10
                enemystats["HP"]-=herodmg 
                print("The acid dealt {} damage to the {}!".format(herodmg, enemystats["Name"]))
            inventory["Corrosive Acid"]-=1
            break
        
        elif item==4 and enemystats["Name"]!="Rat King":
            herodmg=9999
            enemystats["HP"]-=herodmg
            print("The Anti Rat Bomb instantly vaporised the {}!".format(enemystats["Name"]))
            inventory["Anti Rat Bomb"]-=1
            break
        elif item==4 and enemystats["Name"]=="Rat King":
            herodmg=10
            enemystats["HP"]-=herodmg
            print("The Anti Rat Bomb dealt 10 damage to the {}!".format(enemystats["Name"]))
            inventory["Anti Rat Bomb"]-=1
            break        
                  
        elif item==5:
            break
        
        else:
            print("You don't have that item!")
            
            


def negotiation_start():
    #question lists are in this format: [Question, Correct answer, Wrong answer, Neutral answer]
    stronglist=[["Say, why would you pick on a poor chap like me?", "You were in my way.", "I'm sorry, I didn't mean to hurt you", "You attacked me first though."],\
                  ["A shame. If only I had taken this seriously from the start.", "Then take it seriously now.", "I don't think I could've won if you did...", "I wasn't trying my hardest too."],\
                  ["Did I lose...?", "What don't you get?", "You were close though.", "Nah, you won."],\
                  ["I fear neither death...nor you.", "But you should.", "There's no need to, I won't do anything.", "Are you scared of clowns, then?"],\
                  ["Do me a solid and end this quick.", "You're not worth my time.", "I refuse to.", "Is that what you want?"]]
    
    strongopening=["Oh? You're not finishing the job?\n", \
                   "Not killing me? A foolish mistake.\n",\
                   "Letting your enemy live? Unwise.\n"]
    
    weaklist=[["Please let me go, I've done nothing to you.", "I won't do anything to you.", "I'll let you go...to hell.", "You attacked me first!"], \
              ["I also have loved ones that'll miss me. You realise that, right?", "I always did.", "I don't care.", "Now that you mention it..."],\
              ["I would have never accepted this task if I knew how dangerous it was.", "What a pity...", "It was your fault for being uninformed", "Could've just said no."],\
              ["Do me a solid and end this quick.", "I refuse to.", "You're not worth my time.", "Is that what you want?"]]
    
    weakopening=["I knew I shouldn't have signed up for this...\n",\
                 "I'm really going to die...\n",\
                 "I should've just stayed at home.\n",\
                 "Looks like its the end for me...\n"]
    
    carefreelist=[["Let's play a game! Guess what I want to eat!", "Hamburgers?", "Shut up.", "Rice?"], \
                  ["Is there a reason I can't beat you?", "I've got the power of friendship!", "You're weak, that's all.", "I'm just younger."], \
                  ["Hey, you should be showing me some respect!", "You're right, Senpai.", "Never thought about it.", "I prefer mutual respect."],\
                  ["Why are you doing this? This is absolutely pre-paw-sterous!", "You were a b-rat.", "You were in my way.", "I don't know either."],\
                  ["Say, why would you pick on a poor chap like me?", "You attacked me first though.", "You were in my way.", "I'm sorry, I didn't mean to hurt you.", ]]
    
    carefreeopening=["Maybe you're not that a-gnawing after all!\n",\
                     "Man, you killed my vibe. That's wiggety-wack, yo.\n",\
                     "Man, why'd boss put me up to this? I'm just an intern.\n",\
                     "Calm down, I was just joking!\n"]
    
    personality=random.randint(0,2)
    
    #returns a different set of potential questions depending on the random variable generated.
    #also prints out an opening statement to clue the players into the enemy's personality.
    if personality==0:
        opening=random.randint(0,len(strongopening)-1)
        print(strongopening[opening])
        return stronglist
    
    elif personality==1:
        opening=random.randint(0,len(weakopening)-1)
        print(weakopening[opening])
        return weaklist
    
    elif personality==2:
        opening=random.randint(0,len(carefreeopening)-1)
        print(carefreeopening[opening])
        return carefreelist    



def negotiation():
    #accessing global stats for rewards
    global stats
    global inventory
    global enemystats
    
    mood=0
    #generates enemy personality and questions
    #negotiation_start returns a random set of questions and associated answers.
    questionlist=negotiation_start()
    
    for i in range(2):
        #fetches the max index to randomly decide which question to ask.
        #the -1 is there to account for it being a list (element starts at 0)
        maxindex=len(questionlist)-1
        var=random.randint(0,maxindex)
        
        #stores the enemy question and associated answers and prints the question out only.
        question=questionlist[var]
        print(question[0])
        
        #creates a new list, shuffledquestion, which only contains the answers. Since the question is always at
        #element 0, specifying [1:4] removes the question. Shuffles the list before printing it out to ensure
        #that players cannot memorise the position of the correct answer. 
        shuffledquestion=question[1:4]
        random.shuffle(shuffledquestion)
        print()
        
        num=1
        for i in shuffledquestion:
            print("{}) {}".format(num, i))
            num+=1
        choice=int(input("\nYour Choice: "))
        
        #checks if player choice is the correct answer, alters enemy mood accordingly.
        if shuffledquestion[choice-1]==question[1]:
            print("The enemy liked that response!\n")
            mood+=1
        elif shuffledquestion[choice-1]==question[2]:
            print("The enemy hated that response.\n")
            mood-=1
        else:
            print("The enemy is indifferent to your response.\n")
        
        #removes the question that was asked to ensure there are no repeats in one encounter.
        questionlist.pop(var)
    
    #randomly deciding rewards.
    if mood==2:
        print("You're not so bad, I'll help you out a little!")
        reward=random.randint(0,3)
        chance=random.randint(0,1)
        if reward==0:
            print("Received 10 gold!")
            stats["Gold"]+=10
        elif reward==1:
            print("Received 1 potion, 1 bomb and 1 corrosive acid!")
            inventory["Potion"]+=1
            inventory["Bomb"]+=1
            inventory["Corrosive Acid"]+=1
        elif reward==2 and has_orb==False and chance==1:
            print("The Rat King said he felt something powerful at {}".format(orb))
        elif reward==2 and chance!=1:
            print("Received 10 gold!")
            stats["Gold"]+=10            
        elif reward==3:
            print("Here. The King has been hoarding loads of this.")
            print("Received 1 Anti Rat Bomb!")
            inventory["Anti Rat Bomb"]+=1
        return True
            
        
    elif mood==1:
        print("You're okay, I'll help you out a little!")
        reward=random.randint(0,3)
        if reward==0:
            print("Received 6 gold!")
            stats["Gold"]+=6
        elif reward==1:
            print("Received 1 potion!")
            inventory["Potion"]+=1
        elif reward==2:
            print("Received 1 bomb!")
            inventory["Bomb"]+=1
        elif reward==3:
            print("Received 1 corrosive acid!")
            inventory["Corrosive Acid"]+=1
        return True
    
    elif mood==0:
        print("Thanks for letting me go, stranger.")
        return True
    elif mood==-1:
        print("You're just as bad as I thought.")
        print("Enemy HP increased by 5!")
        enemystats["HP"]+=5
        return False
    elif mood==-2:
        print("You're even worse than I thought...")
        print("I'll continue fighting even if I perish...!")
        print("The enemy's eyes flared to life!")
        print("Enemy HP increased by 10!")
        print("Enemy damage increased by 2!")
        enemystats["HP"]+=10
        enemystats["mindmg"]+=2
        enemystats["maxdmg"]+=2
        dmgrange=''
        dmgrange=dmgrange+str(enemystats["mindmg"]) + "-" + str(enemystats["maxdmg"])
        enemystats["Damage"]=dmgrange
        return False
        
    
    
#the main game!
#main_menu is the starting point so it appears outside the loop.
#this while loop will print the current day each time an action is taken. It will also trigger different
#scenarios depending on whether the player is on an open tile, town tile or the rat king tile. 

main_menu()
while True:
    if world_map[pos[0]][pos[1]]=="H/T":
        town_menu()
    elif world_map[pos[0]][pos[1]]=="H/K":
        print("Day {}: You see the Rat King!".format(day))
        boss_fight()
        outdoor_menu()
    else:
        print("\nDay {}. You are out in the open.".format(day))
        combat()
        print("\nDay {}. You are out in the open.".format(day))
        outdoor_menu()