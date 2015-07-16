$(document).ready(function(){
	
	$("#likes").click(function(){
		
		catid = $(this).attr("data-catid2");
		
		$.get('/rango/like_category/', {category_id: catid}, function(data){
			$("#like_count").html(data);
			$('#likes').hide();			
		});
		
	});
	
	$('#suggestion').keyup(function(){
		
		var query;
		
		query = $(this).val();
		
		$.get('/rango/suggest_category/', {suggestion: query}, function(data){
			$('#cats').html(data);	
		});
	
	});	
	
	$(".rango-add").click(function(){
		
		var catid = $(this).attr("data-catid");
		var title = $(this).attr("data-title");
		var url = $(this).attr("data-url");
		
		$.get('/rango/auto_add_page/', {category_id:catid, title:title, url:url}, function(data){
			$("#pages").html(data);
		});
		
	});
	
});