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
password=params['pass'][0]
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

data[found].dl_count+=1
data.unshift(maxId)
File.open("../"+$DATA_PATH,"w",0777){|f|
	Marshal.dump(data,f)
}
filedata=data[found+1]

if filedata.dl_pass!="" && filedata.dl_pass!=password then
	cgi.out{"パスワードが違います"}
	exit
end


content=File.binread("../"+$UPLOAD_PATH+id.to_s)
cgi.out({'Content-Type' => 'multipart/form-data',
	         'Content-Length' => filedata.size,
			 	         'Content-Disposition' => "attachment; filename=\"#{filedata.filename}\""}){content}

