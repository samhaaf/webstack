
<script>
  export let id;
  export let config;
  export let value;
  export let state;

  // validate that the items needing a name have a name
  const unassigned_button = () => alert('No action assigned to button element');
  let name = config.name;

  $: if (value === '') value = null;

</script>

{#if config.type == 'form'}
  <form {id}><slot/></form>
{:else if config.type == 'string'}
  {#if config.label != null}
    <label for={name}>{config.label}</label>
  {/if}
  <input type="text" {id} {name}
    bind:value={value}
    placeholder={config.placeholder}
  >
  <br>
{:else if config.type == 'submit'}
  <button type="button" {id} {name} on:click={config.action || unassigned_button}>
    {config.text || "Submit"}

  </button>
{:else if config.type == 'reset'}
  <button type="button" {id} {name} on:click={config.action || unassigned_button}>
    {config.text || "Reset"}
  </button>
{/if}
