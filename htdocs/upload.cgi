#!/usr/local/bin/ruby
#-*- encoding:utf-8 -*-
require 'cgi'
require 'erb'
require 'tempfile'
require 'socket'
require_relative '../config'

cgi=CGI.new

params=cgi.params
comment_data=cgi['comment'].to_s+""

dl_key=cgi["dlpass"].to_s+"" if $USE_DL_KEY
dl_key="" unless dl_key
edit_key=cgi["editpass"].to_s+"" if $USE_EDIT_KEY
edit_key="" unless edit_key

errors=Hash.new
errors.default=false

# ファイルのチェック
file=params['upload_file'][0]
if errors.size==0 && file=="" then
	#ファイルが指定されていない
	errors['nofile']=true
end

target_file=file #実際に書き込むファイル(TEMP FILE)
target_name=file.original_filename
ext=File.extname(target_name).downcase

if target_file.kind_of?(StringIO) then
	#TempFileに変える
	tmp_file=Tempfile.open(['uploader','.'+ext])
	tmp_file.write(file.read)
	tmp_file.seek(0)
	target_file=tmp_file
	
end

if ext[0]=="." then
	ext=ext.slice(1,ext.length-1)
end

# 拡張子のチェック
if errors.size==0 && $UPLOAD_EXT != [] && !$UPLOAD_EXT.include?(ext) then
	errors['ext']=true
end

#ファイルサイズのチェック
if errors.size==0 && $FILE_SIZE_LIMIT!=-1 && file.length>$FILE_SIZE_LIMIT then
	errros['filesize']=true
end
#コメントの大きさのチェック
if errors.size==0 && comment_data.length>$COMMENT_LIMIT then
	errors['comment_length']=true
end

#DLキーの流さのチェック
if errors.size==0 && dl_key.length>$DL_KEY_LIMIT then
	errors['dl_key_length']=true
end

#編集パスワードのチェック
if errors.size==0 && edit_key.length>$EDIT_KEY_LIMIT then
	errors['edit_key_length']=true
end

#禁止IPのチェック
if errors.size==0 && $USE_DENY_IP && ($DENY_IP =~ cgi.remote_addr.to_s) then
	errors['deny']=true
end

if errors.size==0 && $USE_DENY_HOST then
	begin
		if Socket.getnameinfo([nil, 0, cgi.remote_addr]).first then
			errors['deny']=true
		end
	rescue
	end
end


#WAVEならmp3に変換する
if errors.size==0 && $USE_WAVE_CONVERT && (File.extname(target_name).downcase==".wav" || File.extname(target_name).downcase==".wave") then
	tp_mp3=nil
	Tempfile.open(['conv','.wav']){|tp_wav|
		tp_mp3=Tempfile.open(['conv','.mp3'])
		`cp #{target_file.path} #{tp_wav.path}`
		result=`lame -b 192kbps #{tp_wav.path} #{tp_mp3.path} 2>&1`
		if !result.include?("Writing LAME Tag") then
			errors['wave_convert']=true
		end
	}
	target_file=tp_mp3
	target_name=target_name[0..target_name.length-File.extname(target_name).length]+"mp3"
	ext="mp3"
end

#エラーがあるならエラー画面を表示して終了
if errors.size>0 then
	cgi.out{ERB.new(File.read("../"+$TEMPLATE_PATH+"error.erb")).result(binding)}
	exit
end

data=nil
File.open('../'+$DATA_PATH,File::RDWR|File::CREAT,0777){|f|
	f.flock(File::LOCK_EX)
	data=Marshal.load(f)
	
	maxId=data.shift
	nextId=maxId
	File.open("../"+$UPLOAD_PATH+nextId.to_s,"wb",0777){|fp|
		fp.write(target_file.read)
	}
	data.unshift(FileData.new(0.to_i,nextId,ext,comment_data+"",target_file.size.to_i,Time.now,target_name.to_s.force_encoding("UTF-8"),edit_key,dl_key,cgi.remote_addr.to_s))

	data.unshift(maxId+1)

	f.rewind
	Marshal.dump(data,f)
	f.flush
	f.truncate(f.pos)
}
cgi.out{ERB.new(File.read('../'+$TEMPLATE_PATH+"upload.erb")).result(binding)}
