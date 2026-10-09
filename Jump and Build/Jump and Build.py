import pygame
import sys
import copy
import math
import pickle
import os
BLAU = (0, 0, 255)
ROT=(255,0,0)
WEISS = (255, 255, 255)
SCHWARZ = (0, 0, 0)
GRUEN = (0, 255, 0)
GRID_SIZE = 25
class Box():
    def __init__(self, x, y, b, h,Bild, Kollision):
        self.rect = pygame.Rect(x, y, b, h)
        self.Kollision=Kollision
        self.Bild=Bild
    def box_bewegen(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        
    def zeichne(self, bildschirm):
        if self.Kollision==1:
            bild=pygame.transform.scale(spiel.Bilder[self.Bild], (spiel.gitter, spiel.gitter))
        if self.Kollision==0:
            bild=pygame.transform.scale(spiel.img_block_Checkpoint,(spiel.gitter, spiel.gitter))
        if self.Kollision==2:
            bild=pygame.transform.scale(spiel.img_block_Respawn,(spiel.gitter, spiel.gitter))
        if self.Kollision==3:
            bild=pygame.transform.scale(spiel.Ziel_Flagge,(spiel.gitter, spiel.gitter))
        bildschirm.blit(bild, self.rect)
          
    def kollidiert(self, rect):
        return self.rect.colliderect(rect)

class Lift(Box):
    def __init__(self, x, y, b, h, farbe, ziel_x, ziel_y,Kollision, tempo=2):
        super().__init__(x, y, b, h, farbe, Kollision)
        
        self.vektor_x = ziel_x - x
        self.vektor_y = ziel_y - y
        self.max_distanz = math.hypot(self.vektor_x, self.vektor_y)
        self.aktuelle_distanz = 0
        self.tempo = tempo
        self.hinweg = True
        self.rest_x = 0.0
        self.rest_y = 0.0
        
    def bewege_lift(self, spieler_rect):
        if self.max_distanz == 0:
            return 0, 0
            
        richtung = 1 if self.hinweg else -1
        schritt_x = (self.vektor_x / self.max_distanz) * self.tempo * richtung
        schritt_y = (self.vektor_y / self.max_distanz) * self.tempo * richtung
        
        self.aktuelle_distanz += self.tempo * richtung
        
        if self.aktuelle_distanz >= self.max_distanz:
            self.aktuelle_distanz = self.max_distanz
            self.hinweg = False
        elif self.aktuelle_distanz <= 0:
            self.aktuelle_distanz = 0
            self.hinweg = True
        test_spieler = copy.copy(spieler_rect)
        test_spieler.y += 1
        
            
        self.rest_x += schritt_x
        self.rest_y += schritt_y
        move_x = int(self.rest_x)
        move_y = int(self.rest_y)
        self.rest_x -= move_x
        self.rest_y -= move_y
        if not test_spieler.colliderect(self.rect) or not spiel.gravitation==0 and test_spieler.colliderect(self.rect):
            self.rect.x += move_x
            self.rect.y += move_y
        
        return move_x, move_y
class Spieler:
    def __init__(self, bildschirm_breite, bildschirm_hoehe):
        
        gitter = bildschirm_hoehe/GRID_SIZE
        self.rect = pygame.Rect(bildschirm_breite / 2, bildschirm_hoehe/2, gitter/2, gitter/2)

    def zeichne(self, bildschirm):
        pygame.draw.rect(bildschirm, ROT, self.rect)

class Menu:
    def __init__(self, spiel):
        self.modus=1
        self.spiel = spiel
        self.länge_spiel_sequenz=(len(self.spiel.speicher)-1)
        self.durchlauf=0
        self.bewegung_x=0
        self.bewegung_y=0
        self.seite="links"
        self.zähler=1
        self.zähler_level=1
        self.spieltyp=""
    def spiel_sequenz(self):
        gitter=self.spiel.width/30
        spiel.spieler = self.spiel.speicher[self.durchlauf][0]
        spiel.boxes = self.spiel.speicher[self.durchlauf][1]
        spiel.lifte = self.spiel.speicher[self.durchlauf][3]
        spiel.Bewegung_y=self.spiel.speicher[self.durchlauf][4]
        self.durchlauf+=1
        if self.durchlauf==self.länge_spiel_sequenz:
            self.durchlauf=0
        spiel.Hintergrund_zeichnen()
        self.bewegung_x-=1
        self.bewegung_y-=1
        for i in range(32):
            i-=2
            for j in range(self.spiel.width // 30+2):
                j-=2
                pygame.draw.rect(
                    self.spiel.bildschirm,
                    WEISS,
                    (j * gitter+self.bewegung_x, i * gitter+self.bewegung_y, gitter, gitter),2)

        if (self.bewegung_x*-1)>gitter:
            self.bewegung_x=0
            self.bewegung_y=0
        
        self.spiel.spieler.zeichne(self.spiel.bildschirm)

        for box in self.spiel.boxes:
            box.zeichne(self.spiel.bildschirm)
        
        
    def Text_zeichnen_und_Tasteninputs_für_menu_1(self):
        if self.spiel.mode!="menu2":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.spiel.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.spiel.quit()
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.spiel.boxes = []
                            self.spiel.zielorte = []
                            self.spiel.lifte = []
                            self.spiel.richtungen = []
                            self.spiel.anzahl_liftendpunkte = []
                            self.spiel.mode="menu2"

        
        
        gitter = self.spiel.gitter
        bild = pygame.transform.scale(spiel.Rechteck, (848,140))
        spiel.bildschirm.blit(bild,(self.spiel.width/5*1.5+1,spiel.height/25+1))
        pygame.draw.rect(self.spiel.bildschirm, WEISS, (self.spiel.width/5*1.5,spiel.height/25,850,142),4)
        
        font = pygame.font.Font(None, 150)
        text = font.render("Jump and Build", True, WEISS)
        self.spiel.bildschirm.blit(text , (self.spiel.width/5*1.5+gitter, self.spiel.height/35+self.spiel.gitter))
        
        bild = pygame.transform.scale(spiel.Rechteck, (970,92))
        spiel.bildschirm.blit(bild,(self.spiel.width/5*1.35+1,spiel.height/10*8+30))
        pygame.draw.rect(self.spiel.bildschirm, WEISS, (self.spiel.width/5*1.35,spiel.height/10*8+29,972,94),4)
        font = pygame.font.Font(None, 100)
        text = font.render("Drücke Space um zu starten", True, WEISS)
        self.spiel.bildschirm.blit(text , text.get_rect(center=(self.spiel.width/5*1.35+972/2, self.spiel.height/10*8+29+94/2)))

        if self.spiel.mode!="menu2":
            pygame.display.flip()
    def Text_zeichnen_und_Tasteninputs_für_menu_2(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.spiel.quit()
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.spiel.mode="menu"
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.seite="links"
                    if event.key == pygame.K_RIGHT:
                        self.seite="rechts"
                    if event.key == pygame.K_BACKSPACE:
                        if self.modus==1:
                            if os.path.exists("Welt_1.pkl"):
                                os.remove("Welt_1.pkl")
                        if self.modus==2:
                            if os.path.exists("Welt_2.pkl"):
                                os.remove("Welt_2.pkl")
                        if self.modus==3:
                            if os.path.exists("Welt_3.pkl"):
                                os.remove("Welt_3.pkl")
                    if event.key == pygame.K_SPACE:
                        if self.modus==1:
                            try:
                                with open("Welt_1.pkl", "rb") as datei:
                                      
                                    self.spiel.Welt = pickle.load(datei)
                                    memo={}
                                    
                                    self.spiel.spieler = copy.deepcopy(self.spiel.Welt[0],memo)     
                                    self.spiel.boxes = copy.deepcopy(self.spiel.Welt[1],memo)
                                    self.spiel.zielorte = copy.deepcopy(self.spiel.Welt[2],memo)
                                    self.spiel.lifte = copy.deepcopy(self.spiel.Welt[3],memo)
                                    self.spiel.richtungen = copy.deepcopy(self.spiel.Welt[4],memo)
                                    self.spiel.anzahl_liftendpunkte = copy.deepcopy(self.spiel.Welt[5],memo)
                                    self.spiel.spawnInfos.spieler = copy.deepcopy(self.spiel.Welt[6],memo)
                                    self.spiel.spawnInfos.boxes = copy.deepcopy(self.spiel.Welt[7],memo)
                                    self.spiel.spawnInfos.zielorte = copy.deepcopy(self.spiel.Welt[8],memo)
                                    self.spiel.spawnInfos.lifte = copy.deepcopy(self.spiel.Welt[9],memo)
                                    self.spiel.spawnInfos.richtungen = copy.deepcopy(self.spiel.Welt[10],memo)
                                    self.spiel.spawnInfos.anzahl_liftendpunkte = copy.deepcopy(self.spiel.Welt[11],memo)
                                    self.spiel.bewegung_y_rest=copy.deepcopy(self.spiel.Welt[12],memo)
                                    self.spiel.Bewegung_y=copy.deepcopy(self.spiel.Welt[13],memo)
                                    self.spiel.Hintergrund_zahl=copy.deepcopy(self.spiel.Welt[14],memo)
                                    try:
                                        with open("Rekorde.pkl", "rb") as datei:
                                            if self.spiel.Startmodus==False:
                                                self.spiel.Rekorde= pickle.load(datei)
                                    except FileNotFoundError:
                                        pass
                                    self.spiel.Rekord=self.spiel.Rekorde[0]
                                    self.spieltyp="Welt"
                                    if self.seite=="links":
                                        self.spiel.mode="play"
                                        self.spiel.Startmodus="play"
                                        self.spiel.start_zeit = pygame.time.get_ticks()
                                    if self.seite=="rechts":
                                        self.spiel.passe_in_gitter()
                                        self.spiel.mode="edit"
                                        self.spiel.Startmodus="edit"
                            except FileNotFoundError:
                                self.spiel.boxes = []
                                self.spiel.zielorte = []
                                self.spiel.lifte = []
                                self.spiel.richtungen = []
                                self.spiel.anzahl_liftendpunkte = []
                                
                                self.spiel.mode="edit"
                                self.spiel.Startmodus="edit"

                        if self.modus==2:
                            try:
                                with open("Welt_2.pkl", "rb") as datei:
                                    memo={}
                                    self.spiel.Welt = pickle.load(datei)
                                    self.spiel.spieler = copy.deepcopy(self.spiel.Welt[0],memo)     
                                    self.spiel.boxes = copy.deepcopy(self.spiel.Welt[1],memo)
                                    self.spiel.zielorte = copy.deepcopy(self.spiel.Welt[2],memo)
                                    self.spiel.lifte = copy.deepcopy(self.spiel.Welt[3],memo)
                                    self.spiel.richtungen = copy.deepcopy(self.spiel.Welt[4],memo)
                                    self.spiel.anzahl_liftendpunkte = copy.deepcopy(self.spiel.Welt[5],memo)
                                    self.spiel.spawnInfos.spieler = copy.deepcopy(self.spiel.Welt[6],memo)
                                    self.spiel.spawnInfos.boxes = copy.deepcopy(self.spiel.Welt[7],memo)
                                    self.spiel.spawnInfos.zielorte = copy.deepcopy(self.spiel.Welt[8],memo)
                                    self.spiel.spawnInfos.lifte = copy.deepcopy(self.spiel.Welt[9],memo)
                                    self.spiel.spawnInfos.richtungen = copy.deepcopy(self.spiel.Welt[10],memo)
                                    self.spiel.spawnInfos.anzahl_liftendpunkte = copy.deepcopy(self.spiel.Welt[11],memo)
                                    self.spiel.bewegung_y_rest=copy.deepcopy(self.spiel.Welt[12],memo)
                                    self.spiel.Bewegung_y=copy.deepcopy(self.spiel.Welt[13],memo)
                                    self.spiel.Hintergrund_zahl=copy.deepcopy(self.spiel.Welt[14],memo)
                                    try:
                                        with open("Rekorde.pkl", "rb") as datei:
                                            if self.spiel.Startmodus==False:
                                                self.spiel.Rekorde= pickle.load(datei)
                                    except FileNotFoundError:
                                        pass
                                    self.spiel.Rekord=self.spiel.Rekorde[1]
                                    self.spieltyp="Welt"
                                    if self.seite=="links":
                                        self.spiel.mode="play"
                                        self.spiel.Startmodus="play"
                                        self.spiel.start_zeit = pygame.time.get_ticks()

                                    if self.seite=="rechts":
                                        self.spiel.passe_in_gitter()
                                        self.spiel.mode="edit"
                                        self.spiel.Startmodus="edit"

                            except FileNotFoundError:
                                self.spiel.boxes = []
                                self.spiel.zielorte = []
                                self.spiel.lifte = []
                                self.spiel.richtungen = []
                                self.spiel.anzahl_liftendpunkte = []
                                self.spiel.mode="edit"
                                self.spiel.Startmodus="edit"

                        if self.modus==3:
                            try:
                                with open("Welt_3.pkl", "rb") as datei:
                                    self.spiel.Welt = pickle.load(datei)
                                    memo={}
                                    
                                    self.spiel.spieler = copy.deepcopy(self.spiel.Welt[0],memo)     
                                    self.spiel.boxes = copy.deepcopy(self.spiel.Welt[1],memo)
                                    self.spiel.zielorte = copy.deepcopy(self.spiel.Welt[2],memo)
                                    self.spiel.lifte = copy.deepcopy(self.spiel.Welt[3],memo)
                                    self.spiel.richtungen = copy.deepcopy(self.spiel.Welt[4],memo)
                                    self.spiel.anzahl_liftendpunkte = copy.deepcopy(self.spiel.Welt[5],memo)
                                    self.spiel.spawnInfos.spieler = copy.deepcopy(self.spiel.Welt[6],memo)
                                    self.spiel.spawnInfos.boxes = copy.deepcopy(self.spiel.Welt[7],memo)
                                    self.spiel.spawnInfos.zielorte = copy.deepcopy(self.spiel.Welt[8],memo)
                                    self.spiel.spawnInfos.lifte = copy.deepcopy(self.spiel.Welt[9],memo)
                                    self.spiel.spawnInfos.richtungen = copy.deepcopy(self.spiel.Welt[10],memo)
                                    self.spiel.spawnInfos.anzahl_liftendpunkte = copy.deepcopy(self.spiel.Welt[11],memo)
                                    self.spiel.bewegung_y_rest=copy.deepcopy(self.spiel.Welt[12],memo)
                                    self.spiel.Bewegung_y=copy.deepcopy(self.spiel.Welt[13],memo)
                                    self.spiel.Hintergrund_zahl=copy.deepcopy(self.spiel.Welt[14],memo)
                                    try:
                                        with open("Rekorde.pkl", "rb") as datei:
                                            if self.spiel.Startmodus==False:
                                                self.spiel.Rekorde= pickle.load(datei)
                                    except FileNotFoundError:
                                        pass
                                    self.spiel.Rekord=self.spiel.Rekorde[2]
                                    self.spieltyp="Welt"
                                    if self.seite=="links":
                                        self.spiel.mode="play"
                                        self.spiel.Startmodus="play"
                                        self.spiel.start_zeit = pygame.time.get_ticks()

                                    if self.seite=="rechts":
                                        self.spiel.passe_in_gitter()
                                        self.spiel.mode="edit"
                                        self.spiel.Startmodus="edit"

                            except FileNotFoundError:
                                self.spiel.boxes = []
                                self.spiel.zielorte = []
                                self.spiel.lifte = []
                                self.spiel.richtungen = []
                                self.spiel.anzahl_liftendpunkte = []
                                self.spiel.mode="edit"
                                self.spiel.Startmodus="edit" 

                        if self.modus==4:
                            self.spiel.mode="menu4"
                                
                    if event.key == pygame.K_UP:
                        self.modus-=1
                        if self.modus<1:
                            self.modus=4
                    if event.key == pygame.K_DOWN:
                        self.modus+=1
                        if self.modus>4:
                            self.modus=1
                            
        font = pygame.font.Font(None, 48)
        haupt_x = self.spiel.width / 5 * 1
        haupt_y = self.spiel.height / 5
        bild = pygame.transform.scale(spiel.Rechteck, (1265,640))
        spiel.bildschirm.blit(bild,(haupt_x + 1,haupt_y + 1))
        pygame.draw.rect(self.spiel.bildschirm, WEISS, pygame.Rect(haupt_x, haupt_y, 1267, 642),4)
        box_breite = 690
        box_hoehe = 125
        start_x = self.spiel.width / 5 * 1.7
        start_y = haupt_y + 30
        abstand_y = 140
        farbe1 = GRUEN if self.modus == 1 else WEISS
        rect1_aussen = pygame.Rect(start_x, start_y + 0 * abstand_y, box_breite, box_hoehe)
        bild = pygame.transform.scale(spiel.Rechteck_lila, (box_breite - 4,box_hoehe - 4))
        if farbe1==GRUEN:
            spiel.bildschirm.blit(bild,(start_x + 2,start_y + 0 * abstand_y + 2))
        pygame.draw.rect(self.spiel.bildschirm, farbe1, rect1_aussen,4)
        text1 = font.render("Spiel_Welt1", True, WEISS)
        self.spiel.bildschirm.blit(text1, text1.get_rect(center=rect1_aussen.center))
        if self.modus==1:
            self.farbe_links=GRUEN if self.seite=="links" else WEISS
            self.farbe_rechts=GRUEN if self.seite=="rechts" else WEISS
            rect1_sp_aussen = pygame.Rect(haupt_x*1.05 + 20, start_y + 0 * abstand_y, 200, box_hoehe)
            bild = pygame.transform.scale(spiel.Rechteck_lila, (196,box_hoehe - 4))
            spiel.bildschirm.blit(bild,(haupt_x*1.05+22,start_y + 0 * abstand_y + 2))
            pygame.draw.rect(self.spiel.bildschirm, self.farbe_links, rect1_sp_aussen,4)
            text1_sp = font.render("Spielen", True, WEISS)
            self.spiel.bildschirm.blit(text1_sp, text1_sp.get_rect(center=rect1_sp_aussen.center))

            ed_x = 2 * start_x + box_breite - haupt_x * 1.05 - 220

            rect1_ed_aussen = pygame.Rect(ed_x, start_y + 0 * abstand_y, 200, box_hoehe)
            bild = pygame.transform.scale(spiel.Rechteck_lila, (196,box_hoehe - 4))
            spiel.bildschirm.blit(bild,(ed_x + 2,start_y + 0 * abstand_y + 2))
            pygame.draw.rect(self.spiel.bildschirm, self.farbe_rechts, rect1_ed_aussen,4)
            text1_ed = font.render("Editieren", True, WEISS)
            self.spiel.bildschirm.blit(text1_ed, text1_ed.get_rect(center=rect1_ed_aussen.center))
        farbe2 = GRUEN if self.modus == 2 else WEISS
        rect2_aussen = pygame.Rect(start_x, start_y + 1 * abstand_y, box_breite, box_hoehe)
        bild = pygame.transform.scale(spiel.Rechteck_lila, (box_breite - 4,box_hoehe - 4))
        if farbe2==GRUEN:
            spiel.bildschirm.blit(bild,(start_x + 2,start_y + 1 * abstand_y + 2))
        pygame.draw.rect(self.spiel.bildschirm, farbe2, rect2_aussen,4)
        text2 = font.render("Spiel_Welt2", True, WEISS)
        self.spiel.bildschirm.blit(text2, text2.get_rect(center=rect2_aussen.center))
        if self.modus==2:
            self.farbe_links=GRUEN if self.seite=="links" else WEISS
            self.farbe_rechts=GRUEN if self.seite=="rechts" else WEISS
            rect1_sp_aussen = pygame.Rect(haupt_x*1.05 + 20, start_y + 1 * abstand_y, 200, box_hoehe)
            bild = pygame.transform.scale(spiel.Rechteck_lila, (196,box_hoehe - 4))
            spiel.bildschirm.blit(bild,(haupt_x*1.05 + 22,start_y + 1 * abstand_y+2))
            pygame.draw.rect(self.spiel.bildschirm, self.farbe_links, rect1_sp_aussen,4)
            text1_sp = font.render("Spielen", True, WEISS)
            self.spiel.bildschirm.blit(text1_sp, text1_sp.get_rect(center=rect1_sp_aussen.center))
            ed_x = 2 * start_x + box_breite - haupt_x * 1.05 - 220

            rect1_ed_aussen = pygame.Rect(ed_x, start_y + 1 * abstand_y, 200, box_hoehe)
            bild = pygame.transform.scale(spiel.Rechteck_lila, (196,box_hoehe - 4))
            spiel.bildschirm.blit(bild,(ed_x + 2,start_y + 1 * abstand_y + 2))
            pygame.draw.rect(self.spiel.bildschirm, self.farbe_rechts, rect1_ed_aussen,4)
            
            text1_ed = font.render("Editieren", True, WEISS)
            self.spiel.bildschirm.blit(text1_ed, text1_ed.get_rect(center=rect1_ed_aussen.center))
        
        farbe3 = GRUEN if self.modus == 3 else WEISS
        rect3_aussen = pygame.Rect(start_x, start_y + 2 * abstand_y, box_breite, box_hoehe)
        bild = pygame.transform.scale(spiel.Rechteck_lila, (box_breite - 4,box_hoehe - 4))
        if farbe3==GRUEN:
            spiel.bildschirm.blit(bild,(start_x + 2,start_y + 2 * abstand_y + 2))
        pygame.draw.rect(self.spiel.bildschirm, farbe3, rect3_aussen,4)
        
        text3 = font.render("Spiel_Welt3", True, WEISS)
        self.spiel.bildschirm.blit(text3, text3.get_rect(center=rect3_aussen.center))
        if self.modus==3:
            self.farbe_links=GRUEN if self.seite=="links" else WEISS
            self.farbe_rechts=GRUEN if self.seite=="rechts" else WEISS
            rect1_sp_aussen = pygame.Rect(haupt_x*1.05 + 20, start_y + 2 * abstand_y, 200, box_hoehe)
            bild = pygame.transform.scale(spiel.Rechteck_lila, (196,box_hoehe - 4))
            spiel.bildschirm.blit(bild,(haupt_x*1.05 + 22,start_y + 2 * abstand_y + 2))
            pygame.draw.rect(self.spiel.bildschirm, self.farbe_links, rect1_sp_aussen,4)
            text1_sp = font.render("Spielen", True, WEISS)
            self.spiel.bildschirm.blit(text1_sp, text1_sp.get_rect(center=rect1_sp_aussen.center))
            ed_x = 2 * start_x + box_breite - haupt_x * 1.05 - 220

            rect1_ed_aussen = pygame.Rect(ed_x, start_y + 2 * abstand_y, 200, box_hoehe)
            bild = pygame.transform.scale(spiel.Rechteck_lila, (196,box_hoehe - 4))
            spiel.bildschirm.blit(bild,(ed_x + 2, start_y + 2 * abstand_y))
            pygame.draw.rect(self.spiel.bildschirm, self.farbe_rechts, rect1_ed_aussen,4)
            text1_ed = font.render("Editieren", True, WEISS)
            self.spiel.bildschirm.blit(text1_ed, text1_ed.get_rect(center=rect1_ed_aussen.center))

        farbe4 = GRUEN if self.modus == 4 else WEISS
        rect4_aussen = pygame.Rect(start_x, start_y + 3 * abstand_y, box_breite, box_hoehe)
        bild = pygame.transform.scale(spiel.Rechteck_lila, (box_breite - 4,box_hoehe - 4))
        if farbe4==GRUEN:
            spiel.bildschirm.blit(bild,(start_x + 2, start_y + 3 * abstand_y + 2))
        pygame.draw.rect(self.spiel.bildschirm, farbe4, rect4_aussen,4)
        
        text4 = font.render("Levels", True, farbe4)
        self.spiel.bildschirm.blit(text4, text4.get_rect(center=rect4_aussen.center))
        pygame.display.flip()
    def Text_zeichnen_und_Tasteninputs_für_menu_3(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    self.spiel.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.spiel.mode="menu"
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.zähler-=1
                    if event.key == pygame.K_RIGHT:
                        self.zähler+=1
                    if event.key == pygame.K_SPACE:
                        memo={}
                        self.spiel.start_zeit = pygame.time.get_ticks()
                        self.spiel.spieler = copy.deepcopy(self.spiel.Welt[0],memo)     
                        self.spiel.boxes = copy.deepcopy(self.spiel.Welt[1],memo)
                        self.spiel.zielorte = copy.deepcopy(self.spiel.Welt[2],memo)
                        self.spiel.lifte = copy.deepcopy(self.spiel.Welt[3],memo)
                        self.spiel.richtungen = copy.deepcopy(self.spiel.Welt[4],memo)
                        self.spiel.anzahl_liftendpunkte = copy.deepcopy(self.spiel.Welt[5],memo)
                        self.spiel.spawnInfos.spieler = copy.deepcopy(self.spiel.Welt[6],memo)
                        self.spiel.spawnInfos.boxes = copy.deepcopy(self.spiel.Welt[7],memo)
                        self.spiel.spawnInfos.zielorte = copy.deepcopy(self.spiel.Welt[8],memo)
                        self.spiel.spawnInfos.lifte = copy.deepcopy(self.spiel.Welt[9],memo)
                        self.spiel.spawnInfos.richtungen = copy.deepcopy(self.spiel.Welt[10],memo)
                        self.spiel.spawnInfos.anzahl_liftendpunkte = copy.deepcopy(self.spiel.Welt[11],memo)
                        self.spiel.bewegung_y_rest=copy.deepcopy(self.spiel.Welt[12],memo)
                        self.spiel.Bewegung_y=copy.deepcopy(self.spiel.Welt[13],memo)
                        self.spiel.Hintergrund_zahl=copy.deepcopy(self.spiel.Welt[14],memo)
                        if self.zähler==1:
                            if self.spiel.Startmodus=="edit":
                            
                                self.spiel.speicherdatei=[self.spiel.spieler, self.spiel.boxes, self.spiel.zielorte, self.spiel.lifte, self.spiel.richtungen, self.spiel.anzahl_liftendpunkte,self.spiel.spawnInfos.spieler, self.spiel.spawnInfos.boxes,self.spiel.spawnInfos.zielorte, self.spiel.spawnInfos.lifte,self.spiel.spawnInfos.richtungen, self.spiel.spawnInfos.anzahl_liftendpunkte,self.spiel.bewegung_y_rest, self.spiel.Bewegung_y,self.spiel.Hintergrund_zahl, self.spiel.Rekorde]
                                
                                self.spiel.speichern()
                            if self.spiel.Startmodus=="play":
                                self.spiel.speicherdatei=[self.spiel.Welt[0], self.spiel.Welt[1], self.spiel.Welt[2], self.spiel.Welt[3],self.spiel.Welt[4], self.spiel.Welt[5], self.spiel.Welt[6], self.spiel.Welt[7],self.spiel.Welt[8], self.spiel.Welt[9], self.spiel.Welt[10], self.spiel.Welt[11],self.spiel.Welt[12], self.spiel.Welt[13], self.spiel.Welt[14], self.spiel.Rekorde]
                                self.spiel.speichern()
                            self.spiel.mode="menu"
                        if self.zähler==2 and self.modus!=4:
                            self.spiel.mode="edit"
                        if self.zähler==3 or self.modus==4 and self.zähler==2:
                            self.spiel.Startmodus="play"
                            self.spiel.mode="play"
        if self.zähler==0 and self.modus!=4:
            self.zähler=3
        if self.zähler==0 and self.modus==4:
            self.zähler=2
        if self.zähler==4 or self.modus==4 and self.zähler==3:
            self.zähler=1
        font = pygame.font.Font(None, 120)
        haupt_x = self.spiel.width / 5 * 1
        haupt_y = self.spiel.height / 5
        bild = pygame.transform.scale(spiel.Rechteck, (1267,642))
        spiel.bildschirm.blit(bild,(haupt_x, haupt_y))
        pygame.draw.rect(self.spiel.bildschirm, WEISS, pygame.Rect(haupt_x, haupt_y, 1267, 642),4)
        text = font.render("Du hast das Level geschafft.", True, WEISS)
        self.spiel.bildschirm.blit(text, text.get_rect(center=(((haupt_x+haupt_x+1267)/2,(haupt_y+haupt_y+640/5)/2))))
        text=f"Zeit: {self.spiel.minuten:02d}:{self.spiel.sekunden:02d}:{self.spiel.vergangene_zeit:02d}"
        font=pygame.font.Font(None, 70)
        text = font.render(text, True, WEISS)
        self.spiel.bildschirm.blit(text, text.get_rect(center=(((haupt_x+haupt_x+1267)/2,(haupt_y+haupt_y+640/5*4)/2))))
        if self.spiel.Rekord>self.spiel.vergangene_zeit_backup and self.spiel.Startmodus=="play" or self.spiel.Rekord==False and self.spiel.Startmodus=="play":
            if self.spiel.vergangene_zeit_backup!=0:
                self.spiel.Rekord=self.spiel.vergangene_zeit_backup
        if self.spieltyp=="Welt":
            self.spiel.Rekorde[(self.modus-1)]=self.spiel.Rekord
        if self.spieltyp=="level":
            self.spiel.Rekorde[(self.zähler_level+2)]=self.spiel.Rekord
        self.vergangene_zeit=self.spiel.Rekord
        self.minuten=self.vergangene_zeit//(60*100)
        self.vergangene_zeit-=self.minuten*60*100
        self.sekunden=self.vergangene_zeit//100
        self.vergangene_zeit-=self.sekunden*100
        text=f"Rekord: {self.minuten:02}:{self.sekunden:02}:{self.vergangene_zeit:02}"
        text = font.render(text, True, WEISS)
        self.spiel.bildschirm.blit(text, text.get_rect(center=(((haupt_x+haupt_x+1267)/2,(haupt_y+haupt_y+640/5*6)/2))))
        bild = pygame.transform.scale(spiel.Rechteck_lila, (300,100))
        if self.zähler==1:
            spiel.bildschirm.blit(bild,(haupt_x+100, haupt_y+500))
        pygame.draw.rect(self.spiel.bildschirm, WEISS, pygame.Rect(haupt_x+100, haupt_y+500, 300, 100),4)
        text = font.render("Hauptmenü", True, WEISS)
        self.spiel.bildschirm.blit(text, text.get_rect(center=((haupt_x+100+300/2,haupt_y+500+100/2))))
        verschiebung=384
        if self.zähler==2 and self.modus!=4:
            spiel.bildschirm.blit(bild,(haupt_x+100+verschiebung, haupt_y+500))
        if self.modus!=4:
            text = font.render("Editor", True, WEISS)
            self.spiel.bildschirm.blit(text, text.get_rect(center=((haupt_x+100+verschiebung+300/2,haupt_y+500+100/2))))
            pygame.draw.rect(self.spiel.bildschirm, WEISS, pygame.Rect(haupt_x+100+verschiebung, haupt_y+500, 300, 100),4)
        if self.zähler==3 or self.zähler==2 and self.modus==4:
            spiel.bildschirm.blit(bild,(haupt_x+100+verschiebung*2, haupt_y+500))
        font=pygame.font.Font(None, 40)
        text = font.render("Erneut versuchen", True, WEISS)
        self.spiel.bildschirm.blit(text, text.get_rect(center=((haupt_x+100+verschiebung*2+300/2,haupt_y+500+100/2))))
        pygame.draw.rect(self.spiel.bildschirm, WEISS, pygame.Rect(haupt_x+100+verschiebung*2, haupt_y+500, 300, 100),4)
        pygame.display.flip()
    def Text_zeichnen_und_Tasteninputs_für_menu_4(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    self.spiel.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.spiel.mode="menu2"
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.zähler_level-=1
                        if self.zähler_level==0:
                            self.zähler_level=5
                        elif self.zähler_level==5:
                                self.zähler_level=10
                    if event.key == pygame.K_RIGHT:
                        self.zähler_level+=1
                        if self.zähler_level==6:
                            self.zähler_level=1
                        if self.zähler_level==11:
                            self.zähler_level=6
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        if self.zähler_level<=5:
                            self.zähler_level=self.zähler_level+5
                        else:
                            self.zähler_level=self.zähler_level-5
                    if event.key == pygame.K_SPACE:
                        level=self.zähler_level-1
                        with open("levels.pkl", "rb") as datei:
                            self.spiel.levels= pickle.load(datei)
                            memo={}
                            self.spiel.Welt = self.spiel.levels[level]
                            self.spiel.spieler = copy.deepcopy(self.spiel.Welt[0],memo)     
                            self.spiel.boxes = copy.deepcopy(self.spiel.Welt[1],memo)
                            self.spiel.zielorte = copy.deepcopy(self.spiel.Welt[2],memo)
                            self.spiel.lifte = copy.deepcopy(self.spiel.Welt[3],memo)
                            self.spiel.richtungen = copy.deepcopy(self.spiel.Welt[4],memo)
                            self.spiel.anzahl_liftendpunkte = copy.deepcopy(self.spiel.Welt[5],memo)
                            self.spiel.spawnInfos.spieler = copy.deepcopy(self.spiel.Welt[6],memo)
                            self.spiel.spawnInfos.boxes = copy.deepcopy(self.spiel.Welt[7],memo)
                            self.spiel.spawnInfos.zielorte = copy.deepcopy(self.spiel.Welt[8],memo)
                            self.spiel.spawnInfos.lifte = copy.deepcopy(self.spiel.Welt[9],memo)
                            self.spiel.spawnInfos.richtungen = copy.deepcopy(self.spiel.Welt[10],memo)
                            self.spiel.spawnInfos.anzahl_liftendpunkte = copy.deepcopy(self.spiel.Welt[11],memo)
                            self.spiel.bewegung_y_rest=copy.deepcopy(self.spiel.Welt[12],memo)
                            self.spiel.Bewegung_y=copy.deepcopy(self.spiel.Welt[13],memo)
                            self.spiel.Hintergrund_zahl=copy.deepcopy(self.spiel.Welt[14],memo)
                            try:
                                with open("Rekorde.pkl", "rb") as datei:
                                    if self.spiel.Startmodus==False:
                                        self.spiel.Rekorde= pickle.load(datei)
                            except FileNotFoundError:
                                pass
                            self.spiel.Rekord=self.spiel.Rekorde[(level+3)]
                            self.spiel.mode="play"
                            self.spiel.Startmodus="play"
                            self.spieltyp="level"
                            self.spiel.start_zeit = pygame.time.get_ticks()
                            
        
        
                        
        haupt_x = self.spiel.width / 5 * 1
        haupt_y = self.spiel.height / 5
        bild = pygame.transform.scale(spiel.Rechteck, (1267,642))
        spiel.bildschirm.blit(bild,(haupt_x, haupt_y))
        verschiebung_x=242
        verschiebung_y=342
        for i in range(5):
            for b in range(2):
                font=pygame.font.Font(None, 40)
                Zahl=i+1+b*5
                text=f"Level {Zahl}"
                text = font.render(text, True, WEISS)
                if ((i+1)+b*5)==self.zähler_level:
                    bild=pygame.transform.scale(spiel.Rechteck_lila, (200,200))
                else:
                    bild = pygame.transform.scale(spiel.Rechteck, (200,200))
                
                
                spiel.bildschirm.blit(bild,(haupt_x+50+verschiebung_x*i, haupt_y+b*verschiebung_y+50))
                self.spiel.bildschirm.blit(text, text.get_rect(center=((haupt_x+150+verschiebung_x*i, haupt_y+b*verschiebung_y+150))))
                pygame.draw.rect(self.spiel.bildschirm, WEISS, pygame.Rect(haupt_x+50+verschiebung_x*i, haupt_y+b*verschiebung_y+50,200,200),4)
        pygame.display.flip()
                    
        
                 
        
        
class Editor:
    
    
    
    
    def __init__(self, spiel):
        self.spiel = spiel
        self.modus = 1
        self.lift_start = None
        self.verschiebung_y_Koordinate=0
        self.verschiebung_x_Koordinate=0
        self.width = self.spiel.width
        

    def zeichne_grid(self):
        
        
        
        gitter = self.spiel.height // GRID_SIZE
        for i in range(GRID_SIZE):
            for j in range(self.spiel.width // gitter):

                pygame.draw.rect(
                    self.spiel.bildschirm,
                    SCHWARZ,
                    (j * gitter, i * gitter, gitter, gitter),1)

                
                
    def erklaerung(self, text_gross, text_taste, x, y, selected,Bild):
        
        
        
        gitter = self.spiel.height // 40
        breite = 8*gitter
        hoehe = breite
        bild = pygame.transform.scale(spiel.Rechteck_gerundet, (breite, hoehe))
        
        spiel.bildschirm.blit(bild,(x,y))
        farbe = GRUEN if selected else WEISS
        
        pygame.draw.rect(self.spiel.bildschirm, farbe, (x,y,breite,hoehe),4,border_radius=20)
        if type(Bild)==int:
            spiel.bildschirm.blit(spiel.Bilder[Bild],spiel.Bilder[Bild].get_rect(center=((x+breite/2),(y+hoehe/4))))
        else:
            Bild_block= pygame.transform.scale(Bild, (spiel.gitter*1.5, spiel.gitter*1.5))
            spiel.bildschirm.blit(Bild_block, Bild_block.get_rect(center=((x+breite/2),(y+hoehe/4))))

        font_gross = pygame.font.Font(None, 36)
        font_klein = pygame.font.Font(None, 20)
        text_block_gross = font_gross.render(text_gross, True, WEISS)
        text_block_klein = font_klein.render(text_taste, True, WEISS)
       
        self.spiel.bildschirm.blit(text_block_gross , text_block_gross.get_rect(center=(((x+breite/2)),((hoehe+y-spiel.gitter*1.2)))))
        self.spiel.bildschirm.blit(text_block_klein , text_block_klein.get_rect(center=(((x+breite/2)),((hoehe+y-spiel.gitter*2)))))

    def handle_events(self):
        gitter = self.spiel.height // GRID_SIZE
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = (event.pos[0] // gitter) * gitter
                y = (event.pos[1] // gitter) * gitter
                if self.modus == 1:
                    self.spiel.boxes.append(Box(x, y, gitter, gitter, self.spiel.blocktexture_Block, 1))
                elif self.modus == 2:
                    for i, box in enumerate(self.spiel.boxes):
                        if box.rect.collidepoint((x,y)):
                            if box in self.spiel.lifte:
                                self.spiel.lifte.remove(box)
                            self.spiel.boxes.pop(i)
                elif self.modus == 3:
                    if self.lift_start is None:
                        self.lift_start = (x, y)
                    else:
                        neuer_lift = Lift(self.lift_start[0], self.lift_start[1], gitter, gitter, self.spiel.blocktexture_Lift, x, y, 1)
                        self.spiel.boxes.append(neuer_lift) 
                        self.spiel.lifte.append(neuer_lift)
                        self.lift_start = None
                elif self.modus==4:
                    self.spiel.boxes.append(Box(x, y, gitter, gitter, 0, 0))
                elif self.modus==5:
                    self.spiel.boxes.append(Box(x, y, gitter, gitter, 0, 2))
                elif self.modus==6:
                    self.spiel.boxes.append(Box(x, y, gitter, gitter, 0, 3))
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_COMMA:
                    if self.modus==1:
                        self.spiel.blocktexture_Block-=1
                        if self.spiel.blocktexture_Block<0:
                            self.spiel.blocktexture_Block=(len(self.spiel.Bilder)-1)
                    if self.modus==3:
                        self.spiel.blocktexture_Lift-=1
                        if self.spiel.blocktexture_Lift<0:
                            self.spiel.blocktexture_Lift=(len(self.spiel.Bilder)-1)
                elif event.key == pygame.K_PERIOD:
                    if self.modus==1:
                        self.spiel.blocktexture_Block+=1
                        if self.spiel.blocktexture_Block>=len(self.spiel.Bilder):
                            self.spiel.blocktexture_Block=0
                    if self.modus==3:
                        self.spiel.blocktexture_Lift+=1
                        if self.spiel.blocktexture_Lift>=len(self.spiel.Bilder):
                            self.spiel.blocktexture_Lift=0
                elif event.key == pygame.K_n:
                    self.spiel.Hintergrund_zahl-=1
                    if self.spiel.Hintergrund_zahl<0:
                        self.spiel.Hintergrund_zahl=(len(self.spiel.Hintergrund)-1)
                elif event.key == pygame.K_m:
                    self.spiel.Hintergrund_zahl+=1
                    if self.spiel.Hintergrund_zahl>=len(self.spiel.Hintergrund):
                        self.spiel.Hintergrund_zahl=0
                
                elif event.key == pygame.K_e or event.key == pygame.K_ESCAPE:
                    self.spiel.spieler.rect.x += self.spiel.Abstand_x
                    self.spiel.spieler.rect.y += self.spiel.Abstand_y
                    for box in self.spiel.boxes:
                            box.box_bewegen(self.spiel.Abstand_x, self.spiel.Abstand_y)
                    for zielort in self.spiel.zielorte:
                            zielort.spiel.box_bewegen(self.spiel.Abstand_x, self.spiel.Abstand_y)
                    self.spiel.verschiebe_elemente(self.verschiebung_x_Koordinate, self.verschiebung_y_Koordinate)
                    self.verschiebung_y_Koordinate=0
                    self.verschiebung_x_Koordinate=0
                    self.spiel.spawnInfos.copyfrom(self.spiel, 0, 0)
                    memo={}
                    self.spiel.Welt[0] = copy.deepcopy(self.spiel.spieler,memo)
                    self.spiel.Welt[1] = copy.deepcopy(self.spiel.boxes,memo)
                    self.spiel.Welt[2] = copy.deepcopy(self.spiel.zielorte,memo)
                    self.spiel.Welt[3] = copy.deepcopy(self.spiel.lifte,memo)
                    self.spiel.Welt[4] = copy.deepcopy(self.spiel.richtungen,memo)
                    self.spiel.Welt[5] = copy.deepcopy(self.spiel.anzahl_liftendpunkte,memo)
                    self.spiel.Welt[6] = copy.deepcopy(self.spiel.spawnInfos.spieler,memo)
                    self.spiel.Welt[7] = copy.deepcopy(self.spiel.spawnInfos.boxes,memo)
                    self.spiel.Welt[8] = copy.deepcopy(self.spiel.spawnInfos.zielorte,memo)
                    self.spiel.Welt[9] = copy.deepcopy(self.spiel.spawnInfos.lifte,memo)
                    self.spiel.Welt[10] = copy.deepcopy(self.spiel.spawnInfos.richtungen,memo)
                    self.spiel.Welt[11] = copy.deepcopy(self.spiel.spawnInfos.anzahl_liftendpunkte,memo)
                    self.spiel.Welt[12] = copy.deepcopy(self.spiel.bewegung_y_rest,memo)
                    self.spiel.Welt[13] = copy.deepcopy(self.spiel.Bewegung_y,memo)
                    self.spiel.Welt[14] = copy.deepcopy(self.spiel.Hintergrund_zahl,memo)
                    
                    self.spiel.mode = "play"
                elif event.key == pygame.K_1:
                    self.modus=1
                elif event.key == pygame.K_2:
                    self.modus=2
                elif event.key == pygame.K_3:
                    self.modus=3
                elif event.key == pygame.K_4:
                    self.modus=4
                elif event.key == pygame.K_5:
                    self.modus=5
                elif event.key == pygame.K_6:
                    self.modus=6
        key = pygame.key.get_pressed()

        if key[pygame.K_UP]:
            self.spiel.verschiebe_elemente(0, gitter)
            self.verschiebung_y_Koordinate -= gitter

        if key[pygame.K_DOWN]:
            self.spiel.verschiebe_elemente(0, -gitter)
            self.verschiebung_y_Koordinate += gitter

        if key[pygame.K_RIGHT]:
            self.spiel.verschiebe_elemente(-gitter, 0)
            self.verschiebung_x_Koordinate += gitter

        if key[pygame.K_LEFT]:
            self.spiel.verschiebe_elemente(gitter, 0)
            self.verschiebung_x_Koordinate -= gitter
            

    def zeichnen(self):
        self.spiel.Hintergrund_zeichnen()
        if self.spiel.Bewegung_y >= self.spiel.height * 3:
            self.spiel.counter += 1
            self.spiel.Bewegung_y = 2 * self.spiel.height
            self.spiel.bewegung_y_rest = 0

        if self.spiel.Bewegung_y <= self.spiel.height and self.spiel.counter > 0:
            self.spiel.Bewegung_y = 2 * self.spiel.height
            self.spiel.bewegung_y_rest = 0
            self.spiel.counter -= 1

        if self.spiel.Bewegung_y <= (-self.spiel.height - self.spiel.hoehe_Untergrund * 2):
            self.spiel.counter -= 1
            self.spiel.Bewegung_y = -self.spiel.height - self.spiel.hoehe_Untergrund
            self.spiel.bewegung_y_rest = 0

        if self.spiel.Bewegung_y >= -self.spiel.height and self.spiel.counter < 0:
            self.spiel.Bewegung_y = -self.spiel.height - self.spiel.hoehe_Untergrund
            self.spiel.bewegung_y_rest = 0
            self.spiel.counter += 1
        
        if self.spiel.Bewegung_x>=self.width or self.spiel.Bewegung_x<-self.spiel.width:
            self.spiel.Bewegung_x=0
        self.zeichne_grid()
        
        self.spiel.spieler.zeichne(self.spiel.bildschirm)

        
        for box in self.spiel.boxes:
            box.zeichne(self.spiel.bildschirm)
        if self.modus == 3 and self.lift_start is not None:
            gitter = self.spiel.height // GRID_SIZE
            pygame.draw.rect(self.spiel.bildschirm, BLAU, (self.lift_start[0], self.lift_start[1], gitter, gitter), 2)
        
        self.erklaerung("Block", "Taste 1", 2*spiel.width/7, 15*spiel.height/20, self.modus==1,self.spiel.blocktexture_Block)
        self.erklaerung("Löschen", "Taste 2", 3*spiel.width/7, 15*spiel.height/20, self.modus==2, self.spiel.löschen)
        self.erklaerung("Lifte", "Taste 3", 4*spiel.width/7, 15*spiel.height/20, self.modus==3,self.spiel.blocktexture_Lift)
        self.erklaerung("Checkpoints", "Taste 4", 2*spiel.width/7, spiel.height/13, self.modus==4,self.spiel.img_block_Checkpoint)
        self.erklaerung("Respawn", "Taste 5", 3*spiel.width/7, spiel.height/13, self.modus==5,self.spiel.img_block_Respawn)
        self.erklaerung("Ziel", "Taste 6", 4*spiel.width/7, spiel.height/13, self.modus==6,self.spiel.Ziel_Flagge)
        pygame.display.flip()
        
class SpawnInfos:
    def checkpoint_ausrichten(self,spiel,box):
        dx = spiel.spieler.rect.x - box.rect.x
        dy = spiel.spieler.rect.y - box.rect.y
        self.copyfrom(spiel,dx,dy)
            
    def copyfrom(self,spiel,dx,dy):
        
        
        
        
        memo={}
        self.spieler = copy.deepcopy(spiel.spieler,memo)      
        self.boxes = copy.deepcopy(spiel.boxes,memo) 
        self.zielorte = copy.deepcopy(spiel.zielorte,memo)
        self.lifte = copy.deepcopy(spiel.lifte,memo)
        self.richtungen = copy.deepcopy(spiel.richtungen,memo)
        self.anzahl_liftendpunkte = copy.deepcopy(spiel.anzahl_liftendpunkte,memo)
        self.Bewegung_y = copy.deepcopy(spiel.Bewegung_y,memo)
        self.bewegung_y_rest = copy.deepcopy(spiel.bewegung_y_rest,memo)
        self.counter=copy.deepcopy(spiel.counter,memo)
        for box in self.boxes:
                box.box_bewegen(dx, dy)
        for zielort in self.zielorte:
            zielort.box_bewegen(dx, dy)
        speicherdatei=[copy.deepcopy(spiel.spieler,memo),copy.deepcopy(spiel.boxes,memo),copy.deepcopy(spiel.zielorte,memo),copy.deepcopy(spiel.lifte,memo),copy.deepcopy(spiel.Bewegung_y,memo)]
        return speicherdatei

    def copyto(self, spiel):
        memo={}
        spiel.spieler = copy.deepcopy(self.spieler,memo)     
        spiel.boxes = copy.deepcopy(self.boxes,memo) 
        spiel.zielorte = copy.deepcopy(self.zielorte,memo)
        spiel.lifte = copy.deepcopy(self.lifte,memo)
        spiel.richtungen = copy.deepcopy(self.richtungen,memo)
        spiel.anzahl_liftendpunkte = copy.deepcopy(self.anzahl_liftendpunkte,memo)
        spiel.bewegung_y_rest=self.bewegung_y_rest
        spiel.Bewegung_y=self.Bewegung_y
        spiel.counter=self.counter

class Spiel:
    def __init__(self):
        
        
        pygame.init()
        self.Welt=[]
        for i in range(16):
            
            self.Welt.append(True)
        self.anlauf_rechts=0
        self.anlauf_links=0
        self.start_zeit = 0
        self.abwarten=0
        self.minuten=0
        self.sekunden=0
        self.vergangene_zeit=0
        self.vergangene_zeit_backup=0
        self.bewegung_x_rest=0
        self.bildschirm = pygame.display.set_mode((2000, 1000))
        self.Rekord=False
        self.Rekorde=[False,False,False,False,False,False,False,False,False,False,False,False,False,]
        self.width = self.bildschirm.get_width()
        self.height = self.bildschirm.get_height()
        self.gitter = self.height / GRID_SIZE
        self.spawnInfos = SpawnInfos()
        self.mode = "menu"
        self.Abstand_x=0
        self.Abstand_y=0
        self.Bewegung_x=0
        self.Bewegung_y=0
        self.bewegung_y_rest=0
        self.levels=[]
        if os.path.exists("levels.pkl"):
            with open("levels.pkl", "rb") as datei:
                self.levels = pickle.load(datei)
        with open("spielstand.pkl", "rb") as datei:
            self.speicher = pickle.load(datei)
        self.richtig=False

        self.clock = pygame.time.Clock()
        self.bewegen_rest_x=0
        self.bewegen_rest_y=0
        self.counter=0
        self.Startmodus=False
        self.spieler = Spieler(self.width, self.height)
        self.Bilder = []
        self.Rechteck_lila= pygame.image.load("Rechteck_lila.png").convert_alpha()
        self.Rechteck= pygame.image.load("Rechteck_1.png").convert_alpha()
        self.Rechteck_gerundet=pygame.image.load("Rechteck_abgerundet.png").convert_alpha()
        self.löschen= pygame.image.load("löschen.WEBP").convert_alpha()

        self.img_block_1 = pygame.image.load("block_01.png").convert_alpha()
        self.Bilder.append(self.img_block_1)
        self.img_block_2 = pygame.image.load("block_02.png").convert_alpha()
        self.Bilder.append(self.img_block_2)
        self.img_block_3 = pygame.image.load("block_03.png").convert_alpha()
        self.Bilder.append(self.img_block_3)
        self.img_block_4 = pygame.image.load("block_04.png").convert_alpha()
        self.Bilder.append(self.img_block_4)
        self.img_block_5 = pygame.image.load("block_05.png").convert_alpha()
        self.Bilder.append(self.img_block_5)
        self.img_block_6 = pygame.image.load("block_06.png").convert_alpha()
        self.Bilder.append(self.img_block_6)

        

        self.img_block_8 = pygame.image.load("block_08.png").convert_alpha()
        self.Bilder.append(self.img_block_8)

        self.img_block_Checkpoint = pygame.image.load("block_14.png").convert_alpha()
        

        self.img_block_10 = pygame.image.load("block_10.png").convert_alpha()
        self.Bilder.append(self.img_block_10)

        self.img_block_Respawn = pygame.image.load("block_12.png").convert_alpha()

        self.img_block_11 = pygame.image.load("block_11.png").convert_alpha()
        self.Bilder.append(self.img_block_11)

        self.img_block_13 = pygame.image.load("block_13.png").convert_alpha()
        self.Bilder.append(self.img_block_13)
        self.Ziel_Flagge = pygame.image.load("zielflagge.png").convert_alpha()
        self.Hintergrund = []

        self.img_backgroundCastles = pygame.image.load("backgroundCastles.png").convert_alpha()
        self.img_backgroundCastles=pygame.transform.scale(self.img_backgroundCastles, (self.width, self.height))
        
        self.Hintergrund.append(self.img_backgroundCastles)

        self.img_backgroundColorDesert = pygame.image.load("backgroundColorDesert.png").convert_alpha()
        self.img_backgroundColorDesert = pygame.transform.scale(self.img_backgroundColorDesert, (self.width, self.height))
        self.Hintergrund.append(self.img_backgroundColorDesert)

        self.img_backgroundColorFall = pygame.image.load("backgroundColorFall.png").convert_alpha()
        self.img_backgroundColorFall = pygame.transform.scale(self.img_backgroundColorFall, (self.width, self.height))
        self.Hintergrund.append(self.img_backgroundColorFall)

        self.img_backgroundColorForest = pygame.image.load("backgroundColorForest.png").convert_alpha()
        self.img_backgroundColorForest = pygame.transform.scale(self.img_backgroundColorForest, (self.width, self.height))
        self.Hintergrund.append(self.img_backgroundColorForest)

        self.img_backgroundColorGrass = pygame.image.load("backgroundColorGrass.png").convert_alpha()
        self.img_backgroundColorGrass = pygame.transform.scale(self.img_backgroundColorGrass, (self.width, self.height))
        self.Hintergrund.append(self.img_backgroundColorGrass)

        self.img_backgroundDesert = pygame.image.load("backgroundDesert.png").convert_alpha()
        self.img_backgroundDesert = pygame.transform.scale(self.img_backgroundDesert, (self.width, self.height))
        self.Hintergrund.append(self.img_backgroundDesert)

        self.img_backgroundEmpty = pygame.image.load("backgroundEmpty.png").convert_alpha()
        self.img_backgroundEmpty = pygame.transform.scale(self.img_backgroundEmpty, (self.width, self.height))
        self.Hintergrund.append(self.img_backgroundEmpty)

        self.img_backgroundForest = pygame.image.load("backgroundForest.png").convert_alpha()
        self.img_backgroundForest = pygame.transform.scale(self.img_backgroundForest, (self.width, self.height))
        self.Hintergrund.append(self.img_backgroundForest)
        
        self.Himmel=pygame.image.load("Himmel.png").convert_alpha()
        self.Himmel = pygame.transform.scale(self.Himmel, (self.width, self.height))
        self.Untergrund=[]
        self.Untergrund_blau=pygame.image.load("Untergrund_blau.png").convert_alpha()
        self.Untergrund_desert=pygame.image.load("Untergrund_Desert.png").convert_alpha()
        self.Untergrund_forest=pygame.image.load("Untergrund_Forest.png").convert_alpha()
        self.Untergrund_grass=pygame.image.load("Untergrund_grass.png").convert_alpha()
        self.Untergrund.append(self.Untergrund_blau)
        self.Untergrund.append(self.Untergrund_desert)
        self.Untergrund.append(self.Untergrund_forest)
        self.Untergrund.append(self.Untergrund_forest)
        self.Untergrund.append(self.Untergrund_grass)
        self.Untergrund.append(self.Untergrund_blau)
        self.Untergrund.append(self.Untergrund_blau)
        self.Untergrund.append(self.Untergrund_blau)



        self.hoehe_Untergrund = self.Untergrund_blau.get_height()
        self.width_Untergrund= self.Untergrund_blau.get_width()
        self.Hintergrund_zahl=0
        self.blocktexture_Lift=0
        self.blocktexture_Block=0
        self.boxes = [
        ]
        self.zielorte = []
        self.lifte = []
        self.richtungen = []
        self.anzahl_liftendpunkte = []

        self.gravitation = 0    
        self.sprungkraft = 0    
        self.fallend = True     
        self.sprungtaste_links=False
        self.sprungtaste_rechts=False
        self.editor = Editor(self)
        self.spawnInfos.copyfrom(self,0,0)
        self.menu=Menu(self)

    def speichern(self):
        
        if self.menu.modus==1:
            with open("Welt_1.pkl", "wb") as datei:
                pickle.dump(self.speicherdatei, datei)
        if self.menu.modus==2:
            with open("Welt_2.pkl", "wb") as datei:
                pickle.dump(self.speicherdatei, datei)
        if self.menu.modus==3:
            with open("Welt_3.pkl", "wb") as datei:
                pickle.dump(self.speicherdatei, datei)
        if self.menu.modus==4:
            self.levels[(self.menu.zähler_level-1)]=self.speicherdatei
            with open("levels.pkl", "wb") as datei:
                pickle.dump(self.levels, datei)
        with open("Rekorde.pkl", "wb") as datei:
                pickle.dump(self.speicherdatei[15], datei)
        



    def schwerkraft_anwenden(self):
        
        
        
        if self.fallend:
            dx=int(self.sprungkraft+self.bewegen_rest_x)
            dy=int(self.gravitation+self.bewegen_rest_y)
            self.bewegen_rest_x=(self.sprungkraft+self.bewegen_rest_x)-int(self.sprungkraft+self.bewegen_rest_x)
            self.bewegen_rest_y=(self.gravitation+self.bewegen_rest_y)-int(self.gravitation+self.bewegen_rest_y)
            self.Bewegung_y-=1
            self.Bewegung_y+=dy
            for box in self.boxes:
                box.box_bewegen(dx, dy)
                if dx>0:
                    if box.kollidiert(self.spieler):
                        if box.Kollision==1:
                            for box2 in self.boxes:
                                box2.box_bewegen(-dx, 0)
                            self.Bewegung_x-=1
                            for zielort in self.zielorte:
                                zielort.box_bewegen(-dx,0)
                            if self.gravitation <= 0:
                                self.gravitation=-0.5
                            self.sprungtaste_links=True
                            self.bewegen_rest_x=0
                            self.sprungkraft=0
                if dx<0:
                    if box.kollidiert(self.spieler):
                        if box.Kollision==1:
                            self.Bewegung_x+=1
                            for box2 in self.boxes:
                                box2.box_bewegen(-dx, 0)
                            for zielort in self.zielorte:
                                zielort.box_bewegen(-dx,0)
                            if self.gravitation <= 0:
                                self.gravitation=-0.5
                            self.sprungtaste_rechts=True
                            self.bewegen_rest_x=0
                            self.sprungkraft=0
                    
            for zielort in self.zielorte:
                zielort.box_bewegen(dx, dy)
                if dx<0:
                    if box.kollidiert(self.spieler):
                        if box.Kollision==1:
                            self.Bewegung_x+=1
                            for box2 in self.boxes:
                                box2.box_bewegen(self.anlauf_rechts, 0)
                            for zielort in self.zielorte:
                                zielort.box_bewegen(self.anlauf_rechts,0)
                            if self.gravitation <= 0:
                                self.gravitation=-0.5
                            self.sprungtaste_rechts=True
            if self.sprungkraft < 0:
                self.sprungkraft += 0.5
            elif self.sprungkraft > 0:
                self.sprungkraft -= 0.5
            self.gravitation -= 0.1
    def bewege_lifte(self):
        test_spieler = copy.copy(self.spieler.rect)
        test_spieler.y += 1
        for lift in self.lifte:
            dx, dy = lift.bewege_lift(self.spieler.rect)
            
            if test_spieler.colliderect(lift.rect) and spiel.gravitation==0:
                dx=dx*-1
                dy=dy*-1
                self.Bewegung_x+=dx   
                self.Bewegung_y+=dy
                for i in range(len(self.boxes)):
                    if not self.boxes[i]==lift.rect:
                        self.boxes[i].box_bewegen(dx,dy)
    def kollision_pruefen(self):
        for box in self.boxes:
            test_box = copy.copy(box)
            test_box.rect.y -= 1

            if test_box.kollidiert(self.spieler.rect) and self.gravitation <= 0:
                if test_box.Kollision==1:
                    abstand = self.spieler.rect.y + self.spieler.rect.height - box.rect.y
                    self.sprungtaste_links=False
                    self.sprungtaste_rechts=False
                    if self.sprungkraft!=0:
                        abstand=0
                        for box2 in self.boxes:
                            box2.rect.x-=(self.sprungkraft*2)
                        
                        self.sprungkraft=0
                    for box2 in self.boxes:
                        box2.rect.y += int(abstand)
                    self.fallend = False
                    self.gravitation = 0
                if box.Kollision==0:
                    self.spawnInfos.checkpoint_ausrichten(self,box)
                if box.Kollision==2:
                    self.respawn_Taste()
                if box.Kollision==3:
                    self.mode="menu3"
            elif test_box.kollidiert(self.spieler.rect) and self.gravitation > 0 and (box.rect.y - self.spieler.rect.y) < -10 or test_box.kollidiert(self.spieler.rect) and self.gravitation > 0 and (box.rect.y - self.spieler.rect.y) > 10:
                if box.Kollision==1:
                    abstand = self.spieler.rect.y - (box.rect.y + box.rect.h)

                    for box2 in self.boxes:
                        box2.rect.y += int(abstand)
                    
                    self.fallend = True
                    self.gravitation = 0
                if box.Kollision==0:
                    self.spawnInfos.checkpoint_ausrichten(self,box)
                if box.Kollision==2:
                    self.respawn_Taste()
                if box.Kollision==3:
                    self.mode="menu3"
                    

    def laufe(self):
        
        
        
        for index, zahl in enumerate(self.anzahl_liftendpunkte):
            if index< len(self.richtungen) and not self.mode == "edit":
                bewegung_tempo= 2
                gesamt= (self.richtungen[index][1]**2+self.richtungen[index][0]**2)**0.5
                    
                bewegung_tempo_x= self.richtungen[index][0]/gesamt*bewegung_tempo
                bewegung_tempo_y=self.richtungen[index][1]/gesamt*bewegung_tempo
                test_box=copy.deepcopy(self.boxes[zahl])
                test_box.rect.y-=1
                
                if test_box.kollidiert(self.spieler):
                    self.zielorte[index*2].box_bewegen(-bewegung_tempo_x,-bewegung_tempo_y)
                    self.zielorte[index*2+1].box_bewegen(-bewegung_tempo_x,-bewegung_tempo_y)
                    self.Bewegung_y-=bewegung_tempo_y
                    self.Bewegung_x-=bewegung_tempo_x
                    for i in range(len(self.boxes)):
                        if i!=self.boxes.index(self.boxes[zahl]):
                            self.boxes[i].box_bewegen(-bewegung_tempo_x,-bewegung_tempo_y)
                    
                            
                else:
                    self.boxes[zahl].box_bewegen(bewegung_tempo_x,bewegung_tempo_y )
                if self.zielorte[index*2].rect.x>self.zielorte[index*2+1].rect.x:
                    zielort_kleiner_x=self.zielorte[index*2+1].rect.x
                    zielort_grösser_x=self.zielorte[index*2].rect.x
                else:
                    zielort_kleiner_x=self.zielorte[index*2].rect.x
                    zielort_grösser_x=self.zielorte[index*2+1].rect.x
                if self.zielorte[index*2].rect.y>self.zielorte[index*2+1].rect.y:
                    zielort_kleiner_y=self.zielorte[index*2+1].rect.y
                    zielort_grösser_y=self.zielorte[index*2].rect.y
                else:
                    zielort_kleiner_y=self.zielorte[index*2].rect.y
                    zielort_grösser_y=self.zielorte[index*2+1].rect.y
                if self.richtungen[index][0]<0 and self.boxes[zahl].rect.x<zielort_kleiner_x or self.richtungen[index][0]>0 and self.boxes[zahl].rect.x>zielort_grösser_x or self.richtungen[index][1]<0 and self.boxes[zahl].rect.y<zielort_kleiner_y or self.richtungen[index][1]>0 and self.boxes[zahl].rect.y>zielort_grösser_y:
                    self.richtungen[index][0]=self.richtungen[index][0]*-1
                    self.richtungen[index][1]=self.richtungen[index][1]*-1
    def respawn_Taste(self):
        self.sprungtaste_rechts=False
        self.sprungtaste_links=False
        
        self.spawnInfos.copyto(self)
        self.gravitation=0
                

    def verschiebe_elemente(self, dx, dy):
        
        
        
        self.spieler.rect.x += dx
        self.spieler.rect.y += dy
        self.Bewegung_x+=dx   
        self.Bewegung_y+=dy
        for box in self.boxes:
            box.rect.x += dx
            box.rect.y += dy
            
        for zielort in self.zielorte:
            zielort.rect.x += dx
            zielort.rect.y += dy            

    def springe_links(self):
        self.abwarten+=1
        if self.anlauf_links<3 and self.abwarten>=5:
            self.anlauf_links+=1
            self.abwarten=0
        
        for zielort in self.zielorte:
            zielort.box_bewegen(self.anlauf_links,0)
        self.Bewegung_x+=self.anlauf_links/3
        for box in self.boxes:
            box.box_bewegen(self.anlauf_links,0)
            if box.kollidiert(self.spieler):
                if box.Kollision==1:
                    for box2 in self.boxes:
                        box2.box_bewegen(-self.anlauf_links, 0)
                    self.Bewegung_x-=1
                    for zielort in self.zielorte:
                        zielort.box_bewegen(-self.anlauf_links,0)
                    if self.gravitation <= 0:
                        self.gravitation=-0.5
                    self.sprungtaste_links=True
                if box.Kollision==0:
                    self.spawnInfos.checkpoint_ausrichten(self,box)
                if box.Kollision==2:
                    self.respawn_Taste()
                if box.Kollision==3:
                    self.mode="menu3"
                
                               
    def springe_rechts(self):
        self.abwarten+=1
        if self.anlauf_rechts<3 and self.abwarten>=5:
            self.anlauf_rechts+=1
            self.abwarten=0
        for zielort in self.zielorte:
            zielort.box_bewegen(-self.anlauf_rechts,0)
        self.Bewegung_x-=self.anlauf_rechts/3
        for box in self.boxes:
            box.box_bewegen(-self.anlauf_rechts,0)
            if box.kollidiert(self.spieler):
                if box.Kollision==1:
                    self.Bewegung_x+=1
                    for box2 in self.boxes:
                        box2.box_bewegen(self.anlauf_rechts, 0)
                    for zielort in self.zielorte:
                        zielort.box_bewegen(self.anlauf_rechts,0)
                    if self.gravitation <= 0:
                        self.gravitation=-0.5
                    self.sprungtaste_rechts=True
                if box.Kollision==0:
                    self.spawnInfos.checkpoint_ausrichten(self,box)
                if box.Kollision==2:
                    self.respawn_Taste()
                if box.Kollision==3:
                    self.mode="menu3"

                               
    def springe(self):
        
        
        

        for box in self.boxes:
            if self.sprungtaste_rechts:
                self.sprungkraft = 8
                self.anlauf_rechts=3
                self.sprungtaste_rechts=False
            if self.sprungtaste_links:
                self.sprungkraft = -8
                self.anlauf_links=3
                self.sprungtaste_links=False
        self.gravitation = 5
        self.Bewegung_y+=3+self.gravitation
        for box in self.boxes:
            box.box_bewegen(self.sprungkraft, self.gravitation)
        for zielort in self.zielorte:
            zielort.box_bewegen(self.sprungkraft, self.gravitation)

    def handle_events(self):
        
        
       
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.mode="menu"
                    memo={}
                    self.spieler = copy.deepcopy(self.spawnInfos.spieler, memo)
                    self.boxes = copy.deepcopy(self.spawnInfos.boxes, memo)
                    self.zielorte = copy.deepcopy(self.spawnInfos.zielorte, memo)
                    self.lifte = copy.deepcopy(self.spawnInfos.lifte, memo)
                    self.richtungen = copy.deepcopy(self.spawnInfos.richtungen, memo)
                    self.anzahl_liftendpunkte = copy.deepcopy(self.spawnInfos.anzahl_liftendpunkte, memo)

                    self.bewegung_y_rest = copy.deepcopy(self.spawnInfos.bewegung_y_rest, memo)
                    self.Bewegung_y = copy.deepcopy(self.spawnInfos.Bewegung_y, memo)
                    self.counter = copy.deepcopy(self.spawnInfos.counter, memo)
                            
                    if self.Startmodus=="edit":
                        self.speicherdatei=[self.spieler,self.boxes,self.zielorte,self.lifte,self.richtungen,self.anzahl_liftendpunkte,self.spawnInfos.spieler,self.spawnInfos.boxes,self.spawnInfos.zielorte,self.spawnInfos.lifte,self.spawnInfos.richtungen,self.spawnInfos.anzahl_liftendpunkte,self.bewegung_y_rest,self.Bewegung_y,self.Hintergrund_zahl,self.Rekorde]
                        
                        self.speichern()
                    if self.Startmodus=="play":
                        self.speicherdatei=[self.Welt[0],self.Welt[1],self.Welt[2],self.Welt[3],self.Welt[4],self.Welt[5],self.Welt[6],self.Welt[7],self.Welt[8],self.Welt[9],self.Welt[10],self.Welt[11],self.Welt[12],self.Welt[13],self.Welt[14],self.Rekorde]
                        self.speichern()

                elif event.key == pygame.K_e and not self.fallend and self.Startmodus=="edit":
                    self.editor.width = copy.deepcopy(self.width)
                    
                    self.sprungtaste_links=False
                    self.sprungtaste_rechts=False
                    self.mode = "edit"
                    self.passe_in_gitter()
                elif event.key == pygame.K_UP and not self.fallend or self.sprungtaste_links==True and event.key == pygame.K_UP or self.sprungtaste_rechts==True and event.key == pygame.K_UP:                
                    self.springe()
                elif event.key == pygame.K_r:
                    self.respawn_Taste()
                
        key=pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.sprungkraft>=-3:
            self.sprungtaste_links=False
            self.springe_links()
        elif key[pygame.K_RIGHT] and self.sprungkraft<=3:
            self.sprungtaste_rechts=False
            self.springe_rechts()
        if not key[pygame.K_RIGHT] and self.sprungkraft<3:
            self.anlauf_rechts-=0.1
            if self.anlauf_rechts<0:
                self.anlauf_rechts=0
        if not key[pygame.K_LEFT] and self.sprungkraft>-3:
            self.anlauf_links-=0.1
            if self.anlauf_links<0:
                self.anlauf_links=0

    def respawn (self):
        self.bewegen_rest_x=0
        self.bewegen_rest_y=0

        self.spieler = Spieler(self.width, self.height)

        self.boxes = [
            Box(0, 900, self.gitter, 200, 0,1),
            Box(0, self.height - 20, 1000, 20, 0,1),
        ]
        
        self.zielorte = []
        self.lifte = []
        self.richtungen = []
        self.anzahl_liftendpunkte = []

        self.gravitation = 0  
        self.sprungkraft = 0    
        self.fallend = True     
        self.sprungtaste_links=False
        self.sprungtaste_rechts=False
       
        self.mode = "play"

        self.editor = Editor(self)
    def Timer(self):
        Position=pygame.Rect(240,30,350,102)
        pygame.draw.rect(self.bildschirm,(255,255,255), Position)
        pygame.draw.rect(self.bildschirm, (0,0,0), (242,32,348,100))
        font=pygame.font.Font(None, 100)
        self.vergangene_zeit = (pygame.time.get_ticks() - self.start_zeit)//10
        self.vergangene_zeit_backup=self.vergangene_zeit
        self.minuten=self.vergangene_zeit//(60*100)
        self.vergangene_zeit-=self.minuten*60*100
        self.sekunden=self.vergangene_zeit//100
        self.vergangene_zeit-=self.sekunden*100
        
        zeit=f"{self.minuten:02}:{self.sekunden:02}:{self.vergangene_zeit:02}"
        text2 = font.render(zeit, True, (255,255,255))
        self.bildschirm.blit(text2, text2.get_rect(center=Position.center))
    def passe_in_gitter(self):
        
        
        
        
        self.Abstand_x=self.boxes[0].rect.x%self.gitter
        self.Abstand_y=self.boxes[0].rect.y%self.gitter
        for box in self.boxes:
                box.box_bewegen(-self.Abstand_x, -self.Abstand_y)
        for zielort in self.zielorte:
            zielort.box_bewegen(-self.Abstand_x, -self.Abstand_y)
        self.spieler.rect.x-=self.Abstand_x
        self.spieler.rect.y-=self.Abstand_y
    
    def Hintergrund_zeichnen(self):
        Bewegung_y_ganzzahlig=int(self.Bewegung_y+self.bewegung_y_rest)
        Bewegung_x_ganzzahlig=int(self.Bewegung_x+self.bewegung_x_rest)
        self.bewegung_x_rest=self.Bewegung_x-Bewegung_x_ganzzahlig+self.bewegung_x_rest
        self.bewegung_y_rest=self.Bewegung_y-Bewegung_y_ganzzahlig+self.bewegung_y_rest
        self.bildschirm.fill(SCHWARZ)
        for i in range(3):
            self.bildschirm.blit(self.Hintergrund[self.Hintergrund_zahl], (-self.width+(self.width*i)+Bewegung_x_ganzzahlig,Bewegung_y_ganzzahlig))
        for i in range(3):
            for b in range(3):
                b+=1
                self.bildschirm.blit(self.Himmel,(-self.width+(self.width*i)+Bewegung_x_ganzzahlig,Bewegung_y_ganzzahlig-self.height*b))
        for i in range(5):
            for b in range(4):
                self.bildschirm.blit(self.Untergrund[self.Hintergrund_zahl],(-2*self.width_Untergrund+(self.width_Untergrund*i)+Bewegung_x_ganzzahlig,Bewegung_y_ganzzahlig+self.hoehe_Untergrund*b+self.height))
    def zeichne(self):
        self.Hintergrund_zeichnen()
        
        if self.Bewegung_y >= self.height*3:
            self.counter+=1
            self.Bewegung_y = 2*self.height
            self.bewegung_y_rest = 0
        if self.Bewegung_y<=self.height and self.counter>0:
            self.Bewegung_y = 2*self.height
            self.bewegung_y_rest = 0
            self.counter-=1
        if self.Bewegung_y<=(-self.height-self.hoehe_Untergrund*2):
            self.counter-=1
            self.Bewegung_y = (-self.height-self.hoehe_Untergrund)
            self.bewegung_y_rest = 0
        if self.Bewegung_y>=-self.height and self.counter<0:
            self.Bewegung_y = -self.height-self.hoehe_Untergrund
            self.bewegung_y_rest = 0
            self.counter+=1
        
        if self.Bewegung_x>=self.width or self.Bewegung_x<-self.width:
            self.Bewegung_x=0

        self.spieler.zeichne(self.bildschirm)

        for box in self.boxes:
            box.zeichne(self.bildschirm)

        if self.Startmodus=="play":
                    self.Timer()
        if self.mode!=3:
            pygame.display.flip()

    def run(self):
        while True:
            if self.mode == "edit":
                self.editor.handle_events()
                
                self.editor.zeichnen()
            if self.mode == "play":
                
                self.kollision_pruefen()
                self.schwerkraft_anwenden()
                self.bewege_lifte()
                self.handle_events()
                self.zeichne()
                
                self.fallend = True
            if self.mode =="menu":
                self.menu.spiel_sequenz()
                self.menu.Text_zeichnen_und_Tasteninputs_für_menu_1()
            if self.mode =="menu2":
                self.menu.Text_zeichnen_und_Tasteninputs_für_menu_1()
                self.menu.Text_zeichnen_und_Tasteninputs_für_menu_2()
            if self.mode =="menu3":
                self.menu.Text_zeichnen_und_Tasteninputs_für_menu_3()
            if self.mode=="menu4":
                self.menu.Text_zeichnen_und_Tasteninputs_für_menu_4()
                

            self.clock.tick(90)

    def quit(self):
        memo={}
        self.spieler = copy.deepcopy(self.spawnInfos.spieler, memo)
        self.boxes = copy.deepcopy(self.spawnInfos.boxes, memo)
        self.zielorte = copy.deepcopy(self.spawnInfos.zielorte, memo)
        self.lifte = copy.deepcopy(self.spawnInfos.lifte, memo)
        self.richtungen = copy.deepcopy(self.spawnInfos.richtungen, memo)
        self.anzahl_liftendpunkte = copy.deepcopy(self.spawnInfos.anzahl_liftendpunkte, memo)

        self.bewegung_y_rest = copy.deepcopy(self.spawnInfos.bewegung_y_rest, memo)
        self.Bewegung_y = copy.deepcopy(self.spawnInfos.Bewegung_y, memo)
        self.counter = copy.deepcopy(self.spawnInfos.counter, memo)
                
        if self.Startmodus=="edit":
            self.speicherdatei=[self.spieler,self.boxes,self.zielorte,self.lifte,self.richtungen,self.anzahl_liftendpunkte,self.spawnInfos.spieler,self.spawnInfos.boxes,self.spawnInfos.zielorte,self.spawnInfos.lifte,self.spawnInfos.richtungen,self.spawnInfos.anzahl_liftendpunkte,self.bewegung_y_rest,self.Bewegung_y,self.Hintergrund_zahl,self.Rekorde]
            
            self.speichern()
        if self.Startmodus=="play":
            self.speicherdatei=[self.Welt[0],self.Welt[1],self.Welt[2],self.Welt[3],self.Welt[4],self.Welt[5],self.Welt[6],self.Welt[7],self.Welt[8],self.Welt[9],self.Welt[10],self.Welt[11],self.Welt[12],self.Welt[13],self.Welt[14],self.Rekorde]
            self.speichern()
        pygame.quit()
        sys.exit()
        


if __name__ == "__main__":
    spiel = Spiel()
    spiel.run()






 
