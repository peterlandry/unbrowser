var page = new WebPage(),
    address, output, size;

if (phantom.args.length < 4 || phantom.args.length > 5) {
    console.log('Usage: rasterize.js URL filename viewport_width viewport_height {render_delay_in_ms }');
    phantom.exit();
} else {
    address = phantom.args[0];
    output = phantom.args[1];
    width = phantom.args[2];
    height = phantom.args[3];
    render_delay = phantom.args[4] || 1000;
    page.viewportSize = { width: width, height: height };
    page.open(address, function (status) {
        if (status !== 'success') {
            console.log('Unable to load the address!');
        } else {
            window.setTimeout(function () {
                page.render(output);
                phantom.exit();
            }, render_delay);
        }
    });
}
