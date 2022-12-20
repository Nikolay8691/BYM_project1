document.addEventListener('DOMContentLoaded', function(){
	elem = '.butt';
	document.querySelectorAll(elem).forEach(function(elem){
		elem.onmouseover = function(){
			this.children[1].style.display = "block";
		}
		elem.onmouseout = function(){
			this.children[1].style.display = "";
		}
	});
});
