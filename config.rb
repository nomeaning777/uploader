#-*- encoding: utf-8 -*-

# 設定ファイル

#
# 基本設定
#

$HTTP_PATH = ''  # 設置URL 最後に/を付けること
$TEMPLATE_PATH = 'templates/' # テンプレートフォルダ
$UPLOAD_PATH = 'files/' # ファイルをアップロードをする対象のフォルダ

$DATA_PATH = 'data.dat' # データーベースファイル

$ADMIN_PASSWORD = '' # 管理画面のパスワード

$TITLE = '音楽用アップローダー' # アップローダーのタイトル
# $TITLE_IMAGE = 'title.png' # タイトルの画像

$MESSAGE = <<ENDOFSTRING
<div class="message">
アップローダーです
</div>
ENDOFSTRING
#
# アップロード関連
#
$UPLOAD_EXT = ['mp3','wav','wave'] # アップロード可能な拡張子(空の場合は任意の拡張子に対応)
$USE_DL_KEY = false # DLキーを利用可能にするか
$USE_EDIT_KEY = true # ファイルの編集キーを利用可能にするか
$USE_MP3_PLAYER = false # mp3ファイルのプレビューを利用するか
$MP3_PLAYER_URL = '' # player_mp3_maxiの場所
$USE_WAVE_CONVERT = true
# waveファイルをmp3に変換する

$ALL_FILE_LIMIT = -1 # 保存するファイルの個数．-1なら無限．(現在は無効)
$ALL_FILE_SIZE_LIMIT = -1 # 合計ファイルサイズの最大(現在は無効)
$FILE_SIZE_LIMIT = -1 # 一つのファイルサイズの最大

$COMMENT_LIMIT = 512 # コメントの長さの最大値
$DL_KEY_LIMIT = 50 # DLキーの長さの最大値
$EDIT_KEY_LIMIT = 50 # 編集キーの長さの最大値

$DELETE_FILE = false # ファイルを実際に消去するか(true推奨)
#
# 投稿規制
#
$USE_DENY_IP = false # 拒否IPを利用するか
$DENY_IP = /.+/ # 拒否IPアドレス
$USE_DENY_HOST = false # 拒否ホストを利用するか
$DENY_HOST = /.+/ #拒否ホストアドレス

#
# 表示関連
#
$PAGEPER = 50 # 1ページ当りの表示するファイルの数
$SHOW_FILE_COUNT = true # ファイルの個数を表示する
$SHOW_FILE_SIZE = true # ファイルサイズの合計を表示する
$SHOW_ADMIN_LINK = false # 管理画面へのリンクを表示する
$SHOW_UPLOAD_EXT = false # アップロード可能な拡張子を表示する
#
# 共通で用いる関数類
#

# ファイルサイズを人間に分かりやすく表示する
# 1024→1KBのように
# とりあえず1K=1024で計算
def fileSizeToString(size)
	unit=1024
	if size<unit/2 then
		return size.to_s+"B"
	end
	if size<unit**2/2 then
		return sprintf("%.2f",(size.to_f/unit))+"KB"
	end
	if size<unit**3/2 then
		return sprintf("%.2f",(size.to_f/unit**2))+"MB"
	end
	if size<unit**4/2 then
		return sprintf("%.2f",size.to_f/unit**3)+"GB"
	end
	return sprintf("%.2f",size.to_f/unit**4)+"PB"
end

#
# データーベースの型の定義
#
FileData=Struct.new("FileData",:dl_count,:id,:ext,:comment,:size,:date,:filename,:editpass,:dl_pass,:host)
