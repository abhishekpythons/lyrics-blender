import pygame
import os
import time
BaseDir = os.getcwd()
font = 'hindi\\Amita-Regular.ttf'
font = os.path.join(BaseDir,'fonts',font)
folder='poems\\khuddar'
folder = os.path.join(BaseDir,folder)
filename = os.path.join(folder,'lyrics.srt')
audiofilename = os.path.join(folder, 'song.mp3')
bg = os.path.join(folder, 'bg.jfif')
max_height = 150

class lyrics_player:
    def __init__(self, audioname,filename,bg=None,font='freesansbold.ttf',font_color=(255,255,255)):
        self.audioname = audioname
        self.color = font_color
        self.font=font 
        # self.watermarkfont=font                #here storing string to be used and concert in play
        self.bg_name=bg                             #here storing string to be used and concert in play
        file = open(filename, 'r', encoding='utf-8')
        data = file.read()
        data = data.split('\n\n')
        data[0] = data[0][1:]
        data = [i.split('\n') for i in data]
        self.starts = [i[1].split('-->')[0] for i in data]
        self.ends = [i[1].split('-->')[1] for i in data]
        self.lyrics = [i[2:] for i in data]
        for i in range(len(data)):    
            start, start_mili = self.starts[i].split(',')
            end, end_mili = self.ends[i].split(',') 
            start = [int(i) for i in start.split(':')]
            end = [int(i) for i in end.split(':')]
            start.append(int(start_mili))
            end.append(int(end_mili))
            self.ends[i] = (end[0]*3600000+end[1]*60000+end[2]*1000+end[3])//10
            self.starts[i] = (start[0]*3600000+start[1]*60000+start[2]*1000+start[3])//10
        


    def update(self, lines):
        self.scr.blit(self.bg,(0,0))
        heights=[]
        texts=[]
        for line in lines:
            text = self.font.render(line,1, (230,230,230))
            width=self.win_width-2*self.margin
            height = int((self.win_width-2*self.margin) * (text.get_size()[1]/text.get_size()[0]))
            if height > max_height:
                height =max_height
                width = int(max_height * (text.get_size()[0]/text.get_size()[1]))
            heights.append(height)
            text = pygame.transform.scale(text, (width, height))
            texts.append(text)
        total_height = sum(heights)
        now_height = (self.win_height - total_height)//2
        for text in texts:
            self.scr.blit(text,(self.win_width//2-text.get_size()[0]//2, now_height))
            now_height+=text.get_size()[1]
        pygame.display.update()


    # def watermark(self):
    #     st = 'made by abhishek lyrics blender'
    #     text = self.watermarkfont.render(st,1,(255,0,0,50),(255,255,255))
    #     if self.water_x>-text.get_size()[0]:
    #         self.water_x-=1
    #     else:
    #         self.water_x=self.win_width
    #     self.scr.blit(text,(self.water_x,100))
    #     pygame.display.update()

    def play(self):
        pygame.init()
        self.font = pygame.font.Font(self.font,max_height)
        # self.watermarkfont = pygame.font.Font(self.watermarkfont,100)
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.win_size = self.win_width,self.win_height = pygame.display.Info().current_w,pygame.display.Info().current_h
        self.water_x = self.win_width
        self.margin = self.win_width //10
        self.bg = pygame.Surface(self.win_size)
        self.bg.blit(pygame.image.load(self.bg_name),(0,0)) if self.bg_name else self.bg.fill((0,0,0))
        self.scr = pygame.display.set_mode(self.win_size)
        self.scr.blit(self.bg,(0,0))
        pygame.display.update()
        started_on = pygame.time.get_ticks()
        pygame.mixer.music.load(audiofilename)
        pygame.mixer.music.play()
        while 1:
            for eve in pygame.event.get():
                if eve.type==pygame.constants.QUIT or (eve.type==pygame.constants.KEYDOWN and eve.key==pygame.K_q):
                    pygame.display.quit()
                    break    
            now_time = (pygame.time.get_ticks()-started_on)//10
            if now_time in self.starts:
                self.update(self.lyrics[self.starts.index(now_time)])
                pygame.time.delay(self.ends[self.starts.index(now_time)]-now_time)
            # self.watermark()
            pygame.time.Clock().tick(100000)
    def show(self):
        for i in self.lyrics:
            print(i)

play_now = lyrics_player(audiofilename, filename, bg = bg, font = font)
##play_now.play()
play_now.show()


