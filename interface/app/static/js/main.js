function callPythonToRunQueryResult(){
    var query = document.getElementById("input-query").value;
    eel.display_result(query)
}

function loadHTML(id, fname){
    console.log('div id: ${id}, fname: ${fname}');
}

function load_html() {
    document.getElementById("content").innerHTML='<object type="text/html" data="network.html" ></object>';
}