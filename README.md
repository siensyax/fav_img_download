# お気に入りから画像をダウンロード
このプログラムは，chromeやMicrosoft Edgeなどからブックマーク(お気に入り)をエクスポートしたhtmlファイルにある，全URL先の全画像をダウンロードしてくれるものす．  
「7お気に入りすべて写真DL4.py」というプログラムを実行してください．  
すると，fav_imgというフォルダが作成されます．  
fav_imgこの下に，ドメイン名のフォルダが作成されます．  
ドメイン名のフォルダの下に，そのドメインのサイト名のフォルダが作成されます．  
サイト名のフォルダの中に，そのサイトにある画像が保存されます．  
依存関係は，「Microsoft_Edge_‎2019_‎12_‎28.html」があれば問題ないです．  
私は，ムフフな漫画がアップされているサイトから画像をダウンロードしました．  
しかし，サイトを指定せずに一気に全部ダウンロードできる反面，ダウンロードされる画像はほとんどスクレイピングされていません．  
そのため，ほしくない画像が大量に含まれてしまう可能性が高いです．  
一応，ドメイン名でフォルダ分けしてくれるようにはしました．  
ですので，そのあとはフォルダを探索しながら規則性を見つけて，規則性から自分のほしい画像だけにする，整形の作業は丸投げです  
それと私の環境では，ルーターの関係でたまに画像のダウンロードを遮断されました．  
画像を見るソフトで見たときに，対応してない形式ですって表示されたら，中身がhtmlになっていると思います．  
# 以下に，私の実行時の環境を示します．  
環境はAnacondaで構築しました．仮想環境で必要なモジュールを適宜Anaconda Navigaterで追加しました．  
*OS:Windouws 10  
*Anaconda:  
*Python:3.6.9  
*urllib3:1.24.2  
*requests:2.22.0  
*beautifulsoup:4.8.1  

元レポジストリィ名：fav_img_download
