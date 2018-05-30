function filter(type){
	
	var e = document.getElementById("fil_"+type);
	var opt = e.options[e.selectedIndex];
    var trs = document.querySelectorAll('#dummyID tr');
    
	for(i = 0; i < trs.length; ++i) {
        idtr = trs[i].id.split("_");
        console.log('idtr', idtr);
		if ( type == 'gremio' ){
	
			trs[i].style.display = 'None';
			if ( idtr[1] == opt.value ){trs[i].style.display = 'table-row';}
	
		}else if ( type == 'dependencia' ){

			trs[i].style.display = 'None';
			if ( idtr[0] == opt.innerHTML ){trs[i].style.display = 'table-row';}
	
		}
	
	}
	if (type=='gremio'){
		$("#botonreporte").attr("href","reporte?tipo="+type+"&filtro="+opt.value);
	}
	else {
		$("#botonreporte").attr("href","reporte?tipo="+type+"&filtro="+opt.innerHTML);
	}
}