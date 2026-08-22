(function () {
  var table = document.getElementById('benchmark-table');
  if (!table) return;
  var ascending = {};
  table.querySelectorAll('button[data-col]').forEach(function (button) {
    button.addEventListener('click', function () {
      var column = Number(button.dataset.col);
      ascending[column] = !ascending[column];
      var rows = Array.from(table.tBodies[0].rows);
      rows.sort(function (a, b) {
        var left = a.cells[column].textContent.trim().replace(/[#,]/g, '');
        var right = b.cells[column].textContent.trim().replace(/[#,]/g, '');
        var leftNumber = Number.parseFloat(left);
        var rightNumber = Number.parseFloat(right);
        var result = Number.isNaN(leftNumber) || Number.isNaN(rightNumber)
          ? left.localeCompare(right)
          : leftNumber - rightNumber;
        return ascending[column] ? result : -result;
      });
      rows.forEach(function (row) { table.tBodies[0].appendChild(row); });
      table.querySelectorAll('th button').forEach(function (b) { b.removeAttribute('aria-sort'); });
      button.setAttribute('aria-sort', ascending[column] ? 'ascending' : 'descending');
    });
  });
})();
