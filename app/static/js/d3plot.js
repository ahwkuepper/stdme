var width = window.innerWidth*0.9,
    height = width/960*450;

var rateById = d3.map();

var quantize = d3.scale.quantize()
    .domain([0, 1000])
    .range(d3.range(9).map(function(i) { return "q" + i + "-9"; }));

var projection = d3.geo.albersUsa()
    .scale(width*1.0)
    .translate([width / 2, height / 2]);

var path = d3.geo.path()
    .projection(projection);

var svg = d3.select("#d3plot").append("svg")
    .attr("width", width)
    .attr("height", height);

queue()
    .defer(d3.json, "../static/js/us.json")
    .defer(d3.tsv, "../static/js/chlamydia.tsv", function(d) { rateById.set(d.id, +d.rate); })
    .await(ready);

function ready(error, us) {
  if (error) throw error;
  d3.select(window).on("resize", resize);

  svg.append("g")
      .attr("class", "counties")
    .selectAll("path")
      .data(topojson.feature(us, us.objects.counties).features)
    .enter().append("path")
      .attr("class", function(d) { return quantize(rateById.get(d.id)); })
      .attr("d", path);

  svg.append("path")
      .datum(topojson.mesh(us, us.objects.states, function(a, b) { return a !== b; }))
      .attr("class", "states")
      .attr("d", path);

  window.addEventListener('resize', resize); 

  function resize() {
    width = window.innerWidth*0.9, height = width/960*450;
    svg.attr("width", width).attr("height", height);
    force.size([width, height]).resume();
  }

}

d3.select(self.frameElement).style("height", height + "px");