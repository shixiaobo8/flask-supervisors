(function($,undefined){
	var effect_time = 200;
	$.fn.listMenu = function(options){
		var otherArgs = Array.prototype.slice.call(arguments, 1);
		if (typeof options == 'string') {
			var fn = this[0][options];
			if($.isFunction(fn)){
				return fn.apply(this[0], otherArgs);
			}else{
				throw ("listMenu - No such method: " + options);
			}
		}
		return this.each(function(){
			var defaults = {
				parentField:"",
				idField:"",
				captionField:"",
				rootId:"",
				typefield:"F_MENU_TYPE",
				onCreateText:null,
				onClickItem:null,
				onCreateIcon:null,
				multSelect:true
					
					
					
			};
			var opts = $.extend(defaults,options);
			var dom = this;
			var content;
			/**
			 * 初始化环境
			 */
			this.init = function(){
				$(this).empty();
				content = $("<div class='LM-content' />");
				content.appendTo(this);
				$(this).addClass("PTM");
			};
			/**
			 * 载入数据
			 */
			this.load = function(data){
				this.empty();
				this.decodeData(data);
				
			};
			this.decodeData = function(data){
				var menudata = data;
				var parentname = "";  // 二级菜单的父节点名称
				
				decode(opts.rootId,0);
				function decode(pid,js,pcontent){
					var pct = pcontent;
					$.each(menudata,function(i,item){
						var text = item[opts.captionField];
						var id = item[opts.idField];
						var parentid = item[opts.parentField];
						if(parentid === pid){
							if(js === 0){
								parentname = item.F_MENU_NAME;  // 保存一级菜单的名称，作为二级菜单的父节点名称展示 
								pct = dom.addGroup(id,text,item);
								decode(id,js+1,pct);
							}else{
								item["F_PARENT_NAME"] = parentname;  // 设置二级菜单的父节点名称
								dom.addItem(id,text,pct,item);
							}
						}
					});
				}
				
				
			};
			
			this.addGroup = function(id,text,data){
				var groupTitle = $("<div class='LM-group-title' menuid='"+id+"' />");
				if(data[opts.typefield] == "1"){//是分割线
					groupTitle.append("<hr>");
					groupTitle.addClass("LM-group-split");
					content.append(groupTitle);
					return null;
				}
				
				var groupContent = $("<div class='LM-group-content' formenuid='"+id+"' />");
				var titleText = text;
				if($.isFunction(opts.onCreateText)){
					titleText = opts.onCreateText.call(groupTitle,data);
				}
				groupTitle.html("<div class='LM-title-content' title='"+titleText+"'>" +
						"<span class='LM-title-icon' />"+
						"<span class='LM-title-text' >"+
						titleText +
						"</span>"+
						"<span class='LM-title-mark' />"+
						"</div>");
				
				if($.isFunction(opts.onCreateIcon)){
					var backimg = opts.onCreateIcon.call(groupTitle,data);
					var tIcon = groupTitle.find(".LM-title-icon");
					if(backimg.indexOf(":") >=0){
						var tStyle = tIcon.attr("style")||"";
						tIcon.attr("style",tStyle+";"+backimg);
					}else{
						tIcon.addClass(backimg);
					}
				}
				
				groupTitle.data("item-data",data);
				content.append(groupTitle);
				content.append(groupContent);
				groupTitle.click(function(){
					var $this = $(this);
					if($this.hasClass("menu-hasChildren")){
						if($this.hasClass("menu-select")){
							$this.removeClass("menu-select");
							groupContent.hide(effect_time);
						}else{
							if(opts.multSelect === false){//不支持多选
								$("[menuid]",content).removeClass("menu-select");
								$("[formenuid]",content).hide(effect_time);
							}
							$this.addClass("menu-select");
							groupContent.show(effect_time);
							
						}
					}
					if($.isFunction(opts.onClickItem)){
						var itemdata = $this.data("item-data");
						opts.onClickItem.call(this,itemdata);
					}
				});
				groupContent.hide();
				groupContent.data("for-item",groupTitle);
				return groupContent;
			};
			this.addItem = function(id,text,pct,data){
				var item = $("<div class='PTM-item'menuid='"+id+"' />");
				if(data[opts.typefield] == "1"){//是分割线
					item.append("<hr>");
					item.addClass("LM-group-split");
					pct.append(item);
					return;
				}
				
				
				var titleText = text;
				if($.isFunction(opts.onCreateText)){
					titleText = opts.onCreateText.call(item,data);
				}
				item.html("<div class='LM-item-content' title='"+titleText+"'>" +
						"<span class='LM-item-icon' />"+
						"<span class='LM-item-text' >"+
						titleText +
						"</span>"+
						"</div>");
				
				if($.isFunction(opts.onCreateIcon)){
					var tIcon = item.find(".LM-item-icon");
					var backimg = opts.onCreateIcon.call(tIcon,data);
					if(backimg.indexOf(":") >=0){
						var tStyle = tIcon.attr("style")||"";
						tIcon.attr("style",tStyle+";"+backimg);
					}else{
						tIcon.addClass(backimg);
					}
				}
				
				item.data("item-data",data);
				item.click(function(){
					if($.isFunction(opts.onClickItem)){
						var itemdata = $(this).data("item-data");
						opts.onClickItem.call(this,itemdata);
					}
				});
				pct.append(item);
				pct.data("for-item").addClass("menu-hasChildren");
			};
			/**
			 * 动态设置根节点虚拟的root值
			 */
			this.setRootID = function(id){
				opts.rootId = id;
			};
			this.selectGroup = function(id){
				var selectGroup;
				if(typeof id === "string"){//通过id选中
					selectGroup = $("[menuid='"+id+"']",content);
				}else{
					selectGroup = $("[menuid]",content).eq(id);
				}
				if(selectGroup.length>0 && !selectGroup.hasClass("menu-select")){
					selectGroup.click();
				}
			};
			this.empty = function(){
				content.empty();
			};
			this.init();
			
		});
	};
	
	
	
})(jQuery);