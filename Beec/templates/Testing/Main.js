function go(obj) {
    var page=obj.href;
    document.getElementById('container').innerHTML='<object data="'+page+
      '" type="text/html"><embed src="'+page+'" type="text/html" /></object>';
    return false;
}