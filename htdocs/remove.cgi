#!/usr/local/bin/ruby
#-*- encoding:utf-8 -*-
require 'cgi'
require 'erb'
include ERB::Util
require_relative '../config'

cgi=CGI.new
data=nil

File.open("../"+$DATA_PATH,"r"){|f|
	data=Marshal.load(f)
}
maxId=data.shift

params=cgi.params
id=params["id"][0].to_i
password=params['password'][0]
if !password then
	password=""
end
password+=""

found=-1
0.upto(data.length-1){|i|
	found=i if data[i].id==id
}

if found==-1 then
	cgi.out{ERB.new(File.read("../"+$TEMPLATE_PATH+"notfound.erb")).result(binding)}
	exit
end

filedata=data[found]

if (filedata.editpass=="" || filedata.editpass!=password) && password!=$ADMIN_PASSWORD  then
	cgi.out{"パスワードが違います"}
	exit
end

`rm #{"../"+$UPLOAD_PATH+filedata.id.to_s}` if $DELETE_FILE
data.delete_at(found)

data.unshift(maxId)
File.open("../"+$DATA_PATH,"w",0777){|f|
	Marshal.dump(data,f)
}
filedata=data[found+1]
message="ファイルを消去しました"
cgi.out{ERB.new(File.read('../'+$TEMPLATE_PATH+"success.erb")).result(binding)}
