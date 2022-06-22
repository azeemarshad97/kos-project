function callPythonToRunQueryResult()
/* This is a JavaScript function that is called when the user
clicks the "Run Query" button. It gets the value of the
textarea with the id "input-query" and passes it to the Python
function "display_result" which is defined in the file
"main.py". */
{
    var query = document.getElementById("input-query").value;
    eel.display_result(query)
}


function insertTab(o, e)
/* A function that allows the user to press the tab key to insert a tab character. */
{
	var kC = e.keyCode ? e.keyCode : e.charCode ? e.charCode : e.which;
	if (kC == 9 && !e.shiftKey && !e.ctrlKey && !e.altKey)
	{
		var oS = o.scrollTop;
		if (o.setSelectionRange)
		{
			var sS = o.selectionStart;
			var sE = o.selectionEnd;
			o.value = o.value.substring(0, sS) + "\t" + o.value.substr(sE);
			o.setSelectionRange(sS + 1, sS + 1);
			o.focus();
		}
		else if (o.createTextRange)
		{
			document.selection.createRange().text = "\t";
			e.returnValue = false;
		}
		o.scrollTop = oS;
		if (e.preventDefault)
		{
			e.preventDefault();
		}
		return false;
	}
	return true;
}