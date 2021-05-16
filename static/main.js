

window.onload = init;
let currentModel = 0;
var isTrainTableExist = false;
var isPropertyListExist = false;
var goalOfLoading = "";
var isAnomaliesExist = false;
var activeListElement = undefined;
var anomaliesCellsObjects = [];
var CSVFile;

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
        var isPending = model.status=="pending" ? "list-group-item-danger":"list-group-item-success"

        node.setAttribute('status', model.status);
        node.setAttribute('data-key', model.model_id);
        if (node.getAttribute('data-key') == currentModel) {
          isPending = "list-group-item active";
        }
        node.setAttribute('class', `list-group-item ${isPending}`);

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
        goalOfLoading = "train";
        let trainButton = document.getElementById("train");
        let findButton = document.getElementById("find");
        let typesDiv = document.getElementById("types");

        if (findButton.classList.contains("active")) {
            findButton.classList.remove("active");
        }
        if (trainButton.classList.contains("active")) {
            trainButton.classList.remove("active");
            typesDiv.classList.add("hidden");
        } else {
            trainButton.classList.add("active");
            typesDiv.classList.remove("hidden");
        }
    }

    function findClick() {
        goalOfLoading = "detect";
        let findButton = document.getElementById("find");
        let trainButton = document.getElementById("train");
        let typesDiv = document.getElementById("types");

        if (trainButton.classList.contains("active")) {
            trainButton.classList.remove("active");
        }
        if (findButton.classList.contains("active")) {
            findButton.classList.remove("active");
        } else {
            findButton.classList.add("active");
            typesDiv.classList.add("hidden");
        }
    }

        function hybridClick() {
        goalOfLoading = "train hybrid";
        let hybridButton = document.getElementById("hybrid");
        let regressionButton = document.getElementById("regression");

        if (regressionButton.classList.contains("active")) {
            regressionButton.classList.remove("active");
        }
        if (hybridButton.classList.contains("active")) {
            hybridButton.classList.remove("active");
        } else {
            hybridButton.classList.add("active");
        }
    }

    function regressionClick() {
        goalOfLoading = "train regression";
        let regressionButton = document.getElementById("regression");
        let hybridButton = document.getElementById("hybrid");

        if (hybridButton.classList.contains("active")) {
            hybridButton.classList.remove("active");
        }
        if (regressionButton.classList.contains("active")) {
            regressionButton.classList.remove("active");
        } else {
            regressionButton.classList.add("active");
        }
    }


    async function CSVToJson(file) {
        const text = await file.text();
        var allTextLines = text.split(/\r\n|\n/);
        var headers = allTextLines[0].split(',');
        var table = new Array(headers.length);
        for (var i = 0; i < table.length; i++) {
          table[i] = [];
        }

        for (var i=1; i<allTextLines.length; i++) {
            var data = allTextLines[i].split(',');
            if (data.length == headers.length) {

                for (var j=0; j<headers.length; j++) {
                    table[j].push(data[j]);
                }
            }
        }
        var json = {};
        for (var i = 0; i < headers.length - 1; i++) {
               column= new Array(table[i].length);
               for (var j = 0; j < table[i].length - 1; j++) {
                    column[j] = table[i][j];
               }
               column[j] = table[i][j];
               json[headers[i]] = column;
        }
        return json;
     }

    function dragOverHandler(ev) {
        console.log('File(s) in drop zone');

        // Prevent default behavior (Prevent file from being opened)
        ev.preventDefault();
    }

    async function handleFile(chosenCSVFile){
        if (chosenCSVFile.type != "text/csv") {
            alert("wrong file! not a csv file");
            return;
        }
        json = await CSVToJson(chosenCSVFile);
        if (isJsonOfCSVFileValid(JSON.stringify(json))){
            setTrainTable(JSON.stringify(json));
            setListOfProperties(JSON.stringify(json));
        }
        if (goalOfLoading == "train hybrid") {
            $.ajax({
              type : "POST",
              url : '/api/model?model_type=hybrid',
              dataType: "json",
              contentType: 'application/json;charset=UTF-8',
              accept: 'application/json;charset=UTF-8',
              data: JSON.stringify({"train_data":  json }),
            });
        }
        else if (goalOfLoading == "train regression") {
            $.ajax({
              type : "POST",
              url : '/api/model?model_type=regression',
              dataType: "json",
              contentType: 'application/json;charset=UTF-8',
              accept: 'application/json;charset=UTF-8',
              data: JSON.stringify({"train_data":  json }),
            });
        }
        else if (goalOfLoading=="detect") {
            if (currentModel == 0) {
                alert("please choose a model, no model was chosen");
                return;
            }
            $.ajax({
              type : "POST",
              url : '/api/anomaly?model_id=' + currentModel.toString(),
              dataType: "json",
              contentType: 'application/json;charset=UTF-8',
              accept: 'application/json;charset=UTF-8',
              data: JSON.stringify({"predict_data":  json }),
            });
        }
    }

    async function dropHandler(ev) {
        //getArrayOfTableColumnObjectsAccordingProperty("B");
        var chosenCSVFile;
        console.log('File(s) dropped');

        // Prevent default behavior (Prevent file from being opened)
        ev.preventDefault();

        if (ev.dataTransfer.items) {
        // Use DataTransferItemList interface to access the file(s)
            for (var i = 0; i < ev.dataTransfer.items.length; i++) {
                // If dropped items aren't files, reject them
                if (ev.dataTransfer.items[i].kind === 'file') {
                    CSVFile = ev.dataTransfer.items[i].getAsFile();
                }
            }
        } else {
            // Use DataTransfer interface to access the file(s)
            for (var i = 0; i < ev.dataTransfer.files.length; i++) {
                CSVFile = ev.dataTransfer.files[i].name;
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

    function setTrainTable(jsonString)
    {
      const jsonObject = JSON.parse(jsonString);
      const tableObject = document.getElementById("train-table");
      let numberOfRows = jsonObject[Object.keys(jsonObject)[0]].length;
      let arrayOfRows = [];
        
      if(isTrainTableExist)
      {
        deleteTrainTable();
      }

      let tableHeaders = document.createElement("tr");
      tableObject.appendChild(tableHeaders);

      //create rows(<tr> elements)
      for(let rowNUm = 0; rowNUm < numberOfRows; ++rowNUm)
      {
          let tableRow = document.createElement("tr");
          arrayOfRows.push(tableRow);
          tableObject.appendChild(tableRow);
      }
    
      for(const property in jsonObject) {
          //append properties to header
          let newTableHeader = document.createElement("th");
          newTableHeader.textContent = property;
          tableHeaders.appendChild(newTableHeader);
          for (let i = 0; i < numberOfRows; ++i)
          {
              //append properyValues to rows
              let newRowValue = document.createElement("td");
              newRowValue.textContent = jsonObject[property][i];
              arrayOfRows[i].appendChild(newRowValue);
          }
      }

      isTrainTableExist = true;
    }

    function isJsonOfCSVFileValid(jsonString)
    {
        const jsonObject = JSON.parse(jsonString);
        const numberOfProperties = Object.keys(jsonObject).length;
        if(numberOfProperties == 0)
        {
            return false;
        }

        let numberOfRows = jsonObject[Object.keys(jsonObject)[0]].length;
        for(let i = 0; i < numberOfProperties; ++i)
        {
            if(jsonObject[Object.keys(jsonObject)[i]].length != numberOfRows)
            {
                alert("CSV FLIE NOT VALID!");
                console.log("not valid");
                return false;
            }
        }
        console.log("valid");
        return true;
    }

    function deleteTrainTable()
    {
        const tableObject = document.getElementById("train-table");
        while (tableObject.firstChild) {
            tableObject.removeChild(tableObject.lastChild);
        }
    }

    function getTableColumnIndexAccordingProperty(propertyName)
    {
        const tableObject = document.getElementById("train-table");
        const properties = tableObject.firstChild.children;
        for(let i = 0; i < properties.length; ++i)
        {
            if(properties[i].textContent == propertyName)
            {
                return i;
            }
        }
        return -1;
    }

    function getArrayOfTableColumnObjectsAccordingProperty(propertyName)
    {
        const tableChildren = document.getElementById("train-table").children;
        let arrayOfColumnObjects = [];
        const columnIndex = getTableColumnIndexAccordingProperty(propertyName);
        if(columnIndex == -1)
        {
            return -1;
        }
        for(let i = 1; i < tableChildren.length; ++i)
        {
            arrayOfColumnObjects.push(tableChildren[i].children[columnIndex]);
        }
        return arrayOfColumnObjects
    }

    function updateTableAccordingAnomalies(jsonString)
    {
        const jsonObject = JSON.parse(jsonString);

        if(isAnomaliesExist)
        {
            clearAnomalies();
        }

        for(const property in jsonObject) {
            let propertyColumnObjects = getArrayOfTableColumnObjectsAccordingProperty(property);
            if(propertyColumnObjects != -1)
            {
                for(let i = 0; i < jsonObject[property].length; ++i)
                {
                    anomaliesCellsObjects.push(propertyColumnObjects[jsonObject[property][i]]);
                    propertyColumnObjects[jsonObject[property][i]].style.backgroundColor = "#ff3333";
                }
            }
        }

        isAnomaliesExist = true;
    }

    function clearAnomalies()
    {
        for(let i = 0; i < anomaliesCellsObjects.length; ++i)
        {
            anomaliesCellsObjects.pop().style.backgroundColor = "white";
        }

        isAnomaliesExist = false;
    }

    function setListOfProperties(jsonString)
    {
        const jsonObject = JSON.parse(jsonString);
        const listObject = document.getElementById("headers-list");
        
        if(isPropertyListExist)
        {
            clearListOfProperties();
        }

        for(property in jsonObject)
        {
            let newButton = document.createElement("button");
            newButton.type = "button";
            newButton.className = "list-group-item list-group-item-action";
            newButton.textContent = property;
            newButton.onclick = function() {propertyListClick(this);};
            listObject.appendChild(newButton);
        }

        isPropertyListExist = true;
    }

    function clearListOfProperties()
    {
        const listObject = document.getElementById("headers-list");
        while (listObject.firstChild) {
            listObject.removeChild(listObject.lastChild);
        }

        isPropertyListExist = false;
    }

    function propertyListClick(element)
    {
        if(activeListElement != undefined)
        {
            activeListElement.className = "list-group-item list-group-item-action";
        }
        element.className = "list-group-item list-group-item-action active";
        activeListElement = element;
    }

    function submit() {
        handleFile(CSVFile);
    }