/**
 * Modal Logic Playground -- application code
 *
 * Dependencies: D3, MathJax, MPL
 *
 * Copyright (c) 2013 Ross Kirsling
 * Released under the MIT License.
 */


var chronicle = new Chronicle();

// set up initial nodes and links (edges) of graph, based on MPL model
var lastNodeId = -1,
    nodes = [],
    links = [];

// set up SVG for D3
var width  = 440,
    height = 740,
    colors = d3.scale.category10();

var svg = d3.select('#app-body .graph')
  .append('svg')
  .on('contextmenu', function() { d3.event.preventDefault(); })
  .attr('width', width)
  .attr('height', height);

// init D3 force layout
var force = d3.layout.force()
    .nodes(nodes)
    .links(links)
    .size([width, height])
    .linkDistance(150)
    .charge(-500)
    .on('tick', tick);

// define arrow markers for graph links
svg.append('svg:defs').append('svg:marker')
    .attr('id', 'end-arrow')
    .attr('viewBox', '0 -5 10 10')
    .attr('refX', 6)
    .attr('markerWidth', 3)
    .attr('markerHeight', 3)
    .attr('orient', 'auto')
  .append('svg:path')
    .attr('d', 'M0,-5L10,0L0,5')
    .attr('fill', '#000');

svg.append('svg:defs').append('svg:marker')
    .attr('id', 'start-arrow')
    .attr('viewBox', '0 -5 10 10')
    .attr('refX', 4)
    .attr('markerWidth', 3)
    .attr('markerHeight', 3)
    .attr('orient', 'auto')
  .append('svg:path')
    .attr('d', 'M10,-5L0,0L10,5')
    .attr('fill', '#000');

// line displayed when dragging new nodes

var drag_line = svg.append('svg:path')
  .attr('class', 'link dragline hidden')
  .attr('d', 'M0,0L0,0');


// handles to link and node element groups
var path = svg.append('svg:g').selectAll('path'),
    circle = svg.append('svg:g').selectAll('g'),
    label = svg.append('svg:g').selectAll('text');


// mouse event vars
var selected_node = null,
    selected_link = null,
    mousedown_link = null,
    mousedown_node = null,
    mouseup_node = null;

function resetMouseVars() {
  mousedown_node = null;
  mouseup_node = null;
  mousedown_link = null;
}

// handles for 'Link to Model' dialog
var backdrop = d3.select('.modal-backdrop'),
    linkDialog = d3.select('#link-dialog'),
    linkInputElem = linkDialog.select('input').node();

// handles for dynamic content in panel
var selectedNodeLabel = d3.select('#edit-pane .selected-node-id');
var varLabelInput = d3.select("#edit-pane input.nodelabel"),
    varLabelInputButton = d3.select("#nodelabelbtn"),
    varTransitionUpperInput = d3.select("#edit-pane input.transupper"),
    varTransitionLowerInput = d3.select("#edit-pane input.translower"),
    varTransitionButton = d3.select("#transbtn");


// get string label
function makeAssignmentString(node) {
  return node.vals.join(', ');
}

// set selected node and notify panel of changes
function setSelectedNode(node) {
  selected_node = node;

  // update selected node label
  selectedNodeLabel.html(selected_node ? '<strong>State '+selected_node.id+'</strong>' : 'No state selected');

  // update variable table
  if(selected_node) {
    varLabelInput.attr("style","");
    document.getElementById("nodelabel").value =makeAssignmentString(selected_node);
    
    d3.select(window) // disable keydown/keyup message catching to enable input to work
      .on('keydown', null)
      .on('keyup', null);
    varLabelInputButton.classed('inactive', false);
  } else {
    varLabelInput.attr("style","display:none;");
    varLabelInput.attr("value",""); // clean input
    if( !selected_link) {
        d3.select(window)// enable keydown/keyup message catching to reactivate standard interaction patterns
          .on('keydown', keydown)
          .on('keyup', keyup);
    }
    varLabelInputButton.classed('inactive', true);
  }
  
}

function setLabelForSelectedNode() {
    if(selected_node) {
        newlabels=document.getElementById("nodelabel").value;
        selected_node.vals.splice(0,selected_node.vals.length); //clear le labels
        selected_node.vals.push(newlabels); // add a new one
        chronicle.editState(selected_node.id, newlabels); //update the model
        viewChronicleJson();
        circle.selectAll('text:not(.id)').text(makeAssignmentString);
    }
    //restart();
}



// set selected node and notify panel of changes
function setSelectedLink(link) {
  selected_link = link;

  // update selected node label
  selectedNodeLabel.html(selected_link ? '<strong>Transition '+selected_link.source.id+"->"+selected_link.target.id+'</strong>' : 'No state selected');

  // update variable table
  if(selected_link) {
    varTransitionUpperInput.attr("style","");
    document.getElementById("transupper").value = selected_link.u;
    varTransitionLowerInput.attr("style","");
    document.getElementById("translower").value = selected_link.l;
    
    d3.select(window) // disable keydown/keyup message catching to enable input to work
      .on('keydown', null)
      .on('keyup', null);
    varTransitionButton.classed('inactive', false);
  } else {
    varTransitionUpperInput.attr("style","display:none;");
    varTransitionLowerInput.attr("style","display:none;");
    varTransitionButton.classed('inactive', true);
    if( !selected_node) {
        d3.select(window)// enable keydown/keyup message catching to reactivate standard interaction patterns
          .on('keydown', keydown)
          .on('keyup', keyup);
    }
  }
}

function setBoundForSelectedLink() {
    if(selected_link) {
        selected_link.l= document.getElementById("translower").value;
        selected_link.u= document.getElementById("transupper").value;
        chronicle.addTransition(selected_link.source.id, selected_link.target.id, selected_link.l, selected_link.u);//update the model
        viewChronicleJson();
        label.text(function(d) {
            if( selected_link.target===d.target && selected_link.source===d.source ) {
                return "["+selected_link.l+","+selected_link.u+"]";
            } else {
                return "["+d.l+","+d.u+"]";
            }
        });
    }
}

// update force layout (called automatically each iteration)
function tick() {
  // draw directed edges with proper padding from node centers
  path.attr('d', function(d) {
    var deltaX = d.target.x - d.source.x,
        deltaY = d.target.y - d.source.y,
        dist = Math.sqrt(deltaX * deltaX + deltaY * deltaY),
        normX = deltaX / dist,
        normY = deltaY / dist,
        sourcePadding = d.left ? 17 : 12,
        targetPadding = d.right ? 17 : 12,
        sourceX = d.source.x + (sourcePadding * normX),
        sourceY = d.source.y + (sourcePadding * normY),
        targetX = d.target.x - (targetPadding * normX),
        targetY = d.target.y - (targetPadding * normY);
    return 'M' + sourceX + ',' + sourceY + 'L' + targetX + ',' + targetY;
  });

  circle.attr('transform', function(d) {
    return 'translate(' + d.x + ',' + d.y + ')';
  });
  
  label
    .attr('x', function(d) {
        return (d.target.x + d.source.x)/2;
    })
    .attr('y', function(d) {
        return (d.target.y + d.source.y)/2;
    })
}

// update graph (called when needed)
function restart() {
  // path (link) group
  path = path.data(links);

  // update existing links
  path.classed('selected', function(d) { return d === selected_link; })
    .style('marker-start', function(d) { return d.left ? 'url(#start-arrow)' : ''; })
    .style('marker-end', function(d) { return d.right ? 'url(#end-arrow)' : ''; });
            
  path.enter().append('svg:path')
    .attr('class', 'link')
    .attr('id',function (d,i) { return "path_" + i; })
    .classed('selected', function(d) { return d === selected_link; })
    .style('marker-start', function(d) { return d.left ? 'url(#start-arrow)' : ''; })
    .style('marker-end', function(d) { return d.right ? 'url(#end-arrow)' : ''; })
    .on('mousedown', function(d) {
      if(d3.event.ctrlKey) return;

      // select link
      mousedown_link = d;
      if(mousedown_link === selected_link) selected_link = null;
      else selected_link = mousedown_link;
      setSelectedNode(null);
      setSelectedLink(d);
      restart();
    })

  // remove old links
  path.exit().remove();
  
  label = label.data(links);
  label.enter().append("text")
        .attr("dx",0)
        .attr("dy",0)
        .text(function(d){return "["+d.l+","+d.u+"]"})
        .on('mousedown', function(d) {
          if(d3.event.ctrlKey) return;

          // select link
          mousedown_link = d;
          if(mousedown_link === selected_link) selected_link = null;
          else selected_link = mousedown_link;
          setSelectedNode(null);
          setSelectedLink(d);
          restart();
        });
  label.exit().remove();
  
  
  // circle (node) group
  // NB: the function arg is crucial here! nodes are known by id, not by index!
  circle = circle.data(nodes, function(d) { return d.id; });

  // update existing nodes (selected visual states)
  circle.selectAll('circle')
    .style('fill', function(d) { return (d === selected_node) ? d3.rgb(colors(d.id)).brighter().toString() : colors(d.id); });

  // add new nodes
  var g = circle.enter().append('svg:g');

  g.append('svg:circle')
    .attr('class', 'node')
    .attr('r', 12)
    .style('fill', function(d) { return (d === selected_node) ? d3.rgb(colors(d.id)).brighter().toString() : colors(d.id); })
    .style('stroke', function(d) { return d3.rgb(colors(d.id)).darker().toString(); })
    .on('mouseover', function(d) {
      if(!mousedown_node || d === mousedown_node) return;
      // enlarge target node
      d3.select(this).attr('transform', 'scale(1.1)');
    })
    .on('mouseout', function(d) {
      if(!mousedown_node || d === mousedown_node) return;
      // unenlarge target node
      d3.select(this).attr('transform', '');
    })
    .on('mousedown', function(d) {
      if(d3.event.ctrlKey) return;

      // select node
      mousedown_node = d;
      if(mousedown_node === selected_node) setSelectedNode(null);
      else { 
        setSelectedNode(mousedown_node);
        setSelectedLink(null);
      }
      selected_link = null;

      // reposition drag line
      drag_line
        .style('marker-end', 'url(#end-arrow)')
        .classed('hidden', false)
        .attr('d', 'M' + mousedown_node.x + ',' + mousedown_node.y + 'L' + mousedown_node.x + ',' + mousedown_node.y);

      restart();
    })
    .on('mouseup', function(d) {
      if(!mousedown_node) return;

      // needed by FF
      drag_line
        .classed('hidden', true)
        .style('marker-end', '');

      // check for drag-to-self
      mouseup_node = d;
      if(mouseup_node === mousedown_node) { resetMouseVars(); return; }

      // unenlarge target node
      d3.select(this).attr('transform', '');


      // add link to graph (update if exists)
      // note: links are strictly source < target; arrows separately specified by booleans
      var source, target, direction;
      if(mousedown_node.id < mouseup_node.id) {
        source = mousedown_node;
        target = mouseup_node;
        direction = 'right';
      } else {
        source = mouseup_node;
        target = mousedown_node;
        direction = 'left';
      }

      // add transition to model
      chronicle.addTransition(mousedown_node.id, mouseup_node.id,0,0);
      viewChronicleJson();
      
      var link = links.filter(function(l) {
        return (l.source === source && l.target === target);
      })[0];

      if(!link) {
        if (direction === 'right') {
            link = {source: source, target: target, left: false, right: true, l:0, u:0};
        } else {
            link = {source: target, target: source, left: false, right: true, l:0, u:0};
        }
        links.push(link);
      }

      // select new link
      selected_link = link;
      setSelectedNode(null);
      restart();
    });

  // show node IDs
  g.append('svg:text')
      .attr('x', 0)
      .attr('y', 4)
      .attr('class', 'id')
      .text(function(d) { return d.id; });

  // text shadow
  g.append('svg:text')
      .attr('x', 16)
      .attr('y', 4)
      .attr('class', 'shadow')
      .text(makeAssignmentString);

  // text foreground
  g.append('svg:text')
      .attr('x', 16)
      .attr('y', 4)
      .text(makeAssignmentString);

  // remove old nodes
  circle.exit().remove();

  // set the graph in motion
  force.start();
}

function mousedown() {
  // prevent I-bar on drag
  d3.event.preventDefault();

  // because :active only works in WebKit?
  svg.classed('active', true);

  if(d3.event.ctrlKey || mousedown_node || mousedown_link) return;

  // insert new node at point
  var point = d3.mouse(this),
      node = {id: ++lastNodeId, vals: ['a']};
  node.x = point[0];
  node.y = point[1];
  nodes.push(node);

  // add state to model
  chronicle.addState('a');
  viewChronicleJson();
  restart();
}

function mousemove() {
  if(!mousedown_node) return;

  // update drag line
  drag_line.attr('d', 'M' + mousedown_node.x + ',' + mousedown_node.y + 'L' + d3.mouse(this)[0] + ',' + d3.mouse(this)[1]);

  restart();
}

function mouseup() {
  if(mousedown_node) {
    // hide drag line
    drag_line
      .classed('hidden', true)
      .style('marker-end', '');
  }

  // because :active only works in WebKit?
  svg.classed('active', false);

  // clear mouse event vars
  resetMouseVars();
}


function removeLinkFromModel(link) {
  var sourceId = link.source.id,
      targetId = link.target.id;

  // remove leftward transition
  if(link.left) chronicle.removeTransition(targetId, sourceId);

  // remove rightward transition
  if(link.right) chronicle.removeTransition(sourceId, targetId);
  viewChronicleJson();
}

function spliceLinksForNode(node) {
  var toSplice = links.filter(function(l) {
    return (l.source === node || l.target === node);
  });
  toSplice.map(function(l) {
    links.splice(links.indexOf(l), 1);
  });
}

// only respond once per keydown
var lastKeyDown = -1;


function keydown() {
  d3.event.preventDefault();

  if(lastKeyDown !== -1) return;
  lastKeyDown = d3.event.keyCode;

  // ctrl
  if(d3.event.keyCode === 17) {
    circle.call(force.drag);
    svg.classed('ctrl', true);
    return;
  }

  if(!selected_node && !selected_link) return;
  switch(d3.event.keyCode) {
    case 8: // backspace
    case 46: // delete
      if(selected_node) {
        //model.removeState(selected_node.id);
        nodes.splice(nodes.indexOf(selected_node), 1);
        spliceLinksForNode(selected_node);
      } else if(selected_link) {
        //removeLinkFromModel(selected_link);
        links.splice(links.indexOf(selected_link), 1);
      }
      selected_link = null;
      setSelectedNode(null);
      restart();
      break;
    case 66: // B
      if(selected_link) {
        var sourceId = selected_link.source.id,
            targetId = selected_link.target.id;
        // set link direction to both left and right
        if(!selected_link.left) {
          selected_link.left = true;
          //model.addTransition(targetId, sourceId);
        }
        if(!selected_link.right) {
          selected_link.right = true;
          //model.addTransition(sourceId, targetId);
        }
      }
      restart();
      break;
    case 76: // L
      if(selected_link) {
        var sourceId = selected_link.source.id,
            targetId = selected_link.target.id;
        // set link direction to left only
        if(!selected_link.left) {
          selected_link.left = true;
          //model.addTransition(targetId, sourceId);
        }
        if(selected_link.right) {
          selected_link.right = false;
          //model.removeTransition(sourceId, targetId);
        }
      }
      restart();
      break;
  }
}

function keyup() {
  lastKeyDown = -1;

  // ctrl
  if(d3.event.keyCode === 17) {
    // "uncall" force.drag
    // see: https://groups.google.com/forum/?fromgroups=#!topic/d3-js/-HcNN1deSow
    circle
      .on('mousedown.drag', null)
      .on('touchstart.drag', null);
    svg.classed('ctrl', false);
  }
}

// handles to mode select buttons and left-hand panel
var modeButtons = d3.selectAll('#mode-select button'),
    panes = d3.selectAll('#app-body .panel .tab-pane');

function setAppMode() {

    // enable listeners
    svg.classed('edit', true)
      .on('mousedown', mousedown)
      .on('mousemove', mousemove)
      .on('mouseup', mouseup);
    d3.select(window)
      .on('keydown', keydown)
      .on('keyup', keyup);

    // remove eval classes
    circle
      .classed('waiting', false)
      .classed('true', false)
      .classed('false', false);

  restart();
};

function viewChronicleJson() {
    cljson=chronicle.toJson();
    //console.log(cljson);
    charea = document.getElementById("chronicle");
    //charea = d3.selectAll('#chronicle');
    charea.innerHTML = cljson;
    charea.innerText = cljson;
};

function loadChronicle() {
    jsonstr=document.getElementById("chronicle").value;
    clearChronicle();
    
    console.log("loadChronicle: " + document.getElementById("chronicle").value);
    chronicle.loadFromJson( jsonstr );
    //console.log("loadChronicle after: " + chronicle.toJson() );
    
    //Update the graphical representation from the chronicle model
    console.log("load states ");
    // --> nodes setup
    var states = chronicle.getStates();
    states.forEach(function(state) {
        // state is a list of labels
        var node = {id: ++lastNodeId, vals: state};
        nodes.push(node);
    });
    
    console.log("loaded states:" + nodes);

    // --> links setup
    nodes.forEach(function(source) {
        var sourceId = source.id,
            successors = chronicle.getSuccessorsOf(sourceId);

        successors.forEach(function(transition) {
            console.log(transition);
            //if(sourceId === transition._dest) return; //Abnormal case

            //var target = nodes.filter(function(node) { return node.id === transition._dest; })[0];

            links.push({source: source.id, target: transition._dest, left: false, right: true, l:transition._l, u:transition._u });
        });
    });
    console.log("links: "+links);
    
    console.log("restart ");
    restart();
    viewChronicleJson();
};

function clearChronicle() {
    console.log("clearChronicle");
    links.splice(0,links.length);
    nodes.splice(0,nodes.length);
    lastNodeId=-1;
    
    setSelectedNode(null);
    setSelectedLink(null);
    restart();
    chronicle.clear();
    viewChronicleJson();
}

    
// app starts here
setAppMode();
