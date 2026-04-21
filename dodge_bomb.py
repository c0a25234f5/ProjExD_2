import os
import sys
import pygame as pg
import random

WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH,HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img,(225,0,0),(10,10),10)
    bb_img.set_colorkey((0,0,0))
    bg2_img= pg.transform.flip(bg_img,True,False)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0,1100),random.randint(0,650)

    def check_bound(rect):
            lf=0<rect.left
            ri=rect.right<WIDTH
            tp=0<rect.top
            bt=rect.bottom<HEIGHT
            return[lf,ri,tp,bt]
    clock = pg.time.Clock()
    vx=5
    vy=5
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        x=tmr%3200
        screen.blit(bg_img, [x, 0]) 
        screen.blit(bg2_img,[x-1600,0])
        screen.blit(bg_img, [x-3200,0])

        key_lst = pg.key.get_pressed()
        DELTA={pg.K_UP:[0,-5], pg.K_DOWN:[0,+5], pg.K_LEFT:[-5,0], pg.K_RIGHT:[+5,0]}
        sum_mv = [0, 0]
        for k in DELTA:
            if key_lst[k]:
                sum_mv[0]+=DELTA[k][0]
                sum_mv[1]+=DELTA[k][1]

        bb_chk=check_bound(bb_rct)
        if not bb_chk[0] or not bb_chk[1]:
             vx=-vx
        if not bb_chk[2] or not bb_chk[3]:
             vy=-vy
        bb_rct.move_ip((vx,vy))

        kk_rct.move_ip(sum_mv)
        kk_chk=check_bound(kk_rct)
        if not kk_chk[0] or not kk_chk[1]:
            sum_mv[0]=-sum_mv[0]
        if not kk_chk[2] or not kk_chk[3]:
            sum_mv[1]=-sum_mv[1]
        kk_rct.move_ip(sum_mv)

        if bb_rct.colliderect(kk_rct):
            break
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img,bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
