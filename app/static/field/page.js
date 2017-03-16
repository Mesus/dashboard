
/*
function ChangSelect(oname,text)
{
	document.getElementById(oname).innerHTML=text+"&nbsp;&nbsp;&nbsp;&nbsp;<span class='caret'>";
}*/


function Mk_Csl(type,val)
{
	document.getElementById("div_csl").style.display="none";
	document.getElementById("div_ckl").style.display="none";
	document.getElementById("div_jpckc").style.display="none";
	document.getElementById("div_spckc").style.display="none";
	document.getElementById("div_yjcc").style.display="none";
	document.getElementById("div_"+type).style.display="block";
	switch(type)
	{
		case "csl":
			document.getElementById("span_name").innerHTML="采收量";
			document.getElementById("span_number").innerHTML=val;
			break;
		case "ckl":
			document.getElementById("span_name").innerHTML="出库量";
			document.getElementById("span_number").innerHTML=val;
			break;
		case "jpckc":
			document.getElementById("span_name").innerHTML="精品菜库存量";
			document.getElementById("span_number").innerHTML=val;
			break;
		case "spckc":
			document.getElementById("span_name").innerHTML="商品菜库存量";
			document.getElementById("span_number").innerHTML=val;
			break;
		case "yjcc":
			document.getElementById("span_name").innerHTML="预计出菜量";
			document.getElementById("span_number").innerHTML=val;
			break;
	}
}
function Mk_Sh(type)
{
	document.getElementById("div_yqshl").style.display="none";
	document.getElementById("div_jgshl").style.display="none";
	document.getElementById("div_dbshl").style.display="none";
	document.getElementById("div_"+type).style.display="block";
	switch(type)
	{
		case "yqshl":
			document.getElementById("span_name").innerHTML="逾期损耗量";
			document.getElementById("span_number").innerHTML="";
			break;
		case "jgshl":
			document.getElementById("span_name").innerHTML="加工损耗量";
			document.getElementById("span_number").innerHTML="{{jgshl}}";
			break;
		case "dbshl":
			document.getElementById("span_name").innerHTML="调拨损耗量";
			document.getElementById("span_number").innerHTML="{{dbshl}}";
			break;
	}
}
function Mk_Xs(type)
{
	document.getElementById("div_xsl").style.display="none";
	document.getElementById("div_kgl").style.display="none";
	document.getElementById("div_dbl").style.display="none";
	document.getElementById("div_"+type).style.display="block";
	switch(type)
	{
		case "xsl":
			document.getElementById("span_name").innerHTML="销售量";
			document.getElementById("span_number").innerHTML="{{xsl}}";
			break;
		case "kgl":
			document.getElementById("span_name").innerHTML="可供量";
			document.getElementById("span_number").innerHTML="{{kgl}}";
			break;
		case "dbl":
			document.getElementById("span_name").innerHTML="调拨";
			document.getElementById("span_number").innerHTML="{{dbl}}";
			break;
	}
}

	function LoadSlt(type,xdata,data)
	{
		$('#container1').highcharts({
			chart:{
				type:'column',
                backgroundColor:'rgba(0,0,0,0)',
				options3d: {
					enabled: true,
					alpha: 5,
					beta: 2,
					depth: 50,
					viewDistance: 25
				}
            },
			title:{text:''},
			exporting:{enabled:false},
			legend:{enabled:false},
			credits:{enabled: false},
			plotOptions:{
				column:{
					dataLabels:{
						enabled:true,
						style:{
							fontSize:'1.8em',
							color:'white',
							fontWeight:false
						},
						formatter: function() {  
							return this.y.toFixed(1)+"(Kg)";  
						}  
					}
				},
				series: {        
					cursor: 'column',        
					events: {            
					click: function(event) {
//						LoadModal(type,event.point.category);
					}   
				  }   
				}
			},
			xAxis:{
				categories: xdata,
				labels:{
					style:{
						fontSize:'1.5em',
						color:'white'
					}
				}
			},
			yAxis:{
				title:{text: ''},
				labels:{
					style:{
						fontSize:'1.5em',
						color:'white'
					}
				},
				gridLineColor:'#808184',
				gridLineWidth:'1px'
			},
			tooltip:{
				valueSuffix: 'Kg'
			},
			series:[{
				name: '数量',
				data: data,
				color:'#f6f46f'
			}]
		});
	}
	
	
	function LoadModal(type,name)
	{
//		alert("页面:"+type+",x轴名称:"+name);
		var data=[323.0,125.0,293.0,76.0,189.0,189.0,245.1,65.7,52.1,156.0,0.0];
		var xdata=['北京','上海','广州','成都','云南','扬州','惠州','山东','长沙','深圳包装厂','坝上'];
		LoadModalSlt(xdata,data);
	}
	function LoadModalSlt(xdata,data)
	{
		$('#container2').highcharts({
			chart:{
				type:'column',
                backgroundColor:'rgba(0,0,0,0)',
				options3d: {
					enabled: true,
					alpha: 5,
					beta: 2,
					depth: 50,
					viewDistance: 25
				}
            },
			title:{text:''},
			exporting:{enabled:false},
			legend:{enabled:false},
			credits:{enabled: false},
			plotOptions:{
				column:{
					dataLabels:{
						enabled:true,
						style:{
							fontSize:'1.8em',
							color:'white',
							fontWeight:false
						},
						formatter: function() {  
							return this.y.toFixed(1)+"(Kg)";  
						}  
					}
				}
			},
			xAxis:{
				categories: xdata,
				labels:{
					style:{
						fontSize:'1.5em',
						color:'white'
					}
				}
			},
			yAxis:{
				title:{text: ''},
				labels:{
					style:{
						fontSize:'1.5em',
						color:'white'
					}
				},
				gridLineColor:'#808184',
				gridLineWidth:'1px'
			},
			tooltip:{
				valueSuffix: 'Kg'
			},
			series:[{
				name: '数量',
				data: data,
				color:'#f6f46f'
			}]
		});
		$('#myModal').modal();
	}


