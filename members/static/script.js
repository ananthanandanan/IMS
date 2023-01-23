// Description: Removes trailing comma from product titles
function strip_title() {
  var classname = document.getElementsByClassName("product-cell category");
  
  for (var i = 0; i < classname.length; i++) {
    var title = classname[i].getAttribute("title");
    if (title == null) {
      continue;
    }

    title = title.slice(-1) == "," ? title.slice(0, -1) : title;
    classname[i].setAttribute("title", title);
  }
}
window.onload = strip_title;
