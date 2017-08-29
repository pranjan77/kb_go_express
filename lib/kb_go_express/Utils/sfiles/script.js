$(document).ready(function () {
    $('#example').DataTable({

        dom: 'Bltrip',
				buttons: [
            {
                extend: 'excelHtml5',
                title: 'Data export'
            },
            {
                extend: 'csvHtml5',
                title: 'Data export'
            }
        ],
        initComplete: function () {
            this.api().columns().every(function () {
                var column = this;
                if (column.index() == 0) {
                    input = $('<input type="text" />').appendTo($(column.header())).on('keyup change', function () {
                        if (column.search() !== this.value) {
                            column.search(this.value)
                                .draw();
                        }
                    });
                    return;
                }
                if (column.index() == 1) {
                    input = $('<input type="text" />').appendTo($(column.header())).on('keyup change', function () {
                        if (column.search() !== this.value) {
                            column.search(this.value)
                                .draw();
                        }
                    });
                    return;
                }

                if (column.index() == 2) {

                    return;
                }
                if (column.index() == 6) {
                    return;
                }


                var select = $('<select><option value=""></option></select>')
                    .appendTo($("#filters").find("th").eq(column.index()))
                    .on('change', function () {
                    var val = $.fn.dataTable.util.escapeRegex(
                    $(this).val());                                     

                    column.search(val ? '^' + val + '$' : '', true, false)
                        .draw();
                });
                
                console.log(select);

                column.data().unique().sort().each(function (d, j) {
                    select.append('<option value="' + d + '">' + d + '</option>')
                });
            });
        }
    });

    console.log()
});
