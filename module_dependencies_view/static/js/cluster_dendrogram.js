

// var cluster = d3.layout.cluster()
//     .size([360, radius - 120]);

// var diagonal = d3.svg.diagonal.radial()
//     .projection(function(d) { return [d.y, d.x / 180 * Math.PI]; });

// var svg = d3.select("body").append("svg")
//     .attr("width", radius * 2)
//     .attr("height", radius * 2)
//   .append("g")
//     .attr("transform", "translate(" + radius + "," + radius + ")");

// d3.json('/module/dendrogram/'+identifier, function(error, root) {
//   if (error) throw error;

//   var nodes = cluster.nodes(root);

//   var link = svg.selectAll("path.link")
//       .data(cluster.links(nodes))
//     .enter().append("path")
//       .attr("class", "link")
//       .attr("d", diagonal);

//   var node = svg.selectAll("g.node")
//       .data(nodes)
//     .enter().append("g")
//       .attr("class", "node")
//       .attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + d.y + ")"; })

//   node.append("circle")
//       .attr("r", 4.5);

//   node.append("text")
//       .attr("dy", ".31em")
//       .attr("text-anchor", function(d) { return d.x < 180 ? "start" : "end"; })
//       .attr("transform", function(d) { return d.x < 180 ? "translate(8)" : "rotate(180)translate(-8)"; })
//       .text(function(d) { return d.name; });
// });

// d3.select(self.frameElement).style("height", radius * 2 + "px");
var identifier = $('#tree').data('id'),
    width = 1900,
    height = 10000;

var cluster = d3.layout.cluster()
    .size([height, width - 160]);

var diagonal = d3.svg.diagonal()
    .projection(function(d) { return [d.y, d.x]; });

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height)
  .append("g")
    .attr("transform", "translate(40,0)");

d3.json('/module/dendrogram/'+identifier, function(error, root) {
  if (error) throw error;

  var nodes = cluster.nodes(root),
      links = cluster.links(nodes);

  var link = svg.selectAll(".link")
      .data(links)
    .enter().append("path")
      .attr("class", "link")
      .attr("d", diagonal);

  var node = svg.selectAll(".node")
      .data(nodes)
    .enter().append("g")
      .attr("class", "node")
      .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; })

  node.append("circle")
      .attr("r", 4.5);

  node.append("text")
      .attr("dx", function(d) { return d.children ? -8 : 8; })
      .attr("dy", 3)
      .style("text-anchor", function(d) { return d.children ? "end" : "start"; })
      .text(function(d) { return d.name; });
});

d3.select(self.frameElement).style("height", height + "px");
