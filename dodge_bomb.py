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
    bb_img = pg.Surface((20,20)) #爆弾のsurface作成
    pg.draw.circle(bb_img,(225,0,0),(10,10),10) #爆弾の生成
    bb_img.set_colorkey((0,0,0)) #爆弾surfaceの余白透過
    bg2_img= pg.transform.flip(bg_img,True,False)#左右反転背景の生成
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_rct = bb_img.get_rect() #爆弾rectの生成
    bb_rct.center = random.randint(0,1100),random.randint(0,650) #爆弾rectの初期位置

    def check_bound(rect): #画面外に出たか検出
            lf=0<rect.left #左端
            ri=rect.right<WIDTH #右端
            tp=0<rect.top #上端
            bt=rect.bottom<HEIGHT #下端
            return[lf,ri,tp,bt]
    clock = pg.time.Clock()
    vx=5 #爆弾の標準時のx軸移動
    vy=5 #爆弾の標準時のy軸移動
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        x=tmr%3200
        screen.blit(bg_img, [x, 0]) #背景
        screen.blit(bg2_img,[x-1600,0]) #左右反転の背景
        screen.blit(bg_img, [x-3200,0]) #背景

        key_lst = pg.key.get_pressed()
        DELTA={pg.K_UP:[0,-5], pg.K_DOWN:[0,+5], pg.K_LEFT:[-5,0], pg.K_RIGHT:[+5,0]} #上下左右のみのキー入力
        sum_mv = [0, 0]
        for k in DELTA: #キー入力による移動
            if key_lst[k]:
                sum_mv[0]+=DELTA[k][0]
                sum_mv[1]+=DELTA[k][1]

        bb_chk=check_bound(bb_rct) #爆弾が画面外に出た場合
        if not bb_chk[0] or not bb_chk[1]:
             vx=-vx
        if not bb_chk[2] or not bb_chk[3]:
             vy=-vy
        bb_rct.move_ip((vx,vy))

        kk_chk=check_bound(kk_rct) #こうかとんが画面外に出た場合
        if not kk_chk[0] or not kk_chk[1]:
            sum_mv[0]=-sum_mv[0]
        if not kk_chk[2] or not kk_chk[3]:
            sum_mv[1]=-sum_mv[1]
        kk_rct.move_ip(sum_mv)

        if bb_rct.colliderect(kk_rct): #こうかとんと爆弾の衝突時
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
