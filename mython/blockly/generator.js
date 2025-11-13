/**
 * Gerador Blockly → Mython
 * 
 * Converte blocos do Blockly para código Mython (.logic)
 */

'use strict';

goog.provide('Blockly.Mython');

goog.require('Blockly.Generator');

/**
 * Mython code generator.
 * @type {!Blockly.Generator}
 */
Blockly.Mython = new Blockly.Generator('Mython');

/**
 * List of illegal variable names.
 * This is not intended to be a security feature.  Blockly is 100% client-side,
 * so bypassing this list is trivial.  This is intended to prevent users from
 * accidentally clobbering a built-in object or function.
 * @private
 */
Blockly.Mython.addReservedWords(
    // Keywords
    'if,else,elif,for,while,repeat,define,task,class,init,set,return,' +
    'say,ask,attempt,catch,finally,raise,break,continue,pass,assert,' +
    'async,await,use,from,import,as,open,read,save,load,agent,goal,tool'
);

/**
 * Order of operation precedence.
 */
Blockly.Mython.ORDER_ATOMIC = 0;            // 0 "" ...
Blockly.Mython.ORDER_COLLECTION = 1;        // tuples, lists, dictionaries
Blockly.Mython.ORDER_STRING_CONVERSION = 1; // `expression...`
Blockly.Mython.ORDER_MEMBER = 2;            // . []
Blockly.Mython.ORDER_FUNCTION_CALL = 2;     // ()
Blockly.Mython.ORDER_EXPONENTIATION = 3;    // **
Blockly.Mython.ORDER_UNARY_SIGN = 4;        // + -
Blockly.Mython.ORDER_BITWISE_NOT = 4;       // ~
Blockly.Mython.ORDER_MULTIPLICATIVE = 5;    // * / // %
Blockly.Mython.ORDER_ADDITIVE = 6;          // + -
Blockly.Mython.ORDER_BITWISE_SHIFT = 7;     // << >>
Blockly.Mython.ORDER_BITWISE_AND = 8;       // &
Blockly.Mython.ORDER_BITWISE_XOR = 9;       // ^
Blockly.Mython.ORDER_BITWISE_OR = 10;       // |
Blockly.Mython.ORDER_RELATIONAL = 11;       // in, not in, is, is not, <, <=, >, >=, <>, !=, ==
Blockly.Mython.ORDER_LOGICAL_NOT = 12;      // not
Blockly.Mython.ORDER_LOGICAL_AND = 13;      // and
Blockly.Mython.ORDER_LOGICAL_OR = 14;       // or
Blockly.Mython.ORDER_CONDITIONAL = 15;      // if else
Blockly.Mython.ORDER_LAMBDA = 16;           // lambda
Blockly.Mython.ORDER_NONE = 99;             // (...)

/**
 * Initialise the database of variable names.
 * @param {!Blockly.Workspace} workspace Workspace to generate code from.
 */
Blockly.Mython.init = function(workspace) {
  // Create a dictionary of definitions to be printed before the code.
  Blockly.Mython.definitions_ = Object.create(null);
  // Create a dictionary mapping desired function names in definitions_
  // to actual function names (to avoid collisions with user functions).
  Blockly.Mython.functionNames_ = Object.create(null);

  if (!Blockly.Mython.variableDB_) {
    Blockly.Mython.variableDB_ =
        new Blockly.Names(Blockly.Mython.RESERVED_WORDS_);
  } else {
    Blockly.Mython.variableDB_.reset();
  }

  var defvars = [];
  var variables = Blockly.Variables.allVariables(workspace);
  for (var i = 0; i < variables.length; i++) {
    defvars[i] = Blockly.Mython.variableDB_.getName(variables[i],
        Blockly.VARIABLE_CATEGORY_NAME);
  }
  Blockly.Mython.definitions_['variables'] = defvars.length ?
      '' : '';
};

/**
 * Generate Mython code for all blocks in the workspace.
 * @param {Blockly.Workspace} workspace Workspace to generate code from.
 * @return {string} Generated code.
 */
Blockly.Mython.workspaceToCode = function(workspace) {
  if (!workspace) {
    return '';
  }
  var code = [];
  Blockly.Mython.init(workspace);
  var blocks = workspace.getTopBlocks(true);
  for (var i = 0, block; block = blocks[i]; i++) {
    var line = Blockly.Mython.blockToCode(block);
    if (line instanceof Array) {
      // Value blocks return tuples of code and operator order.
      // Top-level blocks don't have a value.
      line = line[0];
    }
    if (line) {
      if (block.outputConnection) {
        // This block is a naked value.  Ask the language's code generator if
        // it wants to append a semicolon or something.
        code.push(Blockly.Mython.scrubNakedValue(line));
      } else {
        // This block is a statement.  Add a semicolon.
        code.push(line);
      }
    }
  }
  code = code.join('\n');  // Blank line between each section.
  code = Blockly.Mython.finish(code);
  // Final scrubbing of whitespace.
  code = code.replace(/^\s+\n/, '');
  code = code.replace(/\n\s+$/, '\n');
  code = code.replace(/[ \t]+\n/g, '\n');
  return code;
};

/**
 * Generate Mython code for a block.
 * @param {!Blockly.Block} block Block to generate code for.
 * @return {string|!Array} Mython code or [code, order].
 */
Blockly.Mython.blockToCode = function(block) {
  if (block.disabled) {
    return '';
  }
  var func = this[block.type];
  if (typeof func !== 'function') {
    throw Error('Language "Mython" does not know how to generate code ' +
        'for block type "' + block.type + '".');
  }
  // First argument to func.call is the value of 'this' in the generator.
  // Prior to 24 September 2013 'this' was the only way to access the block.
  // The current approach (the provided argument) is more explicit.
  var code = func.call(Blockly.Mython, block);
  if (code instanceof Array) {
    // Value blocks return tuples of code and operator order.
    return [this.scrub_(block, code[0]), code[1]];
  } else if (typeof code === 'string') {
    if (this.STATEMENT_PREFIX) {
      code = this.STATEMENT_PREFIX.replace(/%1/g, '\'' + block.id + '\'') +
          code;
    }
    return this.scrub_(block, code);
  } else if (code === null) {
    // Block has handled code generation itself.
    return '';
  } else {
    throw Error('Invalid code generated: ' + code);
  }
};

/**
 * Naked value statement (semicolon).
 * @param {string} line Line of generated code.
 * @return {string} Legal line of code.
 */
Blockly.Mython.scrubNakedValue = function(line) {
  return line + '\n';
};

/**
 * Encode a string as a properly escaped Mython string, complete with quotes.
 * @param {string} string Text to encode.
 * @return {string} Mython string.
 * @private
 */
Blockly.Mython.quote_ = function(string) {
  // Can't use goog.string.quote since % is also a valid character.
  string = string.replace(/\\/g, '\\\\')
                 .replace(/\n/g, '\\\n')
                 .replace(/'/g, "\\'");
  return '\'' + string + '\'';
};

/**
 * Common tasks for generating Mython from blocks.
 * Handles comments for the specified block and any connected value blocks.
 * Calls any statements following this block.
 * @param {!Blockly.Block} block The current block.
 * @param {string} code The Mython code created for this block.
 * @return {string} Mython code with comments and subsequent blocks added.
 * @private
 */
Blockly.Mython.scrub_ = function(block, code) {
  var commentCode = '';
  // Only collect comments for blocks that aren't inline.
  if (!block.outputConnection || !block.outputConnection.targetBlock()) {
    // Collect comment for this block.
    var comment = block.getCommentText();
    if (comment) {
      commentCode += Blockly.Mython.prefixLines(comment, '# ') + '\n';
    }
    // Collect comments for all value arguments.
    // Don't collect comments for nested statements.
    for (var i = 0; i < block.inputList.length; i++) {
      if (block.inputList[i].type == Blockly.INPUT_VALUE) {
        var childBlock = block.inputList[i].connection.targetBlock();
        if (childBlock) {
          var comment = Blockly.Mython.allNestedComments(childBlock);
          if (comment) {
            commentCode += Blockly.Mython.prefixLines(comment, '# ');
          }
        }
      }
    }
  }
  var nextBlock = block.nextConnection && block.nextConnection.targetBlock();
  var nextCode = Blockly.Mython.blockToCode(nextBlock);
  return commentCode + code + nextCode;
};

// ============================================
// BLOCOS MYTHON
// ============================================

/**
 * Generate code for 'say' block.
 */
Blockly.Mython['say'] = function(block) {
  var text = Blockly.Mython.valueToCode(block, 'TEXT',
      Blockly.Mython.ORDER_NONE) || '""';
  return 'say ' + text + '\n';
};

/**
 * Generate code for 'ask' block.
 */
Blockly.Mython['ask'] = function(block) {
  var varName = Blockly.Mython.nameDB_.getName(
      block.getFieldValue('VAR'), Blockly.VARIABLE_CATEGORY_NAME);
  var prompt = Blockly.Mython.valueToCode(block, 'PROMPT',
      Blockly.Mython.ORDER_NONE) || '""';
  return 'ask ' + varName + ' ' + prompt + '\n';
};

/**
 * Generate code for 'ask_number' block.
 */
Blockly.Mython['ask_number'] = function(block) {
  var varName = Blockly.Mython.nameDB_.getName(
      block.getFieldValue('VAR'), Blockly.VARIABLE_CATEGORY_NAME);
  var prompt = Blockly.Mython.valueToCode(block, 'PROMPT',
      Blockly.Mython.ORDER_NONE) || '""';
  return 'ask number ' + varName + ' ' + prompt + '\n';
};

/**
 * Generate code for 'if' block.
 */
Blockly.Mython['controls_if'] = function(block) {
  var n = 0;
  var code = '', branchCode, conditionCode;
  do {
    conditionCode = Blockly.Mython.valueToCode(block, 'IF' + n,
        Blockly.Mython.ORDER_NONE) || 'False';
    branchCode = Blockly.Mython.statementToCode(block, 'DO' + n);
    // Normalize condition
    conditionCode = conditionCode.replace(/ == /g, ' is ');
    conditionCode = conditionCode.replace(/ != /g, ' is not ');
    conditionCode = conditionCode.replace(/ > /g, ' is over ');
    conditionCode = conditionCode.replace(/ < /g, ' is under ');
    conditionCode = conditionCode.replace(/ >= /g, ' is at least ');
    conditionCode = conditionCode.replace(/ <= /g, ' is at most ');
    
    if (n == 0) {
      code += 'if ' + conditionCode + ':\n' + branchCode;
    } else if (block.elseCount_ && n <= block.elseCount_) {
      code += 'elif ' + conditionCode + ':\n' + branchCode;
    }
    n++;
  } while (block.elseCount_ >= n);
  
  if (block.elseCount_ && block.elseCount_ == n - 1) {
    branchCode = Blockly.Mython.statementToCode(block, 'ELSE');
    code += 'else:\n' + branchCode;
  }
  return code;
};

/**
 * Generate code for 'repeat' block.
 */
Blockly.Mython['controls_repeat'] = function(block) {
  var times = Blockly.Mython.valueToCode(block, 'TIMES',
      Blockly.Mython.ORDER_NONE) || '1';
  var branch = Blockly.Mython.statementToCode(block, 'DO');
  return 'repeat ' + times + ' times:\n' + branch;
};

/**
 * Generate code for 'for_each' block.
 */
Blockly.Mython['controls_forEach'] = function(block) {
  var variable0 = Blockly.Mython.nameDB_.getName(
      block.getFieldValue('VAR'), Blockly.VARIABLE_CATEGORY_NAME);
  var iterable = Blockly.Mython.valueToCode(block, 'LIST',
      Blockly.Mython.ORDER_ITERABLE) || '[]';
  var branch = Blockly.Mython.statementToCode(block, 'DO');
  return 'for each ' + variable0 + ' in ' + iterable + ':\n' + branch;
};

/**
 * Generate code for 'while' block.
 */
Blockly.Mython['controls_whileUntil'] = function(block) {
  var until = block.getFieldValue('MODE') == 'UNTIL';
  var argument0 = Blockly.Mython.valueToCode(block, 'BOOL',
      Blockly.Mython.ORDER_NONE) || 'False';
  var branch = Blockly.Mython.statementToCode(block, 'DO');
  if (until) {
    argument0 = 'not ' + argument0;
  }
  // Normalize condition
  argument0 = argument0.replace(/ == /g, ' is ');
  argument0 = argument0.replace(/ != /g, ' is not ');
  argument0 = argument0.replace(/ > /g, ' is over ');
  argument0 = argument0.replace(/ < /g, ' is under ');
  return 'while ' + argument0 + ':\n' + branch;
};

/**
 * Generate code for 'define' (function) block.
 */
Blockly.Mython['procedures_defreturn'] = function(block) {
  var funcName = Blockly.Mython.nameDB_.getName(
      block.getFieldValue('NAME'), Blockly.PROCEDURE_CATEGORY_NAME);
  var args = [];
  for (var i = 0; i < block.arguments_.length; i++) {
    args[i] = Blockly.Mython.nameDB_.getName(block.arguments_[i],
        Blockly.VARIABLE_CATEGORY_NAME);
  }
  var code = 'define ' + funcName + '(' + args.join(', ') + '):\n';
  var branch = Blockly.Mython.statementToCode(block, 'STACK');
  if (branch) {
    code += branch;
  }
  var returnValue = Blockly.Mython.valueToCode(block, 'RETURN',
      Blockly.Mython.ORDER_NONE) || '';
  if (returnValue) {
    code += 'return ' + returnValue + '\n';
  }
  return code;
};

/**
 * Generate code for 'list' block.
 */
Blockly.Mython['lists_create_with'] = function(block) {
  var elements = new Array(block.itemCount_);
  for (var i = 0; i < block.itemCount_; i++) {
    elements[i] = Blockly.Mython.valueToCode(block, 'ADD' + i,
        Blockly.Mython.ORDER_NONE) || 'None';
  }
  return '[' + elements.join(', ') + ']';
};

/**
 * Generate code for 'add_to_list' block.
 */
Blockly.Mython['lists_add'] = function(block) {
  var item = Blockly.Mython.valueToCode(block, 'ITEM',
      Blockly.Mython.ORDER_NONE) || 'None';
  var list = Blockly.Mython.valueToCode(block, 'LIST',
      Blockly.Mython.ORDER_MEMBER) || '[]';
  return 'add ' + item + ' to ' + list + '\n';
};

/**
 * Generate code for 'set' (variable) block.
 */
Blockly.Mython['variables_set'] = function(block) {
  var argument0 = Blockly.Mython.valueToCode(block, 'VALUE',
      Blockly.Mython.ORDER_ASSIGNMENT) || '0';
  var varName = Blockly.Mython.nameDB_.getName(
      block.getFieldValue('VAR'), Blockly.VARIABLE_CATEGORY_NAME);
  return 'set ' + varName + ' = ' + argument0 + '\n';
};

/**
 * Generate code for 'get' (variable) block.
 */
Blockly.Mython['variables_get'] = function(block) {
  var varName = Blockly.Mython.nameDB_.getName(
      block.getFieldValue('VAR'), Blockly.VARIABLE_CATEGORY_NAME);
  return [varName, Blockly.Mython.ORDER_ATOMIC];
};

/**
 * Generate code for 'text' block.
 */
Blockly.Mython['text'] = function(block) {
  var text = block.getFieldValue('TEXT');
  return [Blockly.Mython.quote_(text), Blockly.Mython.ORDER_ATOMIC];
};

/**
 * Generate code for 'math_number' block.
 */
Blockly.Mython['math_number'] = function(block) {
  var code = block.getFieldValue('NUM');
  return [code, Blockly.Mython.ORDER_ATOMIC];
};

/**
 * Generate code for 'logic_compare' block.
 */
Blockly.Mython['logic_compare'] = function(block) {
  var operator = block.getFieldValue('OP');
  var order = Blockly.Mython.ORDER_RELATIONAL;
  var argument0 = Blockly.Mython.valueToCode(block, 'A', order) || '0';
  var argument1 = Blockly.Mython.valueToCode(block, 'B', order) || '0';
  
  var operators = {
    'EQ': ' is ',
    'NEQ': ' is not ',
    'LT': ' is under ',
    'LTE': ' is at most ',
    'GT': ' is over ',
    'GTE': ' is at least '
  };
  
  var op = operators[operator] || ' == ';
  var code = argument0 + op + argument1;
  return [code, order];
};

/**
 * Finish the code.
 * @param {string} code Generated code.
 * @return {string} Completed code.
 */
Blockly.Mython.finish = function(code) {
  // Indent every line.
  code = Blockly.Mython.prefixLines(code, Blockly.Mython.INDENT);
  return code;
};

/**
 * Common prefix for all lines.
 */
Blockly.Mython.INDENT = '    ';

