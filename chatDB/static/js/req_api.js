function connectionDB(value) {
    const url = "/connection_db";
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(value)
    })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error(error));
}

function executeSql(value) {
    const url = "/execute_sql?sql=" + value;
    fetch(url, {
        method: "GET",
        headers: {},
    })
        .then(response => response.json())
        .then(data => {
            const dataTable = document.getElementById("data-table");
            const headerRow = document.createElement("tr");

            for (const key in data.data) {
                const v = data.data[key]
                for (const field in v) {
                    const fieldNameCell = document.createElement("th");
                    fieldNameCell.textContent = field;
                    headerRow.appendChild(fieldNameCell);
                }
                dataTable.appendChild(headerRow)
            }


            for (const key in data.data) {
                const v = data.data[key]
                const headerRow1 = document.createElement("tr");
                for (const field in v) {
                    const fieldValueCell = document.createElement("td");
                    fieldValueCell.textContent = v[field];
                    fieldValueCell.setAttribute("class", "truncate")
                    headerRow1.appendChild(fieldValueCell);
                }
                dataTable.appendChild(headerRow1)
            }

        })
        .catch(error => console.error(error));
}

function getTables(element) {
    var index = changeColor(element)

    const url = "/get_tables";

    fetch(url, {
        method: "GET",
        headers: {}
    })
        .then(response => response.json())
        .then(data => {
                var targetDiv = document.querySelectorAll(".menuBox___ryfVe")[index];
                for (const key in data.data) {
                    const v = data.data[key]
                    var existingElements = targetDiv.querySelectorAll(".li___name");
                    var innerHTMLArray = Array.from(existingElements).map(function (element) {
                        return element.innerHTML;
                    });
                    var isExs = innerHTMLArray.includes(v.name)
                    if (!isExs) {
                        var newElement = document.createElement("li");
                        newElement.setAttribute("class", "li___name");
                        newElement.setAttribute("title", v);
                        // newElement.setAttribute("onClick", "connectionDB(" + jsonData + ")");
                        newElement.setAttribute("oncontextmenu", "showDropdown(event)");
                        newElement.innerHTML = v;
                        targetDiv.appendChild(newElement);
                    }
                }
            }
        )
        .catch(error => console.error(error));
}

function getConf(element) {

    var index = changeColor(element)

    const url = "/get_database_conf";

    fetch(url, {
        method: "GET",
        headers: {}
    })
        .then(response => response.json())
        .then(data => {
                var targetDiv = document.querySelectorAll(".menuBox___ryfVe")[index];
                for (const key in data.data.conn_all) {
                    if (data.data.conn_all.hasOwnProperty(key)) {
                        const value = data.data.conn_all[key]; // 使用中括号进行访问
                        var jsonData = JSON.stringify(value); // 将数据转换为 JSON 字符串
                        for (const k in value) {
                            const v = value[k]
                            if (v.name) {
                                var existingElements = targetDiv.querySelectorAll(".li___name");
                                var innerHTMLArray = Array.from(existingElements).map(function (element) {
                                    return element.innerHTML;
                                });
                                var isExs = innerHTMLArray.includes(v.name)
                                if (!isExs) {
                                    var newElement = document.createElement("li");
                                    newElement.setAttribute("class", "li___name");
                                    newElement.setAttribute("onClick", "connectionDB(" + jsonData + ")");
                                    newElement.innerHTML = v.name;
                                    targetDiv.appendChild(newElement);
                                }
                            }
                        }
                    }
                }
            }
        )
        .catch(error => console.error(error));
}

function changeColor(element) {
    // 重置所有brandLogo___uAMRL1 div的样式为原始状态
    var divs = document.querySelectorAll('.brandLogo___uAMRL1');
    divs.forEach(function (div) {
        div.classList.remove('selected');
    });

    // 给被点击的brandLogo___uAMRL1 div添加选中样式
    element.classList.add('selected');

    // 获取被点击的brandLogo___uAMRL1 div的索引
    var index = Array.from(divs).indexOf(element);

    // 重置所有componentBox___XjmnM div的样式为原始状态
    var componentBoxes = document.querySelectorAll('.componentBox___XjmnM');
    componentBoxes.forEach(function (box) {
        if (box === componentBoxes[index]) {
            box.removeAttribute("style")
        } else {
            box.setAttribute("style", "display: none;")
        }
    });
    return index
}


// function showDropdown(event) {
//     // 创建下拉框元素
//     var dropdown = document.createElement('div');
//     dropdown.innerHTML = '这是一个下拉框';
//
//     // 设置下拉框的位置
//     dropdown.style.position = 'absolute';
//     dropdown.style.left = event.clientX + 'px';
//     dropdown.style.top = event.clientY + 'px';
//
//     // 添加下拉框到文档中
//     document.body.appendChild(dropdown);
//
//     var currentDropdown = null; // 当前打开的下拉框
//
//         function showDropdown(event) {
//             event.preventDefault(); // 防止默认右键菜单显示
//
//             hideDropdown(); // 隐藏旧的下拉框
//
//             var li = event.target; // 获取当前点击的li元素
//             var dropdownMenu = li.querySelector('.dropdown-menu'); // 获取下拉框元素
//
//             dropdownMenu.style.display = 'block'; // 显示下拉框
//             currentDropdown = dropdownMenu; // 将当前下拉框设置为打开状态
//         }
//
//         function hideDropdown() {
//             if (currentDropdown !== null) {
//                 currentDropdown.style.display = 'none'; // 隐藏旧的下拉框
//                 currentDropdown = null; // 清空当前下拉框
//             }
//         }
//
//         document.addEventListener('click', function(event) {
//             var isClickInside = document.getElementsByClassName('li___name').contains(event.target);
//
//             if (!isClickInside) {
//                 hideDropdown(); // 点击页面其他地方时隐藏下拉框
//             }
//         });
// }


function getSelectedText() {
    var textarea = document.getElementById("myTextarea");
    var selectedText = textarea.value.substring(textarea.selectionStart, textarea.selectionEnd);
    if (selectedText.trim() === "") {
        selectedText = textarea.value;
    }
    executeSql(selectedText)
}