
// ============================在前端实现筛选后表单导出==============================

document.addEventListener('DOMContentLoaded', function(event) {
  // 绑定导出按钮点击事件
  document.getElementById("export-btn").addEventListener('click', function() {
      event.preventDefault();
      exportAllPagesToCSV();
  });
});


function exportAllPagesToCSV() {
  var currentPage = parseInt(document.querySelector('.button span').innerText.match(/\d+/g)[1]);
  var totalPages = parseInt(document.querySelector('.button span').innerText.match(/\d+/g)[2]);
  var csvContent = "\ufeff";
  var headers = [];

  // 递归函数，用于遍历所有分页并收集数据
  function processPage(pageNumber) {
      // 构建分页URL
      var url = new URL(window.location.href);
      url.searchParams.set('page', pageNumber);

      // 发起请求获取当前页的数据
      fetch(url.toString())
          .then(response => response.text())
          .then(data => {
              var parser = new DOMParser();
              var doc = parser.parseFromString(data, "text/html");
              var rows = doc.querySelectorAll('table tr');

              // 获取表头
              if (pageNumber === 1) {
                  var tableHeaders = rows[0].querySelectorAll('th');
                  headers = Array.from(tableHeaders).slice(0, -1).map(th => th.innerText);
                  csvContent += headers.join(",") + "\r\n";
              }

              // 获取并处理表体数据
              for (var i = 1; i < rows.length; i++) {
                  var cols = rows[i].querySelectorAll('td');
                  var rowData = Array.from(cols).slice(0, -1).map(td => td.innerText.replace(/,/g, ''));
                  csvContent += rowData.join(",") + "\r\n";
              }

              // 如果不是最后一页，递归处理下一页
              if (pageNumber < totalPages) {
                  processPage(pageNumber + 1);
              } else {
                  // 所有页面处理完毕，导出CSV
                  downloadCSV(csvContent, 'filtered_form.csv');
              }
          })
          .catch(error => console.error('Error fetching page:', error));
  }

  // 从第一页开始处理
  processPage(1);
}

function downloadCSV(csvContent, filename) {
  var encodedUri = "data:text/csv;charset=utf-8," + encodeURIComponent(csvContent);
  var link = document.createElement('a');
  link.setAttribute('href', encodedUri);
  link.setAttribute('download', filename);
  document.body.appendChild(link); // Required for FF
  link.click();
  document.body.removeChild(link);
}


// document.addEventListener("DOMContentLoaded", function () {
//   // 添加导出按钮点击事件
//   document
//     .getElementById("export-btn")
//     .addEventListener("click", function (event) {
//       event.preventDefault(); // 阻止链接默认行为
//       // 获取表格内容
//       var table = document.querySelector("table");
//       var rows = table.querySelectorAll("tbody tr");
//       // 创建一个字符串，用于构建CSV内容
//       var csvContent = "\ufeff"; // 添加BOM以表示utf-8-sig编码

//       // 添加表头
//       var headers = table.querySelectorAll("thead th");
//       var headerRow = Array.from(headers)
//         .map(function (th, index) {
//           // 跳过最后一个表头
//           if (index < headers.length - 1) {
//             return th.innerText;
//           }
//         })
//         .filter(function (header) {
//           // 过滤掉未定义的项
//           return header !== undefined;
//         })
//         .join(",");
//       csvContent += headerRow + "\r\n";

//       // 添加表体
//       Array.from(rows).forEach(function (row) {
//         var rowData = Array.from(row.querySelectorAll("td"))
//           .map(function (td, index, array) {
//             // 跳过最后一个单元格
//             if (index < array.length - 1) {
//               return td.innerText.replace(/,/g, "，"); // 替换掉可能存在的逗号
//             }
//           })
//           .filter(function (cell) {
//             // 过滤掉未定义的项
//             return cell !== undefined;
//           })
//           .join(",");
//         csvContent += rowData + "\r\n";
//       });

//       // 创建隐藏的链接，并模拟点击以下载文件
//       var encodedUri =
//         "data:text/csv;charset=utf-8," + encodeURIComponent(csvContent);
//       var link = document.createElement("a");
//       link.setAttribute("href", encodedUri);
//       link.setAttribute("download", "filtered_form.csv");
//       document.body.appendChild(link); // required for Firefox
//       link.click();
//       document.body.removeChild(link); // required for Firefox
//     });
// });


