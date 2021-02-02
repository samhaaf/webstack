

function round(number, digits) {
  if (digits === 'undefined') { digits = 0 }
  digits = Math.round(digits);
  return Math.round(number * Math.pow(10, digits)) / Math.pow(10, digits)
}


export {round};
