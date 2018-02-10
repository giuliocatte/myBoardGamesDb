$(function(){
    var config = {
        sortList: [[STARTING_SORT, 0]],
        headers: {}, // per dopo
        widgets: [ 'zebra', 'stickyHeaders'],
        theme: THEME,
        headerTemplate : '{content} {icon}', // necessario per gli sticky headers
        widgetOptions: {
          stickyHeaders_attachTo  : $('#headerwrapper'),
          stickyHeaders_zIndex    : 2,
        }
    }
    config.headers[DONTSORT] = {sorter: false};
    $("#bggdata").tablesorter(config);
});
