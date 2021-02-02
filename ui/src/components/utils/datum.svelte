<script>
  export let value;
  export let type;

  let div_style = ['display: inline-block'];
  let is_cell = ('cell' in $$props);

  if (is_cell) {
    div_style = [...div_style, 'border: inset 2px;']
  }

</script>

<div style={div_style.join(';')}>
  <a>{value}</a>
</div>
