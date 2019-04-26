$(function(){
	$.ajax({
		url:ctx+"/notes/conf.json?"+new Date().getTime(),
		type:"GET",
		dataType:"json",
		success:function(d){
			console.info(d);
			loadNotes(d);
		}
	});
	$(".right-pane .comment").prepend('<a id="downloadDesk" href="'+ctx+'/jqGrid.exe">下载到桌面</a>');
	setTimeout(function(){
		$("#downloadDesk").remove();
	},20000);
	
});
function loadNotes(conf){
	var height = conf.height;
	var img = conf.img;
	var link = conf.link;
	var timeout = conf.timeout;
	var width = conf.width;
	if(height==null || img==null || link==null || timeout==null || width==null){
		return;
	}
	var p = $('<div class="notes-root" style=" "><div class="notes-close" style=" "><img style="width: 100%;height: 100%;" alt="" src="'+ctx+'/close.png" data-bd-imgshare-binded="1"></div></div>');
	p.append('<img class="notes-img" src="{img}" alt="" data-bd-imgshare-binded="0" /><a target="_blank" class="notes-link" href="{link}"><div class=" " style=" "></div></a>'.replace("{link}",link).replace("{img}",img.replace("${ctx}",ctx))); 
	p.css({
		width:width,
		height:height
	});
	$(".notes-close",p).click(function(){
		p.remove();
	});
	var pp = setTimeout(function(){
		p.remove();
	},timeout);
	p.hover(function(){
		clearTimeout(pp);
	},function(){
		pp = setTimeout(function(){
			p.remove();
		},timeout);
	});
	$(document.body).append(p);
	
}