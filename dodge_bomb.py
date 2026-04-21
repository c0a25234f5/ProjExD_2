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
    
    def gameover(screen: pg.surface) -> None: #ゲームオーバーの画面転換
        go_bg_img = pg.Surface((WIDTH,HEIGHT)) #画面全体のsurface作成
        pg.draw.rect(go_bg_img,((0,0,0)),pg.Rect(0,0,WIDTH,HEIGHT)) #画面全体の黒長方形
        go_bg_img.set_alpha(200) #surfaceの透明度設定
        go_font = pg.font.Font(None,80) #gameoverの文字のsurface生成
        go_txt = go_font.render("Game Over",True,(255,255,255)) #文字surfaceに文字規定
        go_bg_img.blit(go_txt,[(WIDTH/2)-135,(HEIGHT/2)]) #文字の出力
        go_kk_img = pg.image.load("fig/8.png") #こうかとんのロード
        go_bg_img.blit(go_kk_img,[(WIDTH/2)-190,(HEIGHT/2)]) #左こうかとんの出力
        go_bg_img.blit(go_kk_img,[(WIDTH/2)+190,(HEIGHT/2)]) #右こうかとんの出力
        screen.blit(go_bg_img,[0,0]) #gameover画面の出力
        pg.display.update()
        pg.time.wait(5000) #5秒間表示

    def init_bb_imgs() -> tuple[list[pg.Surface],list[int]]:
        bb_imgs=[] #爆弾surfaceの初期リスト
        for r in range(1,11):
            bb_img = pg.Surface((20*r,20*r)) #爆弾surfaceの生成
            pg.draw.circle(bb_img,(255,0,0),(10*r,10*r),10*r) #爆弾の作成
            bb_img.set_colorkey((0,0,0)) #背景の透過
            bb_imgs.append(bb_img) #爆弾をリストに追加
            bb_acces = [a for  a in range(1,11)] #加速度のリスト
        return (bb_imgs,bb_acces) #サイズ、加速度リストのタプル
    bb_lst=init_bb_imgs() #爆弾のサイズ、加速度リストの呼び出し

    def get_kk_imgs() -> dict[tuple[int,int],pg.Surface]:
        kk_img2=pg.transform.flip(kk_img,True,False)
        kk_dict = {
            (0,0): pg.transform.rotozoom(kk_img,0,1.0), #入力無し
            (0,-5):pg.transform.rotozoom(kk_img2,90,1.0), #上
            (+5,-5):pg.transform.rotozoom(kk_img2,45,1.0), #右上
            (+5,0):pg.transform.rotozoom(kk_img2,0,1.0), #右
            (+5,+5):pg.transform.rotozoom(kk_img2,-45,1.0), #右下
            (0,+5):pg.transform.rotozoom(kk_img2,-90,1.0), #下
            (-5,+5):pg.transform.rotozoom(kk_img,45,1.0), #左下
            (-5,0):pg.transform.rotozoom(kk_img,0,1.0), #左
            (-5,-5):pg.transform.rotozoom(kk_img,-45,1.0) #左上
        }
        return kk_dict
    kk_mv=get_kk_imgs() #辞書の取得

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

        avx = vx*(bb_lst[1][min(tmr//500, 9)]) #時間経過による爆弾のx軸の加速度上昇
        avy = vy*(bb_lst[1][min(tmr//500, 9)]) #時間経過による爆弾のy軸の加速度上昇
        bb_img = bb_lst[0][min(tmr//500,9)] #時間経過による爆弾サイズの変更
        bb_rct.width = bb_img.get_rect().width #爆弾のサイズ変更に合わせたsurfaceのwidthの変化
        bb_rct.height = bb_img.get_rect().height #爆弾のサイズ変更に合わせたsurfaceのheightの変化
        bb_rct.move_ip(avx,avy) #爆弾の移動

        bb_chk=check_bound(bb_rct) #爆弾が画面外に出た場合
        if not bb_chk[0] or not bb_chk[1]:
             vx=-vx
        if not bb_chk[2] or not bb_chk[3]:
             vy=-vy
        # bb_rct.move_ip((vx,vy))

        kk_chk=check_bound(kk_rct) #こうかとんが画面外に出た場合
        if not kk_chk[0] or not kk_chk[1]:
            sum_mv[0]=-sum_mv[0]
        if not kk_chk[2] or not kk_chk[3]:
            sum_mv[1]=-sum_mv[1]
        kk_rct.move_ip(sum_mv)
        kk_img = kk_mv[tuple(sum_mv)] #こうかとんの移動量取得、向きの設定

        if bb_rct.colliderect(kk_rct): #こうかとんと爆弾の衝突時
            gameover(screen)
            return
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
