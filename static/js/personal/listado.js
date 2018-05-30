function filter(){
    // Campo a filtrar
    var eGremio = document.getElementById("fil_gremio");
    var eDependencia = document.getElementById("fil_dependencia");
    // Opción del campo
    var optGremio = eGremio.options[eGremio.selectedIndex];
    var optDependencia = eDependencia.options[eDependencia.selectedIndex];
    // Todas las filas
    var trs = document.querySelectorAll('#dummyID tr');

    /**
     * Se ocultan aquellos que no cumplen con el criterio de busqueda.
     */
	for(i = 0; i < trs.length; ++i) {
        idtr = trs[i].id.split("_");
        // if ( type == 'gremio' ){
        //     trs[i].style.display = 'table-row';
        //     if ( idtr[1] != opt.value ){
        //         trs[i].style.display = 'none';
        //     }
    
        // }else if ( type == 'dependencia' ){
        //     trs[i].style.display = 'None';
        //     if ( idtr[0] == opt.innerHTML ){
        //         trs[i].style.display = 'table-row';
        //     }
        // }

        if (idtr[0] == optDependencia.innerHTML && idtr[1] == optGremio.value) {
            trs[i].style.display = 'table-row';
        }
        else {
            trs[i].style.display = 'none';
        }
    }
    
    /**
     * Se cambia contexto del reporte.
     */
	if (type=='gremio'){
		$("#botonreporte").attr("href","reporte?tipo="+type+"&filtro="+opt.value);
	}
	else {
		$("#botonreporte").attr("href","reporte?tipo="+type+"&filtro="+opt.innerHTML);
	}
}