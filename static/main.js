
window.onload = init;
let currentModel = 0;
let currentModelSituation = "";

function  init() {
  $.ajax({
    type : "GET",
	  url : '/api/models',
	  dataType: "json",
	  contentType: 'application/json;charset=UTF-8',
	  success: function (data) {
		  render(data);
		  }
    });
    setInterval(function(){ 
      $.ajax({
        type : "GET",
        url : '/api/models',
        dataType: "json",
        contentType: 'application/json;charset=UTF-8',
        success: function (data) {
          render(data);
          }
        });
    }, 3000);//refresh the models every 3 second

}

function render(models) {
	const list = document.getElementById("models");
    while( list.firstChild ){
      list.removeChild( list.firstChild );
    }
    for (let model of models) {
    const node = document.createElement("li");
    const isPending = model.status=="pending" ? "list-group-item-danger":"list-group-item-success"

    node.setAttribute('status', model.status);
  	node.setAttribute('class', `list-group-item ${isPending}`);
  	node.setAttribute('data-key', model.model_id);
  	node.innerHTML = `
    	id: <text>${model.model_id}</text></br>
    	date: ${model.upload_time}</br>
  	`;

    node.addEventListener("click", setSelected)
  	list.append(node);

  }
}

  function setSelected(model) {
    if (model.target.getAttribute('status') == "pending") {
        var snackBar = document.getElementById("snackbar");
         snackBar.className = "show";
         setTimeout(function(){ snackBar.className = snackBar.className.replace("show", ""); }, 5000);
    }
    else if (currentModel == 0) {
        currentModel = model.target.getElementsByTagName("text")[0].textContent;
        model.target.setAttribute('class', `list-group-item active`);
    }
    else if (currentModel == model.target.getElementsByTagName("text")[0].textContent) {
        currentModel = 0;
        const isPending = model.target.getAttribute('status')=="pending" ? "list-group-item-danger":"list-group-item-success"
        model.target.setAttribute('class', `list-group-item ${isPending}`);
    }
    else {
      const list = document.getElementById("models").children;
      for (let child of list) {
        if (child.getElementsByTagName("text")[0].textContent == currentModel) {
          const isPending = child.getAttribute('status')=="pending" ? "list-group-item-danger":"list-group-item-success"
          child.setAttribute('class', `list-group-item ${isPending}`);
        }
      }
      currentModel = model.target.getElementsByTagName("text")[0].textContent;
      model.target.setAttribute('class', `list-group-item active`);
    }
  }

  function search() {
  // Declare variables
  let input, filter, ul, li, a, i, txtValue;
  input = document.getElementById('myInput');
  filter = input.value;
  ul = document.getElementById("models");
  li = ul.getElementsByTagName('li');

  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < li.length; i++) {
    a = li[i].getElementsByTagName("text")[0];
    txtValue = a.textContent || a.innerText;
    if (txtValue.indexOf(filter) > -1) {
      li[i].style.display = "";
    } else {
      li[i].style.display = "none";
    }
  }
}

function trainClick() {
    let trainButton = document.getElementById("train");
    let findButton = document.getElementById("find");

    if (findButton.classList.contains("active")) {
        findButton.classList.remove("active");
    }
    if (trainButton.classList.contains("active")) {
        trainButton.classList.remove("active");
    } else {
        trainButton.classList.add("active");
    }
}

function findClick() {
    let findButton = document.getElementById("find");
    let trainButton = document.getElementById("train");

    if (trainButton.classList.contains("active")) {
        trainButton.classList.remove("active");
    }
    if (findButton.classList.contains("active")) {
        findButton.classList.remove("active");
    } else {
        findButton.classList.add("active");
    }
}

var goalOfLoading = "";


    function dragOverHandler(ev) {
        console.log('File(s) in drop zone');

        // Prevent default behavior (Prevent file from being opened)
        ev.preventDefault();
    }

    function dropHandler(ev) {
        console.log('File(s) dropped');

        // Prevent default behavior (Prevent file from being opened)
        ev.preventDefault();

        if (ev.dataTransfer.items) {
        // Use DataTransferItemList interface to access the file(s)
            for (var i = 0; i < ev.dataTransfer.items.length; i++) {
                // If dropped items aren't files, reject them
                if (ev.dataTransfer.items[i].kind === 'file') {

                    var file = ev.dataTransfer.items[i].getAsFile();
                    //file.name;                                                                                                 //TODO:
                }
            }
        } else {
            // Use DataTransfer interface to access the file(s)
            for (var i = 0; i < ev.dataTransfer.files.length; i++) {
                ev.dataTransfer.files[i].name;                                                                       //TODO:
            }
        }
        // Pass event to removeDragData for cleanup
        removeDragData(ev)
    }

    function removeDragData(ev) {
        console.log('Removing drag data')

        if (ev.dataTransfer.items) {
            // Use DataTransferItemList interface to remove the drag data
            ev.dataTransfer.items.clear();
        } else {
            // Use DataTransfer interface to remove the drag data
            ev.dataTransfer.clearData();
        }
    }

    function changeGoalOfFileLOading(ev, goal) {
        goalOfLoading = goal;
    }