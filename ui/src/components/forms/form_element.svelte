
<script>
  export let id;
  export let config;
  export let value;
  export let state;

  // validate that the items needing a name have a name
  let name = config.name;

  $: if (value === '') value = null;

</script>

{#if config.type == 'form'}
  <form {id}><slot/></form>
{:else if config.type == 'string'}
  <input type="text" {id} {name}
    bind:value={value}
    placeholder={config.placeholder}
  >
{:else if config.type == 'submit'}
  <input type="submit" {id} {name}
    value={config.text || "Submit"}
  >
{:else if config.type == 'reset'}
  <input type="reset" {id} {name}
    value={config.text || "Reset"}
  >
{/if}
