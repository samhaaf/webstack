
let replacer = (key, val) => {
  // if we get a function give us the code for that function
  if (typeof val === 'function') {
    return val.toString().replaceAll('\n\s*');
  }
  return val;
}


let reviver = (key, val) => {
  let fn_regex = [
    new RegExp(`^function\s*([\d\w,\s\*.]*)`),
    new RegExp(`^${key}\s*([\d\w,\s\*.]*\)`),
    /\([\w\d,\s\*.]*\)\s*\=\>/,
    /\w*\s*\=\>/
  ];
  if ( typeof val === 'string' && fn_regex.some((r) => (r.test(val.trim()))) ) {
    let functionTemplate = `(${val})`;
    return eval(functionTemplate);
  }
  return val;
}


let serialize = (object, spaces) => {
  return JSON.stringify(object, replacer, spaces)
}


let deserialize = (expression) => {
  return JSON.parse(expression, reviver)
}


let deepcopy = (object) => deserialize(serialize(object))


export { serialize, deserialize, deepcopy };
