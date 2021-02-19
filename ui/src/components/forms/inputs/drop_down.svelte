

<div class='drop-down-container' id={name} bind:this={cmp}>
  {#if label != null}
    <label for={name}>{label}</label>
  {/if}

  <select bind:value={value} name='drop-down'>

    {#if null_option != null}
      <option value={null}>
        {typeof null_option === 'string' ? null_option : '---'}
      </option>
    {/if}

    {#if values != null}
      {#each values as val}
        {#if are_object_values}
          <option value={val}>{val[display_key]}</option>
        {:else}
          <option value={val}>{val}</option>
        {/if}
      {/each}
    {/if}

  </select>

</div>


<style>

</style>



<script>
  export let name = 'drop-down';
  export let value;
  export let values;
  export let label;
  export let null_option;
  export let key = 'value';
  export let display_key = key;
  export let sort_key = key;

  let are_object_values = false;
  let cmp;

  // $: console.log('dd value', value);

  $: if (Array.isArray(values)) {
    are_object_values = values.every((v) => typeof v === 'object' )
  }

  // $: if (cmp) {
  //   console.log('dd html', (document.getElementById(name) || {}).outerHTML);
  // }

</script>
