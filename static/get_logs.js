loglines = 0

function loadLog(){
    $.getJSON("/api/log",
    function(data) {
        line_count = data.line_count

        log_output = ""
        for (log_line in data.log_lines) {
            if (log_line > (line_count - 21)) {
                log_output = log_output.concat(data.log_lines[log_line] + "<br>");
            }
        }

        $('#log').html(
            log_output
        );
    });
}
setInterval(loadLog, 1000);