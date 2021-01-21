/**
 * Chronicle v0.0.1
 *
 * A library for representing chronicles
 *
 * Author: Thomas Guyet
 * 
 * Inspired by Ross Kirsling (http://github.com/rkirsling/modallogic)
 * Released under the MIT License.
 */

function Transition() {
  //
  var _dest = 0;  // destination state
  var _l = 0;     // lower bound
  var _u = 0;     // upper bound
}

/**
 * Constructor for Chronicle. Takes no initial input.
 * @constructor
 */
function Chronicle() {
  // Array of states of a chronicle.
  // Each state is an object with two properties:
  // - labels: a disjunction of labels
  // - successors: an array of transitions
  // ex: [{labels: ['a'], successors: [ {'b', _u, _l} ]},
  //      {labels: ['b'], successors: []   }]
  var _states = [];

  /**
   * Adds a transition to the model, given source and target state indices.
   */
  this.addTransition = function (source, target, u, l) {
    if (!_states[source] || !_states[target]) return;
    if ( source===target ) return;

    var successors = _states[source].successors,
        len = successors.length;
    var index = 0;
    for (; index < len; index++) {
      if (successors[index]._dest === target) { // update the current transition
          successors[index]._u=u;
          successors[index]._l=l;
          break;
      }
    }	

    if (index === len) {
      var t = new Transition();
      t._dest = target;
      t._u=u;
      t._l=l;
      successors.push( t );
    }
  };

  /**
   * Removes a transition from the model, given source and target state indices.
   */
  this.removeTransition = function (source, target) {
    if (!_states[source]) return;

    var successors = _states[source].successors,
        len = successors.length;
    var index = 0;
    for (; index < len; index++) {
      if (successors[index]._dest === target) {
          break;
      }
    }
    if (index !== len) {
      successors.splice(index, 1);
    }
  };

  /**
   * Returns an array of successor states for a given state index (source).
   */
  this.getSuccessorsOf = function (source) {
    if (!_states[source]) return [];
    return _states[source].successors;
  };
  
  /**
   * Returns an array of successor states for a given state index (source).
   */
  this.getSuccessorsIdOf = function (source) {
    if (!_states[source]) return undefined;
    var indices = [];
    for (var from in _states[source].successors) {
      indices.push_back( from._dest )
    }
    return indices;
  };

  /**
   * Adds a state with a given assignment to the model.
   */
  this.addState = function (label) {
    _states.push({labels: [label], successors: []});
  };

  /**
   * Edits the assignment of a state in the model, given a state index and a new partial assignment.
   */
  this.editState = function (state, label) {
    if (!_states[state]) return;
    _states[state].labels=[label];
  };

  /**
   * Removes a state and all related transitions from the model, given a state index.
   */
  this.removeState = function (state) {
    if (!_states[state]) return;
    //var self = this;

    _states[state] = null;
    _states.forEach(function (source, index) {
      if (source) this.removeTransition(index, state);
    });
  };

  /**
   * Returns an array containing the assignment (or null) of each state in the model.
   */
  this.getStates = function () {
    var stateList = [];
    _states.forEach(function (state) {
      stateList.push(state.labels);
    });
    return stateList;
  };
  
  this.clear = function () {
      _states=[];
  } 
  
  ///////////////  JSON //////////////////
  
  this.toJson = function() {
      var jsonString = JSON.stringify(_states);
      return jsonString;
  };
  
  this.loadFromJson = function(jsonstr) {
      try {
          _states = JSON.parse(jsonstr);
      } catch (e) {
          console.error("Parsing error:", e); 
      }
  }
}
