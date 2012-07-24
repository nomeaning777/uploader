#!/usr/local/bin/ruby
#-*- encoding:utf-8 -*-
require 'cgi'
require 'erb'
include ERB::Util
require_relative '../config'

cgi=CGI.new

PagePer=$PAGEPER
data=nil

if !File.exist?('../'+$DATA_PATH) then
	File.open('../'+$DATA_PATH,"w",0777){|f|
		Marshal.dump([1],f)
	}
end
File.open('../'+$DATA_PATH,"r"){|f|
	data=Marshal.load(f)
}
data.shift #次のIDの情報は使わない
pageCount=(data.length+PagePer-1)/PagePer

params=cgi.params
page=params['page'][0]
pageStart=0
pageEnd=data.length-1
if page!='all' then
	page=page.to_i
	if page<=0 || page>pageCount then
		page=1
	end
	pageStart=(page-1)*PagePer
	pageEnd=[page*PagePer,data.length].min-1
end


erb=ERB.new(File.read('../'+$TEMPLATE_PATH+'index.erb'),nil,'-')
cgi.out({"charset"=>"utf-8"}){erb.result(binding)}

