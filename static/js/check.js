function checkPword(){
	var pword = document.forms['pwordForm']['newPword'].value;
	var patt = /^[a-z0-9!!@#$%\^&*_\-<=>?]{6,}$/i;
	if(! patt.test(pword)){
		alert("密码只能为数字、字母或特殊符号的组合，并且至少6位！");
		return false;
	}
	return true;
}

function importPrompt(){
	return confirm("导入须知：本程序只接受“.csv和excel”格式的表格文件，" +
					"另外，文件的第一行将被视作新建表的表头，所以请确保" + 
					"该行中各列不含特殊符号（如各种标点符号和括号等），并且不应当有重复列！");
}

function tryEncrypt(){
	var form = document.forms['addRowForm'];
	for(var i=0; i<form.length; i++){
		if(form[i].name == "password"){
			originalValue = form[i].value;
			if(originalValue)
				form[i].value = hex_md5(originalValue);
		}
	}
}

function getrow(obj){
   if(event.srcElement.tagName=="TD"){
   curRow=event.srcElement.parentElement;
   curRow.style.background="yellow";
   }
}
function backrow(obj){
	if(event.srcElement.tagName=="TD"){
	curRow=event.srcElement.parentElement;
	curRow.style.background="white";
	}
}
function selectRow(obj) {
    if (event.srcElement.tagName == "TD") {
        curRow = event.srcElement.parentElement;
        curRow.style.background = "blue";
        var items = document.getElementsByTagName("tr");
        var row = curRow.rowIndex;
        var num = 0;
        var length = items[row].cells.length;
        var ss = length;
        var modal = document.getElementsByClassName("query_condition");
        items = document.getElementsByTagName("tr")
        for (var i = 0; i < length-1; i++ ){
            modal[i].getElementsByTagName('input')[0].value = items[row].cells[i+1].innerHTML;
            modal[i].getElementsByTagName('input')[1].value = items[row].cells[i+1].innerHTML;

        }


        //alert("这是第" + (items[row].cells[0].innerHTML) + "行");
        $('#update').modal("show");

    }
}
