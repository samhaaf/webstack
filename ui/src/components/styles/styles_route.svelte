

{#if style_sheet}
  <link rel='stylesheet' href={style_sheet} lang='scss'>
{/if}

<div class='container' style='width: 200px; height: 100px;'>

  Here is an ordinary container.


</div>

<script>

  export let style = 'simple.scss';

  let available_styles = ['simple.scss']
  let style_sheet;

  $: style_sheet = available_styles.includes(style) ? '/css/' + style : '';

</script>
