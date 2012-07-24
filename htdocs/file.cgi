#!/usr/local/bin/ruby
#-*- encoding:utf-8 -*-
require 'cgi'
require 'erb'
include ERB::Util
require_relative '../config.rb'

cgi=CGI.new

data=nil
File.open("../"+$DATA_PATH,"r"){|f|
	data=Marshal.load(f)
}
data.shift

params=cgi.params
id=params['id'][0].to_i
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

filedata=data[found]

if filedata.dl_pass!="" && filedata.dl_pass!=password  then
	errors=Hash.new
	errors.default=false
	if password!="" && filedata.dl_pass!=password then
		errors['mismatch']=true
	end
	cgi.out{ERB.new(File.read("../"+$TEMPLATE_PATH+"pass.erb"),nil,'-').result(binding)}
	exit
end

cgi.out{ERB.new(File.read("../"+$TEMPLATE_PATH+"file.erb"),nil,'-').result(binding)}

