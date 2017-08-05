$(function(){
    var config = {
        sortList: [[STARTING_SORT, 0]],
        headers: {}, // per dopo
        widgets: [ 'zebra', 'stickyHeaders'],
        theme: THEME,
        widgetOptions: {
          stickyHeaders_attachTo      : $('.header-container'),
        }
    }
    config.headers[DONTSORT] = {sorter: false};
    $("#bggdata").tablesorter(config);
});
