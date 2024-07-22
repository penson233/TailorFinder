<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" encoding="utf-8" indent="yes" doctype-system="about:legacy-compat"/>
  <xsl:template match="/">
    <html lang="en">
      <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" />
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" />
        <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.19/css/dataTables.bootstrap.min.css"/>
        <script src="https://code.jquery.com/jquery-3.3.1.js"></script>
        <script src="https://cdn.datatables.net/1.10.19/js/jquery.dataTables.min.js"></script>
        <script src="https://cdn.datatables.net/1.10.19/js/dataTables.bootstrap.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" ></script>
        <style>
          .target:before {
            content: "";
            display: block;
            height: 50px;
            margin: -20px 0 0;
          }
          @media only screen and (min-width:1900px) {
            .container {
              width: 1800px;
              }
          }
          .footer {
            margin-top:60px;
            padding-top:60px;
            width: 100%;
            height: 180px;
            background-color: #f5f5f5;
          }
        .navbar-right {
		 float: right!important;
		 margin-right: -15px;
	   }
        </style>
        <title>Nmap Scanner 扫描报告</title>
      </head>
      <body>
	  <!--导航栏-->
        <nav class="navbar navbar-default navbar-fixed-top">
          <div class="container-fluid">
            <div class="navbar-header">
              <a class="navbar-brand" href="#"><span class="glyphicon glyphicon-home"></span></a>
            </div>
            <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
              <ul class="nav navbar-nav">
                <li><a href="#summary">概要信息</a></li>
                <li><a href="#scannedhosts">主机信息</a></li>
                <li><a href="#onlinehosts">在线主机</a></li>
                <li><a href="#openservices">服务信息</a></li>
              </ul>
            </div>
          </div>
        </nav>

	 <!--内容区-->
        <div class="container">		
		 <h2 id="summary" class="target">扫描概要</h2>
          <div class="target">
			<p >Nmap 版本：<xsl:value-of select="/nmaprun/@version"/></p>
            <p >Nmap命令：<xsl:value-of select="/nmaprun/@args"/></p>
			<p >开始时间：<xsl:value-of select="/nmaprun/@startstr"/> </p>
			<p >结束时间：<xsl:value-of select="/nmaprun/runstats/finished/@timestr"/></p>
          </div>
		  
          <h2 id="scannedhosts" class="target">主机信息<xsl:if test="/nmaprun/runstats/hosts/@down > 1024"><small> (offline hosts are hidden)</small></xsl:if></h2>
          <div class="table-responsive">
            <table id="table-overview" class="table table-striped dataTable" role="grid">
              <thead>
                <tr>
                  <th>状态</th>
                  <th>IP</th>
                  <th>主机名</th>
                  <th>开放TCP端口数</th>
                  <th>开放UDP端口数</th>
                </tr>
              </thead>
              <tbody>
                <xsl:choose>
                  <xsl:when test="/nmaprun/runstats/hosts/@down > 1024">
                    <xsl:for-each select="/nmaprun/host[status/@state='up']">
                      <tr>
                        <td><span class="label label-danger"><xsl:if test="status/@state='up'"><xsl:attribute name="class">label label-success</xsl:attribute></xsl:if><xsl:value-of select="status/@state"/></span></td>
                        <td><xsl:value-of select="address/@addr"/></td>
                        <td><xsl:value-of select="hostnames/hostname/@name"/></td>
                        <td><xsl:value-of select="count(ports/port[state/@state='open' and @protocol='tcp'])"/></td>
                        <td><xsl:value-of select="count(ports/port[state/@state='open' and @protocol='udp'])"/></td>
                      </tr>
                    </xsl:for-each>
                  </xsl:when>
                  <xsl:otherwise>
                    <xsl:for-each select="/nmaprun/host">
                      <tr>
                        <td><span class="label label-danger"><xsl:if test="status/@state='up'"><xsl:attribute name="class">label label-success</xsl:attribute></xsl:if><xsl:value-of select="status/@state"/></span></td>
                        <td><xsl:value-of select="address/@addr"/></td>
                        <td><xsl:value-of select="hostnames/hostname/@name"/></td>
                        <td><xsl:value-of select="count(ports/port[state/@state='open' and @protocol='tcp'])"/></td>
                        <td><xsl:value-of select="count(ports/port[state/@state='open' and @protocol='udp'])"/></td>
                      </tr>
                    </xsl:for-each>
                  </xsl:otherwise>
                </xsl:choose>
              </tbody>
            </table>
          </div>
          <script>
            $(document).ready(function() {			  
			 $('#table-overview').DataTable({
				 language: {
					 "sProcessing": "处理中...",
					 "sLengthMenu": "显示 _MENU_ 项结果",
					 "sZeroRecords": "没有匹配结果",
					 "sInfo": "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
					 "sInfoEmpty": "显示第 0 至 0 项结果，共 0 项",
					 "sInfoFiltered": "(由 _MAX_ 项结果过滤)",
					 "sInfoPostFix": "",
					 "sSearch": "搜索:",
					 "sUrl": "",
					 "sEmptyTable": "表中数据为空",
					 "sLoadingRecords": "载入中...",
					 "sInfoThousands": ",",
					 "oPaginate": {
						 "sFirst": "首页",
						 "sPrevious": "上页",
						 "sNext": "下页",
						 "sLast": "末页"
					 },
					 "oAria": {
						 "sSortAscending": ": 以升序排列此列",
						 "sSortDescending": ": 以降序排列此列"
					 }
				 }
			 });			  
            });
			
          </script>
		  
          <h2 id="onlinehosts" class="target">在线主机</h2>
          <xsl:for-each select="/nmaprun/host[status/@state='up']">
            <div class="panel panel-default">
              <div class="panel-heading">
                <h3 class="panel-title"><xsl:value-of select="address/@addr"/><xsl:if test="count(hostnames/hostname) > 0"> - <xsl:value-of select="hostnames/hostname/@name"/></xsl:if></h3>
              </div>
              <div class="panel-body">
                <xsl:if test="count(hostnames/hostname) > 0">
                  <h4>Hostnames</h4>
                  <ul>
                    <xsl:for-each select="hostnames/hostname">
                      <li><xsl:value-of select="@name"/> (<xsl:value-of select="@type"/>)</li>
                    </xsl:for-each>
                  </ul>
                </xsl:if>
                <h4>端口信息</h4>
                <div class="table-responsive">
                  <table class="table table-bordered">
                    <thead>
                      <tr>
                        <th>端口</th>
                        <th>协议</th>
                        <th>状态</th>
                        <th>探测手段</th>
                        <th>服务</th>
                        <th>组件</th>
                        <th>版本</th>
                        <th>附件信息</th>
                        <th>CPE 信息</th>
                      </tr>
                    </thead>
                    <tbody>
                      <xsl:for-each select="ports/port">
                        <xsl:choose>
                          <xsl:when test="state/@state = 'open'">
                            <tr class="success">
                              <td title="Port"><xsl:value-of select="@portid"/></td>
                              <td title="Protocol"><xsl:value-of select="@protocol"/></td>
                              <td title="State"><xsl:value-of select="state/@state"/></td>
							  <td title="Reason"><xsl:value-of select="state/@reason"/></td>
                              <td title="Service"><xsl:value-of select="service/@name"/></td>
                              <td title="Product"><xsl:value-of select="service/@product"/></td>
                              <td title="Version"><xsl:value-of select="service/@version"/></td>
                              <td title="Extra Info"><xsl:value-of select="service/@extrainfo"/></td>
                              <td title="CPE Info"><xsl:value-of select="service/cpe"/></td>
                            </tr>
							
							  <xsl:for-each select="script">
								<tr class="script">
								  <td></td>
								  <td><xsl:value-of select="@id"/> <xsl:text>&#xA0;</xsl:text></td>
								  <td colspan="7">
									<pre><xsl:value-of select="@output"/> <xsl:text>&#xA0;</xsl:text></pre>
								  </td>
								</tr>

							  </xsl:for-each>
							  
                          </xsl:when>
                          <xsl:when test="state/@state = 'filtered'">
                            <tr class="warning">
                              <td><xsl:value-of select="@portid"/></td>
                              <td><xsl:value-of select="@protocol"/></td>
                              <td><xsl:value-of select="state/@state"/><br/><xsl:value-of select="state/@reason"/></td>
                              <td><xsl:value-of select="service/@name"/></td>
                              <td><xsl:value-of select="service/@product"/></td>
                              <td><xsl:value-of select="service/@version"/></td>
                              <td><xsl:value-of select="service/@extrainfo"/></td>
							  <td><xsl:value-of select="service/cpe"/></td>
                            </tr>
                          </xsl:when>
                          <xsl:when test="state/@state = 'closed'">
                            <tr class="active">
                              <td><xsl:value-of select="@portid"/></td>
                              <td><xsl:value-of select="@protocol"/></td>
                              <td><xsl:value-of select="state/@state"/><br/><xsl:value-of select="state/@reason"/></td>
                              <td><xsl:value-of select="service/@name"/></td>
                              <td><xsl:value-of select="service/@product"/></td>
                              <td><xsl:value-of select="service/@version"/></td>
                              <td><xsl:value-of select="service/@extrainfo"/></td>
							  <td><xsl:value-of select="service/cpe"/></td>
                            </tr>
                          </xsl:when>
                          <xsl:otherwise>
                            <tr class="info">
                              <td><xsl:value-of select="@portid"/></td>
                              <td><xsl:value-of select="@protocol"/></td>
                              <td><xsl:value-of select="state/@state"/><br/><xsl:value-of select="state/@reason"/></td>
                              <td><xsl:value-of select="service/@name"/></td>
                              <td><xsl:value-of select="service/@product"/></td>
                              <td><xsl:value-of select="service/@version"/></td>
                              <td><xsl:value-of select="service/@extrainfo"/></td>
							  <td><xsl:value-of select="service/cpe"/></td>
                            </tr>
                          </xsl:otherwise>
                        </xsl:choose>
                      </xsl:for-each>
                    </tbody>
                  </table>
                </div>
				
                <xsl:if test="count(hostscript/script) > 0">
                  <h4>主机 脚本</h4>
                </xsl:if>
                <xsl:for-each select="hostscript/script">
                  <h5><xsl:value-of select="@id"/></h5>
                  <pre style="white-space:pre-wrap; word-wrap:break-word;"><xsl:value-of select="@output"/></pre>
                </xsl:for-each>
				
              </div>
            </div>
          </xsl:for-each>
		  
		  
		  
          <h2 id="openservices" class="target">服务信息</h2>
          <div class="table-responsive">
            <table id="table-services" class="table table-striped dataTable" role="grid">
              <thead>
                <tr>
                  <th>IP</th>
                  <th>端口</th>
                  <th>协议</th>
                  <th>服务</th>
                  <th>组件</th>
                  <th>版本</th>
                  <th>CPE</th>
                  <th>附加信息</th>
                </tr>
              </thead>
              <tbody>
                <xsl:for-each select="/nmaprun/host">
                  <xsl:for-each select="ports/port[state/@state='open']">
                    <tr>
                      <td><xsl:value-of select="../../address/@addr"/><xsl:if test="count(../../hostnames/hostname) > 0"> - <xsl:value-of select="../../hostnames/hostname/@name"/></xsl:if></td>
                      <td><xsl:value-of select="@portid"/></td>
                      <td><xsl:value-of select="@protocol"/></td>
                      <td><xsl:value-of select="service/@name"/></td>
                      <td><xsl:value-of select="service/@product"/></td>
                      <td><xsl:value-of select="service/@version"/></td>
                      <td><xsl:value-of select="service/cpe"/></td>
                      <td><xsl:value-of select="service/@extrainfo"/></td>
                    </tr>
                  </xsl:for-each>
                </xsl:for-each>
              </tbody>
            </table>
          </div>
          <script>		
            $(document).ready(function() {			  
			 $('#table-services').DataTable({
				 language: {
					 "sProcessing": "处理中...",
					 "sLengthMenu": "显示 _MENU_ 项结果",
					 "sZeroRecords": "没有匹配结果",
					 "sInfo": "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
					 "sInfoEmpty": "显示第 0 至 0 项结果，共 0 项",
					 "sInfoFiltered": "(由 _MAX_ 项结果过滤)",
					 "sInfoPostFix": "",
					 "sSearch": "搜索:",
					 "sUrl": "",
					 "sEmptyTable": "表中数据为空",
					 "sLoadingRecords": "载入中...",
					 "sInfoThousands": ",",
					 "oPaginate": {
						 "sFirst": "首页",
						 "sPrevious": "上页",
						 "sNext": "下页",
						 "sLast": "末页"
					 },
					 "oAria": {
						 "sSortAscending": ": 以升序排列此列",
						 "sSortDescending": ": 以降序排列此列"
					 }
				 }
			 });			  
            });			
          </script>
        </div>
	 <!-- 页脚 -->
		<footer class="footer" style="height: 50px; margin-top: 20px; padding-top: 20px;">
          <div class="container">
            <p class="text-muted">
              This Report Was Generated By <a href='https://www.cnblogs.com/lyshark'>LyShark</a>.<br/>
            </p>
          </div>
        </footer>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>

